#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.archive      import archiveadd,archiveadd_save,archivequery,archive_query,archive_query_detail,archivechange,archiveedit,archiveedit_save
from web.services.archive      import archiveedit_del,archiveedit_push,archiveedit_run,archiveedit_stop,archiveclone,archiveclone_save,archivelogquery,archive_log_query

# 功能：数据库归档API
archive = [
        (r"/archive/add", archiveadd),
        (r"/archive/add/save", archiveadd_save),
        (r"/archive/query", archivequery),
        (r"/archive/_query", archive_query),
        (r"/archive/_query/detail", archive_query_detail),
        (r"/archive/change", archivechange),
        (r"/archive/edit", archiveedit),
        (r"/archive/edit/save", archiveedit_save),
        (r"/archive/edit/del", archiveedit_del),
        (r"/archive/edit/push", archiveedit_push),
        (r"/archive/edit/run", archiveedit_run),
        (r"/archive/edit/stop", archiveedit_stop),
        (r"/archive/clone", archiveclone),
        (r"/archive/clone/save", archiveclone_save),
        (r"/archive/log/query", archivelogquery),
        (r"/archive/log/_query", archive_log_query),
]