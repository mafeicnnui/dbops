#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据库备份管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_minio  import query_minio,query_minio_case,save_minio,get_minio_by_minioid,upd_minio,del_minio,query_minio_log,query_minio_log_detail
from   web.model.t_minio  import push_minio_task,run_minio_task,stop_minio_task,query_minio_log_analyze
from   web.model.t_dmmx   import get_dmm_from_dm,get_backup_server,get_db_backup_server,get_minio_tags,get_sync_server,get_db_backup_tags_by_env_type
from   web.utils.common   import get_day_nday_ago,now,current_rq2,current_rq3
from   web.utils.basehandler import basehandler

class minioquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./minio_query.html"
                    )

class minio_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname     = self.get_argument("tagname")
        v_list      = query_minio(tagname)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class minio_case(basehandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_env = self.get_argument("db_env")
        v_list      = query_minio_case(db_env)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class minioadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./minio_add.html",
                    dm_sync_server=get_sync_server(),
                    dm_sync_type=get_dmm_from_dm('34'),
                    dm_sync_time_type=get_dmm_from_dm('10')
                    )

class minioadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_sync = {}
        d_sync['sync_tag']        = self.get_argument("sync_tag")
        d_sync['task_desc']       = self.get_argument("task_desc")
        d_sync['server_id']       = self.get_argument("sync_server")
        d_sync['sync_type']       = self.get_argument("sync_type")
        d_sync['sync_dir']        = self.get_argument("sync_dir")
        d_sync['sync_service']    = self.get_argument("sync_service")
        d_sync['minio_server']    = self.get_argument("minio_server")
        d_sync['minio_user']      = self.get_argument("minio_user")
        d_sync['minio_pass']      = self.get_argument("minio_pass")
        d_sync['python3_home']    = self.get_argument("python3_home")
        d_sync['script_base']     = self.get_argument("script_base")
        d_sync['script_name']     = self.get_argument("script_name")
        d_sync['run_time']        = self.get_argument("run_time")
        d_sync['api_server']      = self.get_argument("api_server")
        d_sync['status']          = self.get_argument("status")
        d_sync['minio_bucket']    = self.get_argument("minio_bucket")
        d_sync['minio_dpath']     = self.get_argument("minio_dpath")
        d_sync['minio_incr']      = self.get_argument("minio_incr")
        d_sync['minio_incr_type'] = self.get_argument("minio_incr_type")
        result=save_minio(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class miniochange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./minio_change.html"
                   )

class minioedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        sync_tag   = self.get_argument("sync_tag")
        d_sync     = get_minio_by_minioid(sync_tag)
        self.render("./minio_edit.html",
                    sync_tag       = d_sync['sync_tag'],
                    task_desc      = d_sync['comments'],
                    sync_server    = d_sync['server_id'],
                    sync_type      = d_sync['sync_type'],
                    sync_dir       = d_sync['sync_path'],
                    sync_service   = d_sync['sync_service'],
                    minio_server   = d_sync['minio_server'],
                    minio_user     = d_sync['minio_user'],
                    minio_pass     = d_sync['minio_pass'],
                    python3_home   = d_sync['python3_home'],
                    script_base    = d_sync['script_path'],
                    script_name    = d_sync['script_file'],
                    run_time       = d_sync['run_time'],
                    api_server     = d_sync['api_server'],
                    status         = d_sync['status'],
                    minio_bucket   = d_sync['minio_bucket'],
                    minio_dpath    = d_sync['minio_dpath'],
                    minio_incr     = d_sync['minio_incr'],
                    minio_incr_type= d_sync['minio_incr_type'],
                    dm_sync_server = get_sync_server(),
                    dm_sync_type   = get_dmm_from_dm('34'),
                    dm_sync_time_type=get_dmm_from_dm('10')
                    )

class minioclone(basehandler):
    @tornado.web.authenticated
    def get(self):
        sync_tag = self.get_argument("sync_tag")
        d_sync = get_minio_by_minioid(sync_tag)
        self.render("./minio_clone.html",
                    sync_tag         = d_sync['sync_tag']+'_clone',
                    task_desc        = d_sync['comments']+'_clone',
                    sync_server      = d_sync['server_id'],
                    sync_type        = d_sync['sync_type'],
                    sync_dir         = d_sync['sync_path'],
                    sync_service     = d_sync['sync_service'],
                    minio_server     = d_sync['minio_server'],
                    minio_user       = d_sync['minio_user'],
                    minio_pass       = d_sync['minio_pass'],
                    python3_home     = d_sync['python3_home'],
                    script_base      = d_sync['script_path'],
                    script_name      = d_sync['script_file'],
                    run_time         = d_sync['run_time'],
                    api_server       = d_sync['api_server'],
                    status           = d_sync['status'],
                    minio_bucket     = d_sync['minio_bucket'],
                    minio_dpath      = d_sync['minio_dpath'],
                    minio_incr       = d_sync['minio_incr'],
                    minio_incr_type  = d_sync['minio_incr_type'],
                    dm_sync_server   = get_sync_server(),
                    dm_sync_type     = get_dmm_from_dm('34'),
                    dm_sync_time_type= get_dmm_from_dm('10')
                    )


class minioedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_tag']      = self.get_argument("sync_tag")
        d_sync['task_desc']     = self.get_argument("task_desc")
        d_sync['server_id']     = self.get_argument("sync_server")
        d_sync['sync_type']     = self.get_argument("sync_type")
        d_sync['sync_dir']      = self.get_argument("sync_dir")
        d_sync['sync_service']  = self.get_argument("sync_service")
        d_sync['minio_server']  = self.get_argument("minio_server")
        d_sync['minio_user']    = self.get_argument("minio_user")
        d_sync['minio_pass']    = self.get_argument("minio_pass")
        d_sync['python3_home']  = self.get_argument("python3_home")
        d_sync['script_base']   = self.get_argument("script_base")
        d_sync['script_name']   = self.get_argument("script_name")
        d_sync['run_time']      = self.get_argument("run_time")
        d_sync['api_server']    = self.get_argument("api_server")
        d_sync['status']        = self.get_argument("status")
        d_sync['minio_bucket']  = self.get_argument("minio_bucket")
        d_sync['minio_dpath']   = self.get_argument("minio_dpath")
        d_sync['minio_incr']    = self.get_argument("minio_incr")
        d_sync['minio_incr_type'] = self.get_argument("minio_incr_type")
        result=upd_minio(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class minioedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag  = self.get_argument("sync_tag")
        result=del_minio(sync_tag)
        self.write({"code": result['code'], "message": result['message']})

class miniologquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./minio_log_query.html",
                    begin_date=current_rq3(-1),
                    end_date=current_rq2()
                    )

class minio_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        v_list     = query_minio_log(tagname,begin_date,end_date)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class miniologanalyze(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./minio_log_analyze.html",
                      minio_tags     = get_minio_tags(),
                      begin_date     = get_day_nday_ago(now(),15),
                      end_date       = get_day_nday_ago(now(),0)
                    )

class minio_log_analyze(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2,v_list3 = query_minio_log_analyze(tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        d_list['data3'] = v_list3
        v_json = json.dumps(d_list)
        self.write(v_json)


class minioedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_minio_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

