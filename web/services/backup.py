#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.model.t_backup    import query_backup,query_backup_case,save_backup,get_backup_by_backupid,upd_backup,del_backup,query_backup_log,query_backup_log_detail
from   web.model.t_backup    import push_backup_task,run_backup_task,stop_backup_task,query_backup_log_analyze
from web.model.t_dmmx import get_dmm_from_dm, get_backup_server, get_db_backup_server, get_db_backup_tags, \
    get_db_backup_tags_by_env_type, get_db_server
from   web.utils.common      import get_day_nday_ago,now,current_rq2,current_rq3
from   web.utils             import base_handler

class backupquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./backup/backup_query.html",
                    dm_env_type = await get_dmm_from_dm('03'),
                    dm_db_type  = await get_dmm_from_dm('02')
                    )

class backup_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname     = self.get_argument("tagname")
        db_env      = self.get_argument("db_env")
        db_type     = self.get_argument("db_type")
        v_list      = await query_backup(tagname,db_env,db_type)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class backup_case(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_env = self.get_argument("db_env")
        v_list      = await query_backup_case(db_env)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class backupadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./backup/backup_add.html",
                    backup_server = await get_backup_server(),
                    db_server     = await get_db_server(),
                    dm_db_type    = await get_dmm_from_dm('02'),
                    )

class backupadd_save(base_handler.TokenHandler):
    async def post(self):
        d_backup = {}
        d_backup['backup_server']   = self.get_argument("backup_server")
        d_backup['db_server']       = self.get_argument("db_server")
        d_backup['db_type']         = self.get_argument("db_type")
        d_backup['backup_tag']      = self.get_argument("backup_tag")
        d_backup['backup_expire']   = self.get_argument("backup_expire")
        d_backup['backup_base']     = self.get_argument("backup_base")
        d_backup['script_base']     = self.get_argument("script_base")
        d_backup['script_name']     = self.get_argument("script_name")
        d_backup['cmd_name']        = self.get_argument("cmd_name")
        d_backup['run_time']        = self.get_argument("run_time")
        d_backup['task_desc']       = self.get_argument("task_desc")
        d_backup['python3_home']    = self.get_argument("python3_home")
        d_backup['backup_databases']= self.get_argument("backup_databases")
        d_backup['api_server']      = self.get_argument("api_server")
        d_backup['task_desc']       = self.get_argument("task_desc")
        d_backup['status']          = self.get_argument("status")
        d_backup['binlog_status']   = self.get_argument("binlog_status")
        result = await save_backup(d_backup)
        self.write({"code": result['code'], "message": result['message']})

class backupchange(base_handler.TokenHandler):
    async def get(self):
        self.render("./backup/backup_change.html",
                    dm_env_type=await get_dmm_from_dm('03'),
                    dm_db_type=await get_dmm_from_dm('02'))

class backupedit(base_handler.TokenHandler):
    async def get(self):
        backup_id = self.get_argument("backupid")
        d_backup  = await get_backup_by_backupid(backup_id)
        self.render("./backup/backup_edit.html",
                    backup_id        = d_backup['backup_id'],
                    server_id        = d_backup['server_id'] ,
                    db_id            = d_backup['db_id'] ,
                    db_type          = d_backup['db_type'] ,
                    backup_tag       = d_backup['backup_tag'] ,
                    backup_expire    = d_backup['backup_expire'],
                    backup_base      = d_backup['backup_base'],
                    script_base      = d_backup['script_base'],
                    script_name      = d_backup['script_name'],
                    cmd_name         = d_backup['cmd_name'],
                    run_time         = d_backup['run_time'],
                    comments         = d_backup['comments'],
                    python3_home     = d_backup['python3_home'] ,
                    backup_databases = d_backup['backup_databases'],
                    api_server       = d_backup['api_server'] ,
                    status           = d_backup['status'],
                    binlog_status    = d_backup['binlog_status'],
                    backup_server    = await get_backup_server(),
                    db_server        = await get_db_server(),
                    dm_db_type       = await get_dmm_from_dm('02')
                    )

class backupedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_backup = {}
        d_backup['backup_id']        = self.get_argument("backup_id")
        d_backup['backup_server']    = self.get_argument("backup_server")
        d_backup['db_server']        = self.get_argument("db_server")
        d_backup['db_type']          = self.get_argument("db_type")
        d_backup['backup_tag']       = self.get_argument("backup_tag")
        d_backup['backup_expire']    = self.get_argument("backup_expire")
        d_backup['backup_base']      = self.get_argument("backup_base")
        d_backup['script_base']      = self.get_argument("script_base")
        d_backup['script_name']      = self.get_argument("script_name")
        d_backup['cmd_name']         = self.get_argument("cmd_name")
        d_backup['run_time']         = self.get_argument("run_time")
        d_backup['task_desc']        = self.get_argument("task_desc")
        d_backup['python3_home']     = self.get_argument("python3_home")
        d_backup['backup_databases'] = self.get_argument("backup_databases")
        d_backup['api_server']       = self.get_argument("api_server")
        d_backup['task_desc']        = self.get_argument("task_desc")
        d_backup['status']           = self.get_argument("status")
        d_backup['binlog_status']    = self.get_argument("binlog_status")
        result = await upd_backup(d_backup)
        self.write({"code": result['code'], "message": result['message']})

class backupedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        backupid  = self.get_argument("backupid")
        result = await del_backup(backupid)
        self.write({"code": result['code'], "message": result['message']})

class backuplogquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./backup/backup_log_query.html",
                    dm_env_type = await get_dmm_from_dm('03'),
                    begin_date = current_rq3(-1),
                    end_date = current_rq2())

class backup_log_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname    = self.get_argument("tagname")
        db_env     = self.get_argument("db_env")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        v_list     = await query_backup_log(tagname,db_env,begin_date,end_date)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class backup_log_query_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname     = self.get_argument("tagname")
        backup_date = self.get_argument("backup_date")
        v_list      = await query_backup_log_detail(tagname,backup_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class backuploganalyze(base_handler.TokenHandler):
    async def get(self):
        self.render("./backup/backup_log_analyze.html",
                      dm_env_type    = await get_dmm_from_dm('03'),
                      dm_db_type     = await get_dmm_from_dm('02'),
                      db_backup_tags = await get_db_backup_tags(),
                      begin_date     = get_day_nday_ago(now(),15),
                      end_date       = get_day_nday_ago(now(),0)
                    )


class backup_log_analyze(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_list          = {}
        db_env          = self.get_argument("db_env")
        db_type         = self.get_argument("db_type")
        tagname         = self.get_argument("tagname")
        begin_date      = self.get_argument("begin_date")
        end_date        = self.get_argument("end_date")
        v_list1,v_list2 = await query_backup_log_analyze(db_env,db_type,tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        self.write(v_json)

class get_backup_tasks(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_env  = self.get_argument("db_env")
        db_type = self.get_argument("db_type")
        d_list  = {}
        d_list['data'] = await get_db_backup_tags_by_env_type(db_env,db_type)
        v_json  = json.dumps(d_list)
        self.write(v_json)

class backupedit_push(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_backup_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class backupedit_run(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_backup_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(json.loads(v_json))

class backupedit_stop(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_backup_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)