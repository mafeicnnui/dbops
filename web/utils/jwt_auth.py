#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 14:51
# @Author : ma.fei
# @File : jwt_auth.py.py
# @Software: PyCharm

import datetime
import json

import jwt
from jwt import exceptions
from tornado.web import HTTPError

from web.utils.mysql_async import async_processer

JWT_SALT = 'Hopson2021@abcd'
ISS_UER = 'zhitbar.cn'
TIMEOUT = 60


async def create_token(payload, timeout=TIMEOUT):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # create session
    session_id = await insert_session_log(payload['userid'], payload['username'], payload['name'], payload['remote_ip'])
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload['iat'] = datetime.datetime.utcnow()
    payload['iss'] = ISS_UER
    payload['session_id'] = session_id
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return result


async def refresh_token(token, session_id, timeout=TIMEOUT):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    result = parse_payload(token)
    if not result["status"]:
        delete_session_log(session_id)
        raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

    if (await check_sess_exists(session_id)) == 0:
        raise HTTPError(504, json.dumps({'code': 504, 'error': '用户会话过期!'}, ensure_ascii=False))

    payload = result['data']
    print('refresh_token=>payload:', payload)
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload['iat'] = datetime.datetime.utcnow()
    payload['iss'] = ISS_UER
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    # update session
    await update_session_log(payload['session_id'])
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


async def insert_session_log(p_userid, p_username, p_name, p_remote_ip):
    st = """insert into t_session(userid,username,logon_time,name,login_ip,last_update_time) 
                  values('{}','{}',now(),'{}','{}',now())""".format(p_userid, p_username, p_name, p_remote_ip)
    id = await async_processer.exec_ins_sql(st)
    await kickout_session_log(p_username, id)
    return id


async def update_session_log(p_session_id):
    st = """update t_session 
             set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>600 then '2' else '1' end,
                 online_time=TIMESTAMPDIFF(SECOND,logon_time,NOW()),
                 last_update_time=now()
             where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)
    st = """update t_session 
             set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>1800  then '5' 
                       when TIMESTAMPDIFF(SECOND,last_update_time,now())>600 then '2' 
                       else '1' end
             where session_id!={}""".format(p_session_id)
    await async_processer.exec_sql(st)

    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
            select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
            from t_session where state=5"""
    await async_processer.exec_sql(st)
    st = """delete from t_session where state=5"""
    await async_processer.exec_sql(st)


async def delete_session_log(p_session_id):
    st = """update t_session  set state='4' where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)
    st = """delete from t_session where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)


async def kill_session_log(p_session_id):
    st = """update t_session  set state='3' where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)
    st = """delete from t_session where session_id={}""".format(p_session_id)
    await async_processer.exec_sql(st)


async def kickout_session_log(p_username, p_session_id):
    st = """update t_session  set state='6' where username='{}' and session_id!={}""".format(p_username, p_session_id)
    await async_processer.exec_sql(st)
    st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
             select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
               from t_session where username='{}' and state='6'""".format(p_username)
    await async_processer.exec_sql(st)
    st = """delete from t_session where username='{}' and state='6'""".format(p_username)
    await async_processer.exec_sql(st)


async def get_sessoin_state(p_session_id):
    res = await async_processer.query_dict_one("""select state from t_session where session_id={}
                                                       union all
                                                       select state from t_session_history where session_id={} 
                                                    """.format(p_session_id, p_session_id))
    print('get_sessoin_state=>res1=',res)
    print('get_sessoin_state=>res2=',res['state'])
    return res['state']


async def check_sess_exists(p_session_id):
    return (await async_processer.query_one("select count(0) "
                                            "from t_session where session_id={}".format(p_session_id)))[0]
