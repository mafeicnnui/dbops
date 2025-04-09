#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 14:51
# @Author : ma.fei
# @File : jwt_auth.py.py
# @Software: PyCharm

import os
import jwt
import json
import datetime
from jwt import exceptions
from tornado.web import HTTPError
#from web.webssh.mysql_sync import sync_processer
from web.utils.mysql_sync import sync_processer


JWT_SALT = 'Hopson2021@abcd'
ISS_UER = 'zhitbar.cn'
TIMEOUT = 60


def read_json(file):
    with open(file, 'r') as f:
        cfg = json.loads(f.read())
    return cfg


ds = read_json(os.path.join(os.path.dirname(__file__)) + '/../../config/config.json')
print('ds=', ds)


def refresh_token(token, session_id, timeout=TIMEOUT):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    result = parse_payload(token)
    if not result["status"]:
        delete_session_log(session_id)
        raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

    if (check_sess_exists(session_id)) == 0:
        raise HTTPError(504, json.dumps({'code': 504, 'error': '用户会话过期!'}, ensure_ascii=False))

    payload = result['data']
    print('refresh_token=>payload:', payload)
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload['iat'] = datetime.datetime.utcnow()
    payload['iss'] = ISS_UER
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    # update session
    update_session_log(payload['session_id'])
    print('refresh_token=>result:', result)
    return result


def parse_payload(token):
    result = {'status': False, 'code': 200, 'data': None, 'error': None}
    try:
        header = jwt.get_unverified_header(token)
        if header['typ'] != 'jwt':
            result['code'] = 404
            result['error'] = 'token认证方式错误!'
        elif header['alg'] != 'HS256':
            result['code'] = 405
            result['error'] = 'token认证算法错误!'
        else:
            verified_payload = jwt.decode(token, JWT_SALT, issuer=ISS_UER, algorithms=["HS256"])
            print('verified_payload=', verified_payload)
            result['status'] = True
            result['code'] = 200
            result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['code'] = 401
        result['error'] = 'token已失效!'
    except jwt.DecodeError:
        result['code'] = 402
        result['error'] = 'token认证失败!'
    except jwt.InvalidTokenError:
        result['code'] = 403
        result['error'] = '非法的token!'
    return result


def insert_session_log(p_userid, p_username, p_name, p_remote_ip):
    # gen session_id
    st = """insert into t_session(userid,username,logon_time,name,login_ip,last_update_time) 
                  values('{}','{}',now(),'{}','{}',now())""".format(p_userid, p_username, p_name, p_remote_ip)
    id = sync_processer.exec_ins_sql(st)
    # The other same user is logon
    print('kickout_session_log!')
    kickout_session_log(p_username, id)
    print('kickout_session_log!!!!!!!!!!!!!')
    return id


def update_session_log(p_session_id):
    # set state for timeout
    st = """update t_session 
             set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>600 then '2' else '1' end,
                 online_time=TIMESTAMPDIFF(SECOND,logon_time,NOW()),
                 last_update_time=now()
             where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)
    st = """update t_session 
             set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>1800  then '5' 
                       when TIMESTAMPDIFF(SECOND,last_update_time,now())>600 then '2' 
                       else '1' end
             where session_id!={}""".format(p_session_id)
    sync_processer.exec_sql(st)

    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
            select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
            from t_session where state=5"""
    sync_processer.exec_sql(st)
    st = """delete from t_session where state=5"""
    sync_processer.exec_sql(st)


def delete_session_log(p_session_id):
    # set state is logout state
    st = """update t_session  set state='4' where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)
    # set state for timeout
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)
    st = """delete from t_session where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)


def kill_session_log(p_session_id):
    # set state is kill state
    st = """update t_session  set state='3' where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)
    # move session to history
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)
    st = """delete from t_session where session_id={}""".format(p_session_id)
    sync_processer.exec_sql(st)


def kickout_session_log(p_username, p_session_id):
    # set state is kill state
    st = """update t_session  set state='6' where username='{}' and session_id!={}""".format(p_username, p_session_id)
    sync_processer.exec_sql(st)
    # move session to history
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where username='{}' and state='6'""".format(p_username)
    sync_processer.exec_sql(st)
    st = """delete from t_session where username='{}' and state='6'""".format(p_username)
    print('>>>>3', st)
    sync_processer.exec_sql(st)


def get_sessoin_state(p_session_id):
    sql = """select state from t_session where session_id={}
                                                 union all
                                                 select state from t_session_history where session_id={}
                                             """.format(p_session_id, p_session_id)
    return (sync_processer.query_dict_one("""select state from t_session where session_id={}
                                                 union all
                                                 select state from t_session_history where session_id={}
                                             """.format(p_session_id, p_session_id)))['state']


def check_sess_exists(p_session_id):
    return (sync_processer.query_one("select count(0) "
                                     "from t_session where session_id={}".format(p_session_id)))[0]
