#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 15:02
# @Author : ma.fei
# @File : base_handler.py.py
# @Software: PyCharm

import datetime
import json

import jwt
import tornado.web
from jwt import exceptions
from tornado.web import HTTPError

from web.model.t_xtqx import check_url
from web.utils import jwt_auth
from web.utils.common import get_sys_settings_sync
from web.utils.mysql_async import async_processer

JWT_SALT = 'Hopson2021@abcd'
ISS_UER = 'zhitbar.cn'
TIMEOUT = int(get_sys_settings_sync()['TOKEN_EXPIRE_TIME'])


class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(BaseHandler, self).prepare()

    def set_default_headers(self):
        super().set_default_headers()

    async def create_token(self, payload, timeout=TIMEOUT):
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # create session
        session_id = await self.insert_session_log(payload['userid'], payload['username'], payload['name'],
                                                   payload['remote_ip'])
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
        payload['iat'] = datetime.datetime.utcnow()
        payload['iss'] = ISS_UER
        payload['session_id'] = session_id
        result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
        return result

    async def refresh_token(self, token, session_id, timeout=TIMEOUT):
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        result = TokenHandler.parse_payload(token)
        if not result["status"]:
            self.delete_session_log(session_id)
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

        if (await self.check_sess_exists(session_id)) == 0:
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(504, json.dumps({'code': 504, 'error': '用户会话过期!'}, ensure_ascii=False))

        payload = result['data']
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
        payload['iat'] = datetime.datetime.utcnow()
        payload['iss'] = ISS_UER
        result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
        await self.update_session_log(payload['session_id'])
        self.token = result
        return result

    async def insert_session_log(self, p_userid, p_username, p_name, p_remote_ip):
        st = """insert into t_session(userid,username,logon_time,name,login_ip,last_update_time) 
                           values('{}','{}',now(),'{}','{}',now())""".format(p_userid, p_username, p_name, p_remote_ip)
        id = await async_processer.exec_ins_sql(st)
        await self.kickout_session_log(p_username, id)
        return id

    async def update_session_log(self, p_session_id):
        st = """update t_session 
                      set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>600 then '2' else '1' end,
                          online_time=TIMESTAMPDIFF(SECOND,logon_time,NOW()),
                          last_update_time=now()
                      where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)
        st = """update t_session 
                      set state=case when TIMESTAMPDIFF(SECOND,last_update_time,now())>3600  then '5' 
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

    async def delete_session_log(self, p_session_id):
        # set state is logout state
        st = """update t_session  set state='4' where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)
        # set state for timeout
        st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
                      select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
                        from t_session where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)
        st = """delete from t_session where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)

    async def kill_session_log(self, p_session_id):
        # set state is kill state
        st = """update t_session  set state='3' where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)
        # move session to history
        st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
                      select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
                        from t_session where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)
        st = """delete from t_session where session_id={}""".format(p_session_id)
        await async_processer.exec_sql(st)

    async def kickout_session_log(self, p_username, p_session_id):
        st = """update t_session  set state='6' where username='{}' and session_id!={}""".format(p_username,
                                                                                                 p_session_id)
        await async_processer.exec_sql(st)
        st = """insert into t_session_history(session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time) 
                      select session_id,userid,username,logon_time,login_ip,state,online_time,last_update_time
                        from t_session where username='{}' and state='6'""".format(p_username)
        await async_processer.exec_sql(st)
        st = """delete from t_session where username='{}' and state='6'""".format(p_username)
        await async_processer.exec_sql(st)

    async def get_sessoin_state(self, p_session_id):
        return (await async_processer.query_dict_one("""select state from t_session where session_id={}
                                                                union all
                                                                select state from t_session_history where session_id={} 
                                                             """.format(p_session_id, p_session_id)))['state']

    async def check_sess_exists(self, p_session_id):
        return (await async_processer.query_one("select count(0) "
                                                "from t_session where session_id={} "
                                                " AND TIMESTAMPDIFF(MINUTE,last_update_time,NOW())<={}".format(
            p_session_id, TIMEOUT)))[0]


class TokenHandler(BaseHandler):

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

    async def prepare(self):
        head = self.request.headers
        token = head.get("token", "")
        if token == '':
            token = self.get_argument("token")

        result = jwt_auth.parse_payload(token)
        if not result["status"]:
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

        userid = result['data']['userid']
        username = result['data']['username']
        flag = await check_url(userid, self.request.uri.split('?')[0])
        if not flag:
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(502, "用户`{}`无权访问(`{}`)!".format(username, self.request.uri))

        state = await jwt_auth.get_sessoin_state(result['data']['session_id'])
        if state == '3':
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(503, "用户`{}`已下线!".format(username))

        if (await jwt_auth.check_sess_exists(result['data']['session_id'])) == 0:
            self.token_passed = False
            self.token = ''
            self.username = ''
            self.userid = ''
            self.session_id = ''
            raise HTTPError(504, "用户`{}`被强踢!".format(username))

        self.token_passed = True
        self.username = result['data']['username']
        self.userid = result['data']['userid']
        self.session_id = result['data']['session_id']
        self.token = token
        self.result = {'code': True, 'message': "success!"}
