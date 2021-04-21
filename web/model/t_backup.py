#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import requests
import traceback
from web.utils.common  import format_sql
from web.utils.mysql_async  import async_processer

async def query_backup(tagname,db_env,db_type):
    v_where = ' and 1=1 '
    if  tagname!='':
       v_where=v_where+" and a.db_tag='{0}'\n".format(tagname)
    if db_env != '':
        v_where =v_where+ " and c.db_env='{0}'\n".format(db_env)
    if db_type != '':
        v_where =v_where+ " and c.db_type='{0}'\n".format(db_type)
    sql = """SELECT
                  a.id,a.comments,a.db_tag,a.expire,a.run_time,
                  concat(b.server_ip,':',b.server_port),a.api_server,
                  CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS,
                  CASE a.task_status WHEN '1' THEN '<span style=''color: red''>运行中</span>' WHEN '0' THEN '停止' END  STATUS
              FROM t_db_config a,t_server b,t_db_source c
              WHERE a.server_id=b.id  AND a.db_id=c.id AND b.status='1'  {0} """.format(v_where)
    return await async_processer.query_list(sql)

async def query_backup_case(p_db_env):
    st1  = """SELECT 
                   e.comments,c.dmmc AS 'db_type',
                   date_format(d.start_time,'%Y-%m-%d %H:%i:%s') as create_date,
                   date_format(d.end_time,'%Y-%m-%d %H:%i:%s') as end_time, 
                   CASE WHEN SUBSTR(d.total_size,-1)='M' THEN 
                      SUBSTR(d.total_size,1,LENGTH(total_size)-1)
                   WHEN SUBSTR(d.total_size,-1)='G' THEN 
                      SUBSTR(total_size,1,LENGTH(total_size)-1)*1024
                   ELSE 0 END AS total_size,
                   concat(d.elaspsed_backup+d.elaspsed_gzip,'') as backup_time,
                   CASE WHEN d.status='0' THEN '√' ELSE '×' END flag                   
             FROM t_db_source a,t_dmmx b,t_dmmx c,t_db_backup_total d,t_db_config e
             WHERE a.db_env=b.dmm AND b.dm='03'
               and a.db_env='{0}' AND a.db_type=c.dmm AND c.dm='02'
               AND d.db_tag=e.db_tag AND e.db_id=a.id
               AND create_date=(SELECT MAX(create_date) FROM t_db_backup_total X WHERE x.db_tag=d.db_tag) 
             ORDER BY a.market_id,a.db_env,a.db_type""".format(p_db_env)

    st2 = """SELECT 
               CAST(SUM(CASE WHEN d.status='0' THEN 1 ELSE 0 END) AS CHAR) AS  success,
               CAST(SUM(CASE WHEN d.status='1' THEN 1 ELSE 0 END) AS CHAR) AS  failure
            FROM t_db_source a,t_dmmx b,t_dmmx c,t_db_backup_total d,t_db_config e
             WHERE a.db_env=b.dmm AND b.dm='03'
                AND a.db_env='{0}' AND a.db_type=c.dmm AND c.dm='02'
                AND d.db_tag=e.db_tag AND e.db_id=a.id
                AND create_date=(SELECT MAX(create_date) FROM t_db_backup_total X WHERE x.db_tag=d.db_tag) 
              ORDER BY a.market_id,a.db_env,a.db_type""".format(p_db_env)

    rs = await async_processer.query_one(st2)
    res = {
        'data'    : await async_processer.query_list(st1),
        'success' : rs[0],
        'failure' : rs[1]
    }
    return res

async def query_backup_log(tagname,db_env,begin_date,end_date):
    v_where = ' and 1=1 '
    if  tagname != '':
        v_where = v_where+" and a.db_tag='{0}'\n".format(tagname)
    if  db_env != '':
        v_where = v_where+" and c.db_env='{0}'\n".format(db_env)
    if  begin_date != '':
        v_where = v_where+" and b.create_date>='{0}'\n".format(begin_date)
    if  end_date != '':
        v_where = v_where+" and b.create_date<='{0}'\n".format(end_date)

    st = """SELECT  b.id, a.comments, b.db_tag,
                    cast(b.create_date as char),
                    cast(b.start_time as char),
                    cast(b.end_time as char),
                    b.total_size,b.elaspsed_backup, b.elaspsed_gzip,
                    CASE b.STATUS WHEN '1' THEN '<span style=''color: red''>失败</span>' WHEN '0' THEN '成功' END  STATUS
            FROM  t_db_config a,t_db_backup_total b,t_db_source c
            WHERE a.db_tag=b.db_tag AND a.db_id=c.id  AND a.status='1' {0} 
             order by b.create_date,b.db_tag """.format(v_where)

    return await async_processer.query_list(st)

async def query_backup_log_analyze(db_env,db_type,tagname,begin_date,end_date):
    v_where = ' where a.db_tag=b.db_tag and b.db_id=c.id '
    if db_env != '':
        v_where = v_where + " and c.db_env='{0}'\n".format(db_env)
    if db_type != '':
        v_where = v_where + " and c.db_type='{0}'\n".format(db_type)
    if tagname != '':
        v_where = v_where + " and a.db_tag='{0}'\n".format(tagname)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date)
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date)

    st1 = """SELECT 
                cast(a.create_date as char) as create_date,
                CASE WHEN SUBSTR(a.total_size,-1,1)='G' THEN
                       ROUND(SUBSTR(a.total_size,1,LENGTH(a.total_size)-1)*1024,2)
                WHEN SUBSTR(a.total_size,-1,1)='M' THEN
                   ROUND(SUBSTR(a.total_size,1,LENGTH(a.total_size)-1),2)
                WHEN SUBSTR(a.total_size,-1,1)='K' THEN
                   ROUND(SUBSTR(a.total_size,1,LENGTH(a.total_size)-1)/1024,2)         
                END AS "size(MB)"
            FROM t_db_backup_total a,t_db_config b,t_db_source c
            {0} ORDER BY a.start_time""".format(v_where)

    st2 = """SELECT 
                  cast(a.create_date as char) as create_date,
                  a.elaspsed_backup,
                  a.elaspsed_gzip
              FROM t_db_backup_total a,t_db_config b,t_db_source c 
              {0}
              ORDER BY a.start_time
           """.format(v_where)
    return await async_processer.query_list(st1),await async_processer.query_list(st2)

async def query_backup_log_detail(tagname,backup_date):
    v_where = ' and 1=1 '
    if tagname != '':
       v_where = v_where + " and b.db_tag='{0}'\n".format(tagname)
    if backup_date != '':
       v_where = v_where + " and b.create_date='{0}'\n".format(backup_date)

    st = """SELECT 
                a.comments,a.db_tag,b.db_name,b.file_name,b.bk_path,
                CAST(b.create_date AS CHAR),
                CAST(b.start_time AS CHAR),
                CAST(b.end_time AS CHAR),
                b.db_size,b.elaspsed_backup,b.elaspsed_gzip,
                CASE b.STATUS WHEN '1' THEN '<span style=''color: red''>失败</span>' WHEN '0' THEN '成功' END  STATUS,
                error
            FROM  t_db_config a,t_db_backup_detail b,t_db_source c
            WHERE a.db_tag=b.db_tag and a.db_id=c.id and a.status='1' {0} 
              order by b.create_date,b.db_tag """.format(v_where)

    return await async_processer.query_list(st)

async def save_backup(p_backup):
    try:
        res = check_backup(p_backup)
        if res['code'] == '-1':
            return res

        st="""insert into t_db_config
                (server_id,db_id,db_type,db_tag,expire,bk_base,script_path,script_file,bk_cmd,run_time,comments,python3_home,backup_databases,api_server,status) 
               values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}')
           """.format(p_backup['backup_server'],p_backup['db_server'],p_backup['db_type'],
                       p_backup['backup_tag'], p_backup['backup_expire'],format_sql(p_backup['backup_base']),
                       format_sql(p_backup['script_base']),p_backup['script_name'],p_backup['cmd_name'],
                       p_backup['run_time'],p_backup['task_desc'],format_sql(p_backup['python3_home']),
                       p_backup['backup_databases'],p_backup['api_server'], p_backup['status'])
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code':-1,'message':'保存失败!'}

async def upd_backup(p_backup):
    try:
        backupid         = p_backup['backup_id']
        backup_server    = p_backup['backup_server']
        db_server        = p_backup['db_server']
        db_type          = p_backup['db_type']
        backup_tag       = p_backup['backup_tag']
        backup_expire    = p_backup['backup_expire']
        backup_base      = format_sql(p_backup['backup_base'])
        script_base      = format_sql(p_backup['script_base'])
        script_name      = p_backup['script_name']
        cmd_name         = p_backup['cmd_name']
        run_time         = p_backup['run_time']
        task_desc        = p_backup['task_desc']
        python3_home     = format_sql(p_backup['python3_home'])
        backup_databases = p_backup['backup_databases']
        api_server       = p_backup['api_server']
        status           = p_backup['status']

        res = check_backup(p_backup)
        if res['code'] == '-1':
            return res

        st = """update t_db_config 
                  set  server_id         ='{0}', 
                       db_id             ='{1}',
                       db_type           ='{2}', 
                       db_tag            ='{3}', 
                       expire            ='{4}',
                       bk_base           ='{5}', 
                       script_path       ='{6}',
                       script_file       ='{7}', 
                       bk_cmd            ='{8}',
                       run_time          ='{9}',
                       comments          ='{10}',
                       python3_home      ='{11}',
                       backup_databases  ='{12}',
                       api_server        ='{13}',
                       STATUS            ='{14}'
                where id='{15}'""".format(backup_server,db_server,db_type,backup_tag,backup_expire,backup_base,
                                          script_base,script_name,cmd_name,run_time,task_desc,python3_home,
                                          backup_databases,api_server,status,backupid)
        await async_processer.exec_sql(st)
        return {'code':'0','message':'更新成功!'}
    except:
        return {'code': '-1', 'message': '更新失败!'}

async def del_backup(p_backupid):
    try:
        sql="delete from t_db_config  where id='{0}'".format(p_backupid)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except :
        return {'code': '-1', 'message': '删除失败!'}

async def get_backup_by_backupid(p_backupid):
    sql = """select server_id,
                    db_id,
                    db_type,
                    db_tag      as backup_tag,
                    expire      as backup_expire,
                    bk_base     as backup_base,
                    script_path as script_base,
                    script_file as script_name,
                    bk_cmd      as cmd_name,
                    run_time    as run_time,
                    comments,
                    python3_home,
                    backup_databases,
                    api_server,
                    status,
                    id  as backup_id
             from t_db_config where id={0}""".format(p_backupid)
    return await async_processer.query_dict_one(sql)

def check_backup(p_server):
    if p_server["backup_server"]=="":
       return {'code':'-1','message':'备份服务器不能为空!'}

    if p_server["db_server"]=="":
       return {'code': '-1', 'message': '数据库服务不能为空!'}

    if p_server["db_type"]=="":
       return {'code': '-1', 'message': '数据库类型不能为空!'}

    if p_server["backup_tag"]=="":
        return {'code': '-1', 'message': '备份标识号不能为空!'}

    if p_server["backup_expire"] == "":
        return {'code': '-1', 'message': '备份有效期不能为空!'}

    if p_server["backup_base"] == "":
        return {'code': '-1', 'message': '备份主目录不能为空!'}

    if p_server["script_base"] == "":
        return {'code': '-1', 'message': '脚本主目录不能为空!'}

    if p_server["script_name"] == "":
        return {'code': '-1', 'message': '备份脚本名不能为空!'}

    if p_server["cmd_name"] == "":
        return {'code': '-1', 'message': '备份命令名不能为空!'}

    if p_server["run_time"] == "":
        return {'code': '-1', 'message': '运行时间不能为空!'}

    if p_server["task_desc"] == "":
        return {'code': '-1', 'message': '任务描述不能为空!'}

    if p_server["python3_home"] == "":
        return {'code': '-1', 'message': 'PYTHON3主目录不能为空!'}

    if p_server["api_server"] == "":
        return {'code': '-1', 'message': 'API服务器不能为空!'}

    if p_server["status"] == "":
        return {'code': '-1', 'message': '任务状态不能为空!'}

    return {'code': '0', 'message': '验证通过!'}

def push_backup_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/push_script_remote'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    v = ''
    for c in jres['msg']:
        if c.count(p_tag)>0:
           v = v +"<span class='warning'>"+c +"</span>"
        else:
           v = v + c
        v  = v +'<br>'
    jres['msg'] = v
    return jres

def run_backup_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/run_script_remote'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    return jres

def stop_backup_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url  = 'http://{}/stop_script_remote'.format(p_api)
    res  = requests.post(url, data=data)
    jres = res.json()
    return jres