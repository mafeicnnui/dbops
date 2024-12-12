#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/30 11:03
# @Author : 马飞
# @File : run_task.py
# @Software: PyCharm

import datetime
import time
import traceback

import pymysql

from web.utils.common import get_db_conf

cfg = get_db_conf()


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_connection():
    ip = cfg['db_ip']
    port = cfg['db_port']
    service = cfg['db_service']
    user = cfg['db_user']
    password = cfg['db_pass']
    charset = cfg['db_charset']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset=charset)
    return conn


def get_connection_dict():
    ip = cfg['db_ip']
    port = cfg['db_port']
    service = cfg['db_service']
    user = cfg['db_user']
    password = cfg['db_pass']
    charset = cfg['db_charset']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,
                           db=service, charset=charset, cursorclass=pymysql.cursors.DictCursor)
    return conn


def get_connection_ds(p_ds, p_timeout):
    ip = p_ds['db_ip']
    port = p_ds['db_port']
    service = p_ds['db_service']
    user = p_ds['db_user']
    password = p_ds['db_pass']
    charset = cfg['db_charset']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,
                           db=service, charset=charset, read_timeout=p_timeout, write_timeout=p_timeout)
    return conn


def aes_decrypt(p_password, p_key):
    try:
        db = get_connection()
        cr = db.cursor()
        sql = """select aes_decrypt(unhex('{0}'),'{1}')""".format(p_password, p_key[::-1])
        cr.execute(sql)
        rs = cr.fetchone()
        db.commit()
        cr.close()
        db.close()
        return str(rs[0], encoding="utf-8")
    except:
        return ''


def get_audit_rule(p_key):
    db = get_connection_dict()
    cr = db.cursor()
    st = "select * from t_sql_audit_rule where rule_code='{0}'".format(p_key)
    cr.execute(st)
    rs = cr.fetchone()
    cr.close()
    return rs


def get_ds_by_instid(p_inst_id):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """SELECT a.id        as dsid,
                    a.inst_name as db_desc,
                    b.server_ip as db_ip,                    
                    CASE when a.inst_mapping_port is null or a.inst_mapping_port ='' then 
                       a.inst_port 
                    ELSE 
                       a.inst_mapping_port
                    END as db_port,
                    a.inst_type as db_type,
                    a.inst_env  as db_env,
                    a.mgr_user  as db_user,
                    a.mgr_pass  as db_password,
                    ''          as db_service,
                    date_format(a.created_date,'%Y-%m-%d %H:%i:%s')  as created_date
             FROM t_db_inst a,t_server b  WHERE a.server_id=b.id and a.id='{0}'""".format(p_inst_id)
    cr.execute(sql)
    rs = cr.fetchone()
    rs['db_pass'] = aes_decrypt(rs['db_password'], rs['db_user'])
    cr.close()
    db.commit()
    return rs


def get_ds_by_dsid(p_dsid):
    db = get_connection_dict()
    cr = db.cursor()
    sql = """select cast(id as char) as dsid,
                  db_type,
                  db_desc,
                  ip       as db_ip,
                  port     as db_port,
                  service  as db_service,
                  user     as db_user,
                  password as db_password,
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
    cr.execute(sql)
    ds = cr.fetchone()
    ds['db_pass'] = aes_decrypt(ds['db_password'], ds['db_user'])
    return ds


def get_task():
    db = get_connection_dict()
    cr = db.cursor()
    st = "SELECT id,inst_id,db,statement,status,message FROM t_db_inst_opt_log WHERE STATUS='1' order by id LIMIT 1 "
    cr.execute(st)
    rs = cr.fetchone()
    cr.close()
    return rs


def get_ds_task():
    db = get_connection_dict()
    cr = db.cursor()
    st = "SELECT id,ds_id,db,statement,status,message FROM t_db_opt_log WHERE STATUS='1' order by id LIMIT 1 "
    cr.execute(st)
    rs = cr.fetchone()
    cr.close()
    return rs


def upd_task(p_task):
    db = get_connection_dict()
    cr = db.cursor()
    st = '''update t_db_inst_opt_log set start_time='{}', end_time='{}',status ='{}',message='{}' WHERE id='{}'
         '''.format(p_task.get('start_time'), p_task.get('end_time'), p_task.get('status'), p_task.get('message'),
                    p_task.get('id'))
    print('upd_task=', st)
    cr.execute(st)
    rs = cr.fetchone()
    db.commit()
    cr.close()
    return rs


def upd_ds_task(p_task):
    db = get_connection_dict()
    cr = db.cursor()
    st = '''update t_db_opt_log set start_time='{}', end_time='{}',status ='{}',message='{}' WHERE id='{}'
         '''.format(p_task.get('start_time'), p_task.get('end_time'), p_task.get('status'), p_task.get('message'),
                    p_task.get('id'))
    print('upd_ds_task=', st)
    cr.execute(st)
    rs = cr.fetchone()
    db.commit()
    cr.close()
    return rs


def format_sql(v_sql):
    return v_sql.replace("\\", "\\\\").replace("'", "\\'")


'''
  任务状态 ：1：已就绪(已发布)，2：运行中，3：已完成，4：运行失败
'''


def run_task(p_task):
    timeout = int(get_audit_rule('switch_ddl_timeout')['rule_value'])
    p_ds = get_ds_by_instid(p_task['inst_id'])
    p_ds['db_service'] = p_task['db']
    print('p_ds=', p_ds)
    db = get_connection_ds(p_ds, timeout)
    cr = db.cursor()
    try:
        p_task['start_time'] = get_time()
        p_task['end_time'] = ''
        p_task['status'] = '2'
        p_task['message'] = ''
        upd_task(p_task)
        print('statement=>', p_task['statement'])
        cr.execute(p_task['statement'])
        db.commit()
        p_task['end_time'] = get_time()
        p_task['status'] = '3'
        upd_task(p_task)
    except:
        p_task['status'] = '4'
        p_task['message'] = format_sql(traceback.format_exc())
        upd_task(p_task)


def run_ds_task(p_task):
    timeout = int(get_audit_rule('switch_ddl_timeout')['rule_value'])
    p_ds = get_ds_by_dsid(p_task['ds_id'])
    p_ds['db_service'] = p_task['db']
    print('p_ds=', p_ds)
    db = get_connection_ds(p_ds, timeout)
    cr = db.cursor()
    try:
        p_task['start_time'] = get_time()
        p_task['end_time'] = ''
        p_task['status'] = '2'
        p_task['message'] = ''
        upd_ds_task(p_task)
        print('statement=>', p_task['statement'])
        cr.execute(p_task['statement'])
        db.commit()
        p_task['end_time'] = get_time()
        p_task['status'] = '3'
        upd_ds_task(p_task)
    except:
        p_task['status'] = '4'
        p_task['message'] = format_sql(traceback.format_exc())
        upd_ds_task(p_task)


def init_task(p_task):
    p_task['start_time'] = ''
    p_task['end_time'] = ''
    p_task['status'] = '1'
    p_task['message'] = ''


def main():
    while True:
        task = get_task()
        if task:
            print('\nProcessing Task:', task)
            init_task(task)
            upd_task(task)
            print('run task=>', task)
            run_task(task)
        else:
            print('\rTask not ready,sleeping ...', end='')
            time.sleep(1)

        ds_task = get_ds_task()
        if ds_task:
            print('\nProcessing Ds Task:', ds_task)
            init_task(ds_task)
            upd_ds_task(ds_task)
            print('run ds task=>', ds_task)
            run_ds_task(ds_task)
        else:
            print('\rDs Task not ready,sleeping ...', end='')
            time.sleep(1)


if __name__ == '__main__':
    main()
