#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.sql import sqlquery, sql_query, sqlrelease, sql_check, sql_format, sql_check_result, sql_exp_task, \
        _sql_exp_task, es_query_mapping, redisquery, redis_query, redis_db
from web.services.sql    import sql_release,sqlaudit,sql_audit,sqlrun,sql_run,sql_audit_query,sql_audit_detail,sql_run_query
from web.services.sql    import get_tree_by_sql,query_sql_release,sql_detail,sql_exp_xls,sql_exp_pdf,sql_rollback_exp
from web.services.sql    import sql_exp_query,_sql_exp_query,_sql_exp_save,_sql_exp_update,_sql_exp_delete,_sql_exp_export,_sql_exp_detail
from web.services.sql    import expaudit,exp_audit,exp_detail,exp_audit_query,exp_export_data,exp_download,exp_export_data_delete,es_query,esquery,es_index

sql = [
        (r"/sql/query", sqlquery),
        (r"/sql/_query", sql_query),
        (r"/sql/detail", sql_detail),
        (r"/sql/release", sqlrelease),
        (r"/sql/_release", sql_release),
        (r"/sql/_check", sql_check),
        (r"/sql/_check/result", sql_check_result),
        (r"/sql/audit", sqlaudit),
        (r"/sql/_audit", sql_audit),
        (r"/sql/audit/query", sql_audit_query),
        (r"/sql/audit/detail", sql_audit_detail),
        (r"/sql/_format", sql_format),
        (r"/sql/run", sqlrun),
        (r"/sql/_run", sql_run),
        (r"/get/sql/release", query_sql_release),
        (r"/sql/run/query", sql_run_query),
        (r"/get_tree", get_tree_by_sql),
        (r"/sql/export/excel", sql_exp_xls),
        (r"/sql/export/pdf", sql_exp_pdf),
        (r"/sql/rollback/export", sql_rollback_exp),
        (r"/sql/exp/query", sql_exp_query),
        (r"/sql/exp/_query", _sql_exp_query),
        (r"/sql/exp/_save", _sql_exp_save),
        (r"/sql/exp/_update", _sql_exp_update),
        (r"/sql/exp/_delete", _sql_exp_delete),
        (r"/sql/exp/_export", _sql_exp_export),
        (r"/sql/exp/_detail", _sql_exp_detail),
        (r"/sql/exp/audit", expaudit),
        (r"/sql/exp/_audit", exp_audit),
        (r"/exp/audit/query", exp_audit_query),
        (r"/sql/exp/detail", exp_detail),

        (r"/sql/exp/task", sql_exp_task),
        (r"/sql/exp/_task", _sql_exp_task),
        (r"/sql/exp/data", exp_export_data),
        (r"/sql/exp/download", exp_download),
        (r"/sql/exp/data/delete", exp_export_data_delete),

        (r"/es/query", esquery),
        (r"/es/_query", es_query),
        (r"/es/_query/mapping", es_query_mapping),
        (r"/es/_index", es_index),

        (r"/redis/query", redisquery),
        (r"/redis/_query", redis_query),
        (r"/redis/_db", redis_db),

]