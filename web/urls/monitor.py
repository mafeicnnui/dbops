#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.monitor import monitorgraphquery, monitorgraph_query, get_monitor_templete_type, get_monitor_db, \
    get_monitor_index, get_monitor_task, get_monitor_view, get_monitor_view_sys, get_monitor_view_svr, \
    get_monitor_view_proj, get_monitor_view_proj_log
from web.services.monitor import monitorindexquery, monitorindex_query, monitorindexadd_save, monitorindexedit_save, \
    monitorindexedit_del, monitortaskupd_save_gather, monitortaskupd_save_monitor, monitoralertquery, \
    monitoralert_query, monitoralertadd_save, monitoralertupd_save, get_alert_task, monitoralertedit_del, \
    monitoralert_push, get_monitor_view_api, get_monitor_view_api_log, monitor_redis_slowlog, monitorindex_detail, \
    monitor_query_id, monitor_power_empty, monitor_power_empty_warn, monitor_power_full, monitor_power_full_warn, \
    monitor_power_offline, monitor_power_offline_warn
from web.services.monitor import monitortaskquery, monitortask_query, monitortaskadd_save_gather, \
    monitortaskadd_save_monitor, monitortaskedit_del, monitortask_push, monitortask_run, monitortask_stop
from web.services.monitor import monitortempletequery, monitortemplete_query, monitortempleteadd_save, \
    monitortempleteedit_save, monitortempleteedit_del, monitor_sys_indexes, monitor_templete_indexes

monitor = [
    # 功能：数据库监控-指标管理API
    (r"/monitor/index/query", monitorindexquery),
    (r"/monitor/index/_query", monitorindex_query),
    (r"/monitor/index/_detail", monitorindex_detail),
    (r"/monitor/index/add/save", monitorindexadd_save),
    (r"/monitor/index/edit/save", monitorindexedit_save),
    (r"/monitor/index/edit/del", monitorindexedit_del),

    # 功能：数据库监控-模板管理API
    (r"/monitor/templete/query", monitortempletequery),
    (r"/monitor/templete/_query", monitortemplete_query),
    (r"/monitor/templete/add/save", monitortempleteadd_save),
    (r"/monitor/templete/edit/save", monitortempleteedit_save),
    (r"/monitor/templete/edit/del", monitortempleteedit_del),
    (r"/monitor/sys/indexes", monitor_sys_indexes),
    (r"/monitor/templete/indexes", monitor_templete_indexes),

    # 功能：数据库监控-任务管理API
    (r"/monitor/task/query", monitortaskquery),
    (r"/monitor/task/_query", monitortask_query),
    (r"/monitor/task/add/save/gather", monitortaskadd_save_gather),
    (r"/monitor/task/add/save/monitor", monitortaskadd_save_monitor),
    (r"/monitor/task/edit/save/gather", monitortaskupd_save_gather),
    (r"/monitor/task/edit/save/monitor", monitortaskupd_save_monitor),
    (r"/monitor/task/edit/del", monitortaskedit_del),
    (r"/monitor/task/push", monitortask_push),
    (r"/monitor/task/run", monitortask_run),
    (r"/monitor/task/stop", monitortask_stop),
    (r"/get/monitor/templete/type", get_monitor_templete_type),
    (r"/get/monitor/task", get_monitor_task),

    # 功能：数据库监控-图表展示API
    (r"/monitor/graph/query", monitorgraphquery),
    (r"/monitor/graph/_query", monitorgraph_query),
    (r"/get/monitor/db", get_monitor_db),
    (r"/get/monitor/index", get_monitor_index),
    (r"/monitor/view", get_monitor_view),
    (r"/monitor/view/sys", get_monitor_view_sys),
    (r"/monitor/view/svr", get_monitor_view_svr),
    (r"/monitor/view/proj", get_monitor_view_proj),
    (r"/monitor/view/proj/log", get_monitor_view_proj_log),
    (r"/monitor/view/api", get_monitor_view_api),
    (r"/monitor/view/api/log", get_monitor_view_api_log),

    # 功能：数据库监控-告警管理API
    (r"/monitor/alert/query", monitoralertquery),
    (r"/monitor/alert/_query", monitoralert_query),
    (r"/monitor/alert/add/save", monitoralertadd_save),
    (r"/monitor/alert/edit/save", monitoralertupd_save),
    (r"/get/alert/task", get_alert_task),
    (r"/monitor/alert/edit/del", monitoralertedit_del),
    (r"/monitor/alert/push", monitoralert_push),

    (r"/monitor/redis/slowlog", monitor_redis_slowlog),
    (r"/monitor/_query/id", monitor_query_id),

    (r"/monitor/power/empty", monitor_power_empty),
    (r"/monitor/power/empty/warn", monitor_power_empty_warn),
    (r"/monitor/power/full", monitor_power_full),
    (r"/monitor/power/full/warn", monitor_power_full_warn),
    (r"/monitor/power/offline", monitor_power_offline),
    (r"/monitor/power/offline/warn", monitor_power_offline_warn),

]
