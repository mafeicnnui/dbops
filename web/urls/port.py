#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.port   import portadd,portadd_save,portchange,portedit,portedit_save,portedit_del,port_query,portquery,portedit_imp,portedit_exp

# 功能：端口管理API

port = [
        (r"/port/query", portquery),
        (r"/port/_query", port_query),
        (r"/port/add", portadd),
        (r"/port/add/save", portadd_save),
        (r"/port/change", portchange),
        (r"/port/edit", portedit),
        (r"/port/edit/save", portedit_save),
        (r"/port/edit/del", portedit_del),
        (r"/port/edit/imp", portedit_imp),
        (r"/port/edit/exp", portedit_exp),
]