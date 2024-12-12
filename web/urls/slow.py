#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.slow import slowquery, slowadd, slowadd_save, slow_query, slowchange, slowedit_save, slowedit_del, \
    slow_query_by_id, slowedit_push, query_slowlog_plan_by_id, \
    query_db_by_slowlog_instid, \
    query_user_by_slowlog_instid, \
    query_db_by_slowlog_dsid, \
    query_user_by_slowlog_dsid, \
    slowlogquery, slowlog_query, \
    query_slowlog_by_id, query_slowlog_by_id_oracle, query_slowlog_by_id_mssql, \
    slowloganalyze, \
    slowlog_analyze, query_slowlog_detail_by_id

slow = [
    (r"/slow/query", slowquery),
    (r"/slow/_query", slow_query),
    (r"/slow/add", slowadd),
    (r"/slow/add/save", slowadd_save),
    (r"/slow/change", slowchange),
    (r"/slow/edit/save", slowedit_save),
    (r"/slow/edit/del", slowedit_del),
    (r"/slow/edit/push", slowedit_push),
    (r"/slow/query/id", slow_query_by_id),
    (r"/slow/log/query", slowlogquery),
    (r"/slow/log/_query", slowlog_query),
    (r"/slow/log/query/id", query_slowlog_by_id),
    (r"/slow/log/query/id/oracle", query_slowlog_by_id_oracle),
    (r"/slow/log/query/id/mssql", query_slowlog_by_id_mssql),
    (r"/slow/log/detail/id", query_slowlog_detail_by_id),
    (r"/slow/log/plan/id", query_slowlog_plan_by_id),
    (r"/get/inst/db", query_db_by_slowlog_instid),
    (r'/get/inst/user', query_user_by_slowlog_instid),
    (r"/get/ds/db", query_db_by_slowlog_dsid),
    (r'/get/ds/user', query_user_by_slowlog_dsid),
    (r"/slow/log/analyze", slowloganalyze),
    (r"/slow/log/_analyze", slowlog_analyze),
]
