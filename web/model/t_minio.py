#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info,current_rq,aes_encrypt,aes_decrypt,format_sql
from web.utils.common     import get_connection,get_connection_dict,get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle,get_connection_ds_pg
from web.model.t_user     import get_user_by_loginame
import re
import os,json
import traceback
import requests

def query_minio(tagname):
    db = get_connection()
    cr = db.cursor()
    v_where = ' and 1=1 '
    if  tagname!='':
       v_where=v_where+" and a.sync_tag='{0}'\n".format(tagname)

    sql = """SELECT   
                      a.sync_tag,
                      a.comments,
                      concat(b.server_ip,':',b.server_port),
                      (select dmmc from t_dmmx x where x.dm='34' and x.dmm=a.sync_type) as sync_type,
                      a.minio_server,
                      a.run_time,
                      a.api_server,
                      CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
              FROM t_minio_config a,t_server b
              WHERE a.server_id=b.id 
                AND b.status='1'
                {0}
                """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_minio_case(p_db_env):
    result = {}
    db  = get_connection()
    cr  = db.cursor()
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
               AND create_date=DATE_SUB(DATE(NOW()),INTERVAL 1 DAY)
             ORDER BY a.db_env,a.db_type
                """.format(p_db_env)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))

    result['data']=v_list

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
                   AND create_date=DATE_SUB(DATE(NOW()),INTERVAL 1 DAY)
                 ORDER BY a.db_env,a.db_type
                    """.format(p_db_env)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    result['success'] = rs[0]
    result['failure'] = rs[1]
    cr.close()
    db.commit()
    return result

def query_minio_log(tagname,begin_date,end_date):
    db = get_connection()
    cr = db.cursor()
    print('query_minio_log=',tagname,begin_date,end_date)
    v_where = ' and 1=1 '
    if  tagname != '':
        v_where = v_where+" and a.sync_tag='{0}'\n".format(tagname)

    if  begin_date != '':
        v_where = v_where+" and b.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if  end_date != '':
        v_where = v_where+" and b.create_date<='{0}'\n".format(end_date+' 23:59:59')

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
              AND a.status='1'
              {}
            ORDER BY b.sync_tag,b.create_date """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_minio_log_analyze(tagname,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = " where a.sync_tag=b.sync_tag and a.status='1'"

    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)

    if begin_date != '':
        v_where = v_where + " and b.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                     cast(b.create_date as char) as create_date,
                     b.download_time
             FROM t_minio_config a,t_minio_log b
             {0}
             ORDER BY b.sync_tag,b.create_date
          """.format(v_where)

    sql2 = """SELECT 
                  cast(b.create_date as char) as create_date,
                  b.upload_time
             FROM t_minio_config a,t_minio_log b
              {0}
             ORDER BY b.sync_tag,b.create_date
           """.format(v_where)

    sql3 = """SELECT 
                  cast(b.create_date as char) as create_date,
                  b.transfer_file
             FROM t_minio_config a,t_minio_log b
              {0}
             ORDER BY b.sync_tag,b.create_date
           """.format(v_where)

    print(sql1)
    print(sql2)
    print(sql3)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.execute(sql3)
    v_list3 = []
    for r in cr.fetchall():
        v_list3.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2,v_list3

def query_minio_log_detail(tagname,backup_date):
    db = get_connection()
    cr = db.cursor()
    print('query_backup_detail_log=', tagname, backup_date)
    v_where = ' and 1=1 '
    if tagname != '':
        v_where = v_where + " and b.db_tag='{0}'\n".format(tagname)

    if backup_date != '':
        v_where = v_where + " and b.create_date='{0}'\n".format(backup_date)

    sql = """SELECT 
                a.comments,
	            a.db_tag,
                b.db_name,
                b.file_name,
                b.bk_path,
                CAST(b.create_date AS CHAR), 
                CAST(b.start_time AS CHAR),
                CAST(b.end_time AS CHAR),	
                b.db_size,
                b.elaspsed_backup,
                b.elaspsed_gzip,
                CASE b.STATUS WHEN '1' THEN '<span style=''color: red''>失败</span>' WHEN '0' THEN '成功' END  STATUS
            FROM  t_db_config a,t_db_backup_detail b,t_db_source c
            WHERE a.db_tag=b.db_tag
             AND a.db_id=c.id
             AND a.status='1'
                 {0}
             order by b.create_date,b.db_tag """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_minio(p_sync):
    result = {}
    val=check_minio(p_sync,'I')
    if val['code']=='-1':
        return val
    try:
        db       = get_connection()
        cr       = db.cursor()
        result   = {}
        sql      = """insert into t_minio_config(
                           sync_tag,comments,sync_type,
                           server_id,sync_path,sync_service,
                           minio_server, python3_home,script_path,
                           script_file,api_server,run_time,
                           status,minio_user,minio_pass,
                           minio_bucket,minio_dpath,minio_incr,minio_incr_type) 
                    values('{}','{}','{}',
                           '{}','{}','{}',
                           '{}','{}','{}',
                           '{}','{}','{}',
                           '{}','{}','{}',
                           '{}','{}','{}','{}')
                   """.format(p_sync['sync_tag'],p_sync['task_desc'],p_sync['sync_type'],
                              p_sync['server_id'],p_sync['sync_dir'],p_sync['sync_service'],
                              p_sync['minio_server'],p_sync['python3_home'],p_sync['script_base'],
                              p_sync['script_name'],p_sync['api_server'],p_sync['run_time'],
                              p_sync['status'],p_sync['minio_user'],p_sync['minio_pass'],
                              p_sync['minio_bucket'], p_sync['minio_dpath'], p_sync['minio_incr'],p_sync['minio_incr_type'])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_minio(p_sync):
    result={}
    val = check_minio(p_sync,'U')
    if  val['code'] == '-1':
        return val
    try:
        db = get_connection()
        cr = db.cursor()
        sql="""update t_minio_config 
                  set  comments          ='{}',
                       sync_type         ='{}',
                       server_id         ='{}',                        
                       sync_path         ='{}', 
                       sync_service      ='{}',           
                       minio_server      ='{}',   
                       python3_home      ='{}',                        
                       script_path       ='{}',           
                       script_file       ='{}', 
                       api_server        ='{}',
                       run_time          ='{}',
                       STATUS            ='{}',
                       minio_user        ='{}',
                       minio_pass        ='{}',
                       minio_bucket      ='{}',
                       minio_dpath       ='{}',
                       minio_incr        ='{}',
                       minio_incr_type   ='{}'
                where sync_tag='{}'""".format(p_sync['task_desc'],p_sync['sync_type'],p_sync['server_id'],
                                              p_sync['sync_dir'],p_sync['sync_service'],p_sync['minio_server'],
                                              p_sync['python3_home'],p_sync['script_base'], p_sync['script_name'],
                                              p_sync['api_server'],p_sync['run_time'],p_sync['status'],
                                              p_sync['minio_user'],p_sync['minio_pass'],p_sync['minio_bucket'],
                                              p_sync['minio_dpath'], p_sync['minio_incr'],p_sync['minio_incr_type'],
                                              p_sync['sync_tag']
                                              )
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.print_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_minio(p_sync_tag):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_minio_config  where sync_tag='{0}'".format(p_sync_tag)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def check_sync_tag_rep(p_sync):
    db = get_connection()
    cr = db.cursor()
    sql = "select count(0) from t_minio_config  where  sync_tag='{0}'".format(p_sync["sync_tag"])
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    cr.close()
    db.commit()
    return rs[0]

def check_minio(p_sync,p_flag):
    result = {}
    if p_sync["sync_tag"]=="":
        result['code']='-1'
        result['message']='同步标识不能为空！'
        return result

    if check_sync_tag_rep(p_sync)>0 and p_flag=='I':
        result['code'] = '-1'
        result['message'] = '同步标识重复!'
        return result

    if p_sync["task_desc"]=="":
        result['code']='-1'
        result['message']='任务描述不能为空！'
        return result

    if p_sync["server_id"]=="":
        result['code']='-1'
        result['message']='同步服务器不能为空！'
        return result

    if p_sync["sync_type"]=="":
        result['code']='-1'
        result['message']='同步类型不能为空！'
        return result

    if p_sync["sync_type"]=="1" and p_sync["sync_dir"] == "":
        result['code'] = '-1'
        result['message'] = '同步目录不能为空！'
        return result

    if p_sync["sync_type"]=="2" and p_sync["sync_service"] == "":
        result['code'] = '-1'
        result['message'] = '同步服务不能为空！'
        return result

    if p_sync["minio_server"] == "":
        result['code'] = '-1'
        result['message'] = 'MinIO服务地址不能为空！'
        return result

    if p_sync["minio_user"] == "":
        result['code'] = '-1'
        result['message'] = 'MinIO服务用户名不能为空！'
        return result

    if p_sync["minio_pass"] == "":
        result['code'] = '-1'
        result['message'] = 'MinIO服务口令不能为空！'
        return result

    if p_sync["minio_bucket"] == "":
        result['code'] = '-1'
        result['message'] = 'MinIO桶名不能为空！'
        return result

    if p_sync["minio_incr"] == "":
        result['code'] = '-1'
        result['message'] = '增量同步天数不能为空！'
        return result

    if p_sync["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_sync["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '脚本目录不能为空！'
        return result

    if p_sync["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '脚本名称不能为空！'
        return result

    if p_sync["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '运行时间不能为空！'
        return result

    if p_sync["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_sync["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_minio_by_minioid(p_sync_tag):
    db = get_connection_dict()
    cr = db.cursor()
    sql = "select * from t_minio_config where sync_tag='{0}'".format(p_sync_tag)
    cr.execute(sql)
    rs = cr.fetchone()
    cr.close()
    db.commit()
    print(rs)
    return rs

def push_minio_task(p_tag,p_api):
    url = 'http://{}/push_minio_remote'.format(p_api)
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


def run_minio_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_script_remote -d 'tag={1}'".format(p_api,p_tag)
        r  = os.popen(v_cmd).read()
        d  = json.loads(r)

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

def stop_minio_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        r = os.system("curl -XPOST {0}/stop_script_remote -d 'tag={1}'".format(p_api,p_tag))
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
