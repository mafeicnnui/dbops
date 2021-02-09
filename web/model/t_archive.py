#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info,format_sql
from web.utils.common     import get_connection,get_connection_dict
from web.model.t_ds       import get_ds_by_dsid
from web.model.t_user     import get_user_by_loginame
import re
import os,json
import traceback

def query_archive(sync_tag):
    db = get_connection()
    cr = db.cursor()
    v_where=' and  1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.archive_tag='{0}'\n".format(sync_tag)

    sql = """SELECT  a.id,
                 CONCAT(SUBSTR(a.archive_tag,1,40),'...') AS archive_tag,
                 a.archive_tag,
                 a.comments,
                 b.server_desc,
                 -- CONCAT(SUBSTR(CONCAT(sour_schema,'.',sour_table),1,40),'...') AS archive_obj,
                 a.api_server,
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
                FROM t_db_archive_config a,t_server b 
                WHERE a.server_id=b.id AND b.status='1' 
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

def query_archive_detail(archive_id):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT   a.archive_tag,
                      a.comments,
                      b.server_desc,
                      e.dmmc  AS db_type,
                      CONCAT(c.ip,':',c.port,'/',a.sour_schema) AS archive_db_sour,
                      LOWER(a.sour_table) AS sour_table,
                      a.archive_time_col,
                      a.archive_rentition,
                      a.rentition_time,
                      f.dmmc  AS rentition_time_type,
                      CONCAT(d.ip,':',d.port,'/',a.dest_schema) AS archive_db_dest,
                      a.`dest_schema`,
                      a.python3_home,
                      a.script_path,
                      a.script_file,
                      a.batch_size,
                      a.api_server,
                      a.status	                        
            FROM t_db_archive_config a,t_server b,t_db_source c,t_db_source d,t_dmmx e,t_dmmx f
            WHERE a.server_id=b.id 
                AND a.sour_db_id=c.id
                AND a.dest_db_id=d.id
                AND a.archive_db_type=e.dmm
                AND e.dm='02'
                AND f.dm= '20'
                AND a.id='{0}'
            ORDER BY a.id
             """.format(archive_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    print('query_archive_detail=>rs=',rs)
    # v_list=list(rs)
    cr.close()
    db.commit()
    return rs

def query_archive_log(transfer_tag,begin_date,end_date):
    db = get_connection()
    cr = db.cursor()

    v_where=' and 1=1 '
    if transfer_tag != '':
        v_where = v_where + " and a.archive_tag='{0}'\n".format(transfer_tag)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    else:
        v_where = v_where + " and a.create_date>=DATE_ADD(NOW(),INTERVAL -1 hour)\n"

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql = """SELECT 
                  a.id,
                  CONCAT(SUBSTR(a.archive_tag,1,40),'...'),
                  b.comments,
                  a.table_name,               
                  CAST(a.create_date AS CHAR),
                  CAST(a.amount AS CHAR),
                  CAST(a.duration AS CHAR),
                  a.message,
                  CAST(a.percent AS CHAR) 
                FROM
                  t_db_archive_log a,
                  t_db_archive_config b 
                WHERE a.archive_tag = b.archive_tag 
                 AND b.status='1'
                  {0}
                ORDER BY a.create_date DESC,a.archive_tag 
         """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_archive(p_archive):
    result = {}
    val=check_archive(p_archive)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        result  = {}
        sql="""insert into t_db_archive_config(
                         archive_tag,comments,archive_db_type,
                         server_id,sour_db_id,sour_schema,
                         sour_table,archive_time_col,archive_rentition,
                         rentition_time,rentition_time_type,dest_db_id,
                         dest_schema,python3_home,script_path,
                         script_file,batch_size,api_server,
                         status,if_cover,run_time)
               values('{0}','{1}','{2}','{3}','{4}','{5}',
                      '{6}','{7}','{8}','{9}','{10}','{11}',
                      '{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}')
            """.format(p_archive['archive_tag'],p_archive['task_desc'],p_archive['archive_db_type'],
                       p_archive['archive_server'],p_archive['sour_db_server'],p_archive['sour_db_name'],
                       p_archive['sour_tab_name'],p_archive['archive_time_col'], p_archive['archive_rentition'],
                       p_archive['rentition_time'], p_archive['rentition_time_type'],p_archive['dest_db_server'],
                       p_archive['dest_db_name'],p_archive['python3_home'],p_archive['script_base'],
                       p_archive['script_name'], p_archive['batch_size'], p_archive['api_server'],p_archive['status'],
                       p_archive['if_cover'], p_archive['run_time'])
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

def upd_archive(p_archive):
    result={}
    val = check_archive(p_archive)
    if  val['code'] == '-1':
        return val
    try:
        db   = get_connection()
        cr   = db.cursor()

        sql="""update t_db_archive_config 
                  set  
                      archive_tag         ='{0}',
                      comments            ='{1}', 
                      server_id           ='{2}',
                      archive_db_type     ='{3}', 
                      sour_db_id          ='{4}', 
                      sour_schema         ='{5}',
                      sour_table          ='{6}',
                      archive_time_col    ='{7}',
                      archive_rentition   ='{8}',
                      rentition_time      ='{9}',
                      rentition_time_type ='{10}',
                      dest_db_id          ='{11}',
                      dest_schema         ='{12}', 
                      python3_home        ='{13}',
                      script_path         ='{14}',
                      script_file         ='{15}',
                      batch_size          ='{16}',
                      api_server          ='{17}',
                      status              ='{18}',
                      if_cover            ='{19}',
                      run_time            ='{20}'
                where id={21}
            """.format(p_archive['archive_tag'],p_archive['task_desc'],p_archive['archive_server'],
                       p_archive['archive_db_type'],p_archive['sour_db_server'],p_archive['sour_db_name'],
                       p_archive['sour_tab_name'],p_archive['archive_time_col'], p_archive['archive_rentition'],
                       p_archive['rentition_time'], p_archive['rentition_time_type'],p_archive['dest_db_server'],
                       p_archive['dest_db_name'],p_archive['python3_home'],p_archive['script_base'],
                       p_archive['script_name'], p_archive['batch_size'], p_archive['api_server'],p_archive['status'],
                       p_archive['if_cover'], p_archive['run_time'],p_archive['archive_id'])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_archive(p_archiveid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_archive_config  where id='{0}'".format(p_archiveid)
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

def check_archive(p_archive):
    result = {}

    if p_archive["archive_tag"]=="":
        result['code']='-1'
        result['message']='归档标识号不能为空！'
        return result

    if p_archive["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_archive["archive_server"]=="":
        result['code']='-1'
        result['message']='传输服务器不能为空！'
        return result

    if p_archive["sour_db_server"]=="":
        result['code']='-1'
        result['message']='源数据库实例不能为空！'
        return result

    if p_archive["sour_db_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库名不能为空！'
        return result

    if p_archive["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库表名不能为空！'
        return result

    if p_archive['archive_rentition'] == '2':
        if p_archive["dest_db_server"]=="":
            result['code']='-1'
            result['message']='目标数据库实例不能为空！'
            return result

        if p_archive["dest_db_name"] == "":
            result['code'] = '-1'
            result['message'] = '目标数据库名称不能为空！'
            return result

        if p_archive["batch_size"] == "":
            result['code'] = '-1'
            result['message'] = '批大小不能为空！'
            return result

    if p_archive["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_archive["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '归档主目录不能为空！'
        return result

    if p_archive["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '归档脚本名不能为空！'
        return result

    if p_archive["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_archive["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_archive_by_archiveid(p_archiveid):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT   id,archive_tag,server_id,comments,archive_db_type,sour_db_id,sour_schema,
                      sour_table,archive_time_col,archive_rentition,rentition_time,rentition_time_type,dest_db_id,dest_schema,script_path,
                      script_file,python3_home,api_server,status,batch_size,if_cover,run_time
             FROM t_db_archive_config where id={0}
          """.format(p_archiveid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    print('get_archive_by_archiveid->rs=',rs)
    return rs[0]

def push_archive_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'
        v_cmd="curl -XPOST {0}/push_script_remote_archive -d 'tag={1}'".format(p_api,p_tag)
        print('push_archive_task=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)

        if d['code']==200:
           return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print('push_archive_task.error:',traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '{0!'.format(traceback.format_exc())
        return result

def run_archive_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_script_remote_archive -d 'tag={1}'".format(p_api,p_tag)
        print('v_cmd=', v_cmd)
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
          result['message'] = '{0}!'.format(str(e))
          return result

def stop_archive_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '停止成功！'
        v_cmd = "curl -XPOST {0}/stop_script_remote_archive -d 'tag={1}'".format(p_api,p_tag)
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

