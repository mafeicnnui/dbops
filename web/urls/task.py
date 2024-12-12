#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.task import taskquery, task_query, taskadd, taskadd_save, taskchange, taskedit, taskedit_save, \
    taskedit_del, taskedit_push

task = [
    (r"/task/query", taskquery),
    (r"/task/_query", task_query),
    (r"/task/add", taskadd),
    (r"/task/add/save", taskadd_save),
    (r"/task/change", taskchange),
    (r"/task/edit", taskedit),
    (r"/task/edit/save", taskedit_save),
    (r"/task/edit/del", taskedit_del),
    (r"/task/edit/push", taskedit_push),

]
