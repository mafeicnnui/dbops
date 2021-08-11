#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:28
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

import tornado.web
import random
import time
import string
import json
import os
from web.model.t_user      import logon_user_check,check_forget_password,check_modify_password,save_forget_authention_string,check_auth_str_exist
from web.model.t_user      import upd_password,get_user_by_userid,get_user_by_loginame,get_user_roles,check_authcode,get_userid_by_auth
from web.model.t_xtqx      import get_tree_by_userid
from web.model.t_dmmx      import get_dmm_from_dm
from web.utils.common      import send_mail_param,get_sys_settings,get_rand_str,current_time,china_rq,china_week,welcome,china_time
from PIL                   import Image,ImageDraw,ImageFont,ImageFilter
from web.utils.basehandler import basehandler


class logon(tornado.web.RequestHandler):
     def get(self):
        self.render("page-login.html")

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
           self.render("index.html",
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
           self.render("page-404.html")

class main(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("main.html")

class platform(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("platform.html")

class easylife(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("easylife.html")

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
        self.render("page-logout.html")

class error(tornado.web.RequestHandler):
    def get(self):
        self.render("page-500.html")

class logon_welcome(tornado.web.RequestHandler):
    def get(self):
        self.render("./main/welcome.html")

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
        self.render("./user/forget_password.html")

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

class modify_password(tornado.web.RequestHandler):
    def get(self):
        auth_str    = self.get_argument("id")
        self.render("./user/modify_password.html", auth_str=auth_str)

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

class tree(tornado.web.RequestHandler):
    def get(self):
        self.render("./tree/tree.html")

class get_tree(tornado.web.RequestHandler):
    async def post(self):
        logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        result= await get_tree_by_userid(logon_name)
        self.write({"code": result['code'], "message": result['message']})

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
        self.pic_size = (100, 40)
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
        self.font = ImageFont.truetype(self.font_path, 25)
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
            ((self.pic_size[0] - font_width) / self.text_num, (self.pic_size[1] - font_height) / self.text_num), self.text,
            font=self.font,
            fill=self.text_color)
        if self.draw_line:
            n = random.randint(self.line_number[0],self.line_number[1])
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

class forget_password(tornado.web.RequestHandler):
    def get(self):
        self.render("./forget_password.html")

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