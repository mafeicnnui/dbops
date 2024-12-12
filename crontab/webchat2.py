#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/8 11:10
# @Author : ma.fei
# @File : webchat_service.py.py
# @Software: PyCharm
# @Function: EaseBase服务器监控微信推送

import requests
import traceback
import pymysql
import smtplib
import datetime
from email.mime.text import MIMEText
import json

'''
  功能：全局配置
'''
config = {
    "chat_interface": "https://alarm.lifeat.cn/wx/cp/msg/1000012",
    "mysql": "10.2.39.17:23306:puppet:puppet:Puppet@123",
    "warn_level": "紧急"
}

'''
  功能：获取mysql连接，以元组返回
'''


def get_ds_mysql(ip, port, service, user, password):
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8')
    return conn


'''
  功能：获取mysql连接，以字典返回
'''


def get_ds_mysql_dict(ip, port, service, user, password):
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service,
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return conn


'''
 功能：获取数据库连接
'''


def get_config(config):
    db_ip = config['mysql'].split(':')[0]
    db_port = config['mysql'].split(':')[1]
    db_service = config['mysql'].split(':')[2]
    db_user = config['mysql'].split(':')[3]
    db_pass = config['mysql'].split(':')[4]
    config['db_mysql'] = get_ds_mysql(db_ip, db_port, db_service, db_user, db_pass)
    config['db_mysql_dict'] = get_ds_mysql_dict(db_ip, db_port, db_service, db_user, db_pass)
    return config


'''
  功能：调用接口发送消息
'''


def send_message(config, message):
    try:
        r = requests.post(config['chat_interface'], data=bytes(message, 'UTF-8'))
        print(r.text)
    except:
        print(traceback.print_exc())


'''
  功能：发送邮件
  send_mail465('190343@lifeat.cn', 'Hhc5HBtAuYTPGHQ8', '190343@lifeat.cn', v_title, v_content)
'''


def send_mail465(p_from_user, p_from_pass, p_to_user, p_title, p_content):
    to_user = p_to_user.split(",")
    try:
        msg = MIMEText(p_content, 'html', 'utf-8')
        msg["Subject"] = p_title
        msg["From"] = p_from_user
        msg["To"] = ",".join(to_user)
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(e)


'''
 功能：获取server信息
'''


def get_server_info(config, server_id):
    db = config['db_mysql_dict']
    cr = db.cursor()
    st = 'SELECT * FROM t_server where id={}'.format(server_id)
    cr.execute(st)
    rs = cr.fetchone()
    return rs


'''
 功能：获取db信息
'''


def get_db_info(config, db_id):
    db = config['db_mysql_dict']
    cr = db.cursor()
    st = "SELECT a.*,b.dmmc as db_type_name FROM t_db_source a,t_dmmx b where a.db_type=b.dmm and b.dm='02' and a.id={}".format(
        db_id)
    cr.execute(st)
    rs = cr.fetchone()
    return rs


'''
 功能：写告警日志
'''


def write_warn_log(config, server_id, index_code, index_name, index_value, flag):
    db = config['db_mysql_dict']
    cr = db.cursor()
    if flag == 'failure':
        st = '''select count(0) as rec from t_monitor_server_warn_log where server_id={} and index_code='{}' '''.format(
            server_id, index_code)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec'] == 0:
            st = '''insert into t_monitor_server_warn_log(server_id,server_desc,fail_times,succ_times,create_time,is_send_rcv_mail,index_code,index_name,index_value) 
                     values({},'{}',{},{},'{}','{}','{}','{}','{}')
                 '''.format(server_id,
                            get_server_info(config, server_id)['server_desc'],
                            1,
                            0,
                            get_time(),
                            'N',
                            index_code,
                            index_name,
                            index_value
                            )
        else:
            st = '''update  t_monitor_server_warn_log 
                       set 
                          index_value={},
                          fail_times=fail_times+1,
                          succ_times = 0,
                          is_send_rcv_mail='N',
                          update_time=now() 
                      where server_id={} 
                 '''.format(index_value, server_id)
        print('write_warn_log=>failure=', st)
        cr.execute(st)
        db.commit()

    if flag == 'success':
        st = '''select count(0) as rec from t_monitor_server_warn_log where server_id={} '''.format(server_id)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec'] > 0:
            st = '''update  t_monitor_server_warn_log 
                               set 
                                  index_value={},
                                  succ_times=succ_times+1,
                                  fail_times=0,
                                  update_time=now() 
                              where server_id={} 
                         '''.format(index_value, server_id)
            # print('write_warn_log=>success=', st)
            cr.execute(st)
            db.commit()

    if flag == 'recover':
        st = '''select count(0) as rec from t_monitor_server_warn_log 
                  where server_id={} and succ_times=1'''.format(server_id)
        cr.execute(st)
        rs = cr.fetchone()
        if rs['rec'] > 0:
            st = '''update  t_monitor_server_warn_log 
                       set 
                          is_send_rcv_mail='Y',
                          fail_times  = 0,
                          update_time = now() 
                      where server_id = {}
                         '''.format(server_id)
            print('write_warn_log=>recover=', st)
            cr.execute(st)
            db.commit()


'''
 功能：统计某个服务失败次数
'''


def stat_warn_times(config, server_id):
    try:
        db = config['db_mysql_dict']
        cr = db.cursor()
        st = '''select fail_times  from t_monitor_server_warn_log where server_id={} '''.format(server_id)
        cr.execute(st)
        rs = cr.fetchone()
        return rs['fail_times']
    except:
        return 0


'''
 功能：获取某个指标阀值
'''


def get_index_threshold(config, p_index_code):
    try:
        db = config['db_mysql_dict']
        cr = db.cursor()
        st = "SELECT index_threshold*100 as index_threshold FROM t_monitor_index WHERE index_code='{}'".format(
            p_index_code)
        cr.execute(st)
        rs = cr.fetchone()
        return float(rs['index_threshold'])
    except:
        return 0


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def str2datetime(p_rq):
    return datetime.datetime.strptime(p_rq, '%Y-%m-%d %H:%M:%S')


def get_seconds(b):
    a = datetime.datetime.now()
    return int((a - b).total_seconds())


def server_warning(config):
    cfg = get_config(config)
    db = cfg['db_mysql_dict']
    cr = db.cursor()
    ft = '''
          服务器名：{0}:{1}
          告警时间：{2}
          告警级别：{3}
          异常描述：{4}
          失败次数：{5}
          '''

    st = '''
          服务器名：{0}:{1}
          恢复时间：{2}
          告警级别：{3}
          异常描述：{4}
          '''

    '''发送异常邮件或微信'''
    cr.execute('''SELECT 
                         a.server_id,
                         'server_available'  AS index_code,
                         '服务器连接'         AS index_name,
                         a.create_date,
                         CASE WHEN TIMESTAMPDIFF(MINUTE, a.create_date, NOW())>3 THEN '0' ELSE '100' END  AS index_value
                      FROM t_monitor_task_server_log a ,t_server b
                       WHERE  a.server_id=b.id 
                           AND b.server_ip NOT LIKE '10.2.39.%' 
                           AND (a.server_id,a.create_date) IN( 
                                SELECT a.server_id, MAX(a.create_date) FROM t_monitor_task_server_log a GROUP BY server_id) 
                     ''')
    rs = cr.fetchall()
    print('>>>>>>>服务器连接异常告警....')
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        fail_times = stat_warn_times(cfg, r['server_id'])
        if r['index_value'] == '0':
            print(server_info)
            v_title = '{}服务器告警({})'.format(server_info['server_desc'], fail_times + 1)
            v_content = ft.format(server_info['server_ip'], server_info['server_port'],
                                  get_time(),
                                  cfg['warn_level'],
                                  '服务器连接异常!',
                                  fail_times + 1
                                  )
            if fail_times in (3, 4, 5):
                send_message(cfg, v_title + v_content)

            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'failure')
        else:
            # 写恢复告警日志
            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'success')

    '''发送异常恢复邮件或微信'''
    cr.execute("""SELECT * FROM t_monitor_server_warn_log a,t_server b
                         where a.server_id=b.id 
                           AND b.server_ip NOT LIKE '10.2.39.%' 
                             AND a.succ_times=1 
                               AND a.index_code='server_available' 
                                AND a.is_send_rcv_mail='N' order by server_id""")
    rs = cr.fetchall()
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        v_title = '{}服务告警已恢复'.format(server_info['server_desc'])
        v_content = st.format(server_info['server_ip'],
                              server_info['server_port'],
                              get_time(),
                              cfg['warn_level'],
                              r['index_name'] + '已恢复({})'.format(r['index_value'])
                              )

        print(v_title)
        print(v_content)
        if r['fail_times'] >= 3:
            print(v_title)
            send_message(cfg, v_title + v_content)
        write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], '', 'recover')

    '''关送数据库连接'''
    cfg['db_mysql'].close()
    cfg['db_mysql_dict'].close()


def get_max_disk_usage(d_disk):
    n_max_val = 0.0
    for key in d_disk:
        if n_max_val <= float(d_disk[key]):
            n_max_val = float(d_disk[key])
    result = str(n_max_val)
    return result


def disk_warning(config):
    cfg = get_config(config)
    db = cfg['db_mysql_dict']
    cr = db.cursor()
    ft = '''
      服务器名：{0}:{1}
      告警时间：{2}
      告警级别：{3}
      异常描述：{4}
      失败次数：{5}
      '''

    st = '''
      服务器名：{0}:{1}
      恢复时间：{2}
      告警级别：{3}
      异常描述：{4}
      '''

    '''发送异常邮件或微信'''
    cr.execute(''' 
                  SELECT 
                     a.server_id,
                     a.create_date,
                     a.disk_usage      AS index_value,
                     'disk_usage'      AS index_code,
                     '磁盘使用率'       AS index_name,
                     a.create_date
                  FROM t_monitor_task_server_log a ,t_server b
                   WHERE  a.server_id=b.id 
                       AND b.server_ip NOT LIKE '10.2.39.%' 
                       AND (a.server_id,a.create_date) IN( 
                            SELECT a.server_id, MAX(a.create_date) FROM t_monitor_task_server_log a GROUP BY server_id) 
                 ''')
    rs = cr.fetchall()
    print('>>>>>>>磁盘使用率告警....')
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        fail_times = stat_warn_times(cfg, r['server_id'])
        index_threshold = get_index_threshold(config, r['index_code'])
        max_disk_usage = get_max_disk_usage(json.loads(r['index_value']))

        if float(max_disk_usage) > index_threshold:
            print(server_info)
            v_title = '{}服务器告警({})'.format(server_info['server_desc'], fail_times + 1)
            v_content = ft.format(server_info['server_ip'], server_info['server_port'],
                                  get_time(),
                                  cfg['warn_level'],
                                  '{}{}% (阀值{}%)'.format(r['index_name'], max_disk_usage + '%', index_threshold),
                                  fail_times + 1
                                  )
            if fail_times in (3, 4, 5):
                send_message(cfg, v_title + v_content)

            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], max_disk_usage + '%', 'failure')
        else:
            # 写恢复告警日志
            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], max_disk_usage + '%', 'success')

    '''发送异恢复邮件或微信'''
    cr.execute("""SELECT * FROM t_monitor_server_warn_log a,t_server b
                     where a.server_id=b.id 
                       AND b.server_ip NOT LIKE '10.2.39.%' 
                         AND a.succ_times=1 
                           AND a.index_code='disk_usage' 
                            AND a.is_send_rcv_mail='N' order by server_id""")
    rs = cr.fetchall()
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        v_title = '{}服务告警已恢复'.format(server_info['server_desc'])
        v_content = st.format(server_info['server_ip'],
                              server_info['server_port'],
                              get_time(),
                              cfg['warn_level'],
                              r['index_name'] + '已恢复({})'.format(r['index_value'])
                              )

        print(v_title)
        print(v_content)
        if r['fail_times'] >= 3:
            print(v_title)
            send_message(cfg, v_title + v_content)
        write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], '', 'recover')

    '''关送数据库连接'''
    cfg['db_mysql'].close()
    cfg['db_mysql_dict'].close()


def cpu_warning(config):
    cfg = get_config(config)
    db = cfg['db_mysql_dict']
    cr = db.cursor()
    ft = '''
    服务器名：{0}:{1}
    告警时间：{2}
    告警级别：{3}
    异常描述：{4}
    失败次数：{5}
    '''

    st = '''
    服务器名：{0}:{1}
    恢复时间：{2}
    告警级别：{3}
    异常描述：{4}
    '''

    '''发送异常邮件或微信'''
    cr.execute(''' 
                SELECT 
                   a.server_id,
                   a.create_date,
                   cpu_total_usage   AS index_value,
                   'cpu_total_usage' AS index_code,
                   'cpu使用率'        AS index_name,
                   a.create_date
                FROM t_monitor_task_server_log a ,t_server b
                 WHERE  a.server_id=b.id 
                     AND b.server_ip NOT LIKE '10.2.39.%' 
                     AND (a.server_id,a.create_date) IN( 
                          SELECT a.server_id, MAX(a.create_date) FROM t_monitor_task_server_log a GROUP BY server_id) 
               ''')
    rs = cr.fetchall()
    print('>>>>>>>cpu告警....')
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        fail_times = stat_warn_times(cfg, r['server_id'])
        index_threshold = get_index_threshold(config, r['index_code'])

        if float(r['index_value']) > index_threshold:
            print(server_info)
            v_title = '{}服务器告警({})'.format(server_info['server_desc'], fail_times + 1)
            v_content = ft.format(server_info['server_ip'], server_info['server_port'],
                                  get_time(),
                                  cfg['warn_level'],
                                  '{}{}% (阀值{}%)'.format(r['index_name'], r['index_value'], index_threshold),
                                  fail_times + 1
                                  )
            if fail_times in (3, 4, 5):
                send_message(cfg, v_title + v_content)

            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'failure')
        else:
            # 写恢复告警日志
            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'success')

    '''发送异恢复邮件或微信'''
    cr.execute("""SELECT * FROM t_monitor_server_warn_log a,t_server b
                   where a.server_id=b.id 
                     AND b.server_ip NOT LIKE '10.2.39.%' 
                       AND a.succ_times=1 
                         AND a.index_code='cpu_total_usage' 
                          AND a.is_send_rcv_mail='N' order by server_id""")
    rs = cr.fetchall()
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        v_title = '{}服务告警已恢复'.format(server_info['server_desc'])
        v_content = st.format(server_info['server_ip'],
                              server_info['server_port'],
                              get_time(),
                              cfg['warn_level'],
                              r['index_name'] + '已恢复({})'.format(r['index_value'])
                              )

        print(v_title)
        print(v_content)
        if r['fail_times'] >= 3:
            print(v_title)
            send_message(cfg, v_title + v_content)
        write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], '', 'recover')

    '''关送数据库连接'''
    cfg['db_mysql'].close()
    cfg['db_mysql_dict'].close()


def mem_warning(config):
    cfg = get_config(config)
    db = cfg['db_mysql_dict']
    cr = db.cursor()
    ft = '''
    服务器名：{0}:{1}
    告警时间：{2}
    告警级别：{3}
    异常描述：{4}
    失败次数：{5}
    '''

    st = '''
    服务器名：{0}:{1}
    恢复时间：{2}
    告警级别：{3}
    异常描述：{4}
    '''

    '''发送异常邮件或微信'''
    cr.execute('''
                SELECT 
                   a.server_id,
                   a.create_date,
                   mem_usage          AS index_value,
                   'mem_usage'        AS index_code,
                   '内存使用率'        AS index_name 
                FROM t_monitor_task_server_log a ,t_server b
                 WHERE a.server_id=b.id 
                     AND b.server_ip NOT LIKE '10.2.39.%' 
                     AND (a.server_id,a.create_date) IN( 
                          SELECT a.server_id, MAX(a.create_date) FROM t_monitor_task_server_log a GROUP BY server_id) 
               ''')
    rs = cr.fetchall()
    print('>>>>>>>内存告警....')
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        fail_times = stat_warn_times(cfg, r['server_id'])
        index_threshold = get_index_threshold(config, r['index_code'])
        if float(r['index_value']) > index_threshold:
            print(server_info)
            v_title = '{}服务器告警({})'.format(server_info['server_desc'], fail_times + 1)
            v_content = ft.format(server_info['server_ip'], server_info['server_port'],
                                  get_time(),
                                  cfg['warn_level'],
                                  '{}{}% (阀值{}%)'.format(r['index_name'], r['index_value'], index_threshold),
                                  fail_times + 1
                                  )
            if fail_times in (3, 4, 5):
                print(v_title)
                send_message(cfg, v_title + v_content)

            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'failure')
        else:
            # 写恢复告警日志
            write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], r['index_value'], 'success')

    '''发送异恢复邮件或微信'''
    cr.execute("""SELECT * FROM t_monitor_server_warn_log a,t_server b
                   where a.server_id=b.id 
                     AND b.server_ip NOT LIKE '10.2.39.%' 
                      AND a.succ_times=1 
                       AND a.index_code='mem_usage' 
                         AND a.is_send_rcv_mail='N' order by server_id""")
    rs = cr.fetchall()
    for r in rs:
        server_info = get_server_info(cfg, r['server_id'])
        v_title = '{}服务告警已恢复'.format(server_info['server_desc'])
        v_content = st.format(server_info['server_ip'],
                              server_info['server_port'],
                              get_time(),
                              cfg['warn_level'],
                              r['index_name'] + '已恢复({})'.format(r['index_value'])
                              )

        print(v_title)
        print(v_content)
        if r['fail_times'] >= 3:
            send_message(cfg, v_title + v_content)
        write_warn_log(cfg, r['server_id'], r['index_code'], r['index_name'], '', 'recover')

    '''关送数据库连接'''
    cfg['db_mysql'].close()
    cfg['db_mysql_dict'].close()


if __name__ == "__main__":
    # 服务器告警
    server_warning(config)

    # # cpu 告警
    # cpu_warning(config)
    #
    # # 内存告警
    # mem_warning(config)
    #
    # # 磁盘使用率告警
    # disk_warning(config)
