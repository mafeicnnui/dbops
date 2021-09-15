#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:17
# @Author : ma.fei
# @File : user.py.py
# @Software: PyCharm

import json
import uuid
import tornado.web
from web.model.t_role  import get_roles
from web.model.t_user  import save_user,get_user_by_userid,upd_user,del_user
from web.model.t_user  import query_user,get_sys_roles,get_user_roles,save_user_proj_privs
from web.model.t_dmmx  import get_dmm_from_dm
from web.model.t_ds    import query_project
from web.utils.basehandler import basehandler

class userquery(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./user/user_query.html")

class useradd(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        roles  = await get_roles()
        gender = await get_dmm_from_dm('04')
        dept   = await get_dmm_from_dm('01')
        proj_group = await get_dmm_from_dm('18')
        self.render("./user/user_add.html",
                    roles=roles,
                    gender=gender,
                    dept=dept,
                    proj_group=proj_group)

class useradd_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        d_user={}
        d_user['login']        = self.get_argument("login")
        d_user['wkno']         = self.get_argument("wkno")
        d_user['user']         = self.get_argument("user")
        d_user['pass']         = self.get_argument("pass")
        d_user['gender']       = self.get_argument("gender")
        d_user['email']        = self.get_argument("email")
        d_user['phone']        = self.get_argument("phone")
        d_user['proj_group']   = self.get_argument("proj_group")
        d_user['dept']         = self.get_argument("dept")
        d_user['expire_date']  = self.get_argument("expire_date")
        d_user['status']       = self.get_argument("status")
        d_user['privs']        = self.get_argument("privs").split(",")
        d_user['file_path']    = self.get_argument("file_path")
        d_user['file_name']    = self.get_argument("file_name")
        result = await save_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class useradd_save_uploadImage(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas  = self.request.files["file"]
        username = self.get_argument("username")
        try:
            for meta in file_metas:
                file_path = static_path+'/'+'assets/images/users'
                file_name=str(uuid.uuid1())+'_'+username+'.'+meta['filename'].split('.')[-1]
                with open(file_path+'/'+file_name, 'wb') as up:
                    up.write(meta['body'])
            self.write({"code": 0, "file_path": '/static/assets/images/users',"file_name":file_name})
        except Exception as e:
            print(e)
            self.write({"code": -1, "message": '保存图片失败'+str(e)})

class userchange(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./user/user_change.html")

class useredit(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        userid  = self.get_argument("userid")
        d_user  = await get_user_by_userid(userid)
        genders = await get_dmm_from_dm('04')
        depts   = await get_dmm_from_dm('01')
        proj_groups = await get_dmm_from_dm('18')
        self.render("./user/user_edit.html",
                     userid      = d_user['userid'],
                     loginname   = d_user['loginname'],
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
                     image_path  = d_user['image_path'],
                     image_name  = d_user['image_name'],
                     user_image  = d_user['image_path']+'/'+d_user['image_name'],
                     sys_roles   = await get_sys_roles(userid),
                     user_roles  = await get_user_roles(userid),
                     genders     = genders,
                     depts       = depts,
                     proj_groups = proj_groups
                    )

class useredit_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user={}
        d_user['userid']      = self.get_argument("userid")
        d_user['loginname']   = self.get_argument("loginname")
        d_user['wkno']        = self.get_argument("wkno")
        d_user['username']    = self.get_argument("username")
        d_user['password']    = self.get_argument("password")
        d_user['gender']      = self.get_argument("gender")
        d_user['email']       = self.get_argument("email")
        d_user['phone']       = self.get_argument("phone")
        d_user['proj_group']  = self.get_argument("proj_group")
        d_user['dept']        = self.get_argument("dept")
        d_user['expire_date'] = self.get_argument("expire_date")
        d_user['status']      = self.get_argument("status")
        d_user['status']      = self.get_argument("status")
        d_user['roles']       = self.get_argument("roles").split(",")
        d_user['file_path']   = self.get_argument("file_path")
        d_user['file_name']   = self.get_argument("file_name")
        result = await upd_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class useredit_del(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user={}
        d_user['userid']   = self.get_argument("userid")
        result=await del_user(d_user)
        self.write({"code": result['code'], "message": result['message']})

class user_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_user(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class projectquery(basehandler):
    @tornado.web.authenticated
    async def get(self):
        await self.check_valid()
        self.render("./user/projectquery.html")

class project_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname     = self.get_argument("qname")
        userid    = self.get_argument("userid")
        is_grants = self.get_argument("is_grants")
        v_list    = await query_project(qname,userid,is_grants)
        v_json = json.dumps(v_list)
        self.write(v_json)

class projectprivs_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        await self.check_valid()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_proj={}
        d_proj['dsid']          = self.get_argument("dsid")
        d_proj['userid']        = self.get_argument("userid")
        d_proj['priv_query']    = self.get_argument("priv_query")
        d_proj['priv_release']  = self.get_argument("priv_release")
        d_proj['priv_audit']    = self.get_argument("priv_audit")
        d_proj['priv_execute']  = self.get_argument("priv_execute")
        d_proj['priv_order']    = self.get_argument("priv_order")
        result = await save_user_proj_privs(d_proj)
        self.write({"code": result['code'], "message": result['message']})


