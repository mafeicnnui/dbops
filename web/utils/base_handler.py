#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 15:02
# @Author : ma.fei
# @File : base_handler.py.py
# @Software: PyCharm

import json
import tornado.web
from web.utils import jwt_auth
from tornado.web import HTTPError
from web.model.t_xtqx  import check_url
from web.utils.jwt_auth import get_sessoin_state, delete_session_log, check_sess_exists


class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(BaseHandler, self).prepare()

    def set_default_headers(self):
        super().set_default_headers()
        # self.set_header("Access-Control-Allow-Origin", '*')
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class TokenHandler(BaseHandler):

    async def prepare(self):
        # head = self.request.headers
        # token = head.get("token","")
        # if token == '':
        #    token = self.get_argument("token")

        token = self.get_argument("token")

        print('TokenHandler taken:', token)
        result = jwt_auth.parse_payload(token)
        if not result["status"]:
           raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

        userid   = result['data']['userid']
        username = result['data']['username']
        flag = await check_url(userid, self.request.uri.split('?')[0])
        if not flag:
           raise HTTPError(502, "用户`{}`无权访问(`{}`)!".format(username, self.request.uri))

        state = await jwt_auth.get_sessoin_state(result['data']['session_id'])
        if state == '3' :
           raise HTTPError(503, "用户`{}`已下线!".format(username))

        if (await jwt_auth.check_sess_exists(result['data']['session_id'])) == 0:
           raise HTTPError(504, "用户`{}`被强踢!".format(username))

        self.token_passed = True
        self.username = result['data']['username']
        self.userid = result['data']['userid']
        self.session_id = result['data']['session_id']
        self.token = token


class TokenHandlerLogin(BaseHandler):

    async def prepare(self):
        try:
            head = self.request.headers
            token = head.get("token","")
            if token == '':
               token = self.get_argument("token")

            print('TokenHandlerLogin taken:',token)
            result = jwt_auth.parse_payload(token)
            if not result["status"]:
               self.token_passed = False
               self.username = ''
               self.userid = ''
               self.session_id = ''
            else:
               self.token_passed = True
               self.username = result['data']['username']
               self.userid = result['data']['userid']
               self.session_id = result['data']['session_id']
        except:
            self.token_passed = False
            self.username = ''
            self.userid = ''
            self.session_id = ''