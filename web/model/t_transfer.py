#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common     import exception_info,current_rq,aes_encrypt,aes_decrypt,format_sql
from web.utils.common     import get_connection,get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle,get_connection_ds_pg
from web.model.t_ds       import get_ds_by_dsid
from web.model.t_user     import get_user_by_loginame
import re
import os,json
import traceback

def query_transfer(sync_tag):
    db = get_connection()
    cr = db.cursor()
    v_where=' and  1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.transfer_tag='{0}'\n".format(sync_tag)

    sql = """SELECT  a.id,
                 concat(substr(a.transfer_tag,1,40),'...') as transfer_tag,
                 a.transfer_tag,
                 concat(substr(a.comments,1,30),'...') as  comments,
                 b.server_desc,
                 -- concat(substr(concat(sour_schema,'.',sour_table),1,40),'...') as transfer_obj,
                 a.api_server,
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_db_transfer_config a,t_server b 
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

def query_transfer_detail(transfer_id):
    db = get_connection()
    cr = db.cursor()
    sql = """SELECT   a.transfer_tag,
                      a.comments,
                      b.server_desc,
                      e.dmmc  AS transfer_type,
                      CONCAT(c.ip,':',c.port,'/',a.sour_schema) AS transfer_db_sour,
                      a.sour_schema,
                      LOWER(a.sour_table) AS sour_table,
                      a.sour_where,            
                      CONCAT(d.ip,':',d.port,'/',a.dest_schema) AS transfer_db_dest,
                      a.`dest_schema`,
                      a.python3_home,
                      a.script_path,
                      a.script_file,
                      a.batch_size,
                      a.api_server,
                      a.status	                        
                FROM t_db_transfer_config a,t_server b,t_db_source c,t_db_source d,t_dmmx e
                WHERE a.server_id=b.id 
                AND a.sour_db_id=c.id
                AND a.dest_db_id=d.id
                AND a.transfer_type=e.dmm
                AND e.dm='09'
                AND a.id='{0}'
                ORDER BY a.id
             """.format(transfer_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    v_list=list(rs)
    cr.close()
    db.commit()
    return v_list

def query_transfer_log(transfer_tag,begin_date,end_date,task_status):
    db = get_connection()
    cr = db.cursor()

    v_where=' and 1=1 '
    if transfer_tag != '':
        v_where = v_where + " and a.transfer_tag='{0}'\n".format(transfer_tag)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    else:
        v_where = v_where + " and a.create_date>=DATE_ADD(NOW(),INTERVAL -1 hour)\n"

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    if task_status == 'running':
        v_where = v_where + " and a.percent!=100.00 \n"

    if task_status == 'history':
        v_where = v_where + " and a.percent=100.00 \n"

    sql = """SELECT 
                  a.id,
                  concat(substr(a.transfer_tag,1,40),'...'),
                  b.comments,
                  a.table_name,               
                  cast(a.create_date as char),
                  cast(a.amount as char),
                  cast(a.duration as char),
                  cast(a.percent as char)              
                FROM
                  t_db_transfer_log a,
                  t_db_transfer_config b 
                WHERE a.transfer_tag = b.transfer_tag 
                 and b.status='1'
                 {0}
             order by a.create_date desc,a.transfer_tag 
        """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def save_transfer(p_transfer):
    result = {}
    #增加tag重复验证
    val=check_transfer(p_transfer)
    if val['code']=='-1':
        return val
    try:
        db                      = get_connection()
        cr                      = db.cursor()
        result                  = {}
        transfer_tag            = p_transfer['transfer_tag']
        task_desc               = p_transfer['task_desc']
        transfer_server         = p_transfer['transfer_server']
        transfer_type           = p_transfer['transfer_type']
        sour_db_server          = p_transfer['sour_db_server']
        sour_db_name            = p_transfer['sour_db_name']
        sour_tab_name           = p_transfer['sour_tab_name']
        sour_tab_where          = format_sql(p_transfer['sour_tab_where'])
        dest_db_server          = p_transfer['dest_db_server']
        dest_db_name            = p_transfer['dest_db_name']
        python3_home            = p_transfer['python3_home']
        script_base             = p_transfer['script_base']
        script_name             = p_transfer['script_name']
        batch_size              = p_transfer['batch_size']
        api_server              = p_transfer['api_server']
        status                  = p_transfer['status']

        sql="""insert into t_db_transfer_config(
                      transfer_tag,server_id,comments,sour_db_id,sour_schema,
                      sour_table,sour_where,dest_db_id,dest_schema,script_path,
                      script_file,python3_home,api_server,batch_size,status,transfer_type)
               values('{0}','{1}','{2}','{3}','{4}',
                      '{5}','{6}','{7}','{8}','{9}',
                      '{10}','{11}','{12}','{13}','{14}','{15}')
            """.format(transfer_tag,transfer_server,task_desc,sour_db_server,sour_db_name,
                       sour_tab_name,sour_tab_where,dest_db_server,dest_db_name,script_base,
                       script_name,python3_home,api_server,batch_size,status,transfer_type)
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

def upd_transfer(p_transfer):
    result={}
    val = check_transfer(p_transfer)
    if  val['code'] == '-1':
        return val
    try:
        db              = get_connection()
        cr              = db.cursor()
        transfer_id     = p_transfer['transfer_id']
        transfer_tag    = p_transfer['transfer_tag']
        task_desc       = p_transfer['task_desc']
        transfer_server = p_transfer['transfer_server']
        transfer_type   = p_transfer['transfer_type']
        sour_db_server  = p_transfer['sour_db_server']
        sour_db_name    = p_transfer['sour_db_name']
        sour_tab_name   = p_transfer['sour_tab_name']
        sour_tab_where  = p_transfer['sour_tab_where']
        dest_db_server  = p_transfer['dest_db_server']
        dest_db_name    = p_transfer['dest_db_name']
        script_base     = p_transfer['script_base']
        script_name     = p_transfer['script_name']
        python3_home    = p_transfer['python3_home']
        batch_size      = p_transfer['batch_size']
        api_server      = p_transfer['api_server']
        status          = p_transfer['status']

        sql="""update t_db_transfer_config 
                  set  
                      transfer_tag      ='{0}',
                      server_id         ='{1}', 
                      comments          ='{2}', 
                      sour_db_id        ='{3}', 
                      sour_schema       ='{4}',
                      sour_table        ='{5}',
                      sour_where        ='{6}',
                      dest_db_id        ='{7}',
                      dest_schema       ='{8}',                    
                      script_path       ='{9}',
                      script_file       ='{10}',
                      python3_home      ='{11}',
                      api_server        ='{12}',                   
                      status            ='{13}',
                      batch_size        ='{14}',
                      transfer_type     ='{15}'
                where id={16}""".format(transfer_tag,transfer_server,task_desc,sour_db_server,sour_db_name,
                                        sour_tab_name,format_sql(sour_tab_where),dest_db_server,dest_db_name,script_base,
                                        script_name,python3_home,api_server,status,batch_size,transfer_type,transfer_id)
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

def del_transfer(p_transferid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_db_transfer_config  where id='{0}'".format(p_transferid)
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

def check_transfer(p_transfer):
    result = {}

    if p_transfer["transfer_tag"]=="":
        result['code']='-1'
        result['message']='传输标识号不能为空！'
        return result

    if p_transfer["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_transfer["transfer_server"]=="":
        result['code']='-1'
        result['message']='传输服务器不能为空！'
        return result

    if p_transfer["sour_db_server"]=="":
        result['code']='-1'
        result['message']='源数据库实例不能为空！'
        return result

    if p_transfer["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库表名不能为空！'
        return result

    if p_transfer["dest_db_server"]=="":
        result['code']='-1'
        result['message']='目标数据库实例不能为空！'
        return result

    if p_transfer["dest_db_name"] == "":
        result['code'] = '-1'
        result['message'] = '目标数据库名称不能为空！'
        return result

    if p_transfer["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_transfer["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '传输主目录录不能为空！'
        return result

    if p_transfer["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '传输脚本名不能为空！'
        return result

    if p_transfer["batch_size"] == "":
        result['code'] = '-1'
        result['message'] = '批大小不能为空！'
        return result

    if p_transfer["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_transfer["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_transfer_by_transferid(p_transferid):
    db = get_connection()
    cr = db.cursor()
    sql = """select   id,transfer_tag,server_id,comments,sour_db_id,sour_schema,
                      sour_table,sour_where,dest_db_id,dest_schema,script_path,
                      script_file,python3_home,api_server,status,batch_size,transfer_type
             from t_db_transfer_config where id={0}
          """.format(p_transferid)
    cr.execute(sql)
    rs = cr.fetchall()
    d_transfer = {}
    d_transfer['server_id']      = rs[0][0]
    d_transfer['transfer_tag']   = rs[0][1]
    d_transfer['server_id']      = rs[0][2]
    d_transfer['task_desc']      = rs[0][3]
    d_transfer['sour_db_id']     = rs[0][4]
    d_transfer['sour_schema']    = rs[0][5]
    d_transfer['sour_table']     = rs[0][6]
    d_transfer['sour_where']     = rs[0][7]
    d_transfer['dest_db_id']     = rs[0][8]
    d_transfer['dest_schema']    = rs[0][9]
    d_transfer['script_path']    = rs[0][10]
    d_transfer['script_file']    = rs[0][11]
    d_transfer['python3_home']   = rs[0][12]
    d_transfer['api_server']     = rs[0][13]
    d_transfer['status']         = rs[0][14]
    d_transfer['batch_size']     = rs[0][15]
    d_transfer['transfer_type']  = rs[0][16]
    cr.close()
    db.commit()
    print(d_transfer)
    return d_transfer

def push_transfer_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'
        v_cmd="curl -XPOST {0}/push_script_remote_transfer -d 'tag={1}'".format(p_api,p_tag)
        print('push_transfer_task=',v_cmd)
        r=os.popen(v_cmd).read()
        d=json.loads(r)
        if d['code']==200:
           return result
        else:
           result['code'] = '-1'
           result['message'] = '{0}!'.format(d['msg'])
           return result
    except Exception as e:
        print('push_transfer_task.error:',traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '{0!'.format(traceback.format_exc())
        return result

def run_transfer_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_script_remote_transfer -d 'tag={1}'".format(p_api,p_tag)
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

def stop_transfer_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '停止成功！'
        v_cmd = "curl -XPOST {0}/stop_script_remote_transfer -d 'tag={1}'".format(p_api,p_tag)
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

