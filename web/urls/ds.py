#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.ds import dsquery, ds_query_id, ds_query, dsadd, dsadd_save, dschange, dsedit, dsedit_save, \
    dsedit_del, \
    dstest, ds_check_valid, dsclone, dsclone_save, get_db_by_type, dsconsole, ds_sql_query, dslogquery, dslog_query

ds = [
    (r"/ds/query", dsquery),
    (r"/ds/query/id", ds_query_id),
    (r"/ds/_query", ds_query),
    (r"/ds/sql/_query", ds_sql_query),
    (r"/ds/add", dsadd),
    (r"/ds/add/save", dsadd_save),
    (r"/ds/change", dschange),
    (r"/ds/edit", dsedit),
    (r"/ds/edit/save", dsedit_save),
    (r"/ds/clone", dsclone),
    (r"/ds/console", dsconsole),
    (r"/ds/clone/save", dsclone_save),
    (r"/ds/edit/del", dsedit_del),
    (r"/ds/test", dstest),
    (r"/ds/check/valid", ds_check_valid),
    (r"/ds/get/db/type", get_db_by_type),
    (r"/ds/log/query", dslogquery),
    (r"/ds/log/_query", dslog_query),
]
