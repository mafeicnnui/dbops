#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.user         import userquery,useradd,useradd_save,useradd_save_uploadImage,userchange,useredit,useredit_save,useredit_del,user_query,projectquery,project_query,projectprivs_save

# 功能：用户管理API
user = [
        (r"/user/query", userquery),
        (r"/user/_query", user_query),
        (r"/user/add", useradd),
        (r"/user/add/save", useradd_save),
        (r"/user/add/uploadImage", useradd_save_uploadImage),
        (r"/user/change", userchange),
        (r"/user/edit", useredit),
        (r"/user/edit/save", useredit_save),
        (r"/user/edit/del", useredit_del),
        (r"/project/query", projectquery),
        (r"/project/_query", project_query),
        (r"/project/privs/save", projectprivs_save),
]