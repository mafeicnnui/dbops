#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.server import serverquery,server_query,serveradd,serveradd_save,serverchange,serveredit,serveredit_save,serveredit_del,server_by_serverid

server = [
        (r"/server/query", serverquery),
        (r"/server/_query", server_query),
        (r"/server/add", serveradd),
        (r"/server/add/save", serveradd_save),
        (r"/server/change", serverchange),
        (r"/server/edit", serveredit),
        (r"/server/edit/save", serveredit_save),
        (r"/server/edit/del", serveredit_del),
        (r"/get/server/id", server_by_serverid),
]