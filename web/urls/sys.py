#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.sys import audit_rule, audit_rule_save, sys_setting, sys_code, sys_code_type_query, \
    sys_code_detail_query, sys_setting_query, sys_setting_add_save, sys_setting_upd_save, sys_setting_del, sys_upload, \
    sys_upload_file
from web.services.sys import sys_code_detail_add_save, sys_code_detail_upd_save, sys_code_detail_del, sys_code_type
from web.services.sys import sys_query_rule, sys_code_type_add_save, sys_code_type_upd_save, sys_code_type_del

sys = [
    (r"/sys/audit_rule", audit_rule),
    (r"/sys/query_rule", sys_query_rule),
    (r"/sys/audit_rule/save", audit_rule_save),
    (r"/sys/setting", sys_setting),
    (r"/sys/setting/_query", sys_setting_query),
    (r"/sys/setting/add/save", sys_setting_add_save),
    (r"/sys/setting/upd/save", sys_setting_upd_save),
    (r"/sys/setting/del", sys_setting_del),

    (r"/sys/code", sys_code),
    (r"/sys/code/type/_query", sys_code_type_query),
    (r"/sys/code/detail/_query", sys_code_detail_query),
    (r"/sys/code/type/add/save", sys_code_type_add_save),
    (r"/sys/code/type/upd/save", sys_code_type_upd_save),
    (r"/sys/code/type/del", sys_code_type_del),
    (r"/sys/code/detail/add/save", sys_code_detail_add_save),
    (r"/sys/code/detail/upd/save", sys_code_detail_upd_save),
    (r"/sys/code/detail/del", sys_code_detail_del),
    (r"/sys/get/code/type", sys_code_type),

    (r"/sys/upload", sys_upload),
    (r"/sys/upload/file", sys_upload_file),
]
