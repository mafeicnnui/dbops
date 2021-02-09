#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.sync_bigdata import syncadd_bigdata,syncadd_bigdata_save,syncbigdataquery,sync_bigdata_query,sync_bigdata_query_detail,sync_bigdata_query_dataxTemplete
from web.services.sync_bigdata import sync_bigdata_downloads_dataxTemplete,syncchange_bigdata,syncedit_bigdata,syncedit_save_bigdata,syncedit_del_bigdata,syncedit_push_bigdata
from web.services.sync_bigdata import syncedit_pushall_bigdata,syncedit_run_bigdata,syncedit_stop_bigdata,syncclone_bigdata,syncclone_save_bigdata,syncloganalyze_bigdata,sync_log_analyze_bigdata,get_bigdata_sync_tasks
from web.services.sync_bigdata import sync_bigdata_query_es_dataxTemplete,sync_bigdata_downloads_es_dataxTemplete

# 功能：大数据管理API
bigdata = [
        (r"/bigdata/add", syncadd_bigdata),
        (r"/bigdata/add/save", syncadd_bigdata_save),
        (r"/bigdata/query", syncbigdataquery),
        (r"/bigdata/_query", sync_bigdata_query),
        (r"/bigdata/_query/detail", sync_bigdata_query_detail),
        (r"/bigdata/_query/templete", sync_bigdata_query_dataxTemplete),
        (r"/bigdata/_query/downloads", sync_bigdata_downloads_dataxTemplete),
        (r"/bigdata/change", syncchange_bigdata),
        (r"/bigdata/edit", syncedit_bigdata),
        (r"/bigdata/edit/save", syncedit_save_bigdata),
        (r"/bigdata/edit/del", syncedit_del_bigdata),
        (r"/bigdata/clone", syncclone_bigdata),
        (r"/bigdata/clone/save", syncclone_save_bigdata),
        (r"/bigdata/edit/push", syncedit_push_bigdata),
        (r"/bigdata/edit/pushall", syncedit_pushall_bigdata),
        (r"/bigdata/edit/run", syncedit_run_bigdata),
        (r"/bigdata/edit/stop", syncedit_stop_bigdata),
        (r"/bigdata/log/analyze", syncloganalyze_bigdata),
        (r"/bigdata/log/_analyze", sync_log_analyze_bigdata),
        (r"/get/bigdata/sync/task", get_bigdata_sync_tasks),
        (r"/bigdata/_query/es_templete", sync_bigdata_query_es_dataxTemplete),
        (r"/bigdata/_query/es_downloads", sync_bigdata_downloads_es_dataxTemplete),
]