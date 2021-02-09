#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : 马飞
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst_list
from  web.model.t_db_user     import query_db_user,save_db_user,get_user_sql,get_db_name,query_user_by_id,update_db_user,delete_db_user
from  web.model.t_dmmx        import get_dmm_from_dm,get_inst_names


class dbuserquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_user_query.html",
                    dm_inst_list    = query_inst_list(),
                    mysql_sys_privs = get_dmm_from_dm('31'),
                    dm_user_status  = get_dmm_from_dm('25'),
                    dm_env_type     = get_dmm_from_dm('03'),
                    dm_inst_names   = get_inst_names(''),
                 )


class db_user_query_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        user_id  = self.get_argument("user_id")
        v_list   = query_user_by_id(user_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)


class db_user_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        user_name  = self.get_argument("user_name")
        inst_env   = self.get_argument("inst_env")
        inst_id    = self.get_argument("inst_id")
        v_list     = query_db_user(user_name,inst_env,inst_id)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class db_user_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_db_user = {}
        d_db_user['inst_id']     = self.get_argument("add_inst_id")
        d_db_user['db_user']     = self.get_argument("add_db_user")
        d_db_user['db_pass']     = self.get_argument("add_db_pass")
        d_db_user['user_dbs']    = self.get_argument("add_user_dbs")
        d_db_user['user_privs']  = self.get_argument("add_user_privs")
        d_db_user['statement']   = self.get_argument("add_statement")
        d_db_user['status']      = self.get_argument("add_status")
        d_db_user['desc']        = self.get_argument("add_desc")
        print('db_user_save=',d_db_user)
        result = save_db_user(d_db_user)
        self.write({"code": result['code'], "message": result['message']})

class db_user_update(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_db_user = {}
        d_db_user['user_id']     = self.get_argument("upd_user_id")
        d_db_user['inst_id']     = self.get_argument("upd_inst_id")
        d_db_user['db_user']     = self.get_argument("upd_db_user")
        d_db_user['db_pass']     = self.get_argument("upd_db_pass")
        d_db_user['user_dbs']    = self.get_argument("upd_user_dbs")
        d_db_user['user_privs']  = self.get_argument("upd_user_privs")
        d_db_user['statement']   = self.get_argument("upd_statement")
        d_db_user['status']      = self.get_argument("upd_status")
        d_db_user['desc']        = self.get_argument("upd_desc")
        print('db_user_update=',d_db_user)
        result = update_db_user(d_db_user)
        self.write({"code": result['code'], "message": result['message']})


class db_user_delete(basehandler):
    @tornado.web.authenticated
    def post(self):
        user_id  = self.get_argument("user_id")
        print('db_user_delete=',user_id)
        result = delete_db_user(user_id)
        self.write({"code": result['code'], "message": result['message']})

class db_user_sql(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_db_user = {}
        d_db_user['mysql_db_user']       = self.get_argument("mysql_db_user")
        d_db_user['mysql_privs']   = self.get_argument("mysql_privs")
        d_db_user['mysql_dbs']     = self.get_argument("mysql_dbs")
        print('db_user_sql=',d_db_user)
        result = get_user_sql(d_db_user)
        self.write(result)


class db_user_dbs(basehandler):
    def post(self):
        inst_id  = self.get_argument("inst_id")
        print('db_user_dbs=',inst_id)
        result = get_db_name(inst_id)
        self.write({"code": result['code'], "message": result['message']})

class db_user_info(basehandler):
    def post(self):
        inst_id = self.get_argument("inst_id")
        print('db_user_dbs=', inst_id)
        result = get_db_name(inst_id)
        self.write({"code": result['code'], "message": result['message']})

