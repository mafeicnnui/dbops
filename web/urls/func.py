#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.func         import funcquery,func_query,funcadd,funcadd_save,funcchange,funcedit,funcedit_save,funcedit_del

# 功能：功能管理API
func = [
        (r"/func/query", funcquery),
        (r"/func/_query", func_query),
        (r"/func/add", funcadd),
        (r"/func/add/save", funcadd_save),
        (r"/func/change", funcchange),
        (r"/func/edit", funcedit),
        (r"/func/edit/save", funcedit_save),
        (r"/func/edit/del", funcedit_del),
]