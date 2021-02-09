#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/30 11:03
# @Author : 马飞
# @File : run_task.py
# @Software: PyCharm

import time
import pymysql
import traceback
import datetime
from web.utils.common import get_db_conf

cfg = get_db_conf()

def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_connection():
    ip       = cfg['ip']
    port     = cfg['port']
    service  = cfg['db']
    user     = cfg['user']
    password = cfg['password']
    conn     = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,db=service, charset='utf8')
    return conn

def get_connection_dict():
    ip       = cfg['ip']
    port     = cfg['port']
    service  = cfg['db']
    user     = cfg['user']
    password = cfg['password']
    conn     = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,
                               db=service, charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    return conn

def get_connection_ds(p_ds,p_timeout):
    ip       = p_ds['ip']
    port     = p_ds['port']
    service  = p_ds['db']
    user     = p_ds['user']
    password = p_ds['password']
    conn     = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,
                               db=service, charset='utf8',read_timeout=p_timeout,write_timeout=p_timeout)
    return conn

def aes_decrypt(p_password,p_key):
    try:
        db = get_connection()
        cr = db.cursor()
        sql="""select aes_decrypt(unhex('{0}'),'{1}')""".format(p_password,p_key[::-1])
        cr.execute(sql)
        rs=cr.fetchone()
        db.commit()
        cr.close()
        db.close()
        return str(rs[0],encoding = "utf-8")
    except:
        return ''

def get_audit_rule(p_key):
    db = get_connection_dict()
    cr = db.cursor()
    st = "select * from t_sql_audit_rule where rule_code='{0}'".format(p_key)
    cr.execute(st)
    rs=cr.fetchone()
    cr.close()
    return rs

def get_ds_by_instid(p_inst_id):
    db  = get_connection_dict()
    cr  = db.cursor()
    sql = """SELECT a.id        as dsid,
                    a.inst_name as db_desc,
                    b.server_ip as ip,
                    
                    CASE when a.inst_mapping_port is null or a.inst_mapping_port ='' then 
                       a.inst_port 
                    ELSE 
                       a.inst_mapping_port
                    END as port,
                    a.inst_type as db_type,
                    a.inst_env  as db_env,
                    a.mgr_user  as user,
                    a.mgr_pass  as password,
                    ''        as db,
                    date_format(a.created_date,'%Y-%m-%d %H:%i:%s')  as created_date
             FROM t_db_inst a,t_server b  WHERE a.server_id=b.id and a.id='{0}'""".format(p_inst_id)
    cr.execute(sql)
    rs=cr.fetchone()
    rs['password'] = aes_decrypt(rs['password'],rs['user'])
    cr.close()
    db.commit()
    return rs

def get_task():
    db = get_connection_dict()
    cr = db.cursor()
    st = "SELECT id,inst_id,db,statement,status,message FROM t_db_inst_opt_log WHERE STATUS='1' order by id LIMIT 1 "
    cr.execute(st)
    rs = cr.fetchone()
    cr.close()
    return rs

def upd_task(p_task):
    db = get_connection_dict()
    cr = db.cursor()
    st = '''update t_db_inst_opt_log set start_time='{}', end_time='{}',status ='{}',message='{}' WHERE id='{}'
         '''.format(p_task.get('start_time'),p_task.get('end_time'),p_task.get('status'),p_task.get('message'),p_task.get('id'))
    print('upd_task=',st)
    cr.execute(st)
    rs = cr.fetchone()
    db.commit()
    cr.close()
    return rs

def format_sql(v_sql):
    return v_sql.replace("\\","\\\\").replace("'","\\'")

'''
  任务状态 ：1：已就绪(已发布)，2：运行中，3：已完成，4：运行失败
'''
def run_task(p_task):
    timeout              = int(get_audit_rule('switch_ddl_timeout')['rule_value'])
    p_ds                 = get_ds_by_instid(p_task['inst_id'])
    p_ds['service']      = p_task['db']
    db                   = get_connection_ds(p_ds,timeout)
    cr                   = db.cursor()
    try:
        p_task['start_time'] = get_time()
        p_task['end_time']   = ''
        p_task['status']     = '2'
        p_task['message']    = ''
        upd_task(p_task)
        print('statement=>',p_task['statement'])
        cr.execute(p_task['statement'])
        db.commit()
        p_task['end_time'] = get_time()
        p_task['status']   = '3'
        upd_task(p_task)
    except:
        p_task['status'] = '4'
        p_task['message'] = format_sql(traceback.format_exc())
        upd_task(p_task)

def init_task(p_task):
    p_task['start_time'] = ''
    p_task['end_time']   = ''
    p_task['status']     = '1'
    p_task['message']    = ''

def main():
    while True:
      task=get_task()
      if  task:
          print('\nProcessing Task:',task)
          init_task(task)
          upd_task(task)
          print('run task=>',task)
          run_task(task)
      else:
          print('\rTask not ready,sleeping ...',end='')
          time.sleep(1)

if __name__ == '__main__':
   main()

