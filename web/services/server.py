#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from web.model.t_server  import get_server_by_serverid,query_server,save_server,upd_server,del_server,check_server_valid
from web.model.t_dmmx    import get_dmm_from_dm
from web.utils           import base_handler
from web.utils.common import get_sys_settings


class serverquery(base_handler.TokenHandler):
    def get(self):
        self.render("./server/server_query.html")

class server_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = await query_server(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class serveradd(base_handler.TokenHandler):
    async def get(self):
        self.render("./server/server_add.html",
                    dm_proj_type   = await get_dmm_from_dm('05'),
                    dm_server_type = await  get_dmm_from_dm('06'))

class serveradd_save(base_handler.TokenHandler):
    async def post(self):
        d_server = {}
        d_server['market_id']   = self.get_argument("market_id")
        d_server['server_desc'] = self.get_argument("server_desc")
        d_server['server_type'] = self.get_argument("server_type")
        d_server['server_ip']   = self.get_argument("server_ip")
        d_server['server_port'] = self.get_argument("server_port")
        d_server['server_user'] = self.get_argument("server_user")
        d_server['server_pass'] = self.get_argument("server_pass")
        d_server['server_os']   = self.get_argument("server_os")
        d_server['server_cpu']  = self.get_argument("server_cpu")
        d_server['server_mem']  = self.get_argument("server_mem")
        d_server['status']      = self.get_argument("status")
        result = await save_server(d_server)
        self.write({"code": result['code'], "message": result['message']})

class serverchange(base_handler.TokenHandler):
    async def get(self):
        self.render("./server/server_change.html",webssh_url=(await get_sys_settings())['WEBSSH_URL'])

class serveredit(base_handler.TokenHandler):
    async def get(self):
        server_id = self.get_argument("serverid")
        d_server  = await get_server_by_serverid(server_id)
        markets   = await get_dmm_from_dm('05')
        self.render("./server/server_edit.html",
                    markets        = markets,
                    dm_server_type = await get_dmm_from_dm('06'),
                    server_id      = d_server['server_id'],
                    market_id      = d_server['market_id'],
                    server_desc    = d_server['server_desc'],
                    server_type    = d_server['server_type'],
                    server_ip      = d_server['server_ip'],
                    server_port    = d_server['server_port'],
                    server_user    = d_server['server_user'],
                    server_pass    = d_server['server_pass'],
                    server_os      = d_server['server_os'],
                    server_cpu     = d_server['server_cpu'],
                    server_mem     = d_server['server_mem'],
                    status         = d_server['status']
                    )

class serveredit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_server={}
        d_server['server_id']   = self.get_argument("server_id")
        d_server['market_id']   = self.get_argument("market_id")
        d_server['server_desc'] = self.get_argument("server_desc")
        d_server['server_type'] = self.get_argument("server_type")
        d_server['server_ip']   = self.get_argument("server_ip")
        d_server['server_port'] = self.get_argument("server_port")
        d_server['server_user'] = self.get_argument("server_user")
        d_server['server_pass'] = self.get_argument("server_pass")
        d_server['server_os']   = self.get_argument("server_os")
        d_server['server_cpu']  = self.get_argument("server_cpu")
        d_server['server_mem']  = self.get_argument("server_mem")
        d_server['status']      = self.get_argument("status")
        result = await upd_server(d_server)
        self.write({"code": result['code'], "message": result['message']})

class serveredit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        serverid  = self.get_argument("serverid")
        result = await del_server(serverid)
        self.write({"code": result['code'], "message": result['message']})


class server_check_valid(base_handler.TokenHandler):
    async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       result = await check_server_valid(id)
       self.write({"code": result['code'], "message": result['message']})


class server_by_serverid(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id       = self.get_argument("server_id")
        v_list   = await get_server_by_serverid(id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

