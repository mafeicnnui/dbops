#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:17
# @Author : ma.fei
# @File : user.py.py
# @Software: PyCharm

import json
import uuid

from web.model.t_dmmx import get_users_by_query_grants, get_sys_dmlx, \
    get_dmm_from_dm, get_sys_dmlx_dic
from web.model.t_ds import query_project
from web.model.t_role import get_roles
from web.model.t_user import query_user, get_sys_roles, save_user_proj_privs
from web.model.t_user import save_user, get_user_by_userid, upd_user, del_user, query_session, kill_session, \
    get_user_roles_n, query_user_grants, save_user_query_grants, get_user_grants, upd_user_query_grants, \
    del_user_query_grants, save_dict_group_grants, query_dict_groups, del_user_dict_group, get_dict_group, \
    upd_user_dict_group, save_dict_grant_grants, query_dict_grant, get_dict_grant, del_user_dict_grant, \
    upd_user_dict_grant
from web.utils import base_handler


class userquery(base_handler.TokenHandler):
    def get(self):
        self.render("./user/user_query.html")


class user_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_user(qname)
        print('user_query:', v_list)
        v_json = json.dumps(v_list)
        self.write(v_json)


class useradd(base_handler.TokenHandler):
    async def get(self):
        roles = await get_roles()
        gender = await get_dmm_from_dm('04')
        dept = await get_dmm_from_dm('01')
        proj_group = await get_dmm_from_dm('18')
        query_grants = await get_dmm_from_dm('49')
        self.render("./user/user_add.html",
                    roles=roles,
                    gender=gender,
                    dept=dept,
                    proj_group=proj_group,
                    query_grants=query_grants
                    )


class useradd_save(base_handler.TokenHandler):
    async def post(self):
        d_user = {}
        d_user['login'] = self.get_argument("login")
        d_user['wkno'] = self.get_argument("wkno")
        d_user['user'] = self.get_argument("user")
        d_user['pass'] = self.get_argument("pass")
        d_user['gender'] = self.get_argument("gender")
        d_user['email'] = self.get_argument("email")
        d_user['phone'] = self.get_argument("phone")
        d_user['proj_group'] = self.get_argument("proj_group")
        d_user['dept'] = self.get_argument("dept")
        d_user['expire_date'] = self.get_argument("expire_date")
        d_user['status'] = self.get_argument("status")
        d_user['privs'] = self.get_argument("privs").split(",")
        d_user['file_path'] = self.get_argument("file_path")
        d_user['file_name'] = self.get_argument("file_name")
        d_user['query_grants'] = self.get_argument("query_grants")
        result = await save_user(d_user)
        self.write({"code": result['code'], "message": result['message']})


class useradd_save_uploadImage(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas = self.request.files["file"]
        username = self.get_argument("username")
        try:
            for meta in file_metas:
                file_path = static_path + '/' + 'assets/images/users'
                file_name = str(uuid.uuid1()) + '_' + username + '.' + meta['filename'].split('.')[-1]
                with open(file_path + '/' + file_name, 'wb') as up:
                    up.write(meta['body'])
            self.write({"code": 0, "file_path": '/static/assets/images/users', "file_name": file_name})
        except Exception as e:
            print(e)
            self.write({"code": -1, "message": '保存图片失败' + str(e)})


class userchange(base_handler.TokenHandler):
    def get(self):
        self.render("./user/user_change.html")


class useredit(base_handler.TokenHandler):
    async def get(self):
        userid = self.get_argument("userid")
        d_user = await get_user_by_userid(userid)
        genders = await get_dmm_from_dm('04')
        depts = await get_dmm_from_dm('01')
        proj_groups = await get_dmm_from_dm('18')
        query_grants = await get_dmm_from_dm('49')
        self.render("./user/user_edit.html",
                    userid=d_user['userid'],
                    loginname=d_user['loginname'],
                    wkno=d_user['wkno'],
                    username=d_user['username'],
                    password=d_user['password'],
                    gender=d_user['gender'],
                    email=d_user['email'],
                    phone=d_user['phone'],
                    proj_group=d_user['project_group'],
                    dept=d_user['dept'],
                    expire_date=d_user['expire_date'],
                    status=d_user['status'],
                    image_path=d_user['image_path'],
                    image_name=d_user['image_name'],
                    user_image=d_user['image_path'] + '/' + d_user['image_name'],
                    sys_roles=await get_sys_roles(),
                    user_roles=await get_user_roles_n(userid),
                    user_query_grant=d_user['query_grants'],
                    genders=genders,
                    depts=depts,
                    proj_groups=proj_groups,
                    query_grants=query_grants
                    )


class useredit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user = {}
        d_user['userid'] = self.get_argument("userid")
        d_user['loginname'] = self.get_argument("loginname")
        d_user['wkno'] = self.get_argument("wkno")
        d_user['username'] = self.get_argument("username")
        d_user['password'] = self.get_argument("password")
        d_user['gender'] = self.get_argument("gender")
        d_user['email'] = self.get_argument("email")
        d_user['phone'] = self.get_argument("phone")
        d_user['proj_group'] = self.get_argument("proj_group")
        d_user['dept'] = self.get_argument("dept")
        d_user['expire_date'] = self.get_argument("expire_date")
        d_user['status'] = self.get_argument("status")
        d_user['status'] = self.get_argument("status")
        d_user['roles'] = self.get_argument("roles").split(",")
        d_user['file_path'] = self.get_argument("file_path")
        d_user['file_name'] = self.get_argument("file_name")
        d_user['query_grants'] = self.get_argument("query_grants")
        result = await upd_user(d_user)
        self.write({"code": result['code'], "message": result['message']})


class useredit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_user = {}
        d_user['userid'] = self.get_argument("userid")
        result = await del_user(d_user)
        self.write({"code": result['code'], "message": result['message']})


class projectquery(base_handler.TokenHandler):
    def get(self):
        self.render("./user/projectquery.html")


class project_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        userid = self.get_argument("userid")
        is_grants = self.get_argument("is_grants")
        v_list = await query_project(qname, userid, is_grants)
        v_json = json.dumps(v_list)
        self.write(v_json)


class projectprivs_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_proj = {}
        d_proj['dsid'] = self.get_argument("dsid")
        d_proj['userid'] = self.get_argument("userid")
        d_proj['priv_query'] = self.get_argument("priv_query")
        d_proj['priv_release'] = self.get_argument("priv_release")
        d_proj['priv_audit'] = self.get_argument("priv_audit")
        d_proj['priv_execute'] = self.get_argument("priv_execute")
        d_proj['priv_order'] = self.get_argument("priv_order")
        d_proj['priv_export'] = self.get_argument("priv_export")
        result = await save_user_proj_privs(d_proj)
        self.write({"code": result['code'], "message": result['message']})


class sessionquery(base_handler.TokenHandler):
    def get(self):
        self.render("./user/sess_query.html")


class session_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_session(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class session_kill(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        session_id = self.get_argument("session_id")
        v_list = await kill_session(session_id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class userquerygrants(base_handler.TokenHandler):
    async def get(self):
        self.render("./user/user_grants.html",
                    query_grants_user=await get_users_by_query_grants(self.username),
                    )


class user_query_grants(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_user_grants(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class get_user_query_grants(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        print('get_user_query_grants=', id)
        v_list = await get_user_grants(id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class user_query_grants_add_save(base_handler.TokenHandler):
    async def post(self):
        d_user = {}
        d_user['dbid'] = self.get_argument("dbid")
        d_user['db'] = self.get_argument("db")
        d_user['tab'] = self.get_argument("tab")
        d_user['cols'] = self.get_argument("cols")
        d_user['userid'] = self.get_argument("uid")
        result = await save_user_query_grants(d_user)
        self.write({"code": result['code'], "message": result['message']})


class user_query_grants_upd_save(base_handler.TokenHandler):
    async def post(self):
        d_user = {}
        d_user['id'] = self.get_argument("id")
        d_user['dbid'] = self.get_argument("dbid")
        d_user['db'] = self.get_argument("db")
        d_user['tab'] = self.get_argument("tab")
        d_user['cols'] = self.get_argument("cols")
        d_user['uid'] = self.get_argument("uid")
        result = await upd_user_query_grants(d_user)
        self.write({"code": result['code'], "message": result['message']})


class user_query_grants_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        result = await del_user_query_grants(id)
        self.write({"code": result['code'], "message": result['message']})


class userdictgrants(base_handler.TokenHandler):
    async def get(self):
        self.render("./user/dict_grants.html",
                    query_grants_user=await get_users_by_query_grants(self.username),
                    dict_group=await get_dmm_from_dm('50'),
                    query_dmlx=await get_sys_dmlx(),
                    query_dmlx_group=await get_sys_dmlx_dic(),

                    )


class user_dict_group_add_save(base_handler.TokenHandler):
    async def post(self):
        dict = {}
        dict['id'] = self.get_argument("dict_id")
        dict['dm'] = self.get_argument("dict_dmlx")
        dict['dmm'] = self.get_argument("dict_dmmx")
        result = await save_dict_group_grants(dict)
        self.write({"code": result['code'], "message": result['message']})


class user_dict_groups(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_dict_groups(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class user_dict_group_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        result = await del_user_dict_group(id)
        self.write({"code": result['code'], "message": result['message']})


class get_user_dict_group(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        v_list = await get_dict_group(id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class user_dict_group_upd_save(base_handler.TokenHandler):
    async def post(self):
        dict = {}
        dict['id'] = self.get_argument("id")
        dict['group_id'] = self.get_argument("group_id")
        dict['dm'] = self.get_argument("dict_dmlx")
        dict['dmm'] = self.get_argument("dict_dmmx")
        print('dict=', dict)
        result = await upd_user_dict_group(dict)
        self.write({"code": result['code'], "message": result['message']})


class user_dict_grant_add_save(base_handler.TokenHandler):
    async def post(self):
        dict = {}
        dict['user_id'] = self.get_argument("user_id")
        dict['group_id'] = self.get_argument("group_id")
        dict['dm'] = self.get_argument("dict_dmlx")
        dict['dmm'] = self.get_argument("dict_dmmx")
        result = await save_dict_grant_grants(dict)
        self.write({"code": result['code'], "message": result['message']})


class user_dict_grant(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_dict_grant(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class get_user_dict_grant(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        v_list = await get_dict_grant(id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class user_dict_grant_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        result = await del_user_dict_grant(id)
        self.write({"code": result['code'], "message": result['message']})


class user_dict_grant_upd_save(base_handler.TokenHandler):
    async def post(self):
        dict = {}
        dict['id'] = self.get_argument("id")
        dict['user_id'] = self.get_argument("user_id")
        dict['group_id'] = self.get_argument("group_id")
        dict['dm'] = self.get_argument("dict_dmlx")
        dict['dmm'] = self.get_argument("dict_dmmx")
        print('dict=', dict)
        result = await upd_user_dict_grant(dict)
        self.write({"code": result['code'], "message": result['message']})
