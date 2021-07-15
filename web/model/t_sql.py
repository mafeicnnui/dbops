#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 13:18
# @Author  : ma.fei
# @File    : t_sql.py
# @Software: PyCharm

import json
import pymysql
import requests
import traceback
from web.model.t_ds   import get_ds_by_dsid
from web.utils.common import get_connection_ds_sqlserver,get_connection_ds_read_limit
from web.utils.common import exception_info_mysql,format_mysql_error
from web.model.t_sql_check import get_audit_rule

def check_sql(p_dbid,p_sql,curdb):
    result = {}
    result['status'] = '0'
    result['msg']    = ''
    result['data']   = ''
    result['column'] = ''

    if p_dbid == '':
        result['status'] = '1'
        result['msg'] = '请选择数据源!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql =='':
        result['status'] = '1'
        result['msg'] = '请选中查询语句!'
        result['data'] = ''
        result['column'] = ''
        return result

    if p_sql.find('.')==-1 and curdb=='':
        result['status'] = '1'
        result['msg'] = '请选择数据库!'
        result['data'] = ''
        result['column'] = ''
        return result


    if p_sql.upper().count("ALTER") >= 1 or p_sql.upper().count("DROP") >= 1 \
            or p_sql.upper().count("CREATE") >= 1  or  p_sql.upper().count("GRANT") >= 1 \
              or p_sql.upper().count("REVOKE") >= 1 or p_sql.upper().count("TRUNCATE") >= 1 \
               or p_sql.upper().count("UPDATE") >= 1 or p_sql.upper().count("DELETE") >= 1 \
                 or p_sql.upper().count("INSERT") >= 1:
        result['status'] = '1'
        result['msg']    = '不允许进行DDL、DCL、DML操作!'
        result['data']   = ''
        result['column'] = ''
        return result
    return result

def get_sqlserver_result(p_ds,p_sql,curdb):
    result  = {}
    columns = []
    data    = []
    try:
        p_ds['service'] = curdb
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
        cr.execute(p_sql)
        rs = cr.fetchall()
        desc = cr.description
        for i in range(len(desc)):
            columns.append({"title": desc[i][0]})
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except:
        traceback.print_exc()
        result['status'] = '1'
        result['msg'] = traceback.format_exc()
        result['data']   = ''
        result['column'] = ''
        return result

async def get_mysql_result(p_ds,p_sql,curdb):
    result   = {}
    columns  = []
    data     = []
    p_env    = ''
    #get read timeout
    read_timeout = int((await get_audit_rule('switch_timeout'))['rule_value'])
    print('read_timeout=',read_timeout)
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    p_ds['service'] = curdb
    if p_ds['proxy_status'] == '0':
        db = get_connection_ds_read_limit(p_ds, read_timeout)
    else:
        p_ds['ip'] = p_ds['proxy_server'].split(':')[0]
        p_ds['port'] = p_ds['proxy_server'].split(':')[1]
        db = get_connection_ds_read_limit(p_ds, read_timeout)

    try:
        cr = db.cursor()
        cr.execute(p_sql)
        rs = cr.fetchall()
        #get sensitive column
        c_sensitive = (await get_audit_rule('switch_sensitive_columns'))['rule_value'].split(',')
        #process desc
        i_sensitive = []
        desc = cr.description
        for i in range(len(desc)):
            if desc[i][0] in c_sensitive:
                i_sensitive.append(i)
            columns.append({"title": desc[i][0]})

        #check sql rwos
        rule = await get_audit_rule('switch_query_rows')
        if len(rs)>int(rule['rule_value']):
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result

        #process data
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                if i[j] is None:
                   tmp.append('')
                else:
                   if j in  i_sensitive:
                       tmp.append(await (get_audit_rule('switch_sensitive_columns'))['error'])
                   else:
                       tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] = ''
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except pymysql.err.OperationalError as e:
        err= traceback.format_exc()
        if err.find('timed out')>0:
            rule  = get_audit_rule('switch_timeout')
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result
        else:
            result['status'] = '1'
            result['msg'] = format_mysql_error(p_env, exception_info_mysql())
            result['data'] = ''
            result['column'] = ''
            return result
    except:
        print('get_mysql_result=',traceback.format_exc())
        result['status'] = '1'
        result['msg'] = format_mysql_error(p_env,exception_info_mysql())
        result['data'] = ''
        result['column'] = ''
        return result

def get_mysql_proxy_result(p_ds,p_sql,curdb):
    result = {}
    p_ds['service'] = curdb
    url  = "http://{0}/get_mysql_query".format(p_ds['proxy_server'])
    data = {
            'db_ip'     : p_ds['ip'],
            'db_port'   : p_ds['port'],
            'db_service': p_ds['service'],
            'db_user'   : p_ds['user'],
            'db_pass'   : p_ds['password'],
            'db_sql'    : p_sql
    }

    r = requests.post(url,data)
    r = json.loads(r.text)

    if r['code'] == 200:
        result['status'] = '0'
        result['msg']    = ''
        result['data']   = r['data']
        result['column'] = r['column']
    else:
        result['status'] = '1'
        result['msg']    = r['msg']
        result['data']   = ''
        result['column'] = ''
    return result

def get_mysql_proxy_result_dict(p_ds,p_sql,curdb):
    result = {}
    p_ds['service'] = curdb
    url  = "http://{0}/get_mysql_query_dict".format(p_ds['proxy_server'])
    data = {
            'db_ip'      : p_ds['ip'],
            'db_port'    : p_ds['port'],
            'db_service' : p_ds['service'],
            'db_user'    : p_ds['user'],
            'db_pass'    : p_ds['password'],
            'db_sql'     : p_sql
    }

    r = requests.post(url,data)
    r = json.loads(r.text)

    if r['code'] == 200:
        result['status'] = '0'
        result['msg']    = ''
        result['data']   = r['data']
        result['column'] = r['column']
    else:
        result['status'] = '1'
        result['msg']    = r['msg']
        result['data']   = ''
        result['column'] = ''
    return result

def get_sqlserver_proxy_result(p_ds,p_sql,curdb):
    result = {}
    p_ds['service'] = curdb
    url  = "http://{0}/get_mssql_query".format(p_ds['proxy_server'])
    data = {
            'db_ip'      : p_ds['ip'],
            'db_port'    : p_ds['port'],
            'db_service' : p_ds['service'],
            'db_user'    : p_ds['user'],
            'db_pass'    : p_ds['password'],
            'db_sql'     : p_sql
    }

    r = requests.post(url,data)
    r = json.loads(r.text)

    if r['code'] == 200:
        result['status'] = '0'
        result['msg']    = ''
        result['data']   = r['data']
        result['column'] = r['column']
    else:
        result['status'] = '1'
        result['msg']    = r['msg']
        result['data']   = ''
        result['column'] = ''
    return result

def get_sqlserver_proxy_result_dict(p_ds,p_sql,curdb):
    result = {}
    p_ds['service'] = curdb
    url  = "http://{0}/get_mssql_query_dict".format(p_ds['proxy_server'])
    data = {
            'db_ip'  : p_ds['ip'],
            'db_port': p_ds['port'],
            'db_service': p_ds['service'],
            'db_user': p_ds['user'],
            'db_pass': p_ds['password'],
            'db_sql' : p_sql
    }
    r = requests.post(url,data)
    r = json.loads(r.text)

    if r['code'] == 200:
        result['status'] = '0'
        result['msg']    = ''
        result['data']   = r['data']
        result['column'] = r['column']
    else:
        result['status'] = '1'
        result['msg']    = r['msg']
        result['data']   = ''
        result['column'] = ''
    return result

def get_mongo_proxy_result():

    pass

def get_mongo_result():
    pass

def get_redis_proxy_result():
    pass

def get_redis_result():
    pass


async def exe_query(p_dbid,p_sql,curdb):
    result = {}

    # 查询校验
    val = check_sql(p_dbid, p_sql,curdb)
    if val['status'] != '0':
        return val

    p_ds  = await get_ds_by_dsid(p_dbid)

    # 查询MySQL数据源
    if p_ds['db_type']=='0':
        if p_ds['proxy_status'] == '1':
           result = get_mysql_proxy_result(p_ds,p_sql,curdb)
        else:
           result = await get_mysql_result(p_ds,p_sql,curdb)

    # 查询MSQLServer数据源
    if p_ds['db_type'] == '2':
        if p_ds['proxy_status'] == '1':
            result = get_sqlserver_proxy_result(p_ds, p_sql, curdb)
        else:
            result = get_sqlserver_result(p_ds, p_sql, curdb)

    # 查询Redis数据源
    if p_ds['db_type'] == '5':
        if p_ds['proxy_status'] == '1':
            result = get_redis_proxy_result(p_ds, p_sql, curdb)
        else:
            result = get_redis_result(p_ds, p_sql, curdb)

    # 查询MongoDB数据源
    if p_ds['db_type'] == '6':
        if p_ds['proxy_status'] == '1':
            result = get_mongo_proxy_result(p_ds, p_sql, curdb)
        else:
            result = get_mongo_result(p_ds, p_sql, curdb)


    return result