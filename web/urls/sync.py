#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.sync  import syncadd,syncadd_save,syncadd_save_tab,syncadd_del_tab,syncquery,sync_query,sync_query_tab,sync_query_sync_tabs,syncchange,syncedit,syncedit_save,syncclone,syncclone_save,syncedit_del,synclogquery
from web.services.sync  import sync_log_query,sync_log_query_detail,syncedit_push,syncedit_run,syncedit_stop,syncloganalyze,sync_log_analyze,get_sync_tasks,get_sync,get_mssql_tables,get_mysql_tables
from web.services.sync  import get_mssql_columns,get_mysql_columns,get_mssql_incr_columns,get_mysql_incr_columns,sync_real_edit_save
from web.services.sync  import sync_real,sync_real_save,get_mysql_databases,sync_query_tab_real,sync_query_sync_tabs_real,get_ck_databases,sync_real_clone_save

sync = [

        (r"/sync/query", syncquery),
        (r"/sync/_query", sync_query),
        (r"/sync/add", syncadd),
        (r"/sync/add/save", syncadd_save),
        (r"/sync/add/save/tab", syncadd_save_tab),
        (r"/sync/add/del/tab", syncadd_del_tab),
        (r"/sync/_query/tab", sync_query_tab),
        (r"/sync/_query/tab/real", sync_query_tab_real),
        (r"/sync/_query/sync/tabs", sync_query_sync_tabs),
        (r"/sync/_query/sync/tabs/real", sync_query_sync_tabs_real),
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
        (r"/get/sync", get_sync),
        (r"/get_mssql_tables", get_mssql_tables),
        (r"/get_mysql_tables", get_mysql_tables),
        (r"/get_mysql_databases", get_mysql_databases),
        (r"/get_mssql_columns", get_mssql_columns),
        (r"/get_mysql_columns", get_mysql_columns),
        (r"/get_mssql_incr_columns", get_mssql_incr_columns),
        (r"/get_mysql_incr_columns", get_mysql_incr_columns),
        (r"/get_ck_databases", get_ck_databases),
        (r"/sync/real", sync_real),
        (r"/sync/real/add/save", sync_real_save),
        (r"/sync/real/edit/save", sync_real_edit_save),
        (r"/sync/real/clone/save", sync_real_clone_save),

]