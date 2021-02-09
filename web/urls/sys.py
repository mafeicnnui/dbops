#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.sys          import audit_rule,audit_rule_save,sys_setting,sys_code,sys_code_type_query,sys_code_detail_query,sys_test,sys_query_rule,sys_code_type_add_save,sys_code_type_upd_save,sys_code_type_del
from web.services.sys          import sys_code_detail_add_save,sys_code_detail_upd_save,sys_code_detail_del,sys_code_type

# 功能：系统设置API
sys = [
        (r"/sys/audit_rule", audit_rule),
        (r"/sys/query_rule", sys_query_rule),
        (r"/sys/audit_rule/save", audit_rule_save),
        (r"/sys/setting", sys_setting),
        (r"/sys/code", sys_code),
        (r"/sys/code/type/_query", sys_code_type_query),
        (r"/sys/code/detail/_query", sys_code_detail_query),
        (r"/sys/code/type/add/save", sys_code_type_add_save),
        (r"/sys/code/type/upd/save", sys_code_type_upd_save),
        (r"/sys/code/type/del", sys_code_type_del),
        (r"/sys/code/detail/add/save", sys_code_detail_add_save),
        (r"/sys/code/detail/upd/save", sys_code_detail_upd_save),
        (r"/sys/code/detail/del", sys_code_detail_del),
        (r"/sys/test", sys_test),
        (r"/sys/get/code/type", sys_code_type),
]