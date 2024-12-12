#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.user import userquery, useradd, useradd_save, useradd_save_uploadImage, userchange, useredit, \
    useredit_save, useredit_del, user_query, projectquery, project_query, projectprivs_save, sessionquery, \
    session_query, session_kill, userquerygrants, user_query_grants, user_query_grants_add_save, \
    get_user_query_grants, user_query_grants_upd_save, user_query_grants_del, userdictgrants, \
    user_dict_groups, user_dict_group_add_save, user_dict_group_del, get_user_dict_group, user_dict_group_upd_save, \
    user_dict_grant_add_save, user_dict_grant, get_user_dict_grant, user_dict_grant_del, user_dict_grant_upd_save

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
    (r"/user/session", sessionquery),
    (r"/user/_session", session_query),
    (r"/user/_session/kill", session_kill),
    (r"/user/query/grants", userquerygrants),
    (r"/user/query/_grants", user_query_grants),
    (r"/user/query/grants/add/save", user_query_grants_add_save),
    (r"/get/user/query/grants", get_user_query_grants),
    (r"/user/query/grants/upd/save", user_query_grants_upd_save),
    (r"/user/query/grants/del", user_query_grants_del),

    (r"/user/dict/grants", userdictgrants),
    (r"/user/dict/_group", user_dict_groups),
    (r"/user/dict/group/add/save", user_dict_group_add_save),
    (r"/user/dict/group/del", user_dict_group_del),
    (r"/get/user/dict/group", get_user_dict_group),
    (r"/user/dict/group/upd/save", user_dict_group_upd_save),

    (r"/user/dict/grant/add/save", user_dict_grant_add_save),
    (r"/user/dict/_grant", user_dict_grant),
    (r"/user/dict/grant/del", user_dict_grant_del),
    (r"/get/user/dict/grant", get_user_dict_grant),
    (r"/user/dict/grant/upd/save", user_dict_grant_upd_save),

]
