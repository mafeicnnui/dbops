#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   大数据管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_sync_datax import query_datax_sync,save_datax_sync,query_datax_by_id,upd_datax_sync,del_datax_sync,query_datax_sync_log
from   web.model.t_sync_datax import query_datax_sync_detail,query_datax_sync_dataxTemplete,downloads_datax_sync_dataxTemplete,get_datax_sync_tags_by_env
from   web.model.t_sync_datax import push_datax_sync_task,pushall_datax_sync_task,run_datax_sync_task,stop_datax_sync_task,update_datax_sync_status
from   web.model.t_sync_datax import query_datax_sync_log_analyze,query_datax_sync_log_detail,query_sync_log_analyze
from   web.model.t_sync_datax import query_datax_sync_es_dataxTemplete
from   web.model.t_dmmx       import get_dmm_from_dm,get_dmm_from_dm2,get_sync_server,get_datax_sync_db_server,get_db_sync_tags,get_db_sync_tags_by_market_id,get_db_sync_ywlx_by_market_id,get_datax_sync_tags
from   web.utils.common       import current_rq2,get_day_nday_ago,now
from   web.utils.basehandler  import basehandler

class syncbigdataquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_bigdata_query.html",
                    dm_sync_ywlx = get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm('09'),
                    )

class sync_bigdata_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag   = self.get_argument("sync_tag")
        sync_ywlx  = self.get_argument("sync_ywlx")
        sync_type  = self.get_argument("sync_type")
        sync_env   = self.get_argument("sync_env")
        v_list     = query_datax_sync(sync_tag,sync_ywlx,sync_type,sync_env)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class sync_bigdata_query_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_id   = self.get_argument("sync_id")
        v_list    = query_datax_sync_detail(sync_id)
        v_json    = json.dumps(v_list)
        self.write({"code": 0, "message": v_json})

class sync_bigdata_query_dataxTemplete(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_id  = self.get_argument("sync_id")
        templete = query_datax_sync_dataxTemplete(sync_id)
        self.write({"code": 0, "message": templete})

class sync_bigdata_downloads_dataxTemplete(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_id     = self.get_argument("sync_id")
        static_path = self.get_template_path().replace("templates", "static")
        zipfile     = downloads_datax_sync_dataxTemplete(sync_id,static_path)
        self.write({"code": 0, "message": zipfile})


class sync_bigdata_query_es_dataxTemplete(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_id  = self.get_argument("sync_id")
        templete = query_datax_sync_es_dataxTemplete(sync_id)
        self.write({"code": 0, "message": templete})

class sync_bigdata_downloads_es_dataxTemplete(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_id     = self.get_argument("sync_id")
        static_path = self.get_template_path().replace("templates", "static")
        zipfile     = downloads_datax_sync_dataxTemplete(sync_id,static_path)
        self.write({"code": 0, "message": zipfile})

class syncadd_bigdata(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_bigdata_add.html",
                    sync_server       = get_sync_server(),
                    db_server         = get_datax_sync_db_server(),
                    dm_db_type        = get_dmm_from_dm('02'),
                    dm_sync_ywlx      = get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm2('09','5,6'),
                    dm_sync_time_type = get_dmm_from_dm('10'),
                    dm_sync_zk_host   = get_dmm_from_dm('15'),
                    dm_sync_hbase_thrift = get_dmm_from_dm('16')
                    )

class syncadd_bigdata_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_sync = {}
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['sour_db_name']         = self.get_argument("sour_db_name")
        d_sync['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_sync['sour_tab_cols']        = self.get_argument("sour_tab_cols")
        d_sync['sour_incr_col']        = self.get_argument("sour_incr_col")
        d_sync['zk_hosts']             = self.get_argument("zk_hosts")
        d_sync['hbase_thrift']         = self.get_argument("hbase_thrift")
        d_sync['sync_hbase_table']     = self.get_argument("sync_hbase_table")
        d_sync['sync_hbase_rowkey']    = self.get_argument("sync_hbase_rowkey")
        d_sync['sync_hbase_rowkey_separator'] = self.get_argument("sync_hbase_rowkey_separator")
        d_sync['es_service']           = self.get_argument("es_service")
        d_sync['es_index_name']        = self.get_argument("es_index_name")
        d_sync['es_type_name']         = self.get_argument("es_type_name")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['datax_home']           = self.get_argument("datax_home")
        d_sync['sync_time_type']       = self.get_argument("sync_time_type")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        result=save_datax_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncchange_bigdata(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_bigdata_change.html" ,
                    dm_proj_type = get_dmm_from_dm('05'),
                    dm_sync_ywlx = get_dmm_from_dm('08'),
                    dm_sync_data_type = get_dmm_from_dm('09'),

                    )

class syncedit_bigdata(basehandler):
    @tornado.web.authenticated
    def get(self):
        sync_id   = self.get_argument("sync_id")
        d_sync    = query_datax_by_id(sync_id)
        self.render("./sync_bigdata_edit.html",
                    sync_id              = sync_id,
                    sync_server          = get_sync_server(),
                    db_server            = get_datax_sync_db_server(),
                    dm_db_type           = get_dmm_from_dm('02'),
                    dm_sync_ywlx         = get_dmm_from_dm('08'),
                    dm_sync_data_type    = get_dmm_from_dm('09'),
                    dm_sync_time_type    = get_dmm_from_dm('10'),
                    dm_sync_zk_host      = get_dmm_from_dm('15'),
                    dm_sync_hbase_thrift = get_dmm_from_dm('16'),
                    sync_tag             = d_sync['sync_tag'],
                    server_id            = d_sync['server_id'],
                    sour_db_server       = d_sync['sour_db_id'],
                    sync_schema          = d_sync['sync_schema'],
                    sync_table           = d_sync['sync_table'],
                    sync_columns         = d_sync['sync_columns'],
                    sync_incr_col        = d_sync['sync_incr_col'],
                    zk_hosts             = d_sync['zk_hosts'],
                    hbase_thrift         = d_sync['hbase_thrift'],
                    es_service           = d_sync['es_service'],
                    es_index_name        = d_sync['es_index_name'],
                    es_type_name         = d_sync['es_type_name'],
                    sync_hbase_table     = d_sync['sync_hbase_table'],
                    sync_hbase_rowkey    = d_sync['sync_hbase_rowkey_sour'],
                    sync_hbase_rowkey_s  = d_sync['sync_hbase_rowkey_separator'],
                    sync_ywlx            = d_sync['sync_ywlx'],
                    sync_type            = d_sync['sync_type'],
                    script_path          = d_sync['script_path'],
                    run_time             = d_sync['run_time'],
                    comments             = d_sync['comments'],
                    datax_home           = d_sync['datax_home'],
                    sync_time_type       = d_sync['sync_time_type'],
                    sync_gap             = d_sync['sync_gap'],
                    api_server           = d_sync['api_server'],
                    status               = d_sync['status'],
                    python3_home         = d_sync['python3_home'],

        )

class syncedit_save_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['sour_db_name']         = self.get_argument("sour_db_name")
        d_sync['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_sync['sour_tab_cols']        = self.get_argument("sour_tab_cols")
        d_sync['sour_incr_col']        = self.get_argument("sour_incr_col")
        d_sync['zk_hosts']             = self.get_argument("zk_hosts")
        d_sync['hbase_thrift']         = self.get_argument("hbase_thrift")
        d_sync['sync_hbase_table']     = self.get_argument("sync_hbase_table")
        d_sync['sync_hbase_rowkey']    = self.get_argument("sync_hbase_rowkey")
        d_sync['sync_hbase_rowkey_separator'] = self.get_argument("sync_hbase_rowkey_separator")
        d_sync['es_service']           = self.get_argument("es_service")
        d_sync['es_index_name']        = self.get_argument("es_index_name")
        d_sync['es_type_name']         = self.get_argument("es_type_name")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['datax_home']           = self.get_argument("datax_home")
        d_sync['sync_time_type']       = self.get_argument("sync_time_type")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        d_sync['sync_id']              = self.get_argument("sync_id")
        d_sync['python3_home']         = self.get_argument("python3_home")
        result=upd_datax_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncclone_bigdata(basehandler):
    @tornado.web.authenticated
    def get(self):
        sync_id   = self.get_argument("sync_id")
        d_sync    = query_datax_by_id(sync_id)
        self.render("./sync_bigdata_clone.html",
                    sync_id              = sync_id,
                    sync_server          = get_sync_server(),
                    db_server            = get_datax_sync_db_server(),
                    dm_db_type           = get_dmm_from_dm('02'),
                    dm_sync_ywlx         = get_dmm_from_dm('08'),
                    dm_sync_data_type    = get_dmm_from_dm('09'),
                    dm_sync_time_type    = get_dmm_from_dm('10'),
                    dm_sync_zk_host      = get_dmm_from_dm('15'),
                    dm_sync_hbase_thrift = get_dmm_from_dm('16'),
                    sync_tag             = d_sync['sync_tag'].split('_v')[0]+'_v'+str(int(d_sync['sync_tag'].split('_v')[1])+1),
                    server_id            = d_sync['server_id'],
                    sour_db_server       = d_sync['sour_db_id'],
                    sync_schema          = d_sync['sync_schema'],
                    sync_table           = d_sync['sync_table'],
                    sync_columns         = d_sync['sync_columns'],
                    sync_incr_col        = d_sync['sync_incr_col'],
                    zk_hosts             = d_sync['zk_hosts'],
                    hbase_thrift         = d_sync['hbase_thrift'],
                    sync_hbase_table     = d_sync['sync_hbase_table'],
                    sync_hbase_rowkey    = d_sync['sync_hbase_rowkey_sour'],
                    sync_hbase_rowkey_s  = d_sync['sync_hbase_rowkey_separator'],
                    es_service           = d_sync['es_service'],
                    es_index_name        = d_sync['es_index_name'],
                    es_type_name         = d_sync['es_type_name'],
                    sync_ywlx            = d_sync['sync_ywlx'],
                    sync_type            = d_sync['sync_type'],
                    script_path          = d_sync['script_path'],
                    run_time             = d_sync['run_time'],
                    comments             = d_sync['comments'].split('_v')[0]+'_v'+str(int(d_sync['sync_tag'].split('_v')[1])+1),
                    datax_home           = d_sync['datax_home'],
                    sync_time_type       = d_sync['sync_time_type'],
                    sync_gap             = d_sync['sync_gap'],
                    api_server           = d_sync['api_server'],
                    status               = d_sync['status'],
                    python3_home         = d_sync['python3_home'],

        )

class syncclone_save_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['sour_db_name']         = self.get_argument("sour_db_name")
        d_sync['sour_tab_name']        = self.get_argument("sour_tab_name")
        d_sync['sour_tab_cols']        = self.get_argument("sour_tab_cols")
        d_sync['sour_incr_col']        = self.get_argument("sour_incr_col")
        d_sync['zk_hosts']             = self.get_argument("zk_hosts")
        d_sync['hbase_thrift']         = self.get_argument("hbase_thrift")
        d_sync['sync_hbase_table']     = self.get_argument("sync_hbase_table")
        d_sync['sync_hbase_rowkey']    = self.get_argument("sync_hbase_rowkey")
        d_sync['sync_hbase_rowkey_separator'] = self.get_argument("sync_hbase_rowkey_separator")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['datax_home']           = self.get_argument("datax_home")
        d_sync['sync_time_type']       = self.get_argument("sync_time_type")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        d_sync['sync_id']              = self.get_argument("sync_id")
        d_sync['python3_home']         = self.get_argument("python3_home")
        result=save_datax_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})


class syncedit_del_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        syncid  = self.get_argument("syncid")
        result=del_datax_sync(syncid)
        self.write({"code": result['code'], "message": result['message']})

class synclogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_log_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_sync_ywlx=get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class sync_log_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag    = self.get_argument("sync_tag")
        market_id   = self.get_argument("market_id")
        sync_ywlx   = self.get_argument("sync_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = query_datax_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class sync_log_query_detail(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        sync_rqq = self.get_argument("sync_rqq")
        sync_rqz = self.get_argument("sync_rqz")
        v_list=query_datax_sync_log_detail(sync_tag,sync_rqq,sync_rqz)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncloganalyze(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_log_analyze.html",
                      dm_proj_type = get_dmm_from_dm('05'),
                      db_sync_tags = get_db_sync_tags(),
                      begin_date=get_day_nday_ago(now(),0),
                      end_date=get_day_nday_ago(now(),0)
                    )

class sync_log_analyze(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2 = query_datax_sync_log_analyze(market_id,tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        self.write(v_json)

class get_sync_tasks(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id = self.get_argument("market_id")
        d_list  = {}
        v_list  = get_db_sync_tags_by_market_id(market_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        self.write(v_json)

class get_sync_ywlx(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id = self.get_argument("market_id")
        d_list  = {}
        v_list  = get_db_sync_ywlx_by_market_id(market_id)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        self.write(v_json)

class syncedit_push_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_datax_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_pushall_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tags    = self.get_argument("tags")
        v_list = pushall_datax_sync_task(tags)
        v_json = json.dumps(v_list)
        self.write(v_json)


class syncedit_run_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_datax_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_stop_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_datax_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_status(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = update_datax_sync_status()
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncloganalyze_bigdata(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./sync_bigdata_log_analyze.html",
                      db_sync_tags = get_datax_sync_tags(),
                      begin_date=get_day_nday_ago(now(),0),
                      end_date=get_day_nday_ago(now(),0)
                    )

class sync_log_analyze_bigdata(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_env   = self.get_argument("sync_env")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2 = query_sync_log_analyze(sync_env,tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        self.write(v_json)

class get_bigdata_sync_tasks(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_env = self.get_argument("sync_env")
        d_list  = {}
        v_list  = get_datax_sync_tags_by_env(sync_env)
        d_list['data'] = v_list
        v_json  = json.dumps(d_list)
        self.write(v_json)
