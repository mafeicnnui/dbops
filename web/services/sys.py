#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : 马飞
# @File : initialize.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   系统设置                                          #
#                                                                                    #
######################################################################################

import json
import tornado.web
from web.model.t_sys  import save_audit_rule,query_dm,query_rule,query_dm_detail,save_sys_code_type,upd_sys_code_type,del_sys_code
from web.model.t_sys  import save_sys_code_detail,upd_sys_code_detail,del_sys_code_detail
from web.model.t_dmmx import get_sys_dmlx
from web.utils.basehandler import basehandler


class audit_rule(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./audit_rule.html")

class audit_rule_save(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       rule={}
       #DDL规范参数
       rule['switch_check_ddl']               = self.get_argument("switch_check_ddl")
       rule['switch_tab_not_exists_pk']       = self.get_argument("switch_tab_not_exists_pk")
       rule['switch_tab_pk_id']               = self.get_argument("switch_tab_pk_id")
       rule['switch_tab_pk_auto_incr']        = self.get_argument("switch_tab_pk_auto_incr")

       rule['switch_tab_pk_autoincrement_1']  = self.get_argument("switch_tab_pk_autoincrement_1")
       rule['switch_pk_not_int_bigint']       = self.get_argument("switch_pk_not_int_bigint")
       rule['switch_tab_comment']             = self.get_argument("switch_tab_comment")
       rule['switch_col_comment']             = self.get_argument("switch_col_comment")

       rule['switch_col_not_null']            = self.get_argument("switch_col_not_null")
       rule['switch_col_default_value']       = self.get_argument("switch_col_default_value")
       rule['switch_tcol_default_value']      = self.get_argument("switch_tcol_default_value")
       rule['switch_char_max_len']            = self.get_argument("switch_char_max_len")

       rule['switch_tab_has_time_fields']     = self.get_argument("switch_tab_has_time_fields")
       rule['switch_tab_tcol_datetime']       = self.get_argument("switch_tab_tcol_datetime")
       rule['switch_tab_char_total_len']      = self.get_argument("switch_tab_char_total_len")
       rule['switch_tab_ddl_max_rows']        = self.get_argument("switch_tab_ddl_max_rows")

       rule['switch_tab_name_check']          = self.get_argument("switch_tab_name_check")
       rule['switch_idx_name_check']          = self.get_argument("switch_idx_name_check")
       rule['switch_ddl_batch']               = self.get_argument("switch_ddl_batch")
       rule['switch_ddl_timeout']             = self.get_argument("switch_ddl_timeout")

       rule['switch_disable_trigger']         = self.get_argument("switch_disable_trigger")
       rule['switch_disable_func']            = self.get_argument("switch_disable_func")
       rule['switch_disable_proc']            = self.get_argument("switch_disable_proc")
       rule['switch_disable_event']           = self.get_argument("switch_disable_event")

       rule['switch_drop_database']           = self.get_argument("switch_drop_database")
       rule['switch_drop_table']              = self.get_argument("switch_drop_table")
       rule['switch_virtual_col']             = self.get_argument("switch_virtual_col")
       rule['switch_tab_migrate']             = self.get_argument("switch_tab_migrate")

       rule['switch_col_order_rule']          = self.get_argument("switch_col_order_rule")
       rule['switch_col_charset']             = self.get_argument("switch_col_charset")
       rule['switch_tab_charset']             = self.get_argument("switch_tab_charset")
       rule['switch_tab_charset_range']       = self.get_argument("switch_tab_charset_range")

       #表名规范参数
       rule['switch_tab_not_digit_first']     = self.get_argument("switch_tab_not_digit_first")
       rule['switch_tab_two_digit_end']       = self.get_argument("switch_tab_two_digit_end")
       rule['switch_tab_max_len']             = self.get_argument("switch_tab_max_len")
       rule['switch_tab_disable_prefix']      = self.get_argument("switch_tab_disable_prefix")

       #索引规范参数
       rule['switch_idx_name_null']           = self.get_argument("switch_idx_name_null")
       rule['switch_idx_name_rule']           = self.get_argument("switch_idx_name_rule")
       rule['switch_idx_numbers']             = self.get_argument("switch_idx_numbers")
       rule['switch_idx_col_numbers']         = self.get_argument("switch_idx_col_numbers")
       rule['switch_idx_name_col']            = self.get_argument("switch_idx_name_col")

       #批量DML语句开关
       rule['switch_check_dml']              = self.get_argument("switch_check_dml")
       rule['switch_dml_batch']              = self.get_argument("switch_dml_batch")
       rule['switch_dml_where']              = self.get_argument("switch_dml_where")
       rule['switch_dml_order']              = self.get_argument("switch_dml_order")
       rule['switch_dml_select']             = self.get_argument("switch_dml_select")
       rule['switch_dml_max_rows']           = self.get_argument("switch_dml_max_rows")
       rule['switch_dml_ins_cols']           = self.get_argument("switch_dml_ins_cols")
       rule['switch_dml_ins_exists_col']     = self.get_argument("switch_dml_ins_exists_col")

       #查询开关
       rule['switch_query_rows']             = self.get_argument("switch_query_rows")
       rule['switch_timeout']                = self.get_argument("switch_timeout")
       rule['switch_sensitive_columns']      = self.get_argument("switch_sensitive_columns")

       print('audit_rule_save=',rule)
       result = save_audit_rule(rule)
       self.write({"code": result['code'], "message": result['message']})


class sys_setting(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sys_setting.html")

class sys_code(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./sys_code.html",
                   sys_code_type= get_sys_dmlx())

class sys_code_type(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.write({ "message": get_sys_dmlx()})


class sys_code_type_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code     = self.get_argument("code")
        v_list   = query_dm(code)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class sys_code_detail_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code     = self.get_argument("code")
        v_list   = query_dm_detail(code)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class sys_code_type_add_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_name']   = self.get_argument("type_name")
        code['type_code']   = self.get_argument("type_code")
        code['type_status'] = self.get_argument("type_status")
        result = save_sys_code_type(code)
        self.write({"code": result['code'], "message": result['message']})

class sys_code_type_upd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_name']   = self.get_argument("type_name")
        code['type_code']   = self.get_argument("type_code")
        code['type_status'] = self.get_argument("type_status")
        result = upd_sys_code_type(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_type_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code  = self.get_argument("type_code")
        result = del_sys_code(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_detail_add_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_code']     = self.get_argument("type_code")
        code['detail_name']   = self.get_argument("detail_name")
        code['detail_code']   = self.get_argument("detail_code")
        code['detail_status'] = self.get_argument("detail_status")
        result = save_sys_code_detail(code)
        self.write({"code": result['code'], "message": result['message']})

class sys_code_detail_upd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_code']      = self.get_argument("type_code")
        code['detail_name']    = self.get_argument("detail_name")
        code['detail_code']    = self.get_argument("detail_code")
        code['detail_code_old'] = self.get_argument("detail_code_old")
        code['detail_status']  = self.get_argument("detail_status")
        result = upd_sys_code_detail(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_detail_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code    = self.get_argument("type_code")
        detail  = self.get_argument("detail_code")
        result = del_sys_code_detail(code,detail)
        self.write({"code": result['code'], "message": result['message']})


class sys_test(basehandler):
   @tornado.web.authenticated
   def get(self):
       logon_name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("test.html")


class sys_query_rule(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_json    = query_rule()
        v_json    = json.dumps(v_json)
        self.write({"code": 0, "message": v_json})

