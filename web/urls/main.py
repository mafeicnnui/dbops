#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.backup       import backup_case
from web.services.sync         import get_sync_park,get_sync_park_real_time,get_sync_flow,get_sync_flow_real_time
from web.services.sync         import get_sync_flow_device,get_sync_park_charge,get_sync_bi,sync_case,sync_case_log
from web.services.sync         import db_active_num,db_slow_num,sys_stats_num,sys_stats_idx,db_order_num

# 功能：主页面
main = [
        (r"/backup_case", backup_case),
        (r"/sync_case", sync_case),
        (r"/sync_case_log", sync_case_log),
        (r"/get/sync/park", get_sync_park),
        (r"/get/sync/park/realtime", get_sync_park_real_time),
        (r"/get/sync/flow", get_sync_flow),
        (r"/get/sync/flow/realtime", get_sync_flow_real_time),
        (r"/get/sync/flow/device", get_sync_flow_device),
        (r"/get/sync/park/charge", get_sync_park_charge),
        (r"/get/sync/bi", get_sync_bi),
        (r"/get/db/active/num", db_active_num),
        (r"/get/db/order/num", db_order_num),
        (r"/get/db/slow/num", db_slow_num),
        (r"/get/sys/stats/num", sys_stats_num),
        (r"/get/sys/stats/idx", sys_stats_idx),

]