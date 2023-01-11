#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:28
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

import os
import json
import tornado.web
from web.model.t_user      import logon_user_check,check_forget_password,check_modify_password,save_forget_authention_string,check_auth_str_exist
from web.model.t_user      import upd_password,get_user_by_userid,get_user_by_loginame,get_user_roles,check_authcode,get_userid_by_auth
from web.model.t_xtqx      import get_tree_by_userid
from web.model.t_dmmx      import get_dmm_from_dm
from web.utils.common      import send_mail_param,get_sys_settings,get_rand_str,current_time,china_rq,china_week,welcome,china_time,create_captcha
from web.utils.jwt_auth    import  delete_session_log
from web.utils             import base_handler

class logon(tornado.web.RequestHandler):
     def get(self):
        self.render("./login/page-login.html")

class logon_check(base_handler.BaseHandler):
    async def post(self):
        username    = self.get_argument("username")
        password    = self.get_argument("password")
        verify_code = self.get_argument("verify_code")
        verify_img  = str(self.get_secure_cookie("verify_img"), encoding="utf-8")
        remote_ip   = self.request.headers.get("X-Real-Ip", "")
        result      = await logon_user_check(username, password, verify_code, verify_img)
        if result['code'] == '0':
           d_user = await get_user_by_loginame(username)
           token = await self.create_token({"username": username, "userid": d_user['userid'],"name":d_user['name'],"remote_ip":remote_ip})
           self.write({"code": result['code'], "message": result['message'], "token": token})
        else:
           self.write({"code": result['code'], "message": result['message']})

class update_token(base_handler.TokenHandler):
    async def post(self):
        token= await self.refresh_token(self.get_argument("token"),self.session_id)
        print('update_token=',token)
        self.write({"token": token})

class index(base_handler.TokenHandler):
  async def get(self):
    if self.token_passed:
        if (await self.check_sess_exists(self.session_id)) == 0:
            self.render('./login/page-404.html')
        else:
            d_user      = await get_user_by_loginame(self.username)
            genders     = await get_dmm_from_dm('04')
            depts       = await get_dmm_from_dm('01')
            proj_groups = await get_dmm_from_dm('18')
            self.render("./login/index.html",
                        china_rq     =  china_rq(),
                        china_week   =  china_week(),
                        china_time   =  china_time(),
                        welcome      =  welcome(d_user['username']),
                        userid       =  d_user['userid'],
                        loginname    =  d_user['login_name'],
                        wkno         =  d_user['wkno'],
                        username     =  d_user['username'],
                        password     =  d_user['password'],
                        gender       =  d_user['gender'],
                        email        =  d_user['email'],
                        phone        =  d_user['phone'],
                        proj_group   =  d_user['project_group'],
                        dept         =  d_user['dept'],
                        expire_date  =  d_user['expire_date'],
                        status       =  d_user['status'],
                        file_path    =  d_user['file_path'],
                        file_name    =  d_user['file_name'],
                        user_image   =  d_user['file_path'] + '/' + d_user['file_name'],
                        user_roles   =  await get_user_roles(self.userid),
                        genders      =  genders,
                        depts        =  depts,
                        d_user       =  d_user,
                        proj_groups  = proj_groups,
                       )
    else:
        self.redirect('/login')

  def write_error(self, status_code: int, **kwargs) :
      self.redirect('/login')

class get_tree(base_handler.TokenHandler):
    async def post(self):
        result= await get_tree_by_userid(self.username)
        self.write({"code": result['code'], "message": result['message']})

class main(base_handler.BaseHandler):
     def get(self):
        self.render("./main/main.html")

class platform(base_handler.BaseHandler):
     def get(self):
        self.render("./main/platform.html")

class easylife(base_handler.BaseHandler):
     def get(self):
        self.render("./main/easylife.html")

class get_time(base_handler.TokenHandler):
    def post(self):
        self.write(china_time())

class logout_page(base_handler.BaseHandler):
    def get(self):
        self.render("./login/page-logout.html")

class logout(base_handler.TokenHandler):
    async def post(self):
        try:
           await delete_session_log(self.session_id)
           self.write({"code": 0, "message": 'success'})
        except:
           self.write({"code": -1, "message": 'failure'})

class error(base_handler.TokenHandler):
    def get(self):
        self.render("./login/page-500.html")

class forget_password(base_handler.BaseHandler):
    def get(self):
        self.render("./login/forget_password.html")

class forget_password_check_user(base_handler.BaseHandler):
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
           send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'),email, '',v_title, v_content)
           self.write({"code": '0', "message": '授权码已发送至邮箱!'})
        else:
           self.write({"code": result['code'], "message": result['message']})

class forget_password_check_auth(base_handler.BaseHandler):
    async def post(self):
        user     = self.get_argument("user")
        auth     = self.get_argument("auth")
        result   = await check_authcode(user,auth)
        self.write({"code": result['code'], "message": result['message']})

class forget_password_check_pass(base_handler.BaseHandler):
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

class get_verify(base_handler.BaseHandler):
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

# class unlock(base_handler.TokenHandler):
#     async def post(self):
#         await self.check_valid()
#         unlock_password = self.get_argument("unlock_password")
#         username = str(self.get_secure_cookie("username"), encoding="utf-8")
#         d_user   = await get_user_by_loginame(username)
#         if d_user['password']==unlock_password:
#             self.set_secure_cookie("screen_lock_status", 'unlock')
#             self.set_secure_cookie("heartbeat", 'health', expires=time.time() + 300)
#             self.write({"code":0})
#         else:
#             self.write({"code":-1})
#
# class lock(base_handler.TokenHandler):
#     async def post(self):
#         await self.check_valid()
#         self.set_secure_cookie("screen_lock_status", 'locked')
#         self.write({"code":0})
#
# class heartbeat(base_handler.TokenHandler):
#     def post(self):
#         status = self.get_secure_cookie("heartbeat")
#         if status is None:
#             self.write({"code": 'undefined'})
#         else:
#             self.write({"code": str(status, encoding="utf-8")})
#
# class lock_status(base_handler.TokenHandler):
#   def post(self):
#       status = self.get_secure_cookie("screen_lock_status")
#       if status is None:
#          self.write({"code": 'undefined'})
#       else:
#          self.write({"code": str(status, encoding="utf-8")})
