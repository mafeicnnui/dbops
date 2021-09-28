#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : ma.fei
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json

from web.utils import base_handler
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst,save_db_inst,upd_db_inst,query_inst_by_id,get_dss_for_inst,get_ds_by_instid,get_tree_by_instid_mssql
from  web.model.t_db_inst     import get_tree_by_instid,exe_query,del_db_inst,get_tab_ddl_by_instid,get_idx_ddl_by_instid,drop_tab_by_instid
from  web.model.t_db_inst     import query_db_inst_para,save_db_inst_para,upd_db_inst_para,del_db_inst_para,query_db_inst_log
from  web.model.t_db_inst     import create_db_inst,destroy_db_inst,log_db_inst,manager_db_inst,update_db_config,query_db_config
from  web.model.t_dmmx        import get_dmm_from_dm,get_gather_server,get_sys_dmlx_from_dm,get_slow_inst_names


'''新增实例'''
class dbinstquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./db/db_inst_mgr.html",
                    dm_inst_type = await get_dmm_from_dm('02'),
                    dm_inst_env = await get_dmm_from_dm('03'))

class db_inst_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_name  = self.get_argument("inst_name")
        v_list = await query_inst(inst_name)
        v_json = json.dumps(v_list)
        self.write(v_json)

class db_inst_query_by_id(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        v_list   = await query_inst_by_id(inst_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class db_inst_save(base_handler.TokenHandler):
    async def post(self):
        d_inst = {}
        d_inst['inst_name']         = self.get_argument("inst_name")
        d_inst['server_id']         = self.get_argument("server_id")
        d_inst['inst_ip']           = self.get_argument("inst_ip")
        d_inst['inst_port']         = self.get_argument("inst_port")
        d_inst['inst_ver']          = self.get_argument("inst_ver")
        d_inst['templete_id']       = self.get_argument("templete_id")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['inst_env']          = self.get_argument("inst_env")
        d_inst['is_rds']            = self.get_argument("is_rds")
        d_inst['mgr_user']          = self.get_argument("mgr_user")
        d_inst['mgr_pass']          = self.get_argument("mgr_pass")
        d_inst['api_server']        = self.get_argument("api_server")
        d_inst['python3_home']      = self.get_argument("python3_home")
        d_inst['script_path']       = self.get_argument("script_path")
        d_inst['script_file']       = self.get_argument("script_file")
        d_inst['inst_mapping_port'] = self.get_argument("inst_mapping_port")
        result = await save_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_update(base_handler.TokenHandler):
    async def post(self):
        d_inst = {}
        d_inst['inst_id']           = self.get_argument("inst_id")
        d_inst['inst_name']         = self.get_argument("inst_name")
        d_inst['server_id']         = self.get_argument("server_id")
        d_inst['inst_ip']           = self.get_argument("inst_ip")
        d_inst['inst_port']         = self.get_argument("inst_port")
        d_inst['inst_ver']          = self.get_argument("inst_ver")
        d_inst['templete_id']       = self.get_argument("templete_id")
        d_inst['inst_type']         = self.get_argument("inst_type")
        d_inst['inst_env']          = self.get_argument("inst_env")
        d_inst['is_rds']            = self.get_argument("is_rds")
        d_inst['mgr_user']          = self.get_argument("mgr_user")
        d_inst['mgr_pass']          = self.get_argument("mgr_pass")
        d_inst['api_server']        = self.get_argument("api_server")
        d_inst['python3_home']      = self.get_argument("python3_home")
        d_inst['script_path']       = self.get_argument("script_path")
        d_inst['script_file']       = self.get_argument("script_file")
        d_inst['inst_mapping_port'] = self.get_argument("inst_mapping_port")
        result = await upd_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_delete(base_handler.TokenHandler):
    async def post(self):
        inst_id  = self.get_argument("inst_id")
        result   = await del_db_inst(inst_id)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_create(base_handler.TokenHandler):
    async def post(self):
        inst_id = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        result = await create_db_inst(api_server,inst_id)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_destroy(base_handler.TokenHandler):
    async def post(self):
        inst_id = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        result = await destroy_db_inst(api_server,inst_id)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_manager(base_handler.TokenHandler):
    async def post(self):
        inst_id    = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        op_type    = self.get_argument("op_type")
        result     = await manager_db_inst(api_server,inst_id,op_type)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_log(base_handler.TokenHandler):
    async def post(self):
        inst_id = self.get_argument("inst_id")
        result = await log_db_inst(inst_id)
        self.write({"code": result['code'], "message": result['message']})


'''实例管理'''
class dbinstmgr(base_handler.TokenHandler):
    async def get(self):
        inst_id   = self.get_argument("inst_id")
        inst_type = self.get_argument("inst_type")
        dss = await get_dss_for_inst(inst_id)
        print('dss=',dss)
        self.render("./db/db_inst_console.html", dss = dss,inst_type=inst_type)


class get_tree_by_inst(base_handler.TokenHandler):
    async def post(self):
        inst_id   = self.get_argument("inst_id")
        msg        = self.get_argument("msg")
        p_ds      = await get_ds_by_instid(inst_id)
        result    = {}
        if p_ds['db_type'] == '0':
           result    = await get_tree_by_instid(inst_id,msg)
        elif p_ds['db_type'] == '2':
           result    = await get_tree_by_instid_mssql(inst_id)
        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})


class get_inst_tab_ddl(base_handler.TokenHandler):
   async def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result  = await get_tab_ddl_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_inst_idx_ddl(base_handler.TokenHandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = await get_idx_ddl_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})


class drop_inst_tab(base_handler.TokenHandler):
    async def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result  = await drop_tab_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_sql_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       inst_id= self.get_argument("inst_id")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       result = await exe_query(self.userid,inst_id,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class dbinstcrtquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./db/db_inst_create.html",
                    dm_inst_type = await get_dmm_from_dm('02'),
                    dm_inst_env  = await get_dmm_from_dm('03'),
                    dm_db_server = await get_gather_server(),
                    dm_inst_ver  = await get_dmm_from_dm('27'),
                    dm_inst_cfg  = await get_sys_dmlx_from_dm('30'),
                    )

class db_inst_crt_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_name  = self.get_argument("inst_name")
        v_list     = await query_inst(inst_name)
        v_json     = json.dumps(v_list)
        self.write(v_json)

'''参数管理'''
class dbinstparaquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./db/db_inst_para.html",
                    index_types = await get_dmm_from_dm('23'),
                    index_val_types = await get_dmm_from_dm('24'),
                    index_db_types   = await get_dmm_from_dm('02'))

class dbinstpara_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        para_name   = self.get_argument("para_name")
        v_list      = await query_db_inst_para(para_name)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class dbinstparaadd_save(base_handler.TokenHandler):
    async def post(self):
        d_para = {}
        d_para['para_name']           = self.get_argument("para_name")
        d_para['para_value']          = self.get_argument("para_value")
        d_para['para_desc']           = self.get_argument("para_desc")
        d_para['para_status']         = self.get_argument("para_status")
        result = await save_db_inst_para(d_para)
        self.write({"code": result['code'], "message": result['message']})


class dbinstparaedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_para = {}
        d_para['para_id']         = self.get_argument("para_id")
        d_para['para_name']       = self.get_argument("para_name")
        d_para['para_value']      = self.get_argument("para_value")
        d_para['para_desc']       = self.get_argument("para_desc")
        d_para['para_status']     = self.get_argument("para_status")
        result = await upd_db_inst_para(d_para)
        self.write({"code": result['code'], "message": result['message']})

class dbinstparaedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        para_name  = self.get_argument("para_name")
        result = await del_db_inst_para(para_name)
        self.write({"code": result['code'], "message": result['message']})


'''操作日志'''
class dbinstoptlogquery(base_handler.TokenHandler):
    def get(self):
        self.render("./db/db_inst_opt_log_query.html" )

class dbinstoptlog_query(basehandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        log_name     = self.get_argument("log_name")
        v_list       = await query_db_inst_log(log_name)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class dbinstcfgquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./db/db_inst_cfg_query.html",
                    dm_env_type     = await get_dmm_from_dm('03'),
                    dm_inst_names   = await get_slow_inst_names(''),
                 )

class db_inst_cfg_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_env   = self.get_argument("inst_env")
        inst_id    = self.get_argument("inst_id")
        v_list     = await query_db_config(inst_env,inst_id)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class db_inst_cfg_update(base_handler.TokenHandler):
    async def post(self):
        d_db_para = {}
        d_db_para['para_id']    = self.get_argument("para_id")
        d_db_para['para_name']  = self.get_argument("para_name")
        d_db_para['para_val']   = self.get_argument("para_val")
        result = await update_db_config(d_db_para)
        self.write({"code": result['code'], "message": result['message']})
