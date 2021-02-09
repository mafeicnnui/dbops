#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.menu import menuquery,menu_query,menuadd,menuadd_save,menuchange,menuedit,menuedit_save,menuedit_del

# 功能：菜单管理API
menu = [
        (r"/menu/query", menuquery),
        (r"/menu/_query", menu_query),
        (r"/menu/add", menuadd),
        (r"/menu/add/save", menuadd_save),
        (r"/menu/change", menuchange),
        (r"/menu/edit", menuedit),
        (r"/menu/edit/save", menuedit_save),
        (r"/menu/edit/del", menuedit_del),
]