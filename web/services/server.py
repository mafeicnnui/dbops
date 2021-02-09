#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   服务器管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_server    import get_server_by_serverid,query_server,save_server,upd_server,del_server,check_server_valid
from   web.model.t_dmmx      import get_dmm_from_dm
from   web.utils.basehandler import basehandler


class serverquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./server_query.html")

class server_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_server(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class serveradd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./server_add.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_server_type= get_dmm_from_dm('06'))

class serveradd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        print(d_server)
        result=save_server(d_server)
        self.write({"code": result['code'], "message": result['message']})

class serverchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./server_change.html")

class serveredit(basehandler):
    @tornado.web.authenticated
    def get(self):
        server_id = self.get_argument("serverid")
        d_server  = get_server_by_serverid(server_id)
        markets   = get_dmm_from_dm('05')
        self.render("./server_edit.html",
                    markets        = markets,
                    dm_server_type = get_dmm_from_dm('06'),
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

class serveredit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        result=upd_server(d_server)
        self.write({"code": result['code'], "message": result['message']})

class serveredit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        serverid  = self.get_argument("serverid")
        result=del_server(serverid)
        self.write({"code": result['code'], "message": result['message']})


class server_check_valid(basehandler):
    @tornado.web.authenticated
    def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       result = check_server_valid(id)
       self.write({"code": result['code'], "message": result['message']})


class server_by_serverid(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id       = self.get_argument("server_id")
        v_list   = get_server_by_serverid(id)
        v_json   = json.dumps(v_list)
        self.write(v_json)