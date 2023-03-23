#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from web.model.t_sync import query_sync, query_sync_tab, query_sync_tab_cfg, save_sync, save_sync_tab, del_sync_tab, \
    get_sync_by_syncid, upd_sync, del_sync, query_sync_log, query_sync_log_detail, query_db_real_sync, \
    save_sync_clone_real
from   web.model.t_sync import push_sync_task,run_sync_task,stop_sync_task,query_sync_log_analyze,query_sync_log_analyze2,query_sync_case,query_sync_case_log,query_sync_tab_cfg_real
from   web.model.t_sync import query_sync_park,query_sync_park_real_time,query_sync_flow,query_sync_flow_real_time,query_sync_flow_device,query_sync_park_charge,query_sync_bi,get_sync_by_sync_tag
from   web.model.t_sync import get_mssql_tables_list,get_mysql_tables_list,get_mssql_columns_list,get_mysql_columns_list,get_mssql_incr_columns_list,get_mysql_incr_columns_list
from web.model.t_dmmx import get_dmm_from_dm, get_dmm_from_dm2, get_sync_server, get_sync_db_mysql_server, \
    get_datax_sync_db_server_doris, get_sync_db_server, get_db_sync_tags, get_db_sync_tags_by_market_id, \
    get_db_sync_ywlx, get_db_sync_ywlx_by_market_id, get_datax_real_sync_db_server
from   web.model.t_sync import query_db_active_num,query_db_slow_num,query_sys_stats_num,query_sys_stats_idx,query_db_order_num,save_sync_real,get_mysql_databases_list,query_sync_tab_real
from   web.model.t_sync import upd_sync_real,get_ck_databases_list
from   web.utils.common import current_rq2,get_day_nday_ago,now,DateEncoder
from   web.utils import base_handler

class syncquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_query.html",
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_sync_ywlx = await get_dmm_from_dm('08'),
                    dm_sync_data_type = await get_dmm_from_dm('09'),
                    )

class sync_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag    = self.get_argument("sync_tag")
        market_id   = self.get_argument("market_id")
        sync_ywlx   = self.get_argument("sync_ywlx")
        sync_type   = self.get_argument("sync_type")
        task_status = self.get_argument("task_status")
        v_list      = await query_sync(sync_tag,market_id,sync_ywlx,sync_type,task_status)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class sync_query_tab(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        sync_tab = self.get_argument("sync_tab")
        v_list   = await query_sync_tab(sync_tag,sync_tab)
        v_json   = json.dumps(v_list)
        self.write(v_json)


class sync_query_tab_real(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        sync_tab = self.get_argument("sync_tab")
        v_list   = await query_sync_tab_real(sync_tag, sync_tab)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sync_query_sync_tabs(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "html/text; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        v_result = await query_sync_tab_cfg(sync_tag)
        self.write(v_result)

class sync_query_sync_tabs_real(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "html/text; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        v_result = await query_sync_tab_cfg_real(sync_tag)
        self.write(v_result)

class syncadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_add.html",
                    sync_server       = await get_sync_server(),
                    db_server         = await get_sync_db_server(),
                    dm_db_type        = await get_dmm_from_dm('02'),
                    dm_sync_ywlx      = await get_dmm_from_dm('08'),
                    dm_sync_data_type = await get_dmm_from_dm2('09','1,2,3,4'),
                    dm_sync_time_type = await get_dmm_from_dm('10')
                    )

class syncadd_save(base_handler.TokenHandler):
    async def post(self):
        d_sync = {}
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['desc_db_server']       = self.get_argument("desc_db_server")
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['script_name']          = self.get_argument("script_name")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['sync_schema']          = self.get_argument("sync_schema")
        d_sync['sync_schema_dest']     = self.get_argument("sync_schema_dest")
        d_sync['sync_tables']          = self.get_argument("sync_tables")
        d_sync['sync_batch_size']      = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['sync_col_name']        = self.get_argument("sync_col_name")
        d_sync['sync_col_val']         = self.get_argument("sync_col_val")
        d_sync['sync_time_type']       = self.get_argument("sync_time_type")
        d_sync['sync_repair_day']      = self.get_argument("sync_repair_day")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        result = await save_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})


class syncadd_save_tab(base_handler.TokenHandler):
    async def post(self):
        d_sync = {}
        d_sync['sync_id']           = self.get_argument("sync_id")
        d_sync['sync_tag']          = self.get_argument("sync_tag")
        d_sync['db_name']           = self.get_argument("db_name")
        d_sync['schema_name']       = self.get_argument("schema_name")
        d_sync['tab_name']          = self.get_argument("tab_name")
        d_sync['sync_cols']         = self.get_argument("sync_cols")
        d_sync['sync_incr_col']     = self.get_argument("sync_incr_col")
        d_sync['sync_time']         = self.get_argument("sync_time")
        d_sync['tab_status']        = self.get_argument("tab_status")
        result = await save_sync_tab(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncadd_del_tab(base_handler.TokenHandler):
    async def post(self):
        sync_id = self.get_argument("sync_id")
        result = await del_sync_tab(sync_id)
        self.write({"code": result['code'], "message": result['message']})

class syncchange(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_change.html" ,
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_sync_ywlx = await get_dmm_from_dm('08'),
                    dm_sync_data_type = await get_dmm_from_dm('09'),)

class syncedit(base_handler.TokenHandler):
    async def get(self):
        sync_id   = self.get_argument("sync_id")
        print('sync_id=',sync_id)
        d_sync    = await get_sync_by_syncid(sync_id)
        if d_sync['sync_ywlx']  == '21':
            self.render("./sync/sync_edit_real.html",
                        sync_id                  =  sync_id,
                        sync_server              =  await get_sync_server(),
                        db_server                =  await get_sync_db_server(),
                        db_server_doris          =  await get_datax_real_sync_db_server(),
                        dm_db_type               =  await get_dmm_from_dm('02'),
                        dm_sync_ywlx             =  await get_dmm_from_dm('08'),
                        dm_sync_data_type        =  await get_dmm_from_dm('09'),
                        dm_sync_time_type        =  await get_dmm_from_dm('10'),
                        dm_real_sync_status      =  await get_dmm_from_dm('47'),
                        server_id                =  d_sync['server_id'],
                        sour_db_server           =  d_sync['sour_db_server'],
                        desc_db_server           =  d_sync['desc_db_server'],
                        sour_db_log_server       =  d_sync['log_db_id'],
                        log_db_name              =  d_sync['log_db_name'],
                        sync_tag                 =  d_sync['sync_tag'],
                        sync_ywlx                =  d_sync['sync_ywlx'],
                        sync_data_type           =  d_sync['sync_data_type'],
                        script_base              =  d_sync['script_base'],
                        script_name              =  d_sync['script_name'],
                        run_time                 =  d_sync['run_time'],
                        task_desc                =  d_sync['task_desc'],
                        python3_home             =  d_sync['python3_home'],
                        sync_schema              =  d_sync['sync_schema'],
                        sync_schema_dest         =  d_sync['sync_schema_dest'],
                        sync_tables              =  d_sync['sync_tables'],
                        sync_batch_size          =  d_sync['sync_batch_size'],
                        sync_batch_size_incr     =  d_sync['sync_batch_size_incr'],
                        sync_gap                 =  d_sync['sync_gap'],
                        process_num              =  d_sync['process_num'],
                        apply_timeout            =  d_sync['apply_timeout'],
                        api_server               =  d_sync['api_server'],
                        status                   =  d_sync['status'],
                        desc_db_prefix           =  d_sync['desc_db_prefix'],
                        ch_cluster_name          =  d_sync['ch_cluster_name'],
                        real_sync_status         =  d_sync['real_sync_status'],
                    )
        else:
            self.render("./sync/sync_edit.html",
                        sync_id              = sync_id,
                        sync_server          = await get_sync_server(),
                        db_server            = await get_sync_db_server(),
                        dm_db_type           = await get_dmm_from_dm('02'),
                        dm_sync_ywlx         = await get_dmm_from_dm('08'),
                        dm_sync_data_type    = await get_dmm_from_dm('09'),
                        dm_sync_time_type    = await get_dmm_from_dm('10'),
                        server_id            = d_sync['server_id'],
                        sour_db_server       = d_sync['sour_db_server'],
                        desc_db_server       = d_sync['desc_db_server'],
                        sync_tag             = d_sync['sync_tag'],
                        sync_ywlx            = d_sync['sync_ywlx'],
                        sync_data_type       = d_sync['sync_data_type'],
                        script_base          = d_sync['script_base'],
                        script_name          = d_sync['script_name'],
                        run_time             = d_sync['run_time'],
                        task_desc            = d_sync['task_desc'],
                        python3_home         = d_sync['python3_home'],
                        sync_schema          = d_sync['sync_schema'],
                        sync_schema_dest     = d_sync['sync_schema_dest'],
                        sync_tables          = d_sync['sync_tables'],
                        sync_batch_size      = d_sync['sync_batch_size'],
                        sync_batch_size_incr = d_sync['sync_batch_size_incr'],
                        sync_gap             = d_sync['sync_gap'],
                        sync_col_name        = d_sync['sync_col_name'],
                        sync_col_val         = d_sync['sync_col_val'],
                        sync_time_type       = d_sync['sync_time_type'],
                        sync_repair_day       = d_sync['sync_repair_day'],
                        api_server           = d_sync['api_server'],
                        status               = d_sync['status'],
                        )

class syncedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_server']        = self.get_argument("sync_server")
        d_sync['sour_db_server']     = self.get_argument("sour_db_server")
        d_sync['desc_db_server']     = self.get_argument("desc_db_server")
        d_sync['sync_tag']           = self.get_argument("sync_tag")
        d_sync['sync_ywlx']          = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']     = self.get_argument("sync_data_type")
        d_sync['script_base']        = self.get_argument("script_base")
        d_sync['script_name']        = self.get_argument("script_name")
        d_sync['run_time']           = self.get_argument("run_time")
        d_sync['task_desc']          = self.get_argument("task_desc")
        d_sync['python3_home']       = self.get_argument("python3_home")
        d_sync['sync_schema']        = self.get_argument("sync_schema")
        d_sync['sync_schema_dest']   = self.get_argument("sync_schema_dest")
        d_sync['sync_tables']        = self.get_argument("sync_tables")
        d_sync['sync_batch_size']    = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']           = self.get_argument("sync_gap")
        d_sync['sync_col_name']      = self.get_argument("sync_col_name")
        d_sync['sync_col_val']       = self.get_argument("sync_col_val")
        d_sync['sync_time_type']     = self.get_argument("sync_time_type")
        d_sync['sync_repair_day']    = self.get_argument("sync_repair_day")
        d_sync['api_server']         = self.get_argument("api_server")
        d_sync['status']             = self.get_argument("status")
        d_sync['sync_id']            = self.get_argument("sync_id")
        result = await upd_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncclone(base_handler.TokenHandler):
    async def get(self):
        sync_id = self.get_argument("sync_id")
        d_sync  = await get_sync_by_syncid(sync_id)
        if d_sync['sync_ywlx']  == '21' :
            self.render("./sync/sync_clone_real.html",
                        sync_id              =  sync_id,
                        sync_server          = await get_sync_server(),
                        db_server            = await get_sync_db_server(),
                        db_server_doris      = await get_datax_real_sync_db_server(),
                        dm_db_type           = await get_dmm_from_dm('02'),
                        dm_sync_ywlx         = await get_dmm_from_dm('08'),
                        dm_sync_data_type    = await get_dmm_from_dm('09'),
                        dm_sync_time_type    = await get_dmm_from_dm('10'),
                        dm_real_sync_status  = await get_dmm_from_dm('47'),
                        server_id            = d_sync['server_id'],
                        sour_db_server       = d_sync['sour_db_server'],
                        desc_db_server       = d_sync['desc_db_server'],
                        sour_db_log_server   = d_sync['log_db_id'],
                        log_db_name          = d_sync['log_db_name'],
                        sync_tag             = d_sync['sync_tag']+'_clone',
                        sync_ywlx            = d_sync['sync_ywlx'],
                        sync_data_type       = d_sync['sync_data_type'],
                        script_base          = d_sync['script_base'],
                        script_name          = d_sync['script_name'],
                        run_time             = d_sync['run_time'],
                        task_desc            = d_sync['task_desc'],
                        python3_home         = d_sync['python3_home'],
                        sync_schema          = d_sync['sync_schema'],
                        sync_schema_dest     = d_sync['sync_schema_dest'],
                        sync_tables          = d_sync['sync_tables'],
                        sync_batch_size      = d_sync['sync_batch_size'],
                        sync_batch_size_incr = d_sync['sync_batch_size_incr'],
                        sync_gap             = d_sync['sync_gap'],
                        apply_timeout        = d_sync['apply_timeout'],
                        api_server           = d_sync['api_server'],
                        status               = d_sync['status'],
                        desc_db_prefix       = d_sync['desc_db_prefix'],
                        process_num          = d_sync['process_num'],
                        ch_cluster_name      = d_sync['ch_cluster_name'],
                        real_sync_status     = d_sync['real_sync_status'],
                        )
        else:
            self.render("./sync/sync_clone.html",
                        sync_server          = await get_sync_server(),
                        db_server            = await get_sync_db_server(),
                        dm_db_type           = await get_dmm_from_dm('02'),
                        dm_sync_ywlx         = await get_dmm_from_dm('08'),
                        dm_sync_data_type    = await get_dmm_from_dm('09'),
                        dm_sync_time_type    = await get_dmm_from_dm('10'),
                        server_id            = d_sync['server_id'],
                        sour_db_server       = d_sync['sour_db_server'],
                        desc_db_server       = d_sync['desc_db_server'],
                        sync_tag             = d_sync['sync_tag']+'_clone',
                        sync_ywlx            = d_sync['sync_ywlx'],
                        sync_data_type       = d_sync['sync_data_type'],
                        script_base          = d_sync['script_base'],
                        script_name          = d_sync['script_name'],
                        run_time             = d_sync['run_time'],
                        task_desc            = d_sync['task_desc']+'_clone',
                        python3_home         = d_sync['python3_home'],
                        sync_schema          = d_sync['sync_schema'],
                        sync_schema_dest     = d_sync['sync_schema_dest'],
                        sync_tables          = d_sync['sync_tables'],
                        sync_batch_size      = d_sync['sync_batch_size'],
                        sync_batch_size_incr = d_sync['sync_batch_size_incr'],
                        sync_gap             = d_sync['sync_gap'],
                        sync_col_name        = d_sync['sync_col_name'],
                        sync_col_val         = d_sync['sync_col_val'],
                        sync_time_type       = d_sync['sync_time_type'],
                        sync_repair_day      = d_sync['sync_repair_day'],
                        api_server           = d_sync['api_server'],
                        status               = d_sync['status'],
                        )

class syncclone_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_server']     = self.get_argument("sync_server")
        d_sync['sour_db_server']  = self.get_argument("sour_db_server")
        d_sync['desc_db_server']  = self.get_argument("desc_db_server")
        d_sync['sync_tag']        = self.get_argument("sync_tag")
        d_sync['sync_ywlx']       = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']  = self.get_argument("sync_data_type")
        d_sync['script_base']     = self.get_argument("script_base")
        d_sync['script_name']     = self.get_argument("script_name")
        d_sync['run_time']        = self.get_argument("run_time")
        d_sync['task_desc']       = self.get_argument("task_desc")
        d_sync['python3_home']    = self.get_argument("python3_home")
        d_sync['sync_schema']     = self.get_argument("sync_schema")
        d_sync['sync_schema_dest'] = self.get_argument("sync_schema_dest")
        d_sync['sync_tables']     = self.get_argument("sync_tables")
        d_sync['sync_batch_size'] = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']       = self.get_argument("sync_gap")
        d_sync['sync_col_name']  = self.get_argument("sync_col_name")
        d_sync['sync_col_val']   = self.get_argument("sync_col_val")
        d_sync['sync_time_type'] = self.get_argument("sync_time_type")
        d_sync['sync_repair_day'] = self.get_argument("sync_repair_day")
        d_sync['api_server']     = self.get_argument("api_server")
        d_sync['status']         = self.get_argument("status")
        result = await save_sync(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class syncedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        syncid  = self.get_argument("syncid")
        result  = await del_sync(syncid)
        self.write({"code": result['code'], "message": result['message']})

class synclogquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_log_query.html",
                    dm_proj_type= await get_dmm_from_dm('05'),
                    dm_sync_ywlx= await get_dmm_from_dm('08'),
                    begin_date=current_rq2(),
                    end_date=current_rq2()
                    )

class sync_log_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag    = self.get_argument("sync_tag")
        market_id   = self.get_argument("market_id")
        sync_ywlx   = self.get_argument("sync_ywlx")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = await query_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class sync_log_query_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        sync_rqq = self.get_argument("sync_rqq")
        sync_rqz = self.get_argument("sync_rqz")
        v_list   = await query_sync_log_detail(sync_tag,sync_rqq,sync_rqz)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncloganalyze(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_log_analyze.html",
                      dm_proj_type = await get_dmm_from_dm('05'),
                      db_sync_tags = await get_db_sync_tags(),
                      begin_date   = get_day_nday_ago(now(),0),
                      end_date     = get_day_nday_ago(now(),0)
                    )

class sync_log_analyze(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        tagname    = self.get_argument("tagname")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2,v_list3 = await query_sync_log_analyze(market_id,tagname,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        d_list['data3'] = v_list3
        v_json = json.dumps(d_list)
        self.write(v_json)

class syncloganalyze2(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_log_analyze2.html",
                      dm_proj_type = await get_dmm_from_dm('05'),
                      db_sync_ywlx = await get_db_sync_ywlx(),
                      begin_date   = get_day_nday_ago(now(),0),
                      end_date     = get_day_nday_ago(now(),0)
                    )

class sync_log_analyze2(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        sync_type  = self.get_argument("sync_type")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        d_list     = {}
        v_list1,v_list2 = await query_sync_log_analyze2(market_id,sync_type,begin_date,end_date)
        d_list['data1'] = v_list1
        d_list['data2'] = v_list2
        v_json = json.dumps(d_list)
        self.write(v_json)

class get_sync_tasks(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id = self.get_argument("market_id")
        d_list  = {}
        v_list  = await get_db_sync_tags_by_market_id(market_id)
        d_list['data'] = v_list
        v_json = json.dumps(d_list)
        self.write(v_json)

class get_sync(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        v_list  = await get_sync_by_sync_tag(sync_tag)
        v_json  = json.dumps(v_list,cls=DateEncoder)
        self.write(v_json)

class syncedit_push(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = push_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_run(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = run_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class syncedit_stop(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag    = self.get_argument("tag")
        api    = self.get_argument("api")
        v_list = stop_sync_task(tag,api)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_sync_park(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_park()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_park_real_time(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_park_real_time()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_flow(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_flow()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_flow_real_time(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_flow_real_time()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_flow_device(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_flow_device()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_park_charge(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_park_charge()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_sync_bi(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sync_bi()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class sync_case(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list      = await query_sync_case()
        v_json      = json.dumps(v_list)
        self.write(v_json)

class sync_case_log(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        v_list      = await query_sync_case_log(sync_tag)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class db_active_num(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_id       = self.get_argument("db_id")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = await query_db_active_num(db_id,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class db_real_sync(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        max_id   = int(self.get_argument("max_id"))
        v_list   = await query_db_real_sync(sync_tag,max_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class db_order_num(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list      = await query_db_order_num()
        v_json      = json.dumps(v_list)
        self.write(v_json)

class db_slow_num(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id     = self.get_argument("inst_id")
        ds_id       = self.get_argument("ds_id")
        begin_date  = self.get_argument("begin_date")
        end_date    = self.get_argument("end_date")
        v_list      = await query_db_slow_num(inst_id,ds_id,begin_date,end_date)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class sys_stats_num(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        server_id  = self.get_argument("server_id")
        begin_date = self.get_argument("begin_date")
        end_date   = self.get_argument("end_date")
        v_list     = await query_sys_stats_num(server_id,begin_date,end_date)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class sys_stats_idx(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list     = await query_sys_stats_idx()
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_mssql_tables(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        proxy_server = self.get_argument("proxy_server")
        v_list = get_mssql_tables_list(db_ip,db_port,db_service,db_user,db_pass,proxy_server)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_mysql_tables(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        proxy_server = self.get_argument("proxy_server")
        v_list     = get_mysql_tables_list(db_ip, db_port, db_service, db_user, db_pass,proxy_server)
        v_json     = json.dumps(v_list)
        self.write(v_list)

class get_mysql_databases(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip = self.get_argument("db_ip")
        db_port = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user = self.get_argument("db_user")
        db_pass = self.get_argument("db_pass")
        proxy_server = self.get_argument("proxy_server")
        v_list = get_mysql_databases_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server)
        v_json = json.dumps(v_list)
        self.write(v_list)

class get_ck_databases(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip = self.get_argument("db_ip")
        db_port = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user = self.get_argument("db_user")
        db_pass = self.get_argument("db_pass")
        proxy_server = self.get_argument("proxy_server")
        v_list = get_ck_databases_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server)
        v_json = json.dumps(v_list)
        self.write(v_list)

class get_mssql_columns(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        db_tab     = self.get_argument("db_tab")
        proxy_server = self.get_argument("proxy_server")
        v_list = get_mssql_columns_list(db_ip,db_port,db_service,db_user,db_pass,db_tab,proxy_server)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_mysql_columns(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        db_tab     = self.get_argument("db_tab")
        proxy_server = self.get_argument("proxy_server")
        v_list     = get_mysql_columns_list(db_ip, db_port, db_service, db_user, db_pass,db_tab,proxy_server)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class get_mssql_incr_columns(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        db_tab     = self.get_argument("db_tab")

        proxy_server = self.get_argument("proxy_server")
        v_list = get_mssql_incr_columns_list(db_ip,db_port,db_service,db_user,db_pass,db_tab,proxy_server)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_mysql_incr_columns(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_ip      = self.get_argument("db_ip")
        db_port    = self.get_argument("db_port")
        db_service = self.get_argument("db_service")
        db_user    = self.get_argument("db_user")
        db_pass    = self.get_argument("db_pass")
        db_tab     = self.get_argument("db_tab")
        proxy_server = self.get_argument("proxy_server")
        v_list     = get_mysql_incr_columns_list(db_ip, db_port, db_service, db_user, db_pass,db_tab,proxy_server)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class sync_real(base_handler.TokenHandler):
    async def get(self):
        self.render("./sync/sync_add_real.html",
                    sync_server       = await get_sync_server(),
                    db_mysql_server   = await get_sync_db_mysql_server(),
                    db_server_doris   = await get_datax_real_sync_db_server(),
                    db_server         = await get_sync_db_server(),
                    dm_db_type        = await get_dmm_from_dm('02'),
                    dm_sync_ywlx      = await get_dmm_from_dm('08'),
                    dm_sync_data_type = await get_dmm_from_dm2('09','2,7,8'),
                    dm_sync_time_type = await get_dmm_from_dm('10'),
                    dm_real_sync_status = await get_dmm_from_dm('47'),
                   )

class sync_real_save(base_handler.TokenHandler):
    async def post(self):
        d_sync = {}
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['desc_db_server']       = self.get_argument("desc_db_server")
        d_sync['sour_db_log_server']   = self.get_argument("sour_db_log_server")
        d_sync['log_db_name']          = self.get_argument("log_db_name")
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['script_name']          = self.get_argument("script_name")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['sync_tables']          = self.get_argument("sync_tables")
        d_sync['sync_batch_size']      = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['process_num']          = self.get_argument("process_num")
        d_sync['apply_timeout']        = self.get_argument("apply_timeout")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        d_sync['desc_db_prefix']       = self.get_argument("desc_db_prefix")
        d_sync['ch_cluster_name']      = self.get_argument("ch_cluster_name")
        d_sync['real_sync_status']     = self.get_argument("real_sync_status")
        result = await save_sync_real(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class sync_real_edit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['desc_db_server']       = self.get_argument("desc_db_server")
        d_sync['sour_db_log_server']   = self.get_argument("sour_db_log_server")
        d_sync['log_db_name']          = self.get_argument("log_db_name")
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['script_name']          = self.get_argument("script_name")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['sync_tables']          = self.get_argument("sync_tables")
        d_sync['sync_batch_size']      = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['process_num']          = self.get_argument("process_num")
        d_sync['apply_timeout']        = self.get_argument("apply_timeout")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        d_sync['sync_id']              = self.get_argument("sync_id")
        d_sync['desc_db_prefix']       = self.get_argument("desc_db_prefix")
        d_sync['ch_cluster_name']      = self.get_argument("ch_cluster_name")
        d_sync['real_sync_status']     = self.get_argument("real_sync_status")
        result = await upd_sync_real(d_sync)
        self.write({"code": result['code'], "message": result['message']})

class sync_real_clone_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_sync = {}
        d_sync['sync_server']          = self.get_argument("sync_server")
        d_sync['sour_db_server']       = self.get_argument("sour_db_server")
        d_sync['desc_db_server']       = self.get_argument("desc_db_server")
        d_sync['sour_db_log_server']   = self.get_argument("sour_db_log_server")
        d_sync['log_db_name']          = self.get_argument("log_db_name")
        d_sync['sync_tag']             = self.get_argument("sync_tag")
        d_sync['sync_ywlx']            = self.get_argument("sync_ywlx")
        d_sync['sync_data_type']       = self.get_argument("sync_data_type")
        d_sync['script_base']          = self.get_argument("script_base")
        d_sync['script_name']          = self.get_argument("script_name")
        d_sync['run_time']             = self.get_argument("run_time")
        d_sync['task_desc']            = self.get_argument("task_desc")
        d_sync['python3_home']         = self.get_argument("python3_home")
        d_sync['sync_tables']          = self.get_argument("sync_tables")
        d_sync['sync_batch_size']      = self.get_argument("sync_batch_size")
        d_sync['sync_batch_size_incr'] = self.get_argument("sync_batch_size_incr")
        d_sync['sync_gap']             = self.get_argument("sync_gap")
        d_sync['process_num']          = self.get_argument("process_num")
        d_sync['apply_timeout']        = self.get_argument("apply_timeout")
        d_sync['api_server']           = self.get_argument("api_server")
        d_sync['status']               = self.get_argument("status")
        d_sync['desc_db_prefix']       = self.get_argument("desc_db_prefix")
        d_sync['sync_id']              = self.get_argument("sync_id")
        d_sync['ch_cluster_name']      = self.get_argument("ch_cluster_name")
        d_sync['real_sync_status']     = self.get_argument("real_sync_status")
        result = await save_sync_clone_real(d_sync)
        self.write({"code": result['code'], "message": result['message']})