#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:03
# @Author : ma.fei
# @File : menu.py
# @Software: PyCharm

import json

from web.model.t_xtqx import query_func, get_privs, save_func, get_func_by_funcid, upd_func, del_func
from web.utils import base_handler


class funcquery(base_handler.TokenHandler):
    def get(self):
        self.render("./func/func_query.html")


class func_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname = self.get_argument("qname")
        v_list = await query_func(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class funcadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./func/func_add.html",
                    menus=await get_privs())


class funcadd_save(base_handler.TokenHandler):
    async def post(self):
        d_func = {}
        d_func['priv_id'] = self.get_argument("priv_id")
        d_func['func_name'] = self.get_argument("func_name")
        d_func['func_url'] = self.get_argument("func_url")
        d_func['status'] = self.get_argument("status")
        result = await save_func(d_func)
        self.write({"code": result['code'], "message": result['message']})


class funcchange(base_handler.TokenHandler):
    def get(self):
        self.render("./func/func_change.html")


class funcedit(base_handler.TokenHandler):
    async def get(self):
        funcid = self.get_argument("funcid")
        d_func = await get_func_by_funcid(funcid)
        self.render("./func/func_edit.html",
                    funcid=d_func['funcid'],
                    func_name=d_func['func_name'],
                    func_url=d_func['func_url'],
                    priv_id=d_func['priv_id'],
                    status=d_func['status'],
                    menus=await get_privs(),
                    )


class funcedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_func = {}
        d_func['funcid'] = self.get_argument("funcid")
        d_func['func_name'] = self.get_argument("func_name")
        d_func['func_url'] = self.get_argument("func_url")
        d_func['priv_id'] = self.get_argument("priv_id")
        d_func['status'] = self.get_argument("status")
        result = await upd_func(d_func)
        self.write({"code": result['code'], "message": result['message']})


class funcedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        funcid = self.get_argument("funcid")
        result = await del_func(funcid)
        self.write({"code": result['code'], "message": result['message']})
