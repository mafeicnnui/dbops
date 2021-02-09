#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.role         import rolequery,roleadd,roleadd_save,role_query,rolechange,roleedit,roleedit_save,roleedit_del

# 功能：角色管理API
role = [
        (r"/role/query", rolequery),
        (r"/role/_query", role_query),
        (r"/role/add", roleadd),
        (r"/role/add/save", roleadd_save),
        (r"/role/change", rolechange),
        (r"/role/edit", roleedit),
        (r"/role/edit/save", roleedit_save),
        (r"/role/edit/del", roleedit_del),
]