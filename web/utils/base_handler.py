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

class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(BaseHandler, self).prepare()

    def set_default_headers(self):
        super().set_default_headers()
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class TokenHandler(BaseHandler):

    async def prepare(self):
        head = self.request.headers
        token = head.get("token","")
        if token == '':
           token = self.get_argument("token")

        result = jwt_auth.parse_payload(token)
        if not result["status"]:
           raise HTTPError(result['code'], json.dumps(result, ensure_ascii=False))

        userid = result['data']['userid']
        username = result['data']['username']
        flag = await check_url(userid, self.request.uri.split('?')[0])
        if not flag:
           raise HTTPError(502, "用户`{}`无权访问(`{}`)!".format(username, self.request.uri))

        self.token_passed = True
        self.token_msg_dict = result
        self.token_msg_json = json.dumps(result, ensure_ascii=False)


class TokenHandler2(BaseHandler):

    async def prepare(self):
        head = self.request.headers
        token = head.get("token","")
        if token == '':
           token = self.get_argument("token")

        result = jwt_auth.parse_payload(token)
        print('TokenHandler2=',result)
        if not result["status"]:
           self.token_passed = False
        else:
           self.token_passed = True
        self.token_msg_dict = result
        self.token_msg_json = json.dumps(result, ensure_ascii=False)
