#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 15:43
# @Author : ma.fei
# @File : role.py.py
# @Software: PyCharm

import json
import tornado.web
from   web.utils.basehandler import basehandler
from web.model.t_slow        import save_slow, check_slow, query_slow, upd_slow, del_slow, query_slow_by_id, analyze_slow_log, \
                                    query_slow_log_plan, get_slow_db_by_instid, get_slow_user_by_instid
from   web.model.t_slow      import push_slow,query_slow_log_by_id,query_slow_log_by_id_oracle,query_slow_log_by_id_mssql,query_slow_log,query_slow_log_detail,\
                                    get_slow_db_by_dsid,get_slow_user_by_dsid,query_slow_log_oracle,query_slow_log_mssql
from   web.model.t_dmmx      import get_dmm_from_dm, get_slow_inst_names,get_slow_dbs_names, get_gather_server,get_sync_db_server
from   web.utils.common      import current_rq2,current_rq3,current_rq4
from   web.model.t_ds        import get_ds_by_dsid

class slowquery(basehandler):
    @tornado.web.authenticated
    async def get(self):
        self.render("./slow/slow_log_query.html",
                     begin_date    = current_rq3(-1),
                     end_date      = current_rq2(),
                     dm_inst_names = await get_slow_inst_names(''),
                     dm_dbs_names  = await get_slow_dbs_names('')
                    )

class slow_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        ds_id     = self.get_argument("ds_id")
        inst_id   = self.get_argument("inst_id")
        inst_env  = self.get_argument("inst_env")
        inst_type = self.get_argument("inst_type")
        v_list    = await query_slow(inst_id,ds_id,inst_env,inst_type)
        v_json    = json.dumps(v_list)
        self.write(v_json)

class slowadd(basehandler):
    @tornado.web.authenticated
    async def get(self):
        self.render("./slow/slow_add.html",
                    dm_db_type      = await get_dmm_from_dm('02'),
                    dm_inst_names   = await get_slow_inst_names(''),
                    dm_db_server    = await get_gather_server(),
                    dm_stats_method = await get_dmm_from_dm('37'),
                    # db_server       = (await get_sync_db_server_by_type('0'))['message'],
                    db_server       = await get_sync_db_server()
                    )

class slowadd_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        d_slow={}
        d_slow['db_type']        = self.get_argument("db_type")
        d_slow['db_source']      = self.get_argument("db_source")
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
        result = await save_slow(d_slow)
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
    async def get(self):
        self.render("./slow/slow_change.html",
                    dm_env_type   = await get_dmm_from_dm('03'),
                    dm_inst_type  = await get_dmm_from_dm('38'),
                    dm_inst_names = await get_slow_inst_names(''),
                    dm_dbs_names  = await get_slow_dbs_names(''),
                    dm_db_server  = await get_gather_server()
                    )

class slow_query_by_id(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        v_list   = await query_slow_by_id(slow_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class slowedit_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_slow = {}
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
        result = await upd_slow(d_slow)
        self.write({"code": result['code'], "message": result['message']})

class slowedit_del(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id  = self.get_argument("slow_id")
        result = await del_slow(slow_id)
        self.write({"code": result['code'], "message": result['message']})

class slowedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        slow_id    = self.get_argument("slow_id")
        api_server = self.get_argument("api_server")
        v_list     = push_slow(api_server,slow_id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class slowlogquery(basehandler):
    @tornado.web.authenticated
    async def get(self):
        self.render("./slow/slow_log_query.html",
                     begin_date    = current_rq4(0,1),
                     end_date      = current_rq4(0,-1),
                     dm_inst_names = await get_slow_inst_names(''),
                     dm_dbs_names  = await get_slow_dbs_names('')
                    )

class slowlog_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id          = self.get_argument("inst_id")
        ds_id            = self.get_argument("ds_id")
        db_name          = self.get_argument("db_name")
        db_user          = self.get_argument("db_user")
        db_host          = self.get_argument("db_host")
        begin_date       = self.get_argument("begin_date")
        end_date         = self.get_argument("end_date")
        begin_query_time = self.get_argument("begin_query_time")
        end_query_time   = self.get_argument("end_query_time")
        db_sql           = self.get_argument("db_sql")
        dss              = await get_ds_by_dsid(ds_id)
        if dss['db_type'] == '1':
            v_list = await query_slow_log_oracle(ds_id,db_user,begin_date,end_date,begin_query_time,end_query_time,db_sql)
        elif dss['db_type'] == '2':
            v_list = await query_slow_log_mssql(ds_id, db_user, begin_date, end_date, begin_query_time, end_query_time,db_sql)
        else:
            v_list =  await query_slow_log(  inst_id, ds_id, db_name, db_user, db_host, begin_date, end_date, begin_query_time,end_query_time, db_sql)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_by_id(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id   = self.get_argument("sql_id")
        v_list   = await query_slow_log_by_id(sql_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)


class query_slowlog_by_id_oracle(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_list = await query_slow_log_by_id_oracle(sql_id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_by_id_mssql(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_list = await query_slow_log_by_id_mssql(sql_id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class query_slowlog_detail_by_id(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_list = await query_slow_log_detail(sql_id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class query_slowlog_plan_by_id(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/text; charset=UTF-8")
        sql_id = self.get_argument("sql_id")
        v_plan = await query_slow_log_plan(sql_id)
        self.write(v_plan)

class query_db_by_inst(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        v_list   = await get_slow_db_by_instid(inst_id)
        v_json   = json.dumps({'data':v_list})
        self.write(v_json)

class query_db_by_slowlog_instid(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        v_list   = await get_slow_db_by_instid(inst_id)
        v_json   = json.dumps({'data':v_list})
        self.write(v_json)

class query_user_by_slowlog_instid(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id = self.get_argument("inst_id")
        v_list  = await get_slow_user_by_instid(inst_id)
        v_json  = json.dumps({'data':v_list})
        self.write(v_json)

class query_db_by_slowlog_dsid(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_id  = self.get_argument("db_id")
        v_list   = await get_slow_db_by_dsid(db_id)
        v_json   = json.dumps({'data':v_list})
        self.write(v_json)

class query_user_by_slowlog_dsid(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_id = self.get_argument("db_id")
        v_list  = await get_slow_user_by_dsid(db_id)
        v_json  = json.dumps({'data':v_list})
        self.write(v_json)

class slowloganalyze(basehandler):
    @tornado.web.authenticated
    async def get(self):
        self.render("./slow/slow_log_analyze.html",
                     begin_date    = current_rq4(0,1),
                     end_date      = current_rq4(0,-1),
                     dm_inst_names = await get_slow_inst_names(''),
                     dm_dbs_names  = await get_slow_dbs_names(''),
                    )

class slowlog_analyze(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id          = self.get_argument("inst_id")
        ds_id            = self.get_argument("ds_id")
        db_name          = self.get_argument("db_name")
        db_user          = self.get_argument("db_user")
        db_host          = self.get_argument("db_host")
        begin_date       = self.get_argument("begin_date")
        end_date         = self.get_argument("end_date")
        begin_query_time = self.get_argument("begin_query_time")
        end_query_time   = self.get_argument("end_query_time")
        db_sql           = self.get_argument("db_sql")
        v_list           = await analyze_slow_log(inst_id,ds_id,db_name,db_user,db_host,begin_date,end_date,begin_query_time,end_query_time,db_sql)
        v_json           = json.dumps(v_list)
        self.write(v_json)

