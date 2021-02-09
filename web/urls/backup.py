#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.backup       import backupquery,backup_query,backupadd,backupadd_save,backupchange,backupedit,backupedit_save,backupedit_del,backuplogquery
from web.services.backup       import backup_log_query,backup_log_query_detail,backupedit_push,backupedit_run,backupedit_stop,backuploganalyze,backup_log_analyze,get_backup_tasks

# 功能：数据库备份API
backup = [
        (r"/backup/query", backupquery),
        (r"/backup/_query", backup_query),
        (r"/backup/add", backupadd),
        (r"/backup/add/save", backupadd_save),
        (r"/backup/change", backupchange),
        (r"/backup/edit", backupedit),
        (r"/backup/edit/save", backupedit_save),
        (r"/backup/edit/del", backupedit_del),
        (r"/backup/edit/push", backupedit_push),
        (r"/backup/edit/run", backupedit_run),
        (r"/backup/edit/stop", backupedit_stop),
        (r"/backup/log/query", backuplogquery),
        (r"/backup/log/_query", backup_log_query),
        (r"/backup/log/_query/detail", backup_log_query_detail),
        (r"/backup/log/analyze", backuploganalyze),
        (r"/backup/log/_analyze", backup_log_analyze),
        (r"/get/backup/task", get_backup_tasks),
]