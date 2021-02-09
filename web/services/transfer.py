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
from   web.model.t_transfer import query_transfer,save_transfer,get_transfer_by_transferid,upd_transfer,del_transfer
from   web.model.t_transfer import query_transfer_log,push_transfer_task,run_transfer_task,stop_transfer_task,query_transfer_detail
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server
from   web.utils.common import current_rq2
from   web.utils.basehandler import basehandler


class transferquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_query.html"
                    )

class transfer_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_tag   = self.get_argument("transfer_tag")
        v_list   = query_transfer(transfer_tag)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class transfer_query_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_id   = self.get_argument("transfer_id")
        print('transfer_id=',transfer_id)
        v_list    = query_transfer_detail(transfer_id)
        v_json    = json.dumps(v_list)
        self.write({"code": 0, "message": v_json})


class transferadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_add.html",
                    sync_server=get_sync_server(),
                    db_server=get_sync_db_server(),
                    dm_transfer_type=get_dmm_from_dm('09'),
                    )

class transferadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_transfer = {}
        d_transfer['transfer_tag']         = self.get_argument("transfer_tag")
        d_transfer['task_desc']            = self.get_argument("task_desc")
        d_transfer['transfer_server']      = self.get_argument("transfer_server")
        d_transfer['transfer_type']        = self.get_argument("transfer_type")
        d_transfer['sour_db_server']       = self.get_argument("sour_db_server")
        d_transfer['sour_db_name']         = self.get_argument("sour_db_name")
        d_transfer['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_transfer['sour_tab_where']       = self.get_argument("sour_tab_where")
        d_transfer['dest_db_server']       = self.get_argument("dest_db_server")
        d_transfer['dest_db_name']         = self.get_argument("dest_db_name")
        d_transfer['python3_home']         = self.get_argument("python3_home")
        d_transfer['script_base']          = self.get_argument("script_base")
        d_transfer['script_name']          = self.get_argument("script_name")
        d_transfer['batch_size']           = self.get_argument("batch_size")
        d_transfer['api_server']           = self.get_argument("api_server")
        d_transfer['status']               = self.get_argument("status")
        result=save_transfer(d_transfer)
        self.write({"code": result['code'], "message": result['message']})

class transferchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_change.html")

class transferedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        transfer_id   = self.get_argument("transferid")
        d_transfer    = get_transfer_by_transferid(transfer_id)
        self.render("./transfer_edit.html",
                    transfer_server      = get_sync_server(),
                    dm_transfer_type     = get_dmm_from_dm('09'),
                    db_server            = get_sync_db_server(),
                    transfer_id          = transfer_id,
                    transfer_tag         = d_transfer['transfer_tag'],
                    transfer_db_type     = d_transfer['transfer_type'],
                    task_desc            = d_transfer['task_desc'],
                    server_id            = d_transfer['server_id'],
                    sour_db_id           = d_transfer['sour_db_id'],
                    sour_schema          = d_transfer['sour_schema'],
                    sour_table           = d_transfer['sour_table'],
                    sour_where           = d_transfer['sour_where'],
                    dest_db_id           = d_transfer['dest_db_id'],
                    dest_schema          = d_transfer['dest_schema'],
                    script_path          = d_transfer['script_path'],
                    script_name          = d_transfer['script_file'],
                    python3_home         = d_transfer['python3_home'],
                    batch_size           = d_transfer['batch_size'],
                    api_server           = d_transfer['api_server'],
                    status               = d_transfer['status'],
                    )

class transferedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_transfer = {}
        d_transfer['transfer_id']     = self.get_argument("transfer_id")
        d_transfer['transfer_tag']    = self.get_argument("transfer_tag")
        d_transfer['task_desc']       = self.get_argument("task_desc")
        d_transfer['transfer_server'] = self.get_argument("transfer_server")
        d_transfer['transfer_type']   = self.get_argument("transfer_type")
        d_transfer['sour_db_server']  = self.get_argument("sour_db_server")
        d_transfer['sour_db_name']    = self.get_argument("sour_db_name")
        d_transfer['sour_tab_name']   = self.get_argument("sour_tab_name")
        d_transfer['sour_tab_where']  = self.get_argument("sour_tab_where")
        d_transfer['dest_db_server']  = self.get_argument("dest_db_server")
        d_transfer['dest_db_name']    = self.get_argument("dest_db_name")
        d_transfer['python3_home']    = self.get_argument("python3_home")
        d_transfer['script_base']     = self.get_argument("script_base")
        d_transfer['script_name']     = self.get_argument("script_name")
        d_transfer['batch_size']      = self.get_argument("batch_size")
        d_transfer['api_server']      = self.get_argument("api_server")
        d_transfer['status']          = self.get_argument("status")
        result=upd_transfer(d_transfer)
        self.write({"code": result['code'], "message": result['message']})

class transferedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_id  = self.get_argument("transferid")
        result=del_transfer(transfer_id)
        self.write({"code": result['code'], "message": result['message']})

class transferlogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_log_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_sync_ywlx=get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class transfer_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag    = self.get_argument("sync_tag")
        market_id   = self.get_argument("market_id")
        sync_ywlx   = self.get_argument("sync_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = query_transfer_log(sync_tag,market_id,sync_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class transferedit_push(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_transfer_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class transferedit_run(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_transfer_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class transferedit_stop(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_transfer_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class transferclone(basehandler):
    @tornado.web.authenticated
    def get(self):
        transfer_id   = self.get_argument("transfer_id")
        d_transfer    = get_transfer_by_transferid(transfer_id)
        self.render("./transfer_clone.html",
                    transfer_server   = get_sync_server(),
                    dm_transfer_type  = get_dmm_from_dm('09'),
                    db_server         = get_sync_db_server(),
                    transfer_id       = transfer_id,
                    transfer_tag      = d_transfer['transfer_tag'].split('_v')[0]+'_v'+str(int(d_transfer['transfer_tag'].split('_v')[1])+1),
                    transfer_db_type  = d_transfer['transfer_type'],
                    task_desc         = d_transfer['task_desc'].split('_v')[0]+'_v'+str(int(d_transfer['task_desc'].split('_v')[1])+1),
                    server_id         = d_transfer['server_id'],
                    sour_db_id        = d_transfer['sour_db_id'],
                    sour_schema       = d_transfer['sour_schema'],
                    sour_table        = d_transfer['sour_table'],
                    sour_where        = d_transfer['sour_where'],
                    dest_db_id        = d_transfer['dest_db_id'],
                    dest_schema       = d_transfer['dest_schema'],
                    script_path       = d_transfer['script_path'],
                    script_name       = d_transfer['script_file'],
                    python3_home      = d_transfer['python3_home'],
                    batch_size        = d_transfer['batch_size'],
                    api_server        = d_transfer['api_server'],
                    status            = d_transfer['status'],

        )

class transferclone_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_transfer = {}
        d_transfer['transfer_tag']    = self.get_argument("transfer_tag")
        d_transfer['task_desc']       = self.get_argument("task_desc")
        d_transfer['transfer_server'] = self.get_argument("transfer_server")
        d_transfer['transfer_type']   = self.get_argument("transfer_type")
        d_transfer['sour_db_server']  = self.get_argument("sour_db_server")
        d_transfer['sour_db_name']    = self.get_argument("sour_db_name")
        d_transfer['sour_tab_name']   = self.get_argument("sour_tab_name")
        d_transfer['sour_tab_where']  = self.get_argument("sour_tab_where")
        d_transfer['dest_db_server']  = self.get_argument("dest_db_server")
        d_transfer['dest_db_name']    = self.get_argument("dest_db_name")
        d_transfer['python3_home']    = self.get_argument("python3_home")
        d_transfer['script_base']     = self.get_argument("script_base")
        d_transfer['script_name']     = self.get_argument("script_name")
        d_transfer['batch_size']      = self.get_argument("batch_size")
        d_transfer['api_server']      = self.get_argument("api_server")
        d_transfer['status']          = self.get_argument("status")
        result = save_transfer(d_transfer)
        self.write({"code": result['code'], "message": result['message']})

class transferlogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./transfer_log_query.html",
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class transfer_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        transfer_tag    = self.get_argument("transfer_tag")
        begin_date      = self.get_argument("begin_date")
        end_date        = self.get_argument("end_date")
        task_status     = self.get_argument("task_status")
        v_list          = query_transfer_log(transfer_tag,begin_date,end_date,task_status)
        v_json          = json.dumps(v_list)
        self.write(v_json)