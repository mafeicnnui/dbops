#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 13:02
# @Author  : 马飞
# @File    : comm.py.py
# @Software: PyCharm

import datetime
import decimal
import json
import os
import random
import re
import smtplib
import socket
import string
import time
import traceback
import paramiko
from email.mime.text import MIMEText

import aiomysql
import pymongo
import pymssql
import pymysql
import redis
import requests
import sqlparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from clickhouse_driver import connect
from elasticsearch import Elasticsearch
from humanize import naturalsize

from web.utils.mysql_async import async_processer
from web.utils.mysql_sync import sync_processer


def get_server(p_host):
    if p_host == "124.127.103.190":
        res = "124.127.103.190:65482"
    elif p_host.find(':') >= 0:
        res = p_host
    else:
        res = p_host + ':81'
    return res


def read_json(file):
    with open(file, 'r') as f:
        cfg = json.loads(f.read())
    return cfg


def get_db_conf():
    config = read_json('./config/config.json')
    return config


def get_connection():
    cfg = get_db_conf()
    conn = pymysql.connect(host=cfg['db_ip'],
                           port=int(cfg['db_port']),
                           user=cfg['db_user'],
                           passwd=cfg['db_pass'],
                           db=cfg['db_service'],
                           charset=cfg['db_charset'])
    return conn


def get_connection_dict():
    cfg = get_db_conf()
    conn = pymysql.connect(host=cfg['db_ip'],
                           port=int(cfg['db_port']),
                           user=cfg['db_user'],
                           passwd=cfg['db_pass'],
                           db=cfg['db_service'],
                           charset=cfg['db_charset'],
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


def get_connection_ds(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8',
                           read_timeout=30000)
    return conn


def get_connection_ds_dict(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8',
                           read_timeout=30000, cursorclass=pymysql.cursors.DictCursor)
    return conn


def get_connection_ds_read_limit(p_ds, p_timeout):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8',
                           read_timeout=p_timeout, connect_timeout=p_timeout)
    return conn


async def get_connection_ds_read_limit_aiomysql(p_ds, p_timeout, p_event_loop):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = await aiomysql.connect(host=ip,
                                  port=int(port),
                                  user=user,
                                  password=password,
                                  db=service,
                                  connect_timeout=p_timeout,
                                  loop=p_event_loop,
                                  charset='utf8')
    return conn


async def get_connection_ds_read_limit_aiomysql_dict(p_ds, p_timeout, p_event_loop):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = await aiomysql.connect(host=ip,
                                  port=int(port),
                                  user=user,
                                  password=password,
                                  db=service,
                                  connect_timeout=p_timeout,
                                  loop=p_event_loop,
                                  charset='utf8',
                                  cursorclass=aiomysql.DictCursor)
    return conn


def get_connection_ds_read_limit_ck(p_ds, p_timeout):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = connect(database=service, user=user, password=password, host=ip, port=port, connect_timeout=p_timeout)
    return conn


def get_connection_ds_write_limit(p_ds, p_timeout):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password,
                           db=service, charset='utf8', read_timeout=p_timeout, write_timeout=p_timeout,
                           connect_timeout=p_timeout)
    return conn


def get_connection_ds_mongo(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    if user is None or user == '':
        conn = pymongo.MongoClient(host=ip, port=int(port))
        return conn
    else:
        conn = pymongo.MongoClient('mongodb://{0}:{1}/'.format(ip, int(port)))
        db = conn[service]
        db.authenticate(user, password)
        return conn


def get_connection_ds_redis(p_ds):
    conn = redis.Redis(host=p_ds['ip'], port=int(p_ds['port']), db=0)
    return conn


def get_connection_ds_es(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    conn = Elasticsearch([ip], port=int(port))
    return conn


def get_connection_ds_uat(p_ds):
    ip = p_ds['uat_ip']
    port = p_ds['uat_port']
    service = p_ds['uat_service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymysql.connect(host=ip, port=int(port), user=user, passwd=password, db=service, charset='utf8')
    return conn


def get_connection_ds_sqlserver(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymssql.connect(server=ip, port=int(port), user=user, password=password, database=service, charset='utf8',
                           timeout=3)
    return conn


def get_connection_ds_ck(p_ds):
    ip = p_ds['ip']
    port = p_ds['port']
    service = p_ds['service']
    user = p_ds['user']
    password = p_ds['password']
    conn = connect(database=service, user=user, password=password, host=ip, port=port)
    return conn


def get_connection_ds_uat_sqlserver(p_ds):
    ip = p_ds['uat_ip']
    port = p_ds['uat_port']
    service = p_ds['uat_service']
    user = p_ds['user']
    password = p_ds['password']
    conn = pymssql.connect(server=ip, port=int(port), user=user, password=password, database=service, charset='utf8')
    return conn


def get_connection_ds_oracle(p_ds):
    return None


def get_connection_ds_oracle_uat(p_ds):
    return None


def get_connection_ds_pg(p_ds):
    return None


def get_connection_ds_pg_uat(p_ds):
    return None


def current_rq():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month).rjust(2, '0')
    day = str(datetime.datetime.now().day).rjust(2, '0')
    return year + month + day


def current_rq2():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month).rjust(2, '0')
    day = str(datetime.datetime.now().day).rjust(2, '0')
    return year + '-' + month + '-' + day


def current_rq3(n_days):
    rq = datetime.datetime.now() + datetime.timedelta(days=n_days)
    year = str(rq.year)
    month = str(rq.month).rjust(2, '0')
    day = str(rq.day).rjust(2, '0')
    return year + '-' + month + '-' + day


def current_rq4(n_days, n_hour):
    rq = datetime.datetime.now() + datetime.timedelta(days=n_days)
    year = str(rq.year)
    month = str(rq.month).rjust(2, '0')
    day = str(rq.day).rjust(2, '0')
    hour = str(rq.hour - n_hour).rjust(2, '0')
    return year + '-' + month + '-' + day + ' ' + hour + ':00:00'


def now():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month).rjust(2, '0')
    day = str(datetime.datetime.now().day).rjust(2, '0')
    return year + '-' + month + '-' + day


def get_nday_list(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days


def get_day_nday_ago(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]


def current_time():
    now_time = datetime.datetime.now()
    time1_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    return time1_str


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def china_rq():
    year = str(datetime.datetime.now().year) + '年'
    month = str(datetime.datetime.now().month).rjust(2, '0') + '月'
    day = str(datetime.datetime.now().day).rjust(2, '0') + '日'
    return year + month + day


def china_time():
    hour = str(datetime.datetime.now().hour) + '点'
    min = str(datetime.datetime.now().minute).rjust(2, '0') + '分'
    sec = str(datetime.datetime.now().second).rjust(2, '0') + '秒'
    return hour + min + sec


def china_week():
    week = get_week_day(datetime.datetime.now())
    return week


def welcome(username):
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        return '{0}，上午好！'.format(username)
    elif hour >= 12 and hour < 18:
        return '{0}，下午好！'.format(username)
    elif hour >= 18 and hour < 23:
        return '{0}，晚上好！'.format(username)
    elif hour >= 23 or hour >= 0 and hour < 6:
        return '{0}，早点休息！'.format(username)


def exception_info():
    e_str = traceback.format_exc()
    print(e_str)


def get_ds_message(p_ds):
    v_env = ''
    v_type = ''
    if p_ds['db_env'] == '1':
        v_env = 'PROD'
    if p_ds['db_env'] == '2':
        v_env = 'DEV'
    if p_ds['db_type'] == '0':
        v_type = 'MySQL'
    if p_ds['db_type'] == '1':
        v_type = 'PostgreSQL'
    if p_ds['db_type'] == '2':
        v_type = 'SQLServer'
    if p_ds['db_type'] == '3':
        v_type = 'Oracle'
    msg = """
            <b>运行环境：</b>{0}</br>
            <b>数据类型：</b>{1}</br>
          """.format(v_env, v_type)
    return msg


def exception_info_mysql():
    e_str = traceback.format_exc()
    while True:
        if e_str[-1] == '\n' or e_str[-1] == '\r':
            e_str = e_str[0:-1]
            continue
        else:
            break
    return e_str[e_str.find("pymysql.err."):]


def exception_info_sqlserver():
    e_str = traceback.format_exc()
    while True:
        if e_str[-1] == '\n' or e_str[-1] == '\r':
            e_str = e_str[0:-1]
            continue
        else:
            break
    return e_str


def format_sql(v_sql):
    return v_sql.replace("\\", "\\\\").replace("'", "\\'")


def format_mysql_error(env, msg):
    p_msg = msg[0:msg.find('During')]. \
        replace("pymysql.err.InternalError: (", ""). \
        replace("pymysql.err.ProgrammingError: (", ""). \
        replace("pymysql.err.OperationalError: (", ""). \
        replace(")", "").replace('"', '').replace("'", "").split(',')
    return p_msg[1]


def format_sqlserver_error(env, msg):
    p_msg = ''
    if msg.find('pymssql.InternalError: (') > 0:
        p_msg = msg[msg.find('pymssql.InternalError: ('):]. \
            replace("pymssql.OperationalError: (", ""). \
            replace(")", "").replace('b\"', '').replace('"', '').replace("'", ""). \
            replace("'b", "").replace("\\n", "").split(',')

    if msg.find('pymssql.ProgrammingError: (') > 0:
        p_msg = msg[msg.find('pymssql.ProgrammingError: ('):]. \
            replace("pymssql.ProgrammingError: (", ""). \
            replace(")", "").replace('b\"', '').replace('"', '').replace("'", ""). \
            replace("'b", "").replace("\\n", "").split(',')

    if msg.find('pymssql.OperationalError: (') > 0:
        p_msg = msg[msg.find('pymssql.OperationalError: ('):]. \
            replace("pymssql.OperationalError: (", ""). \
            replace(")", "").replace('b\"', '').replace('"', '').replace("'", ""). \
            replace("'b", "").replace("\\n", "").split(',')

    return """
              <b>运行环境：</b>{0}</br>
              <b>错误代码：</b>{1}</br>
              <b>错误消息：</b>{2}
           """.format(env, p_msg[0], ','.join(p_msg[1:]))


def format_check(env, msg):
    return """
              <b>运行环境：</b>{0}</br>            
              <b>错误消息：</b>{1}
           """.format(env, msg)


async def aes_encrypt(p_password, p_key):
    sql = """select hex(aes_encrypt('{0}','{1}'))""".format(p_password, p_key[::-1])
    rs = await async_processer.query_one(sql)
    return rs[0]


async def aes_decrypt(p_password, p_key):
    sql = """select aes_decrypt(unhex('{0}'),'{1}')""".format(p_password, p_key[::-1])
    rs = await async_processer.query_one(sql)
    return str(rs[0], encoding="utf-8")


def aes_decrypt_sync(p_password, p_key):
    sql = """select aes_decrypt(unhex('{0}'),'{1}')""".format(p_password, p_key[::-1])
    rs = sync_processer.query_one(sql)
    return str(rs[0], encoding="utf-8")


def get_rand_str(p_len):
    rand = ''
    for i in range(p_len):
        char1 = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9)), chr(random.randint(97, 122))])
        rand = rand + char1
    return rand


def send_mail(p_from_user, p_from_pass, p_to_user, p_title, p_content):
    to_user = p_to_user.split(",")
    try:
        msg = MIMEText(p_content, 'html', 'utf-8')
        msg["Subject"] = p_title
        msg["From"] = p_from_user
        msg["To"] = ",".join(to_user)
        server = smtplib.SMTP("smtp.exmail.qq.com", 25)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
        return 0
    except smtplib.SMTPException as e:
        return -1


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


def send_mail587(p_from_user, p_from_pass, p_to_user, p_title, p_content):
    to_user = p_to_user.split(",")
    try:
        msg = MIMEText(p_content, 'html', 'utf-8')
        msg["Subject"] = p_title
        msg["From"] = p_from_user
        msg["To"] = ",".join(to_user)
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 587)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(e)


def socket_port(ip, port):
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
    except:
        return False


def get_available_port():
    for p in [465, 25]:
        if socket_port("smtp.exmail.qq.com", p):
            return p


def send_mail_25(p_sendserver, p_from_user, p_from_pass, p_to_user, p_to_cc, p_title, p_content):
    to_user = p_to_user.split(",")
    to_cc = p_to_cc.split(",")
    try:
        msg = MIMEText(p_content, 'html', 'utf-8')
        msg["Subject"] = p_title
        msg["From"] = p_from_user
        msg["To"] = ",".join(to_user)
        msg["Cc"] = ",".join(to_cc)
        server = smtplib.SMTP(p_sendserver, 25)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(e)


def send_mail_465(p_sendserver, p_from_user, p_from_pass, p_to_user, p_to_cc, p_title, p_content):
    to_user = p_to_user.split(",")
    to_cc = p_to_cc.split(",")
    try:
        msg = MIMEText(p_content, 'html', 'utf-8')
        msg["Subject"] = p_title
        msg["From"] = p_from_user
        msg["To"] = ",".join(to_user)
        msg["Cc"] = ",".join(to_cc)
        server = smtplib.SMTP_SSL(p_sendserver, 465, timeout=10)
        server.set_debuglevel(0)
        server.login(p_from_user, p_from_pass)
        server.sendmail(p_from_user, to_user, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(e)


def send_mail_param(p_sendserver, p_from_user, p_from_pass, p_to_user, p_to_cc, p_title, p_content):
    try:
        port = get_available_port()
        if port == 465:
            print('send_mail_465')
            send_mail_465(p_sendserver, p_from_user, p_from_pass, p_to_user, p_to_cc, p_title, p_content)
        else:
            print('send_mail_25')
            send_mail_25(p_sendserver, p_from_user, p_from_pass, p_to_user, p_to_cc, p_title, p_content)
        print('send_mail_param send success!')
    except:
        print("send_mail_param exception:")
        traceback.print_exc()


'''
  功能：调用接口发送消息
'''


async def send_message(toUser, title, message, detail_url,ds,msg_type):
    if ds['dsid'] in('245','249','16','84') and msg_type=='RUNNING':
        to_user ="{}|{}".format(toUser, '850927')
    else:
        to_user = toUser

    WX_URL = (await get_sys_settings())['WX_URL']
    msg = {
        "title": title,
        "toUser": to_user,
        "description": message,
        "url": detail_url,
        "msgType": "textcard",
        "agentId": 1000093
    }
    headers = {
        "User-Agent": "PostmanRuntime/7.26.8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }
    try:
        print('send_message>>:', msg)
        r = requests.post(WX_URL, data=json.dumps(msg, cls=DateEncoder), headers=headers)
        print(r.text)
    except:
        print(traceback.print_exc())


async def send_message_qw( message):
    """
        功能：调用接口发送企微消息
    """
    WX_URL = (await get_sys_settings())['QYWX_URL']
    msg = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }
    print('send_message_qw=',msg,type(msg))
    headers ={"Content-Type": "application/json" }
    try:
        r = requests.post(WX_URL, json=msg, headers=headers)
        print(r.text)
    except :
        print(traceback.print_exc())

async def send_message_qw_mobiles( message,mobiles):
    """
        功能：调用接口发送企微消息
    """
    wx_url = (await get_sys_settings())['QYWX_URL']
    msg = {
        "mentioned_mobile_list":mobiles,
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }
    print('send_message_qw_mobiles=',msg,type(msg))
    headers ={"Content-Type": "application/json" }
    try:
        r = requests.post(wx_url, json=msg, headers=headers)
        print(r.text)
    except :
        print(traceback.print_exc())

'''
  功能：调用接口发送消息
'''
def send_message_sync(toUser, title, message, detail_url,ds,msg_type):
    if ds['dsid'] in('245','249','16','84') and msg_type=='RUNNING':
        to_user ="{}|{}".format(toUser, '850927')
    else:
        to_user = toUser
    WX_URL = get_sys_settings_sync()['WX_URL']
    msg = {
        "title": title,
        "toUser": to_user,
        "description": message,
        "url": detail_url,
        "msgType": "textcard",
        "agentId": 1000093
    }
    headers = {
        "User-Agent": "PostmanRuntime/7.26.8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(WX_URL, data=json.dumps(msg, cls=DateEncoder), headers=headers)
        print(r.text)
    except:
        print(traceback.print_exc())


def send_message_qw_sync( message):
    """
        功能：调用接口发送企微消息
    """
    WX_URL = get_sys_settings_sync()['QYWX_URL']
    msg = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
         }
    }
    headers ={
        "Content-Type": "application/json"
    }
    try:
        print('send_qw message>>:', msg)
        r = requests.post(WX_URL, json=msg, headers=headers)
        print(r.text)
    except:
        print(traceback.print_exc())


async def get_sys_settings():
    st = "SELECT `key`,`value`,`desc` FROM  t_sys_settings"
    rs = await async_processer.query_dict_list(st)
    settings = {}
    for s in rs:
        settings[s['key']] = s['value']
    return settings


def get_sys_settings_sync():
    st = "SELECT `key`,`value`,`desc` FROM  t_sys_settings"
    rs = sync_processer.query_dict_list(st)
    settings = {}
    for s in rs:
        settings[s['key']] = s['value']
    return settings


def get_file_contents(filename):
    file_handle = open(filename, 'r')
    line = file_handle.readline()
    lines = ''
    while line:
        lines = lines + line
        line = file_handle.readline()
    lines = lines + line
    file_handle.close()
    return lines


def format_exception(v_sql):
    try:
        return v_sql.split(',')[1].replace("'", "").replace('"', '')[0:-1] + '!'
    except:
        return v_sql


def format_sql(v_sql):
    return v_sql.replace("\\", "\\\\").replace("'", "\\'")


def beauty_sql(p_sql):
    result = {}
    result['code'] = '0'
    v_sql_list = sqlparse.split(p_sql)
    v_ret = ''
    for v in v_sql_list:
        v_sql = sqlparse.format(v, reindent=True, keyword_case='upper')
        if v_sql.upper().count('CREATE') > 0 or v_sql.upper().count('ALTER') > 0:
            v_tmp = re.sub(' {5,}', '  ', v_sql).strip()
        else:
            v_tmp = re.sub('\n{2,}', '\n\n', v_sql).strip(' ')
        v_ret = v_ret + v_tmp + '\n\n'
    result['message'] = v_ret[0:-2]
    return result


'''
    功能：将datatime类型序列化json可识别类型
'''


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, int):
            return str(obj)
        elif isinstance(obj, float):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class create_captcha:
    def __init__(self):
        '''
          install font
          #sudo yum install ttf-dejavu
          #sudo mkdir /usr/share/fonts/dejavu
          #sudo cp /usr/local/lib64/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf /usr/share/fonts/dejavu
          #fc-cache
          #fc-list
        '''
        self.font_path = 'DejaVuSans.ttf'

        # 生成验证码位数
        self.text_num = 5
        # 生成图片尺寸
        self.pic_size = (100, 30)
        # 背景颜色，默认为白色
        self.bg_color = (255, 255, 255)
        # 字体颜色，默认为蓝色
        self.text_color = (0, 0, 255)
        # 干扰线颜色，默认为红色
        self.line_color = (255, 0, 0)
        # 是否加入干扰线
        self.draw_line = True
        # 加入干扰线条数上下限
        self.line_number = (1, 5)
        # 是否加入干扰点
        self.draw_points = True
        # 干扰点出现的概率(%)
        self.point_chance = 2

        self.image = Image.new('RGBA', (self.pic_size[0], self.pic_size[1]), self.bg_color)
        self.font = ImageFont.truetype(self.font_path, 20)
        self.draw = ImageDraw.Draw(self.image)
        self.text = self.gene_text()

    def gene_text(self):
        # 随机生成一个字符串
        source = list(string.ascii_letters)
        for i in range(0, 10):
            source.append(str(i))
        return ''.join(random.sample(source, self.text_num))

    def gene_line(self):
        # 随机生成干扰线
        begin = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        end = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        self.draw.line([begin, end], fill=self.line_color)

    def gene_points(self):
        # 随机绘制干扰点
        for w in range(self.pic_size[0]):
            for h in range(self.pic_size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - self.point_chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def gene_code(self):
        # 生成验证码图片
        font_width, font_height = self.font.getsize(self.text)
        self.draw.text(
            ((self.pic_size[0] - font_width) / self.text_num, (self.pic_size[1] - font_height) / self.text_num),
            self.text,
            font=self.font,
            fill=self.text_color)
        if self.draw_line:
            n = random.randint(self.line_number[0], self.line_number[1])
            print(n)
            for i in range(n):
                self.gene_line()
        if self.draw_points:
            self.gene_points()
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        self.image = self.image.transform((self.pic_size[0], self.pic_size[1]), Image.PERSPECTIVE, params)  # 创建扭曲
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        return self.image


async def get_audit_rule(p_key):
    sql = "select * from t_sql_audit_rule where rule_code='{0}'".format(p_key)
    return await async_processer.query_dict_one(sql)


def get_seconds(b):
    a = datetime.datetime.now()
    return int((a - b).total_seconds())


def dict2num(now_dict):
    for key, value in now_dict.items():
        if isinstance(value, dict):
            dict2num(value)
        elif isinstance(value, list):
            for dic in value:
                dict2num(dic)
        elif (isinstance(value, int)
              or isinstance(value, float)
              or isinstance(value, decimal.Decimal)) and len(str(now_dict[key])) > 16:
            now_dict[key] = str(value)
        else:
            pass


def fmt_val(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, datetime.timedelta):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, int):
        return obj
    else:
        return str(obj).replace("\\", "\\\\").replace("'", "\\'")


def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    readable_size = naturalsize(file_size)
    return readable_size

def exec_ssh_cmd(p_cfg, p_cmd):
    stdout_lines = []
    stderr_lines = []
    cmd_exec_status = True
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=p_cfg['msg']['server_ip'], port=int(p_cfg['msg']['server_port']),
                    username=p_cfg['msg']['server_user'], password=p_cfg['msg']['server_pass'])
        stdin, stdout, stderr = ssh.exec_command(p_cmd, timeout=60)
        stdout_lines = stdout.readlines()
        stderr_lines = stderr.readlines()
        if stdout.channel.recv_exit_status() != 0:
            raise paramiko.SSHException()
        ssh.close()
    except paramiko.SSHException as e:
        print("Failed to execute the command on '{}': {}".format(p_cfg['msg']['server_ip'], str(e)))
        if len(stderr_lines) > 0:
            print("Error reported by {}: {}".format(p_cfg['msg']['server_ip'], "\n".join(stderr_lines)))
        cmd_exec_status = False
    return {'status': cmd_exec_status, 'stdout': stdout_lines}


def gen_transfer_file(p_cfg, p_flag, p_templete):
    f_path = os.getcwd()
    f_templete = '{}/templete/{}/{}'.format(f_path, p_flag, p_templete)
    f_local = '{}/script/{}'.format(f_path, p_templete)
    f_remote = '{0}/{1}'.format(p_cfg['msg']['script_path'], p_templete)
    print('f_path=', f_path)
    print('f_templete=', f_templete)
    print('f_local=', f_local)
    print('f_remote=', f_remote)
    print('p_cfg_msg=', p_cfg['msg'])
    os.system('cp -f {0} {1}'.format(f_templete, f_local))
    with open(f_local, 'w') as f:
        f.write(get_file_contents(f_templete).
                replace('$$API_SERVER$$', p_cfg['msg']['api_server'].split(',')[0]).
                replace('$$PYTHON3_HOME$$', p_cfg['msg']['python3_home']).
                # replace('$$SCRIPT_PATH$$',  p_cfg['msg']['script_path']).
                replace('$$SCRIPT_PATH$$',
                        p_cfg['msg'].get('script_path') if p_cfg['msg'].get('script_path') is not None else '').
                # replace('$$SCRIPT_FILE$$',  p_cfg['msg']['script_file']).
                replace('$$SCRIPT_FILE$$',
                        p_cfg['msg'].get('script_file') if p_cfg['msg'].get('script_file') is not None else '').
                replace('$$PORT$$', p_cfg['msg'].get('proxy_local_port') if p_cfg['msg'].get(
            'proxy_local_port') is not None else '').
                replace('$$DB_TAG$$', p_cfg['msg'].get('db_tag') if p_cfg['msg'].get('db_tag') is not None else '').
                replace('$$INST_ID$$', p_cfg['msg'].get('inst_id') if p_cfg['msg'].get('inst_id') is not None else '').
                replace('$$SLOW_ID$$', p_cfg['msg'].get('slow_id') if p_cfg['msg'].get('slow_id') is not None else ''))

    return f_local, f_remote


def ftp_transfer_file(p_cfg, p_local, p_remote):
    try:
        transport = paramiko.Transport((p_cfg['msg']['server_ip'], int(p_cfg['msg']['server_port'])))
        transport.connect(username=p_cfg['msg']['server_user'], password=p_cfg['msg']['server_pass'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localpath=p_local, remotepath=p_remote)
        transport.close()
        print('Script:{0} send to {1} ok.'.format(p_local, p_remote))
        return True
    except:
        traceback.print_exc()
        return False


class ssh_helper:
    def __init__(self, cfg, timeout=600):
        self.server_ip = cfg['server_ip']
        self.server_port = int(cfg['server_port'])
        self.username = cfg['server_user']
        self.password = cfg['server_pass']
        self.ssh = paramiko.SSHClient()
        self.timeout = timeout
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.server_ip, port=self.server_port, username=self.username, password=self.password)

    def exec(self, cmd):
        stdout_lines = []
        stderr_lines = []
        cmd_exec_status = True
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=self.timeout)
            stdout_lines = stdout.readlines()
            stderr_lines = stderr.readlines()
            if stdout.channel.recv_exit_status() != 0:
                raise paramiko.SSHException()
            print('Execute remote cmd: {}'.format(cmd))
        except paramiko.SSHException as e:
            print("Failed to execute the command on '{}': {}".format(self.server_ip, str(e)))
            if len(stderr_lines) > 0:
                print("Error reported by {}: {}".format(self.server_ip, "\n".join(stderr_lines)))
            cmd_exec_status = False
        return {'status': cmd_exec_status, 'stdout': stdout_lines, 'stderr': stderr_lines}

    def exec_win(self, cmd):
        stdout_lines = []
        stderr_lines = []
        cmd_exec_status = True
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=self.timeout)
            # stdout_lines = stdout.readlines()
            # stderr_lines = stderr.readlines()
            if stdout.channel.recv_exit_status() != 0:
                raise paramiko.SSHException()
            print('Execute remote cmd: {}'.format(cmd))
        except paramiko.SSHException as e:
            print("Failed to execute the command on '{}': {}".format(self.server_ip, str(e)))
            if len(stderr_lines) > 0:
                print("Error reported by {}: {}".format(self.server_ip, "\n".join(stderr_lines)))
            cmd_exec_status = False
        return {'status': cmd_exec_status, 'stdout': stdout_lines, 'stderr': stderr_lines}

    def close(self):
        self.ssh.close()


class ftp_helper:
    def __init__(self, cfg, timeout=6):
        self.server_ip = cfg['server_ip']
        self.server_port = int(cfg['server_port'])
        self.username = cfg['server_user']
        self.password = cfg['server_pass']
        self.timeout = timeout
        self.transport = paramiko.Transport((self.server_ip, self.server_port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def transfer(self, local, remote):
        try:
            print('Transfering:{0}  to {1} ok.'.format(local, remote))
            self.sftp.put(localpath=local, remotepath=remote)
            print('Script:{0} send to {1} ok.'.format(local, remote))
            return True
        except:
            traceback.print_exc()
            return False

    def close(self):
        self.transport.close()