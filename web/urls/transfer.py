#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.transfer     import transferadd,transferadd_save,transferchange,transferedit,transferedit_save,transferedit_del,transfer_query,transferedit_push,transferedit_run,transferedit_stop
from web.services.transfer     import transferquery,transferclone,transferclone_save,transferlogquery,transfer_log_query,transfer_query_detail

# 功能：数据库传输API
transfer = [
        (r"/transfer/query", transferquery),
        (r"/transfer/_query", transfer_query),
        (r"/transfer/_query/detail", transfer_query_detail),
        (r"/transfer/add", transferadd),
        (r"/transfer/add/save", transferadd_save),
        (r"/transfer/change", transferchange),
        (r"/transfer/edit", transferedit),
        (r"/transfer/edit/save", transferedit_save),
        (r"/transfer/edit/del", transferedit_del),
        (r"/transfer/edit/push", transferedit_push),
        (r"/transfer/edit/run", transferedit_run),
        (r"/transfer/edit/stop", transferedit_stop),
        (r"/transfer/clone", transferclone),
        (r"/transfer/clone/save", transferclone_save),
        (r"/transfer/log/query", transferlogquery),
        (r"/transfer/log/_query", transfer_log_query),
]