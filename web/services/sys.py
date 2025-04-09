#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : ma.fei
# @File : initialize.py
# @Software: PyCharm

import json
import os.path
import traceback
import datetime
from web.model.t_dmmx import get_sys_dmlx, get_gather_server
from web.model.t_server import get_server_by_serverid
from web.model.t_sys import save_audit_rule, query_dm, query_rule, query_dm_detail, save_sys_code_type, \
    upd_sys_code_type, del_sys_code, query_settings, save_sys_setting, upd_sys_setting, del_sys_setting
from web.model.t_sys import save_sys_code_detail, upd_sys_code_detail, del_sys_code_detail
from web.utils import base_handler
from web.utils.common import get_file_size, ftp_helper, ssh_helper,get_seconds


class audit_rule(base_handler.TokenHandler):
    def get(self):
        self.render("./sys/audit_rule.html")


class audit_rule_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        rule = {}
        # DDL规范参数
        rule['switch_check_ddl'] = self.get_argument("switch_check_ddl")
        rule['switch_tab_not_exists_pk'] = self.get_argument("switch_tab_not_exists_pk")
        rule['switch_tab_pk_id'] = self.get_argument("switch_tab_pk_id")
        rule['switch_tab_pk_auto_incr'] = self.get_argument("switch_tab_pk_auto_incr")

        rule['switch_tab_pk_autoincrement_1'] = self.get_argument("switch_tab_pk_autoincrement_1")
        rule['switch_pk_not_int_bigint'] = self.get_argument("switch_pk_not_int_bigint")
        rule['switch_tab_comment'] = self.get_argument("switch_tab_comment")
        rule['switch_col_comment'] = self.get_argument("switch_col_comment")

        rule['switch_col_not_null'] = self.get_argument("switch_col_not_null")
        rule['switch_col_default_value'] = self.get_argument("switch_col_default_value")
        rule['switch_tcol_default_value'] = self.get_argument("switch_tcol_default_value")
        rule['switch_char_max_len'] = self.get_argument("switch_char_max_len")

        rule['switch_tab_has_time_fields'] = self.get_argument("switch_tab_has_time_fields")
        rule['switch_tab_tcol_datetime'] = self.get_argument("switch_tab_tcol_datetime")
        rule['switch_tab_char_total_len'] = self.get_argument("switch_tab_char_total_len")
        rule['switch_tab_ddl_max_rows'] = self.get_argument("switch_tab_ddl_max_rows")

        rule['switch_tab_name_check'] = self.get_argument("switch_tab_name_check")
        rule['switch_idx_name_check'] = self.get_argument("switch_idx_name_check")
        rule['switch_ddl_batch'] = self.get_argument("switch_ddl_batch")
        rule['switch_ddl_timeout'] = self.get_argument("switch_ddl_timeout")

        rule['switch_disable_trigger'] = self.get_argument("switch_disable_trigger")
        rule['switch_disable_func'] = self.get_argument("switch_disable_func")
        rule['switch_disable_proc'] = self.get_argument("switch_disable_proc")
        rule['switch_disable_event'] = self.get_argument("switch_disable_event")

        rule['switch_drop_database'] = self.get_argument("switch_drop_database")
        rule['switch_drop_table'] = self.get_argument("switch_drop_table")
        rule['switch_virtual_col'] = self.get_argument("switch_virtual_col")
        rule['switch_tab_migrate'] = self.get_argument("switch_tab_migrate")

        rule['switch_col_order_rule'] = self.get_argument("switch_col_order_rule")
        rule['switch_col_charset'] = self.get_argument("switch_col_charset")
        rule['switch_tab_charset'] = self.get_argument("switch_tab_charset")
        rule['switch_tab_charset_range'] = self.get_argument("switch_tab_charset_range")

        # 表名规范参数
        rule['switch_tab_not_digit_first'] = self.get_argument("switch_tab_not_digit_first")
        rule['switch_tab_two_digit_end'] = self.get_argument("switch_tab_two_digit_end")
        rule['switch_tab_max_len'] = self.get_argument("switch_tab_max_len")
        rule['switch_tab_disable_prefix'] = self.get_argument("switch_tab_disable_prefix")

        # 索引规范参数
        rule['switch_idx_name_null'] = self.get_argument("switch_idx_name_null")
        rule['switch_idx_name_rule'] = self.get_argument("switch_idx_name_rule")
        rule['switch_idx_numbers'] = self.get_argument("switch_idx_numbers")
        rule['switch_idx_col_numbers'] = self.get_argument("switch_idx_col_numbers")
        rule['switch_idx_name_col'] = self.get_argument("switch_idx_name_col")

        # 批量DML语句开关
        rule['switch_check_dml'] = self.get_argument("switch_check_dml")
        rule['switch_dml_batch'] = self.get_argument("switch_dml_batch")
        rule['switch_dml_where'] = self.get_argument("switch_dml_where")
        rule['switch_dml_order'] = self.get_argument("switch_dml_order")
        rule['switch_dml_select'] = self.get_argument("switch_dml_select")
        rule['switch_dml_max_rows'] = self.get_argument("switch_dml_max_rows")
        rule['switch_dml_ins_cols'] = self.get_argument("switch_dml_ins_cols")
        rule['switch_dml_ins_exists_col'] = self.get_argument("switch_dml_ins_exists_col")

        # 查询开关
        rule['switch_query_rows'] = self.get_argument("switch_query_rows")
        rule['switch_timeout'] = self.get_argument("switch_timeout")
        rule['switch_sensitive_columns'] = self.get_argument("switch_sensitive_columns")

        # 导出开关
        rule['switch_export_rows'] = self.get_argument("switch_export_rows")
        rule['switch_export_timeout'] = self.get_argument("switch_export_timeout")

        result = await save_audit_rule(rule)
        self.write({"code": result['code'], "message": result['message']})


class sys_setting(base_handler.TokenHandler):
    async def get(self):
        self.render("./sys/sys_setting.html",
                    sys_code_type=await get_sys_dmlx())


class sys_code(base_handler.TokenHandler):
    async def get(self):
        self.render("./sys/sys_code.html",
                    sys_code_type=await get_sys_dmlx())


class sys_code_type(base_handler.TokenHandler):
    async def post(self):
        self.write({"message": await get_sys_dmlx()})


class sys_code_type_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = self.get_argument("code")
        v_list = await query_dm(code)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sys_code_detail_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = self.get_argument("code")
        v_list = await query_dm_detail(code)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sys_code_type_add_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_name'] = self.get_argument("type_name")
        code['type_code'] = self.get_argument("type_code")
        code['type_status'] = self.get_argument("type_status")
        result = await save_sys_code_type(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_type_upd_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_name'] = self.get_argument("type_name")
        code['type_code'] = self.get_argument("type_code")
        code['type_status'] = self.get_argument("type_status")
        result = await upd_sys_code_type(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_type_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = self.get_argument("type_code")
        result = await del_sys_code(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_detail_add_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_code'] = self.get_argument("type_code")
        code['detail_name'] = self.get_argument("detail_name")
        code['detail_code'] = self.get_argument("detail_code")
        code['detail_status'] = self.get_argument("detail_status")
        code['detail_desc'] = self.get_argument("detail_desc")
        result = await save_sys_code_detail(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_detail_upd_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['type_code'] = self.get_argument("type_code")
        code['detail_name'] = self.get_argument("detail_name")
        code['detail_code'] = self.get_argument("detail_code")
        code['detail_code_old'] = self.get_argument("detail_code_old")
        code['detail_status'] = self.get_argument("detail_status")
        code['detail_desc'] = self.get_argument("detail_desc")
        result = await upd_sys_code_detail(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_code_detail_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = self.get_argument("type_code")
        detail = self.get_argument("detail_code")
        result = await del_sys_code_detail(code, detail)
        self.write({"code": result['code'], "message": result['message']})


class sys_query_rule(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_json = await query_rule()
        v_json = json.dumps(v_json)
        self.write({"code": 0, "message": v_json})


class sys_setting_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = self.get_argument("code")
        v_list = await query_settings(code)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sys_setting_add_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['key'] = self.get_argument("key")
        code['value'] = self.get_argument("value")
        code['desc'] = self.get_argument("desc")
        code['status'] = self.get_argument("status")
        result = await save_sys_setting(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_setting_upd_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        code = {}
        code['key'] = self.get_argument("key")
        code['value'] = self.get_argument("value")
        code['desc'] = self.get_argument("desc")
        code['status'] = self.get_argument("status")
        result = await upd_sys_setting(code)
        self.write({"code": result['code'], "message": result['message']})


class sys_setting_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        key = self.get_argument("key")
        result = await del_sys_setting(key)
        self.write({"code": result['code'], "message": result['message']})


class sys_upload(base_handler.TokenHandler):
    async def get(self):
        self.render("./sys/file_upload.html",
                    servers=await get_gather_server(),
                    )


class sys_upload_file(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas = self.request.files["file"]
        path_name = self.get_argument("path_name")
        serverid = self.get_argument("serverid")
        try:
            res = []
            for meta in file_metas:
                file_path = static_path + '/' + 'uploads'
                file_name = file_path + '/' + meta['filename']
                remote_name = path_name + '/' + meta['filename']
                with open(file_name, 'wb') as up:
                    up.write(meta['body'])
                print('{} import sucess'.format(meta['filename']))
                res.append({
                    'local_name': file_name,
                    'remote_name': remote_name,
                    'file_size': get_file_size(file_name)
                })
            print('文件先传至/static/upload目录成功!')
            server = await get_server_by_serverid(serverid)
            ftp = ftp_helper(server)
            for f in res:
                start_time = datetime.datetime.now()
                ftp.transfer(f['local_name'], f['remote_name'])
                f.update({'elapsed_time': get_seconds(start_time)})
                print('file {} upload sucess!'.format(f['local_name']))
            ret = []
            for p in res:
                print(p)
                ret.append((p['remote_name'], p['file_size'], p['elapsed_time']))
            self.write({"code": 0, "message": ret})
        except Exception as e:
            traceback.print_exc()
            self.write({"code": -1, "message": '导入失败' + str(e)})


class get_sys_dir(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        server_id = self.get_argument("server_id")
        path_name = self.get_argument("path_name")
        server = await get_server_by_serverid(server_id)
        ssh = ssh_helper(server)
        cmd = 'find {} -mindepth 1 -maxdepth 1 -type d | grep -v "/\."'.format(path_name)
        print(cmd)
        res = ssh.exec(cmd)
        if res['status']:
            self.write({"code": 0, "message": [r.replace('\n','') for r in res['stdout']]})
        else:
            self.write({"code": -1, "message": res['stderr']})
