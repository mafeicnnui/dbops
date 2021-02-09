#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.sync         import syncadd,syncadd_save,syncadd_save_tab,syncadd_del_tab,syncquery,sync_query,sync_query_tab,sync_query_sync_tabs,syncchange,syncedit,syncedit_save,syncclone,syncclone_save,syncedit_del,synclogquery
from web.services.sync         import sync_log_query,sync_log_query_detail,syncedit_push,syncedit_run,syncedit_stop,syncloganalyze,sync_log_analyze,get_sync_tasks,get_sync

# 功能：数据库同步API
sync = [

        (r"/sync/query", syncquery),
        (r"/sync/_query", sync_query),
        (r"/sync/add", syncadd),
        (r"/sync/add/save", syncadd_save),
        (r"/sync/add/save/tab", syncadd_save_tab),
        (r"/sync/add/del/tab", syncadd_del_tab),
        (r"/sync/_query/tab", sync_query_tab),
        (r"/sync/_query/sync/tabs", sync_query_sync_tabs),
        (r"/sync/change", syncchange),
        (r"/sync/edit", syncedit),
        (r"/sync/edit/save", syncedit_save),
        (r"/sync/clone", syncclone),
        (r"/sync/clone/save", syncclone_save),
        (r"/sync/edit/del", syncedit_del),
        (r"/sync/edit/push", syncedit_push),
        (r"/sync/edit/run", syncedit_run),
        (r"/sync/edit/stop", syncedit_stop),
        (r"/sync/log/query", synclogquery),
        (r"/sync/log/_query", sync_log_query),
        (r"/sync/log/_query/detail", sync_log_query_detail),
        (r"/sync/log/analyze", syncloganalyze),
        (r"/sync/log/_analyze", sync_log_analyze),
        (r"/get/sync/task", get_sync_tasks),
        (r"/get/sync",     get_sync),
]