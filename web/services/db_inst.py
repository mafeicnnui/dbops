#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : 马飞
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst,save_db_inst,upd_db_inst,query_inst_by_id,get_dss_for_inst,get_ds_by_instid,get_tree_by_instid_mssql
from  web.model.t_db_inst     import get_tree_by_instid,exe_query,del_db_inst,get_tab_ddl_by_instid,get_idx_ddl_by_instid,drop_tab_by_instid
from  web.model.t_db_inst     import query_db_inst_para,save_db_inst_para,upd_db_inst_para,del_db_inst_para,query_db_inst_log
from  web.model.t_db_inst     import create_db_inst,destroy_db_inst,log_db_inst,manager_db_inst
from  web.model.t_dmmx        import get_dmm_from_dm,get_gather_server,get_sys_dmlx_from_dm

'''新增实例'''
class dbinstquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_mgr.html",
                    dm_inst_type=get_dmm_from_dm('02'),
                    dm_inst_env=get_dmm_from_dm('03'))

class db_inst_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_name  = self.get_argument("inst_name")
        v_list = query_inst(inst_name)
        v_json = json.dumps(v_list)
        self.write(v_json)

class db_inst_query_by_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_id  = self.get_argument("inst_id")
        v_list   = query_inst_by_id(inst_id)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class db_inst_save(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        result = save_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_update(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        result = upd_db_inst(d_inst)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_delete(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id   = self.get_argument("inst_id")
        print('db_inst_delete=',inst_id)
        result = del_db_inst(inst_id)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_create(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        result = create_db_inst(api_server,inst_id)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_destroy(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        result = destroy_db_inst(api_server,inst_id)
        self.write({"code": result['code'], "message": result['message']})

class db_inst_manager(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id    = self.get_argument("inst_id")
        api_server = self.get_argument("api_server")
        op_type    = self.get_argument("op_type")
        result = manager_db_inst(api_server,inst_id,op_type)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_log(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id = self.get_argument("inst_id")
        result = log_db_inst(inst_id)
        self.write({"code": result['code'], "message": result['message']})


'''实例管理'''
class dbinstmgr(basehandler):
    @tornado.web.authenticated
    def get(self):
        inst_id   = self.get_argument("inst_id")
        inst_type = self.get_argument("inst_type")
        self.render("./db_inst_console.html", dss=get_dss_for_inst(inst_id),inst_type=inst_type)


class get_tree_by_inst(basehandler):
    @tornado.web.authenticated
    def post(self):
        inst_id   = self.get_argument("inst_id")
        p_ds      = get_ds_by_instid(inst_id)
        result    = {}
        if p_ds['db_type'] == '0':
           result    = get_tree_by_instid(inst_id)
        elif p_ds['db_type'] == '2':
           result    = get_tree_by_instid_mssql(inst_id)
        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})



class get_inst_tab_ddl(basehandler):
    def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result = get_tab_ddl_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_inst_idx_ddl(basehandler):
    def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = get_idx_ddl_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})


class drop_inst_tab(basehandler):
    @tornado.web.authenticated
    def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result = drop_tab_by_instid(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})


class db_inst_sql_query(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
       inst_id= self.get_argument("inst_id")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       result = exe_query(userid,inst_id,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class dbinstcrtquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_create.html",
                    dm_inst_type = get_dmm_from_dm('02'),
                    dm_inst_env  = get_dmm_from_dm('03'),
                    dm_db_server = get_gather_server(),
                    dm_inst_ver  = get_dmm_from_dm('27'),
                    dm_inst_cfg  = get_sys_dmlx_from_dm('30'),
                    )

class db_inst_crt_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_name  = self.get_argument("inst_name")
        v_list = query_inst(inst_name)
        v_json = json.dumps(v_list)
        self.write(v_json)



'''参数管理'''
class dbinstparaquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_para.html",
                    index_types= get_dmm_from_dm('23'),
                    index_val_types=get_dmm_from_dm('24'),
                    index_db_types= get_dmm_from_dm('02'),
                    )

class dbinstpara_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        para_name   = self.get_argument("para_name")
        v_list       = query_db_inst_para(para_name)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class dbinstparaadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_para = {}
        d_para['para_name']           = self.get_argument("para_name")
        d_para['para_value']          = self.get_argument("para_value")
        d_para['para_desc']           = self.get_argument("para_desc")
        d_para['para_status']         = self.get_argument("para_status")
        result = save_db_inst_para(d_para)
        self.write({"code": result['code'], "message": result['message']})


class dbinstparaedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_para = {}
        d_para['para_id']             = self.get_argument("para_id")
        d_para['para_name']           = self.get_argument("para_name")
        d_para['para_value']          = self.get_argument("para_value")
        d_para['para_desc']           = self.get_argument("para_desc")
        d_para['para_status']         = self.get_argument("para_status")
        result=upd_db_inst_para(d_para)
        self.write({"code": result['code'], "message": result['message']})

class dbinstparaedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        para_name  = self.get_argument("para_name")
        result=del_db_inst_para(para_name)
        self.write({"code": result['code'], "message": result['message']})


'''操作日志'''
class dbinstoptlogquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_opt_log_query.html"
                    )

class dbinstoptlog_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        log_name   = self.get_argument("log_name")
        v_list       = query_db_inst_log(log_name)
        v_json       = json.dumps(v_list)
        self.write(v_json)