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
from   web.model.t_archive import query_archive,save_archive,get_archive_by_archiveid,upd_archive,del_archive
from   web.model.t_archive import query_archive_log,push_archive_task,run_archive_task,stop_archive_task,query_archive_detail
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server,get_sync_db_server_by_type
from   web.utils.common import current_rq2
from   web.utils.basehandler import basehandler


class archivequery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_query.html")

class archive_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag  = self.get_argument("archive_tag")
        v_list       = query_archive(archive_tag)
        v_json       = json.dumps(v_list)
        self.write(v_json)

class archive_query_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archive_id")
        v_list      = query_archive_detail(archive_id)
        v_json      = json.dumps(v_list)
        self.write({"code": 0, "message": v_json})

class archiveadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_add.html",
                    archive_server=get_sync_server(),
                    dm_db_type=get_dmm_from_dm('02'),
                    dm_archive_type=get_dmm_from_dm('09'),
                    dm_archive_time_type=get_dmm_from_dm('20'),
                    dm_archive_rentition=get_dmm_from_dm('21'),
                    )

class archiveadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_archive = {}
        d_archive['archive_tag']          = self.get_argument("archive_tag")
        d_archive['task_desc']            = self.get_argument("task_desc")
        d_archive['archive_server']       = self.get_argument("archive_server")
        d_archive['archive_db_type']      = self.get_argument("archive_db_type")
        d_archive['sour_db_server']       = self.get_argument("sour_db_server")
        d_archive['sour_db_name']         = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_archive['archive_time_col']     = self.get_argument("archive_time_col")
        d_archive['archive_rentition']    = self.get_argument("archive_rentition")
        d_archive['rentition_time']       = self.get_argument("rentition_time")
        d_archive['rentition_time_type']  = self.get_argument("rentition_time_type")
        d_archive['if_cover']             = self.get_argument("if_cover")
        d_archive['dest_db_server']       = self.get_argument("dest_db_server")
        d_archive['dest_db_name']         = self.get_argument("dest_db_name")
        d_archive['python3_home']         = self.get_argument("python3_home")
        d_archive['script_base']          = self.get_argument("script_base")
        d_archive['script_name']          = self.get_argument("script_name")
        d_archive['run_time']             = self.get_argument("run_time")
        d_archive['batch_size']           = self.get_argument("batch_size")
        d_archive['api_server']           = self.get_argument("api_server")
        d_archive['status']               = self.get_argument("status")
        result=save_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archivechange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_change.html")

class archiveedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        archive_id   = self.get_argument("archiveid")
        d_archive    = get_archive_by_archiveid(archive_id)
        print('xxxxx=',get_sync_db_server_by_type(d_archive['archive_db_type'])['message'])
        print('yyyyy=', d_archive['dest_db_id'])
        print('zzzzz=', d_archive['sour_db_id'])

        self.render("./archive_edit.html",
                    dm_db_type           = get_dmm_from_dm('02'),
                    dm_archive_server    = get_sync_server(),
                    dm_archive_type      = get_dmm_from_dm('09'),
                    dm_archive_time_type = get_dmm_from_dm('20'),
                    dm_archive_rentition = get_dmm_from_dm('21'),
                    dm_archive_instance  = get_sync_db_server_by_type(d_archive['archive_db_type'])['message'],
                    archive_id           = archive_id,
                    archive_tag          = d_archive['archive_tag'],
                    task_desc            = d_archive['comments'],
                    archive_server       = d_archive['server_id'],
                    archive_db_type      = d_archive['archive_db_type'],
                    sour_db_id           = d_archive['sour_db_id'],
                    sour_schema          = d_archive['sour_schema'],
                    sour_table           = d_archive['sour_table'],
                    archive_time_col     = d_archive['archive_time_col'],
                    archive_rentition    = d_archive['archive_rentition'],
                    rentition_time       = d_archive['rentition_time'],
                    rentition_time_type  = d_archive['rentition_time_type'],
                    if_cover             = d_archive['if_cover'],
                    dest_db_id           = d_archive['dest_db_id'],
                    dest_schema          = d_archive['dest_schema'],
                    script_path          = d_archive['script_path'],
                    script_name          = d_archive['script_file'],
                    run_time             = d_archive['run_time'],
                    python3_home         = d_archive['python3_home'],
                    batch_size           = d_archive['batch_size'],
                    api_server           = d_archive['api_server'],
                    status               = d_archive['status']
                    )

class archiveedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_archive = {}
        d_archive['archive_id']          = self.get_argument("archive_id")
        d_archive['archive_tag']         = self.get_argument("archive_tag")
        d_archive['task_desc']           = self.get_argument("task_desc")
        d_archive['archive_server']      = self.get_argument("archive_server")
        d_archive['archive_db_type']     = self.get_argument("archive_db_type")
        d_archive['sour_db_server']      = self.get_argument("sour_db_server")
        d_archive['sour_db_name']        = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']       = self.get_argument("sour_tab_name")
        d_archive['archive_time_col']    = self.get_argument("archive_time_col")
        d_archive['archive_rentition']   = self.get_argument("archive_rentition")
        d_archive['rentition_time']      = self.get_argument("rentition_time")
        d_archive['rentition_time_type'] = self.get_argument("rentition_time_type")
        d_archive['if_cover']            = self.get_argument("if_cover")
        d_archive['dest_db_server']      = self.get_argument("dest_db_server")
        d_archive['dest_db_name']        = self.get_argument("dest_db_name")
        d_archive['python3_home']        = self.get_argument("python3_home")
        d_archive['script_base']         = self.get_argument("script_base")
        d_archive['script_name']         = self.get_argument("script_name")
        d_archive['run_time']            = self.get_argument("run_time")
        d_archive['batch_size']          = self.get_argument("batch_size")
        d_archive['api_server']          = self.get_argument("api_server")
        d_archive['status']              = self.get_argument("status")
        print(d_archive)
        result=upd_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archiveedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archiveid")
        result=del_archive(archive_id)
        self.write({"code": result['code'], "message": result['message']})

class archivelogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_log_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_sync_ywlx=get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class archive_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag    = self.get_argument("archive_tag")
        market_id   = self.get_argument("market_id")
        archive_ywlx   = self.get_argument("archive_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = query_archive_log(archive_tag,market_id,archive_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class archiveedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveedit_run(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveedit_stop(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_archive_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class archiveclone(basehandler):
    @tornado.web.authenticated
    def get(self):
        archive_id   = self.get_argument("archive_id")
        d_archive    = get_archive_by_archiveid(archive_id)
        self.render("./archive_clone.html",
                    dm_db_type          = get_dmm_from_dm('02'),
                    dm_archive_server   = get_sync_server(),
                    dm_archive_type     = get_dmm_from_dm('09'),
                    dm_archive_time_type= get_dmm_from_dm('20'),
                    dm_archive_rentition= get_dmm_from_dm('21'),
                    dm_archive_instance = get_sync_db_server_by_type(d_archive['archive_db_type'])['message'],
                    archive_id          = archive_id,
                    archive_tag         = d_archive['archive_tag'] + '_clone',
                    task_desc           = d_archive['comments'] + '_clone',
                    archive_server      = d_archive['server_id'],
                    archive_db_type     = d_archive['archive_db_type'],
                    sour_db_id          = d_archive['sour_db_id'],
                    sour_schema         = d_archive['sour_schema'],
                    sour_table          = d_archive['sour_table'],
                    archive_time_col    = d_archive['archive_time_col'],
                    archive_rentition   = d_archive['archive_rentition'],
                    rentition_time      = d_archive['rentition_time'],
                    rentition_time_type = d_archive['rentition_time_type'],
                    if_cover            = d_archive['if_cover'],
                    dest_db_id          = d_archive['dest_db_id'],
                    dest_schema         = d_archive['dest_schema'],
                    script_path         = d_archive['script_path'],
                    script_name         = d_archive['script_file'],
                    run_time            = d_archive['run_time'],
                    python3_home        = d_archive['python3_home'],
                    batch_size          = d_archive['batch_size'],
                    api_server          = d_archive['api_server'],
                    status              = d_archive['status'],
        )

class archiveclone_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_archive = {}
        d_archive['archive_tag']         = self.get_argument("archive_tag")
        d_archive['task_desc']           = self.get_argument("task_desc")
        d_archive['archive_server']      = self.get_argument("archive_server")
        d_archive['archive_db_type']     = self.get_argument("archive_db_type")
        d_archive['sour_db_server']      = self.get_argument("sour_db_server")
        d_archive['sour_db_name']        = self.get_argument("sour_db_name")
        d_archive['sour_tab_name']       = self.get_argument("sour_tab_name")
        d_archive['archive_time_col']    = self.get_argument("archive_time_col")
        d_archive['archive_rentition']   = self.get_argument("archive_rentition")
        d_archive['rentition_time']      = self.get_argument("rentition_time")
        d_archive['rentition_time_type'] = self.get_argument("rentition_time_type")
        d_archive['if_cover']            = self.get_argument("if_cover")
        d_archive['dest_db_server']      = self.get_argument("dest_db_server")
        d_archive['dest_db_name']        = self.get_argument("dest_db_name")
        d_archive['python3_home']        = self.get_argument("python3_home")
        d_archive['script_base']         = self.get_argument("script_base")
        d_archive['script_name']         = self.get_argument("script_name")
        d_archive['run_time']            = self.get_argument("run_time")
        d_archive['batch_size']          = self.get_argument("batch_size")
        d_archive['api_server']          = self.get_argument("api_server")
        d_archive['status']              = self.get_argument("status")
        result = save_archive(d_archive)
        self.write({"code": result['code'], "message": result['message']})

class archivelogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_log_query.html",
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class archive_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_tag    = self.get_argument("archive_tag")
        begin_date      = self.get_argument("begin_date")
        end_date        = self.get_argument("end_date")
        v_list          = query_archive_log(archive_tag,begin_date,end_date)
        v_json          = json.dumps(v_list)
        self.write(v_json)