#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:28
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm


import time
import json
import os
import tornado.web
from web.model.t_user      import logon_user_check,check_forget_password,check_modify_password,save_forget_authention_string,check_auth_str_exist
from web.model.t_user      import upd_password,get_user_by_userid,get_user_by_loginame,get_user_roles,check_authcode,get_userid_by_auth
from web.model.t_xtqx      import get_tree_by_userid
from web.model.t_dmmx      import get_dmm_from_dm
from web.utils.common      import send_mail_param,get_sys_settings,get_rand_str,current_time,china_rq,china_week,welcome,china_time,create_captcha
from web.utils.basehandler import basehandler


class logon(tornado.web.RequestHandler):
     def get(self):
        self.render("./login/page-login.html")

class index(basehandler):
    @tornado.web.authenticated
    async def get(self):
        username    = str(self.get_secure_cookie("username"), encoding="utf-8")
        userid      = str(self.get_secure_cookie("userid"), encoding="utf-8")
        d_user      = await get_user_by_loginame(username)
        genders     = await get_dmm_from_dm('04')
        depts       = await get_dmm_from_dm('01')
        proj_groups = await get_dmm_from_dm('18')
        if username:
           self.render("./login/index.html",
                       china_rq    = china_rq(),
                       china_week  = china_week(),
                       china_time  = china_time(),
                       welcome     = welcome(d_user['username']),
                       userid      = d_user['userid'],
                       loginname   = d_user['login_name'],
                       wkno        = d_user['wkno'],
                       username    = d_user['username'],
                       password    = d_user['password'],
                       gender      = d_user['gender'],
                       email       = d_user['email'],
                       phone       = d_user['phone'],
                       proj_group  = d_user['project_group'],
                       dept        = d_user['dept'],
                       expire_date = d_user['expire_date'],
                       status      = d_user['status'],
                       file_path   = d_user['file_path'],
                       file_name   = d_user['file_name'],
                       user_image  = d_user['file_path']+'/'+d_user['file_name'],
                       user_roles  = await get_user_roles(userid),
                       genders     = genders,
                       depts       = depts,
                       d_user      = d_user,
                       proj_groups = proj_groups,
                       view_url    = self.get_secure_cookie("view_url")
                       )
        else:
           self.render("./login/page-404.html")

class main(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./main/main.html")

class platform(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./main/platform.html")

class easylife(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./main/easylife.html")

class tree(tornado.web.RequestHandler):
     def post(self):
        result={}
        msg=get_tree()
        result['code'] = 0
        result['message']=msg
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"code": result['code'], "message": result['message']})

class unlock(basehandler):
    async def post(self):
        await self.check_valid()
        unlock_password = self.get_argument("unlock_password")
        username = str(self.get_secure_cookie("username"), encoding="utf-8")
        d_user   = await get_user_by_loginame(username)
        if d_user['password']==unlock_password:
            self.set_secure_cookie("screen_lock_status", 'unlock')
            self.set_secure_cookie("heartbeat", 'health', expires=time.time() + 300)
            self.write({"code":0})
        else:
            self.write({"code":-1})

class lock(basehandler):
    async def post(self):
        await self.check_valid()
        self.set_secure_cookie("screen_lock_status", 'locked')
        self.write({"code":0})

class heartbeat(tornado.web.RequestHandler):
    def post(self):
        status = self.get_secure_cookie("heartbeat")
        if status is None:
            self.write({"code": 'undefined'})
        else:
            self.write({"code": str(status, encoding="utf-8")})

class lock_status(tornado.web.RequestHandler):
  def post(self):
      status = self.get_secure_cookie("screen_lock_status")
      if status is None:
         self.write({"code": 'undefined'})
      else:
         self.write({"code": str(status, encoding="utf-8")})

class get_time(tornado.web.RequestHandler):
    def post(self):
        self.write(china_time())

class logout(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("username", '',expires_days=None)
        self.set_secure_cookie("userid", '', expires_days=None)
        self.set_secure_cookie("screen_lock_status", 'unlock')
        self.render("./login/page-logout.html")

class error(tornado.web.RequestHandler):
    def get(self):
        self.render("./login/page-500.html")

class logon_check(basehandler):
     async def post(self):
        username    = self.get_argument("username")
        password    = self.get_argument("password")
        verify_code = self.get_argument("verify_code")
        verify_img  = str(self.get_secure_cookie("verify_img"), encoding="utf-8")
        result      = await logon_user_check(username, password, verify_code, verify_img)
        if result['code'] == '0':
            d_user = await get_user_by_loginame(username)
            self.set_secure_cookie("username", username,expires=time.time() + 1800)
            self.set_secure_cookie("userid", d_user['userid'], expires=time.time() + 1800)
            self.set_secure_cookie("screen_lock_status", 'unlock')
            self.set_secure_cookie("heartbeat", 'health', expires=time.time() + 300)
        self.write({"code": result['code'], "message": result['message'], "url": result['url']})

class forget_password(tornado.web.RequestHandler):
    def get(self):
        self.render("./login/forget_password.html")

class forget_password_check_user(tornado.web.RequestHandler):
    async def post(self):
        user    = self.get_argument("user")
        email   = self.get_argument("email")
        result  = await check_forget_password(user,email)
        if result['code']=='0':
           auth_string = get_rand_str(64)
           while await check_auth_str_exist(auth_string):
               auth_string = get_rand_str(64)
           await save_forget_authention_string(user,auth_string)
           v_title   = '用户:{0} 口令变更激活邮件.{1}'.format(user,current_time())
           v_content = """<p><h4>用户名：</h4>{}<p><h4>授权码：</h4>{}<p><h4>有效期：</h4>1分钟""".format(user,auth_string)
           settings  = await get_sys_settings()
           send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'),email, v_title, v_content)
           self.write({"code": '0', "message": '授权码已发送至邮箱!'})
        else:
           self.write({"code": result['code'], "message": result['message']})


class forget_password_check_auth(tornado.web.RequestHandler):
    async def post(self):
        user     = self.get_argument("user")
        auth     = self.get_argument("auth")
        result   = await check_authcode(user,auth)
        self.write({"code": result['code'], "message": result['message']})

class forget_password_check_pass(tornado.web.RequestHandler):
    async def post(self):
        user    = self.get_argument("user")
        auth    = self.get_argument("auth")
        newpass = self.get_argument("newpass")
        reppass = self.get_argument("reppass")
        result  = check_modify_password(user, newpass, reppass, auth)
        if result['code'] == '-1':
            self.write({"code": result['code'], "message": result['message']})
        else:
            p_userid = await get_userid_by_auth(auth)
            p_user = await get_user_by_userid(p_userid)
            p_user['password'] = newpass
            result2 = await upd_password(p_user)
            self.write({"code": result2['code'], "message": result2['message']})


class get_tree(tornado.web.RequestHandler):
    async def post(self):
        logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        result= await get_tree_by_userid(logon_name)
        self.write({"code": result['code'], "message": result['message']})



class get_verify(tornado.web.RequestHandler):
    def post(self):
        x = create_captcha()
        image = x.gene_code()
        chars = x.text
        static_path = self.get_template_path().replace("templates", "static")
        self.set_secure_cookie("verify_img", chars, expires_days=None)
        os.system("rm -rf  {0}".format(static_path + '/assets/images/logon/verify*.png'))
        file = static_path + '/assets/images/logon/verify' + chars + '.png'
        image.save(file)
        v_dict = {"image": file.split('/')[-1], "verify": chars}
        v_json = json.dumps(v_dict)
        self.write(v_json)



class check(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        if qname == '':
            self.write('{"code":"-1","message":"用户名不能为空!"}')
        else:
            self.write('{"code":"0","message":"验证成功！"}')