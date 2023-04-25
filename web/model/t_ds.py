#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import re
import json
import pymysql
import requests
import datetime
import traceback

from web.utils.common      import get_connection_ds_read_limit, get_audit_rule, get_connection_ds_read_limit_ck,get_seconds
from web.utils.common      import exception_info_mysql,exception_info_sqlserver,format_mysql_error,format_sqlserver_error
from web.utils.common      import exception_info,current_rq,aes_encrypt,aes_decrypt,format_sql,aes_decrypt_sync
from web.utils.common      import get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle
from web.utils.common      import get_connection_ds_pg,get_connection_ds_mongo,get_connection_ds_redis,get_connection_ds_es
from web.model.t_user      import get_user_by_loginame
from web.utils.mysql_async import async_processer
from web.utils.mysql_sync  import sync_processer


def check_ds(p_ds,p_flag):
    result = {}
    if p_ds["ip"]=="":
        result['code']='-1'
        result['message']='IP地址不能为空！'
        return result
    '''
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", p_ds["ip"])==None:
        result['code'] = '-1'
        result['message'] = 'IP地址不正确！'
        return result
    '''
    if p_ds["port"] == "":
        result['code'] = '-1'
        result['message'] = '端口不能为空！'
        return result

    if re.match(r"^([1-9][0-9]{3,4})$",p_ds["port"])==None:
        result['code'] = '-1'
        result['message'] = '端口必须为4-5位连续数字且不能以0开头！'
        return result

    if p_ds["user"] == "" and p_ds['db_type']=='0':
        result['code'] = '-1'
        result['message'] = '用户不能为空！'
        return result

    if p_ds["pass"] == "" and p_ds['db_type']=='0':
        result['code'] = '-1'
        result['message'] = '口令不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

async def query_ds(dsname,market_id,db_env,ds_type,ds_status):
    v_where=' and 1=1 '
    if dsname != '':
        v_where = v_where + " and binary concat(a.db_desc,b.dmmc,':/',ip,':',port,'/',service)  like '%{0}%'\n".format(dsname)

    if market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(market_id)

    if db_env != '':
        v_where = v_where + " and a.db_env='{0}'\n".format(db_env)

    if ds_status != '':
        v_where = v_where + " and a.status='{0}'\n".format(ds_status)

    if ds_type == 'backup':
        v_where = v_where + " and a.user='puppet'\n"

    if ds_type == 'sync':
        v_where = v_where + " and a.user!='puppet'\n"

    sql = """select  a.id,
                    d.dmmc as market_name,
                    a.db_desc,
                    c.dmmc as db_env,
                    concat(substr(concat(b.dmmc,':/',ip,':',port,'/',service),1,40),'...')  as name,              
                    user,
                    case status when '1' then '是' when '0' then '否' end  status,                    
                    updator,date_format(last_update_date,'%Y-%m-%d') last_update_date           
          from t_db_source a,t_dmmx b,t_dmmx c,t_dmmx d
          where a.db_type=b.dmm and b.dm='02'
            and a.db_env=c.dmm  and c.dm='03' 
            and a.market_id=d.dmm  and d.dm='05' 
            {0}
        order by a.db_desc""".format(v_where)
    return await async_processer.query_list(sql)

async def query_project(p_name,p_userid,is_grants):
    if is_grants=='false':
       v_where = ''' and not exists(select 1 from t_user_proj_privs d
                                    where d.proj_id=a.id and d.user_id={0})'''.format(p_userid)
    else:
       v_where = ''' and  exists(select 1 from t_user_proj_privs d
                                          where d.proj_id=a.id and d.user_id={0})'''.format(p_userid)
    if p_name == "":
        sql ="""SELECT  a.id,
                        a.db_desc,
                        concat(substr(CONCAT(b.dmmc,':/',ip,':',PORT,'/',service),1,30),'...') AS NAME,             
                        c.dmmc AS db_env,
                        -- updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{0}' AND priv_id='1') AS query_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{1}' AND priv_id='2') AS release_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{2}' AND priv_id='3') AS audit_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{3}' AND priv_id='4') AS execute_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{4}' AND priv_id='5') AS order_priv ,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{5}' AND priv_id='6') AS export_priv                          
                FROM t_db_source a,t_dmmx b,t_dmmx c
                WHERE a.db_type=b.dmm AND b.dm='02'
                  AND a.db_env=c.dmm AND c.dm='03' 
                  and a.status='1'
                  {6}
                ORDER BY a.ip,PORT,a.service""".format(p_userid,p_userid,p_userid,p_userid,p_userid,p_userid,v_where)
    else:
        sql = """SELECT a.id,
                        a.db_desc,
                        concat(substr(CONCAT(b.dmmc,':/',ip,':',PORT,'/',service),1,30),'...') AS NAME, 
                        c.dmmc AS db_env,
                        updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date ,
                         (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{0}' AND priv_id='1') AS query_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{1}' AND priv_id='2') AS release_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{2}' AND priv_id='3') AS audit_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{3}' AND priv_id='4') AS execute_priv,
                        (SELECT COUNT(0) FROM t_user_proj_privs 
                           WHERE proj_id=a.id AND user_id='{4}' AND priv_id='5') AS order_priv
                FROM t_db_source a,t_dmmx b,t_dmmx c
                WHERE a.db_type=b.dmm AND b.dm='02'
                  AND a.db_env=c.dmm AND c.dm='03'
                  and a.status='1'                
                  AND (binary concat(a.ip,':',a.port,'/',a.service)  like '%{5}%'  or a.db_desc like '%{6}%')
                  {7}
                order by a.ip,port,a.service""".format(p_userid,p_userid,p_userid,p_userid,p_userid,p_name,p_name,v_where)
    return await async_processer.query_list(sql)

async def get_dsid():
    sql="select ifnull(max(id),0)+1 from t_db_source"
    return (await async_processer.query_one(sql))[0]

async def check_ds_repeat(p_ds):
    result = {}
    sql = """select count(0)  from t_db_source where ip='{0}'  and port='{1}' and service='{2}' and user='{3}'
          """.format(p_ds["ip"],p_ds["port"], p_ds["service"], p_ds["user"])
    rs1 = await async_processer.query_one(sql)
    sql = """select count(0) from t_db_source where db_desc='{0}' """.format(p_ds["db_desc"])
    rs2 = await async_processer.query_one(sql)
    if rs1[0]>0:
        result['code'] = True
        result['message'] = '数据源不能重复!'
    elif rs2[0]>0:
        result['code'] = True
        result['message'] = '数据源描述不能重复!'
    else:
        result['code'] = False
        result['message'] = '!'
    return result

async def get_ds_by_dsid(p_dsid):
    sql="""select cast(id as char) as dsid,
                  db_type,
                  db_desc,
                  ip,
                  port,
                  service,
                  user,
                  password,
                  status,
                  date_format(creation_date,'%Y-%m-%d %H:%i:%s') as creation_date,
                  creator,
                  date_format(last_update_date,'%Y-%m-%d %H:%i:%s') as last_update_date,
                  updator ,
                  db_env,
                  inst_type,
                  market_id,
                  proxy_status,
                  proxy_server,
                  id_ro,
                  stream_load,
                  related_id
           from t_db_source where id={0}""".format(p_dsid)
    #print(sql)
    ds = await async_processer.query_dict_one(sql)
    ds['password'] = '' if ds['password']=='' else await aes_decrypt(ds['password'],ds['user'])
    ds['url'] = 'MySQL://{0}:{1}/{2}'.format(ds['ip'], ds['port'], ds['service'])
    return ds

def get_ds_by_dsid_sync(p_dsid):
    sql="""select cast(id as char) as dsid,
                  db_type,
                  db_desc,
                  ip,
                  port,
                  service,
                  user,
                  password,
                  status,
                  date_format(creation_date,'%Y-%m-%d %H:%i:%s') as creation_date,
                  creator,
                  date_format(last_update_date,'%Y-%m-%d %H:%i:%s') as last_update_date,
                  updator ,
                  db_env,
                  inst_type,
                  market_id,
                  proxy_status,
                  proxy_server,
                  id_ro
           from t_db_source where id={0}""".format(p_dsid)
    ds = sync_processer.query_dict_one(sql)
    ds['password'] = aes_decrypt_sync(ds['password'],ds['user'])
    ds['url'] = 'MySQL://{0}:{1}/{2}'.format(ds['ip'], ds['port'], ds['service'])
    return ds

async def get_ds_by_dsid_by_cdb(p_dsid,p_cdb):
    sql="""select cast(id as char) as id,db_type,db_desc,
                  ip,port,
                  CASE WHEN service=NULL OR service='' THEN
                    '{0}'
                  ELSE
                     service 
                  END AS service,
                  user,password,status,creation_date,creator,last_update_date,updator ,
                  db_env,inst_type,market_id,
                  proxy_status,proxy_server
           from t_db_source where id={1}
        """.format(p_cdb,p_dsid)
    print(sql)
    ds = await async_processer.query_dict_one(sql)
    ds['password'] = await aes_decrypt(ds['password'], ds['user'])
    ds['url'] = 'MySQL://{0}:{1}/{2}'.format(ds['ip'], ds['port'], ds['service'])
    return ds

async def get_dss(p_server_id):
    if p_server_id=='':
        sql = """select cast(id as char) as id,a.db_desc as name
                  from t_db_source a,t_dmmx b
                   where a.db_type=b.dmm and b.dm='02' and a.status='1'  order by a.db_desc
              """
    else:
        sql = """select cast(id as char) as id,a.db_desc as name
                   from t_db_source a,t_dmmx b
                      where a.db_type=b.dmm 
                        and b.dm='02' 
                        and a.status='1' 
                        and a.market_id=(select market_id from t_server where id='{0}')
                        order by a.db_desc
              """.format(p_server_id)
    return await async_processer.query_list(sql)

async def get_dss_by_dsid(p_dsid):
     sql = "select cast(id as char) as id,db_desc as name from t_db_source  where id ={}".format(p_dsid)
     return await async_processer.query_list(sql)

async def get_dss_sql_query(logon_name):
    d_user= await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               AND a.id IN(SELECT proj_id FROM t_user_proj_privs WHERE user_id='{0}' AND priv_id='1')
               order by a.db_desc
        """.format(d_user['userid'])
    return  await async_processer.query_list(sql)

async def get_dss_sql_query_grants(userid):
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               AND a.id IN(SELECT proj_id FROM t_user_proj_privs WHERE user_id='{0}' AND priv_id='1')
               order by a.db_desc
        """.format(userid)
    return  await async_processer.query_list(sql)

async def get_dss_sql_query_tab(userid):
    sql = """select cast(id as char) as id,a.db_desc as name
               from t_db_source a,t_dmmx b
               where a.db_type=b.dmm and b.dm='02' and a.status='1'
                   AND a.id IN(SELECT dbid FROM t_user_query_grants WHERE uid='{0}')
                   order by a.db_desc
            """.format(userid)
    return await async_processer.query_list(sql)

async def get_dss_sql_query_type(p_db_type,p_logon_name):
    d_user = await get_user_by_loginame(p_logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1' and a.db_type='{0}'
             AND a.id IN(SELECT proj_id FROM t_user_proj_privs WHERE user_id='{1}' AND priv_id='1')
               order by a.db_desc
        """.format(p_db_type,d_user['userid'])
    return  await async_processer.query_list(sql)

async def get_dss_sql_release(logon_name):
    d_user = await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and a.id in (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='2')
        """.format(d_user['userid'])
    return await async_processer.query_list(sql)

async def get_dss_sql_audit(logon_name):
    d_user = await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and a.id IN (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='3')
               order by a.db_desc
        """.format(d_user['userid'])
    return await async_processer.query_list(sql)

async def get_dss_sql_run(logon_name):
    d_user=await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and a.id in (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='4')
               order by a.db_desc
        """.format(d_user['userid'])
    return await async_processer.query_list(sql)

async def get_dss_order(logon_name):
    d_user = await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and a.id in (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='5')
               order by a.db_desc
        """.format(d_user['userid'])
    return await async_processer.query_list(sql)

async def get_dss_order_online():
    sql="""SELECT CAST(id AS CHAR) AS id,a.flag1 AS NAME 
           FROM t_db_source a
           WHERE a.status='1' AND a.`db_env` IN('1','2','3')       
              AND a.`db_type` IN(0,5,6)
               AND a.id IN(1,2,16,84,206,221,218,32,220)
               ORDER BY a.db_type,a.id"""
    return await async_processer.query_list(sql)

async def get_dss_sql_export(logon_name):
    d_user = await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and a.id IN (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='6')
               order by a.db_desc
        """.format(d_user['userid'])
    return await async_processer.query_list(sql)

async def save_ds(p_ds):
    result = {}
    val=check_ds(p_ds,'add')
    if val['code']=='-1':
        return val
    try:
        ds_id           = await get_dsid()
        ds_market_id    = p_ds['market_id']
        ds_inst_type    = p_ds['inst_type']
        ds_db_type      = p_ds['db_type']
        ds_db_env       = p_ds['db_env']
        ds_db_desc      = p_ds['db_desc']
        ds_ip           = format_sql(p_ds['ip'])
        ds_port         = p_ds['port']
        ds_service      = p_ds['service']
        ds_user         = p_ds['user']
        ds_proxy_status = p_ds['proxy_status']
        ds_proxy_server = p_ds['proxy_server']
        read_db         = p_ds.get('read_db')
        stream_load     = p_ds['stream_load']
        related_id      = p_ds['related_id']
        status          = p_ds['status']

        if p_ds['pass'] != '':
            ds_pass    = await aes_encrypt(p_ds['pass'], ds_user)
        else:
            ds_pass    = p_ds['pass']

        sql="""insert into t_db_source
                (id,db_type,db_env,db_desc,ip,port,service,user,password,status,creation_date,
                 creator,last_update_date,updator,market_id,inst_type,proxy_status,proxy_server,id_ro,stream_load,related_id) 
               values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}')
            """.format(ds_id,ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,
                       ds_user,ds_pass,status,current_rq(),'DBA',current_rq(),'DBA',ds_market_id,ds_inst_type,
                       ds_proxy_status,ds_proxy_server,read_db,stream_load,related_id)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

async def upd_ds(p_ds):
    result={}
    val = check_ds(p_ds,'upd')
    if  val['code'] == '-1':
        return val
    try:
        ds_id           = p_ds['dsid']
        ds_market_id    = p_ds['market_id']
        ds_inst_type    = p_ds['inst_type']
        ds_db_type      = p_ds['db_type']
        ds_db_env       = p_ds['db_env']
        ds_db_desc      = p_ds['db_desc']
        ds_ip           = format_sql(p_ds['ip'])
        ds_port         = p_ds['port']
        ds_service      = p_ds['service']
        ds_user         = p_ds['user']
        ds_proxy_status = p_ds['proxy_status']
        ds_proxy_server = p_ds['proxy_server']
        ds_read_db      = p_ds['read_db']
        stream_load     = p_ds['stream_load']
        related_id      = p_ds['related_id']

        if p_ds['pass']!='':
           ds_pass     = await aes_encrypt(p_ds['pass'],ds_user)
        else:
           ds_pass     = p_ds['pass']
        status         = p_ds['status']

        sql="""update t_db_source 
                  set  db_type      ='{0}', 
                       db_env       ='{1}',
                       db_desc      ='{2}' ,                        
                       ip           ='{3}',      
                       port         ='{4}' ,           
                       service      ='{5}' ,                           
                       user         ='{6}' ,           
                       password     ='{7}' , 
                       status       ='{8}' ,
                       last_update_date ='{9}' ,
                       updator      ='{10}',
                       market_id    ='{11}',
                       inst_type    ='{12}',
                       proxy_status ='{13}',
                       proxy_server ='{14}',
                       id_ro        ='{15}',
                       stream_load  ='{16}',
                       related_id   ='{17}'
                where id='{18}'""".format(ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,
                                          ds_user,ds_pass,status,current_rq(),'DBA',ds_market_id,ds_inst_type,
                                          ds_proxy_status,ds_proxy_server,ds_read_db,stream_load,related_id,ds_id)
        print(sql)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

async def del_ds(p_dsid):
    result={}
    try:
        sql="delete from t_db_source  where id='{0}'".format(p_dsid)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

async def check_ds_valid(p_id):
    result = {}
    try:
        p_ds = await get_ds_by_dsid(p_id)
        if p_ds['db_type']=='0':
           conn=get_connection_ds(p_ds)
        elif p_ds['db_type']=='1':
           conn = get_connection_ds_oracle(p_ds)
        elif p_ds['db_type']=='2':
           conn = get_connection_ds_sqlserver(p_ds)
        elif p_ds['db_type']=='3':
           conn=get_connection_ds_pg(p_ds)
        elif p_ds['db_type'] == '4':
           conn = get_connection_ds_es(p_ds)
        elif p_ds['db_type']=='5':
           conn=get_connection_ds_redis(p_ds)
        elif p_ds['db_type']=='6':
           conn=get_connection_ds_mongo(p_ds)
        result['code'] = '0'
        result['message'] = '验证通过'
        print('ds=',conn)
        return result
    except:
        exception_info()
        result['code'] = '-1'
        result['message'] = '验证失败'
        return result

def check_sql(p_dsid,p_sql,curdb):
    result = {}
    result['status'] = '0'
    result['msg']    = ''
    result['data']   = ''
    result['column'] = ''
    if p_dsid == '':
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
    return result

def get_ck_proxy_result(p_ds,p_sql,curdb):
    result = {}
    p_ds['service'] = curdb
    url  = "http://{0}/get_ck_query".format(p_ds['proxy_server'])
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

async def get_ck_result(p_ds,p_sql,curdb):
    result   = {}
    columns  = []
    data     = []
    p_env    = ''
    start_time = datetime.datetime.now()
    #get read timeout
    read_timeout = int((await get_audit_rule('switch_timeout'))['rule_value'])
    print('read_timeout=',read_timeout)
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    p_ds['service'] = curdb
    if p_ds['proxy_status'] == '0':
        db = get_connection_ds_read_limit_ck(p_ds, read_timeout)
    else:
        p_ds['ip'] = p_ds['proxy_server'].split(':')[0]
        p_ds['port'] = p_ds['proxy_server'].split(':')[1]
        db = get_connection_ds_read_limit_ck(p_ds, read_timeout)

    try:
        # check sql rwos
        cr = db.cursor()
        st = """select count(0) from ({}) AS x""".format(p_sql)
        cr.execute(st)
        rs = cr.fetchone()
        rule = await get_audit_rule('switch_query_rows')
        if rs[0] > int(rule['rule_value']):
            result['status'] = '1'
            result['msg'] = rule['error'].format(rule['rule_value'])
            result['data'] = ''
            result['column'] = ''
            return result

        # execute query
        cr.execute(p_sql)
        rs = cr.fetchall()
        # get sensitive column
        c_sensitive = (await get_audit_rule('switch_sensitive_columns'))['rule_value'].split(',')
        # process desc
        i_sensitive = []
        desc = cr.description
        for i in range(len(desc)):
            if desc[i][0] in c_sensitive:
                i_sensitive.append(i)
            columns.append({"title": desc[i][0]})

        #process data
        for i in rs:
            tmp = []
            for j in range(len(desc)):
                if i[j] is None:
                   tmp.append('')
                else:
                   if j in  i_sensitive:
                       tmp.append((await get_audit_rule('switch_sensitive_columns'))['error'])
                   else:
                       tmp.append(str(i[j]))
            data.append(tmp)

        result['status'] = '0'
        result['msg'] =str(get_seconds(start_time))
        result['data'] = data
        result['column'] = columns
        cr.close()
        db.close()
        return result
    except pymysql.err.OperationalError as e:
        err= traceback.format_exc()
        if err.find('timed out')>0:
            rule  = await get_audit_rule('switch_timeout')
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
        print('get_ck_result=',traceback.format_exc())
        result['status'] = '1'
        result['msg'] = format_mysql_error(p_env,exception_info_mysql())
        result['data'] = ''
        result['column'] = ''
        return result

async def get_mysql_result(p_ds,p_sql,curdb):
    result   = {}
    columns  = []
    data     = []
    p_env    = ''
    # get read timeout
    read_timeout = int((await get_audit_rule('switch_timeout'))['rule_value'])

    p_ds['service'] = curdb
    db = get_connection_ds_read_limit(p_ds, read_timeout)
    cr = db.cursor()
    try:
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
                       tmp.append(get_audit_rule('switch_sensitive_columns')['error'])
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
        print('get_mysql_result=', err)
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

async def write_ds_opr_log(p_userid,p_dsid,p_sql,curdb):
    st = '''insert into t_db_opt_log(user_id,ds_id,db,statement,status) values('{}','{}','{}','{}','{}')
         '''.format(p_userid,p_dsid,curdb,format_sql(p_sql),'1')
    await async_processer.exec_sql(st)
    return {'status':'2','msg':'发布成功!','data':'','column':''}

def get_sqlserver_result(p_ds,p_sql,p_curdb):
    result  = {}
    columns = []
    data    = []
    p_env   = ''
    if p_ds['db_env']=='1':
        p_env='PROD'
    if p_ds['db_env']=='2':
        p_env='DEV'

    try:
        db = get_connection_ds_sqlserver(p_ds)
        cr = db.cursor()
        cr.execute('use {}'.format(p_curdb))
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
        result['status'] = '1'
        result['msg'] = format_sqlserver_error(p_env,exception_info_sqlserver())
        result['data']   = ''
        result['column'] = ''
        return result

'''
  操作日志查询
'''
async def query_ds_opt_log(p_log_name):
    v_where=' '
    if p_log_name != '':
        v_where = " where a.statement like '%{0}%' or a.db like '%{1}%'".format(p_log_name,p_log_name)
    sql = """SELECT
                 a.id,  
                 b.name,
                 c.db_desc,
                 a.db,
                 DATE_FORMAT(a.start_time,'%Y-%m-%d %H:%i:%s') AS start_time,
                 DATE_FORMAT(a.end_time,'%Y-%m-%d %H:%i:%s') AS end_time,
                 d.dmmc as status,
                 a.statement,
                 a.message
            FROM t_db_opt_log a,t_user b,t_db_source c,t_dmmx d
            WHERE a.user_id=b.id
              AND a.ds_id=c.id
              AND a.status=d.dmm
              AND d.dm='28' {0} ORDER BY a.start_time desc ,a.db,a.id""".format(v_where)
    return await async_processer.query_list(sql)


async def exe_query(p_userid,p_dsid,p_sql,curdb):
    result = {}

    # 查询校验
    val = check_sql(p_dsid, p_sql,curdb)
    if val['status'] != '0':
        return val

    p_ds = await get_ds_by_dsid(p_dsid)

    # mysql
    if p_ds['db_type']=='0':
        if len(re.findall(r'^select',p_sql.strip().lower(),re.M))>0 or len(re.findall(r'^show', p_sql.strip().lower(), re.M)) > 0:
           result = await get_mysql_result(p_ds,p_sql,curdb)
        else:
           result = await write_ds_opr_log(p_userid,p_dsid,p_sql,curdb)

    # sqlserver
    if p_ds['db_type'] == '2':
        result = get_sqlserver_result(p_ds, p_sql,curdb)

        # 查询ClickHouse 数据源
    if p_ds['db_type'] == '9':
        if p_ds['proxy_status'] == '1':
            result = get_ck_proxy_result(p_ds, p_sql, curdb)
        else:
            result = await get_ck_result(p_ds, p_sql, curdb)

    return result



async def db_encrypt(p_env,p_plain,p_userid):
    if p_env in ('1', '2', '3', '4'):
       ss_agent_dsid=228
       ss_agent_ds =  await get_ds_by_dsid_by_cdb(ss_agent_dsid,'encrypt_db')
       print('db_encrypt ds =',ss_agent_ds)
       st = """UPDATE t_cipher SET dev_plain='{}' WHERE id={}""".format(p_plain,p_userid)
       await async_processer.exec_sql_by_ds(ss_agent_ds, st)
       rs = await async_processer.query_dict_one('select dev_cipher from t_cipher where id={}'.format(p_userid))
       print('db_encrypt rs=',rs)
       return rs['dev_cipher']


async def db_decrypt(p_env,p_cipher,p_userid):
    if p_env in('1','2','3','4') :
        st = """UPDATE t_cipher SET dev_cipher='{}' WHERE id={}""".format(p_cipher,p_userid)
        await async_processer.exec_sql(st)
        ss_agent_dsid = 228
        ss_agent_ds = await get_ds_by_dsid_by_cdb(ss_agent_dsid, 'encrypt_db')
        print('db_encrypt ds =', ss_agent_ds)
        rs = await async_processer.query_dict_one_by_ds(ss_agent_ds,'select dev_plain from t_cipher where id={}'.format(p_userid))
        print('db_decrypt rs=', rs)
        return rs['dev_plain']