#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : bigdata.py.py
# @Software: PyCharm

from web.services.datax import syncadd_datax,syncadd_datax_save,syncdataxquery,sync_datax_query,sync_datax_query_detail,sync_datax_query_dataxTemplete
from web.services.datax import sync_datax_downloads_dataxTemplete,syncchange_datax,syncedit_datax,syncedit_save_datax,syncedit_del_datax,syncedit_push_datax
from web.services.datax import syncedit_pushall_datax,syncedit_run_datax,syncedit_stop_datax,syncclone_datax,syncclone_save_datax,syncloganalyze_datax,sync_log_analyze_datax,get_datax_sync_tasks
from web.services.datax import sync_datax_query_es_dataxTemplete,sync_datax_downloads_es_dataxTemplete

datax = [
        (r"/datax/add", syncadd_datax),
        (r"/datax/add/save", syncadd_datax_save),
        (r"/datax/query", syncdataxquery),
        (r"/datax/_query", sync_datax_query),
        (r"/datax/_query/detail", sync_datax_query_detail),
        (r"/datax/_query/templete", sync_datax_query_dataxTemplete),
        (r"/datax/_query/downloads", sync_datax_downloads_dataxTemplete),
        (r"/datax/change", syncchange_datax),
        (r"/datax/edit", syncedit_datax),
        (r"/datax/edit/save", syncedit_save_datax),
        (r"/datax/edit/del", syncedit_del_datax),
        (r"/datax/clone", syncclone_datax),
        (r"/datax/clone/save", syncclone_save_datax),
        (r"/datax/edit/push", syncedit_push_datax),
        (r"/datax/edit/pushall", syncedit_pushall_datax),
        (r"/datax/edit/run", syncedit_run_datax),
        (r"/datax/edit/stop", syncedit_stop_datax),
        (r"/datax/log/analyze", syncloganalyze_datax),
        (r"/datax/log/_analyze", sync_log_analyze_datax),
        (r"/get/datax/sync/task", get_datax_sync_tasks),
        (r"/datax/_query/es_templete", sync_datax_query_es_dataxTemplete),
        (r"/datax/_query/es_downloads", sync_datax_downloads_es_dataxTemplete),
]