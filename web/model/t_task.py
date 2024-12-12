#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import os
import traceback

import requests

from web.utils.mysql_async import async_processer


async def query_task(tagname):
    v_where = ' and 1=1 '
    if tagname != '':
        v_where = v_where + " and a.task_tag='{0}'\n".format(tagname)
    sql = """SELECT   a.task_tag,
                      a.comments,
                      concat(b.server_ip,':',b.server_port),
                      a.script_file,
                      a.run_time,
                      a.api_server,
                      CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
              FROM t_task a,t_server b
              WHERE a.server_id=b.id 
                AND b.status='1' {0} """.format(v_where)
    return await async_processer.query_list(sql)


async def query_minio_case(p_db_env):
    res = {}
    sql = """SELECT 
                   c.dmmc AS 'db_type',
                   a.db_desc,
                   date_format(d.start_time,'%Y-%m-%d %H:%i:%s') as create_date,                  
                   CASE WHEN SUBSTR(d.total_size,-1)='M' THEN 
                      SUBSTR(d.total_size,1,LENGTH(total_size)-1)
                   WHEN SUBSTR(d.total_size,-1)='G' THEN 
                      SUBSTR(total_size,1,LENGTH(total_size)-1)*1024
                   ELSE 0 END AS total_size,
                   concat(d.elaspsed_backup+d.elaspsed_gzip,'') as backup_time,
                   CASE WHEN d.status='0' THEN '√' ELSE '×' END flag                   
             FROM t_db_source a,t_dmmx b,t_dmmx c,t_db_backup_total d,t_db_config e
             WHERE a.market_id='000' 
               AND a.db_env=b.dmm AND b.dm='03'
               and a.db_env='{0}'
               AND a.db_type=c.dmm AND c.dm='02'
               AND d.db_tag=e.db_tag
               AND e.db_id=a.id
               AND create_date=DATE_SUB(DATE(NOW()),INTERVAL 1 DAY) ORDER BY a.db_env,a.db_type""".format(p_db_env)
    res['data'] = await async_processer.query_list(sql)

    sql = """SELECT 
                      cast(SUM(CASE WHEN d.status='0' THEN 1 ELSE 0 END) as char) AS  success,       
                      cast(SUM(CASE WHEN d.status='1' THEN 1 ELSE 0 END) as char) AS  failure              
             FROM t_db_source a,t_dmmx b,t_dmmx c,t_db_backup_total d,t_db_config e
             WHERE a.market_id='000' 
               AND a.db_env=b.dmm AND b.dm='03'
               and a.db_env='{0}'
               AND a.db_type=c.dmm AND c.dm='02'
               AND d.db_tag=e.db_tag
               AND e.db_id=a.id
               AND create_date=DATE_SUB(DATE(NOW()),INTERVAL 1 DAY) ORDER BY a.db_env,a.db_type""".format(p_db_env)
    rs = await async_processer.query_one(sql)
    res['success'] = rs[0]
    res['failure'] = rs[1]
    return res


async def query_task_log(tagname, begin_date, end_date):
    v_where = ' and 1=1 '
    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)
    if begin_date != '':
        v_where = v_where + " and b.create_date>='{0}'\n".format(begin_date + ' 0:0:0')
    if end_date != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(end_date + ' 23:59:59')
    sql = """SELECT a.sync_tag,
                    a.comments,
                    b.sync_day,
                    b.download_time,
                    b.upload_time,
                    b.total_time,
                    b.transfer_file,
                    DATE_FORMAT(b.create_date,'%Y-%m-%d %h:%i:%s')  AS create_date
            FROM  t_minio_config a ,t_minio_log b
            WHERE a.sync_tag=b.sync_tag
              AND a.status='1' {} ORDER BY b.sync_tag,b.create_date """.format(v_where)
    return await async_processer.query_list(sql)


async def save_task(p_sync):
    val = await check_task(p_sync, 'I')
    if val['code'] == '-1':
        return val
    try:
        sql = """insert into t_task(
                       task_tag,comments,server_id,python3_home,script_path,script_file,api_server,run_time,status) 
                values('{}','{}','{}','{}','{}','{}','{}','{}','{}')
               """.format(p_sync['task_tag'], p_sync['task_desc'], p_sync['server_id'],
                          p_sync['python3_home'], p_sync['script_base'], p_sync['script_name'],
                          p_sync['api_server'], p_sync['run_time'], p_sync['status'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_task(p_sync):
    val = await check_task(p_sync, 'U')
    if val['code'] == '-1':
        return val
    try:
        sql = """update t_task 
                  set  comments       ='{}',
                       server_id      ='{}', 
                       python3_home   ='{}',                        
                       script_path    ='{}',           
                       script_file    ='{}', 
                       api_server     ='{}',
                       run_time       ='{}',
                       STATUS         ='{}'
                where task_tag='{}'""".format(p_sync['task_desc'], p_sync['server_id'], p_sync['python3_home'],
                                              p_sync['script_base'], p_sync['script_name'], p_sync['api_server'],
                                              p_sync['run_time'], p_sync['status'], p_sync['task_tag'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_task(p_task_tag):
    try:
        sql = "delete from t_task  where task_tag='{0}'".format(p_task_tag)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


async def check_tag_rep(p_task):
    sql = "select count(0) from t_task  where  task_tag='{0}'".format(p_task["task_tag"])
    rs = await async_processer.query_one(sql)
    return rs[0]


async def check_task(p_task, p_flag):
    result = {}
    if p_task["task_tag"] == "":
        result['code'] = '-1'
        result['message'] = '任务标识不能为空！'
        return result

    if (await check_tag_rep(p_task)) > 0 and p_flag == 'I':
        result['code'] = '-1'
        result['message'] = '同步标识重复!'
        return result

    if p_task["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_task["server_id"] == "":
        result['code'] = '-1'
        result['message'] = '同步服务器不能为空！'
        return result

    if p_task["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '脚本目录不能为空！'
        return result

    if p_task["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '脚本名称不能为空！'
        return result

    if p_task["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '运行时间不能为空！'
        return result

    if p_task["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_task["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result


async def get_task_by_taskid(p_task_tag):
    sql = "select * from t_task where task_tag='{0}'".format(p_task_tag)
    return await async_processer.query_dict_one(sql)


def push_task(p_tag, p_api):
    url = 'http://{}/push_task_remote'.format(p_api)
    res = requests.post(url, data={'tag': p_tag})
    jres = res.json()
    v = ''
    for c in jres['msg']['crontab'].split('\n'):
        if c.count(p_tag) > 0:
            v = v + "<span class='warning'>" + c + "</span>"
        else:
            v = v + c
        v = v + '<br>'
    jres['msg']['crontab'] = v
    return jres


def run_task(p_tag, p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_task_remote -d 'tag={1}'".format(p_api, p_tag)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result
    except Exception as e:
        result['code'] = '-1'
        result['message'] = '{0!'.format(str(e))
        return result


def stop_task(p_tag, p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        r = os.system("curl -XPOST {0}/stop_task_remote -d 'tag={1}'".format(p_api, p_tag))
        if r == 0:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '执行失败！'
            return result
    except:
        result['code'] = '-1'
        result['message'] = '执行失败！'
        return result
