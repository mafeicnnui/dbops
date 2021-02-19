#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/8 11:10
# @Author : ma.fei
# @File : webchat.py.py
# @Software: PyCharm
# @Function: EaseBase服务监控微信推送

import requests
import traceback
import pymysql
import smtplib
import datetime
from email.mime.text import MIMEText

'''
  功能：全局配置
'''
config = {
    "chat_interface":"https://alarm.lifeat.cn/wx/cp/msg/1000011",
    "mysql":"10.2.39.17:23306:puppet:puppet:Puppet@123",
    "warn_level":"紧急"
}

'''
  功能：获取mysql连接，以元组返回
'''
def get_ds_mysql(ip,port,service ,user,password):
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8')
    return conn

'''
  功能：获取mysql连接，以字典返回
'''
def get_ds_mysql_dict(ip,port,service ,user,password):
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service,
                           charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    return conn


'''
 功能：获取数据库连接
'''
def get_config(config):
    db_ip                   = config['mysql'].split(':')[0]
    db_port                 = config['mysql'].split(':')[1]
    db_service              = config['mysql'].split(':')[2]
    db_user                 = config['mysql'].split(':')[3]
    db_pass                 = config['mysql'].split(':')[4]
    config['db_mysql']      = get_ds_mysql(db_ip,db_port,db_service,db_user,db_pass)
    config['db_mysql_dict'] = get_ds_mysql_dict(db_ip, db_port, db_service, db_user, db_pass)
    return config

'''
  功能：调用接口发送消息
'''
def send_message(config,message):
    try:
        r = requests.post(config['chat_interface'], data=bytes(message, 'UTF-8'))
        print(r.text)
    except:
        print(traceback.print_exc())

'''
  功能：发送邮件
  send_mail465('190343@lifeat.cn', 'Hhc5HBtAuYTPGHQ8', '190343@lifeat.cn', v_title, v_content)
'''
def send_mail465(p_from_user,p_from_pass,p_to_user,p_title,p_content):
    to_user=p_to_user.split(",")
    try:
        msg            = MIMEText(p_content,'html','utf-8')
        msg["Subject"] = p_title
        msg["From"]    = p_from_user
        msg["To"]      = ",".join(to_user)
        server         = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(e)


'''
 功能：获取server信息
'''
def get_server_info(config,server_id):
    db = config['db_mysql_dict']
    cr = db.cursor()
    st = 'SELECT * FROM t_server where id={}'.format(server_id)
    cr.execute(st)
    rs=cr.fetchone()
    return rs


'''
 功能：获取db信息
'''
def get_db_info(config,db_id):
    db = config['db_mysql_dict']
    cr = db.cursor()
    st = "SELECT a.*,b.dmmc as db_type_name FROM t_db_source a,t_dmmx b where a.db_type=b.dmm and b.dm='02' and a.id={}".format(db_id)
    cr.execute(st)
    rs=cr.fetchone()
    return rs

'''
 功能：获取影响范围
'''
def get_effect_range(config,server_id,db_id):
    db = config['db_mysql_dict']
    cr = db.cursor()
    st = '''SELECT GROUP_CONCAT(CONCAT(flag,':',times,'个')) as result 
            FROM(SELECT 
                    b.dmmc AS flag,
                    COUNT(0) AS times
                 FROM  t_db_sync_config a,t_dmmx b 
                 WHERE a.sync_ywlx=b.dmm AND b.dm='08' 
                   AND a.server_id={} 
                   AND (a.sour_db_id={} OR a.desc_db_id={})
                 GROUP BY b.dmmc) AS X'''.format(server_id,db_id,db_id)
    cr.execute(st)
    rs=cr.fetchone()
    return rs['result']+' 数据同步任务'

'''
 功能：写告警日志
'''
def write_warn_log(config,server_id,db_id,flag,p_warn_type):
    db = config['db_mysql_dict']
    cr = db.cursor()
    if flag == 'failure':
        st ='''select count(0) as rec from t_monitor_warn_log where server_id={} and db_id={}'''.format(server_id, db_id)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec']==0:
            st = '''insert into t_monitor_warn_log(server_id,server_desc,db_id,db_desc,fail_times,succ_times,create_time,is_send_rcv_mail,warn_type) 
                     values({},'{}',{},'{}',{},{},'{}','{}','{}')
                 '''.format(server_id,
                            get_server_info(config,server_id)['server_desc'],
                            db_id,
                            get_db_info(config,db_id)['db_desc'],
                            1,
                            0,
                            get_time(),
                            'N',
                            p_warn_type
                            )
        else:
            st = '''update  t_monitor_warn_log 
                       set 
                          fail_times=fail_times+1,
                          succ_times = 0,
                          is_send_rcv_mail='N',
                          warn_type = '{}',
                          update_time=now() 
                      where server_id={} and db_id={}
                 '''.format(p_warn_type,server_id, db_id)
        print('write_warn_log=>failure=',st)
        cr.execute(st)
        db.commit()

    if flag =='success':
        st ='''select count(0) as rec from t_monitor_warn_log where server_id={} and db_id={}'''.format(server_id,db_id)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec'] > 0:
            st = '''update  t_monitor_warn_log 
                               set 
                                  succ_times=succ_times+1,
                                  fail_times=0,
                                  warn_type = '{}',
                                  update_time=now() 
                              where server_id={} and db_id={}
                         '''.format(p_warn_type,server_id, db_id)
            print('write_warn_log=>success=', st)
            cr.execute(st)
            db.commit()

    if flag =='recover':
        st ='''select count(0) as rec from t_monitor_warn_log 
                  where server_id={} and db_id={} and succ_times=1'''.format(server_id,db_id)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec'] > 0:
            st = '''update  t_monitor_warn_log 
                       set 
                          is_send_rcv_mail='Y',
                          fail_times  = 0,
                          warn_type   = {},
                          update_time = now() 
                      where server_id = {} and db_id = {} 
                         '''.format(p_warn_type,server_id, db_id)
            print('write_warn_log=>recover=', st)
            cr.execute(st)
            db.commit()


'''
 功能：统计某个服务失败次数
'''
def stat_warn_times(config,server_id,db_id):
    try:
        db = config['db_mysql_dict']
        cr = db.cursor()
        st = '''select fail_times  from t_monitor_warn_log where server_id={} and db_id={}'''.format(server_id, db_id)
        cr.execute(st)
        rs = cr.fetchone()
        return rs['fail_times']
    except:
        return 0


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def str2datetime(p_rq):
    return datetime.datetime.strptime(p_rq, '%Y-%m-%d %H:%M:%S')


def get_seconds(b):
    a=datetime.datetime.now()
    return int((a-b).total_seconds())

if __name__ == "__main__":
    cfg = get_config(config)
    db  = cfg['db_mysql_dict']
    cr  = db.cursor()
    ft  = '''
告警级别：{}
异常描述：{}服务不可用!
影响范围：{}
服务器名：{}:{}
数据库名：{}:{}
告警时间：{}
失败次数：{}
'''
    ft2 = '''
告警级别：{}
异常描述：服务器网络异常（{}分钟)!
影响范围：{}
服务器名：{}:{}
数据库名：{}:{}
告警时间：{}
失败次数：{}
'''
    st  = '''
告警级别：{}
影响范围：{}
服务器名：{}:{}
数据库名：{}:{}
恢复时间：{}
'''

    '''发送异常邮件或微信'''
    cr.execute('SELECT server_id,server_desc,service_service,flag FROM v_monitor_service')
    rs  = cr.fetchall()
    for r in rs:
        for s in r['service_service'].split(','):
            server_info = get_server_info(cfg, r['server_id'])
            db_info     = get_db_info(cfg, s.split('@')[1])
            fail_time   = stat_warn_times(cfg, r['server_id'], s.split('@')[1])

            '''    
                 1.只发送生产环境服务消息
                 2.当前数据源状态失败
                 3.或者当前数据源状态成功，但是采集时间离现在超过10分钟
            '''
            v_title   = ''
            v_content = ''
            v_type    = ''
            n_timeout = get_seconds(str2datetime(s.split('@')[2]))
            if s.split('@')[0] == '0' and db_info['db_env']=='1' \
                    or s.split('@')[0] == '1' and n_timeout>600:
                 print(server_info)
                 print(db_info)
                 print('fail_time=', fail_time)

                 if s.split('@')[0] == '0' and db_info['db_env']=='1' :
                     v_type      = 'service'
                     v_title     = '{}服务异常({})'.format(db_info['db_desc'], fail_time + 1)
                     v_content   = ft.format(
                                               cfg['warn_level'],
                                               db_info['db_type_name'],
                                               get_effect_range(cfg, r['server_id'], s.split('@')[1]),
                                               server_info['server_ip'],
                                               server_info['server_port'],
                                               db_info['ip'],
                                               db_info['port'],
                                               get_time(),
                                               fail_time+1
                                              )

                 if s.split('@')[0] == '1' and get_seconds(str2datetime(s.split('@')[2]))>300:
                     v_type      = 'network'
                     v_title     = '{}网络异常({})'.format(db_info['db_desc'], fail_time + 1)
                     v_content   = ft2.format(
                                               cfg['warn_level'],
                                               str(int(n_timeout / 60)),
                                               get_effect_range(cfg, r['server_id'], s.split('@')[1]),
                                               server_info['server_ip'],
                                               server_info['server_port'],
                                               db_info['ip'],
                                               db_info['port'],
                                               get_time(),
                                               fail_time + 1
                                             )

                 if fail_time in(0,1,2):
                    print('send_mail=',fail_time)
                    send_message(cfg,v_title+v_content)

                 write_warn_log(cfg,r['server_id'],s.split('@')[1],'failure',v_type)
            else:
                #写恢复告警日志
                write_warn_log(cfg, r['server_id'], s.split('@')[1], 'success',v_type)

    print('''发送异恢复邮件或微信''')
    cr.execute("SELECT * FROM t_monitor_warn_log where succ_times=1 and is_send_rcv_mail='N' order by server_id,db_id")
    rs = cr.fetchall()
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        db_info     = get_db_info(cfg, r['db_id'])
        v_type      = ''
        v_title     = ''

        if r['warn_type'] == '':
           v_title  = '{}服务已恢复'.format(db_info['db_desc'])
        else:
           v_title  = '{}网络已恢复'.format(db_info['server_desc'])

        v_content   = st.format(
                                cfg['warn_level'],
                                get_effect_range(cfg, r['server_id'], r['db_id']),
                                server_info['server_ip'],
                                server_info['server_port'],
                                db_info['ip'],
                                db_info['port'],
                                get_time(),
                              )
        print(v_title)
        print(v_content)
        send_message(cfg,v_title+v_content)
        write_warn_log(cfg, r['server_id'], r['db_id'], 'recover',v_type)

    '''关送数据库连接'''
    cfg['db_mysql'].close()
    cfg['db_mysql_dict'].close()
