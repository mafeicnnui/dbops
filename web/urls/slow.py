#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.slow   import slowquery,slowadd,slowadd_save,slow_query,slowchange,slowedit_save,slowedit_del,slow_query_by_id,slowedit_push,query_slowlog_plan_by_id
from web.services.slow   import slowlogquery,slowlog_query,query_slowlog_by_id,query_db_by_inst,query_user_by_inst,slowloganalyze,slowlog_analyze,query_slowlog_detail_by_id

# 功能：慢日志API
slow = [
        (r"/slow/query",                     slowquery),
        (r"/slow/_query",                    slow_query),
        (r"/slow/add",                       slowadd),
        (r"/slow/add/save",                  slowadd_save),
        (r"/slow/change",                    slowchange),
        (r"/slow/edit/save",                 slowedit_save),
        (r"/slow/edit/del",                  slowedit_del),
        (r"/slow/edit/push",                 slowedit_push),
        (r"/slow/query/id" ,                 slow_query_by_id),
        (r"/slow/log/query",                 slowlogquery),
        (r"/slow/log/_query",                slowlog_query),
        (r"/slow/log/query/id",              query_slowlog_by_id),
        (r"/slow/log/detail/id",             query_slowlog_detail_by_id),
        (r"/slow/log/plan/id",               query_slowlog_plan_by_id),
        (r"/get/inst/db",                    query_db_by_inst),
        (r"/get/inst/user",                  query_user_by_inst),
        (r"/slow/log/analyze",               slowloganalyze),
        (r"/slow/log/_analyze",              slowlog_analyze),
]