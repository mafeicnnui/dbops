#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:43
# @Author : ma.fei
# @File : role.py.py
# @Software: PyCharm

import json

from web.model.t_role import save_role, check_role, query_role, upd_role, del_role, get_role_by_roleid
from web.model.t_xtqx import get_privs, get_privs_role, get_privs_sys, get_func_privs, get_privs_func, \
    get_privs_func_role
from web.utils import base_handler


class rolequery(base_handler.TokenHandler):
    async def get(self):
        self.render("./role/role_query.html")


class roleadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./role/role_add.html",
                    privs=await get_privs(),
                    func_privs=await get_func_privs())


class roleadd_save(base_handler.TokenHandler):
    async def post(self):
        d_role = {}
        d_role['name'] = self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs'] = self.get_argument("privs").split(",")
        d_role['func_privs'] = self.get_argument("func_privs").split(",")
        result = await save_role(d_role)
        self.write({"code": result['code'], "message": result['message']})


class role_check(base_handler.TokenHandler):
    async def post(self):
        d_role = {}
        d_role['name'] = self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs'] = self.get_argument("privs").split(",")
        result = await check_role(d_role)
        self.write({"code": result['code'], "message": result['message']})


class role_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_role(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class rolechange(base_handler.TokenHandler):
    async def get(self):
        self.render("./role/role_change.html")


class roleedit(base_handler.TokenHandler):
    async def get(self):
        roleid = self.get_argument("roleid")
        d_role = await get_role_by_roleid(roleid)
        self.render("./role/role_edit.html",
                    roleid=d_role['roleid'],
                    name=d_role['name'],
                    status=d_role['status'],
                    priv_sys=await get_privs_sys(roleid),
                    priv_role=await get_privs_role(roleid),
                    func_privs=await get_privs_func(roleid),
                    func_privs_role=await get_privs_func_role(roleid),
                    )


class roleedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_role = {}
        d_role['roleid'] = self.get_argument("roleid")
        d_role['name'] = self.get_argument("name")
        d_role['status'] = self.get_argument("status")
        d_role['privs'] = self.get_argument("privs").split(",")
        d_role['func_privs'] = self.get_argument("func_privs").split(",")
        result = await upd_role(d_role)
        self.write({"code": result['code'], "message": result['message']})


class roleedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        roleid = self.get_argument("roleid")
        result = await del_role(roleid)
        self.write({"code": result['code'], "message": result['message']})
