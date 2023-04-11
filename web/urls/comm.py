#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.sql import get_tab_ddl, get_tab_idx, get_dmm_dm, get_database, get_tables, get_columns, get_tab_stru, \
        get_keys, get_incr_col, get_ds, get_ds_by_query_grants, get_columns_by_query_grants

# 功能：主页面API
comm = [
        # 功能：公用API
        (r"/get_tab_ddl", get_tab_ddl),
        (r"/get_tab_idx", get_tab_idx),
        (r"/get_database", get_database),
        (r"/get_tables", get_tables),
        (r"/get_columns", get_columns),
        (r"/get_columns_by_query_grants", get_columns_by_query_grants),
        (r"/get_keys", get_keys),
        (r"/get_incr_col", get_incr_col),
        (r"/get_tab_stru", get_tab_stru),
        (r"/get_ds", get_ds),
        (r"/get_ds_by_query_grants", get_ds_by_query_grants),
        (r"/get/dmm/dm", get_dmm_dm),
]