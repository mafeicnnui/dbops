#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:43
# @Author : 马飞
# @File : role.py.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   角色管理                                          #
#                                                                                    #
######################################################################################
import json
import tornado.web
from   web.model.t_slow      import save_slow,check_slow,query_slow,upd_slow,del_slow,query_slow_by_id,analyze_slow_log,query_slow_log_plan
from   web.model.t_slow      import push_slow,query_slow_log_by_id,query_slow_log,get_db_by_inst_id,get_user_by_inst_id,query_slow_log_detail
from   web.utils.basehandler import basehandler
from   web.model.t_dmmx      import get_dmm_from_dm,get_inst_names,get_gather_server
from   web.utils.common      import current_rq2,current_rq3,current_rq4


class slowquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_log_query.html",
                     begin_date    = current_rq3(-1),
                     end_date      =  current_rq2(),
                     dm_inst_names = get_inst_names(''),
                    )

class slow_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        inst_env = self.get_argument("inst_env")
        v_list = query_slow(inst_id,inst_env)
        v_json = json.dumps(v_list)
        self.write(v_json)

class slowadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_add.html",
                    dm_inst_names=get_inst_names(''),
                    dm_db_server=get_gather_server(),
                    )

class slowadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_slow={}
        d_slow['inst_id']        = self.get_argument("inst_id")
        d_slow['server_id']      = self.get_argument("server_id")
        d_slow['slow_time']      = self.get_argument("slow_time")
        d_slow['slow_log_name']  = self.get_argument("slow_log_name")
        d_slow['python3_home']   = self.get_argument("python3_home")
        d_slow['run_time']       = self.get_argument("run_time")
        d_slow['exec_time']      = self.get_argument("exec_time")
        d_slow['script_path']    = self.get_argument("script_path")
        d_slow['script_file']    = self.get_argument("script_file")
        d_slow['api_server']     = self.get_argument("api_server")
        d_slow['slow_status']    = self.get_argument("slow_status")
        result = save_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slow_check(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_slow = {}
        d_slow['inst_id']     = self.get_argument("inst_id")
        d_slow['slow_status'] = self.get_argument("slow_status")
        result = check_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slowchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_change.html",
                    dm_env_type  = get_dmm_from_dm('03'),
                    dm_inst_names = get_inst_names(''),
                    dm_db_server=get_gather_server(),
                    )

class slow_query_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        v_list   = query_slow_by_id(slow_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)


class slowedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_slow={}
        d_slow['slow_id']       = self.get_argument("slow_id")
        d_slow['inst_id']       = self.get_argument("inst_id")
        d_slow['server_id']     = self.get_argument("server_id")
        d_slow['slow_time']     = self.get_argument("slow_time")
        d_slow['slow_log_name'] = self.get_argument("slow_log_name")
        d_slow['python3_home']  = self.get_argument("python3_home")
        d_slow['run_time']      = self.get_argument("run_time")
        d_slow['exec_time']     = self.get_argument("exec_time")
        d_slow['script_path']   = self.get_argument("script_path")
        d_slow['script_file']   = self.get_argument("script_file")
        d_slow['api_server']    = self.get_argument("api_server")
        d_slow['slow_status']   = self.get_argument("slow_status")
        result=upd_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slowedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        result=del_slow(slow_id)
        self.write({"code": result['code'], "message": result['message']})


class slowedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id    = self.get_argument("slow_id")
        api_server = self.get_argument("api_server")
        v_list=push_slow(api_server,slow_id)
        v_json = json.dumps(v_list)
        self.write(v_json)



class slowlogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_log_query.html",
                     begin_date    = current_rq4(0,1),
                     end_date      =  current_rq4(0,-1),
                     dm_inst_names = get_inst_names(''),
                    )

class slowlog_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id    = self.get_argument("inst_id")
        db_name    = self.get_argument("db_name")
        db_user    = self.get_argument("db_user")
        db_host    = self.get_argument("db_host")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        v_list     = query_slow_log(inst_id,db_name,db_user,db_host,begin_date,end_date)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id   = self.get_argument("sql_id")
        v_list   = query_slow_log_by_id(sql_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_detail_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_list = query_slow_log_detail(sql_id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_plan_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/text; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_plan = query_slow_log_plan(sql_id)
        self.write(v_plan)

class query_db_by_inst(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        d_list  = {}
        v_list  = get_db_by_inst_id(inst_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        self.write(v_json)

class query_user_by_inst(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id = self.get_argument("inst_id")
        d_list  = {}
        v_list  = get_user_by_inst_id(inst_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        self.write(v_json)


class slowloganalyze(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./slow_log_analyze.html",
                     begin_date    = current_rq4(0,1),
                     end_date      =  current_rq4(0,-1),
                     dm_inst_names = get_inst_names(''),
                    )

class slowlog_analyze(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id    = self.get_argument("inst_id")
        db_name    = self.get_argument("db_name")
        db_user    = self.get_argument("db_user")
        db_host    = self.get_argument("db_host")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        v_list     = analyze_slow_log(inst_id,db_name,db_user,db_host,begin_date,end_date)
        v_json     = json.dumps(v_list)
        self.write(v_json)

