#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import re
from web.utils.common      import exception_info,current_rq,aes_encrypt,aes_decrypt,format_sql
from web.utils.common      import get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle
from web.utils.common      import get_connection_ds_pg,get_connection_ds_mongo,get_connection_ds_redis,get_connection_ds_es
from web.model.t_user      import get_user_by_loginame
from web.utils.mysql_async import async_processer

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

async def query_ds(dsname,market_id,db_env,ds_type):
    v_where=' and 1=1 '
    if dsname != '':
        v_where = v_where + " and binary concat(a.db_desc,b.dmmc,':/',ip,':',port,'/',service)  like '%{0}%'\n".format(dsname)

    if market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(market_id)

    if db_env != '':
        v_where = v_where + " and a.db_env='{0}'\n".format(db_env)

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
                        updator,DATE_FORMAT(last_update_date,'%Y-%m-%d') last_update_date,
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
                  {5}
                ORDER BY a.ip,PORT,a.service""".format(p_userid,p_userid,p_userid,p_userid,p_userid,v_where)
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
                  proxy_server
           from t_db_source where id={0}""".format(p_dsid)
    ds = await async_processer.query_dict_one(sql)
    ds['password'] = await aes_decrypt(ds['password'],ds['user'])
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
                  db_env,inst_type,market_id
           from t_db_source where id={1}
        """.format(p_cdb,p_dsid)
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

async def get_dss_sql_query(logon_name):
    d_user= await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               AND a.id IN(SELECT proj_id FROM t_user_proj_privs WHERE user_id='{0}' AND priv_id='1')
               order by a.db_desc
        """.format(d_user['userid'])
    return  await async_processer.query_list(sql)

async def get_dss_sql_release(logon_name):
    d_user = await get_user_by_loginame(logon_name)
    sql="""select cast(id as char) as id,a.db_desc as name 
           from t_db_source a,t_dmmx b
           where a.db_type=b.dmm and b.dm='02' and a.status='1'
               and (select proj_id from t_user_proj_privs where proj_id=a.id and user_id='{0}' and priv_id='2')
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

        if p_ds['pass'] != '':
            ds_pass    = await aes_encrypt(p_ds['pass'], ds_user)
        else:
            ds_pass    = p_ds['pass']
        status         = p_ds['status']

        sql="""insert into t_db_source
                (id,db_type,db_env,db_desc,ip,port,service,user,password,status,creation_date,creator,last_update_date,updator,market_id,inst_type,proxy_status,proxy_server) 
               values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}')
            """.format(ds_id,ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,
                       ds_user,ds_pass,status,current_rq(),'DBA',current_rq(),'DBA',ds_market_id,ds_inst_type,
                       ds_proxy_status,ds_proxy_server)
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
        print('upd_ds...p_ds=',p_ds)

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
                       proxy_server ='{14}'
                where id='{15}'""".format(ds_db_type,ds_db_env,ds_db_desc,ds_ip,ds_port,ds_service,
                                          ds_user,ds_pass,status,current_rq(),'DBA',ds_market_id,ds_inst_type,
                                          ds_proxy_status,ds_proxy_server,ds_id)

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