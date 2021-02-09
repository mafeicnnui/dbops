#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.ds  import dsquery,ds_query_id,ds_query,dsadd,dsadd_save,dschange,dsedit,dsedit_save,dsedit_del,dstest,ds_check_valid,dsclone,dsclone_save,get_db_by_type

# 功能：数据源管理API
ds = [
        (r"/ds/query", dsquery),
        (r"/ds/query/id", ds_query_id),
        (r"/ds/_query", ds_query),
        (r"/ds/add", dsadd),
        (r"/ds/add/save", dsadd_save),
        (r"/ds/change", dschange),
        (r"/ds/edit", dsedit),
        (r"/ds/edit/save", dsedit_save),
        (r"/ds/clone", dsclone),
        (r"/ds/clone/save", dsclone_save),
        (r"/ds/edit/del", dsedit_del),
        (r"/ds/test", dstest),
        (r"/ds/check/valid", ds_check_valid),
        (r"/ds/get/db/type", get_db_by_type),
]