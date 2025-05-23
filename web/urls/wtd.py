#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.sql import orderquery, order_query, order_delete, order_query_xh, order_check_xh, order_update, \
    online_query, online_detail, prod_online_update, prod_online_delete, prod_online_audit, prod_online_audit_canal, \
    online_ver_desc
from web.services.sql import wtd_save, wtd_release, wtd_update, wtd_delete, \
    get_order_no, wtd_query, wtd_detail, get_order_env, \
    get_order_type, get_order_status, get_order_handler, \
    wtd_save_uploadImage, wtd_attachment, wtd_attachment_number, \
    prod_online_save, prod_online_order_number

# 功能：我的工单
wtd = [

    (r"/order/query", orderquery),
    (r"/order/_query", order_query),
    (r"/order/_query/xh", order_query_xh),
    (r"/order/_check/xh", order_check_xh),
    (r"/order/_delete", order_delete),
    (r"/order/_update", order_update),
    (r"/wtd/_query", wtd_query),
    (r"/wtd/detail", wtd_detail),
    (r"/get/order/no", get_order_no),
    (r"/wtd/save", wtd_save),
    (r"/wtd/save/uploadImage", wtd_save_uploadImage),
    (r"/wtd/release", wtd_release),
    (r"/wtd/update", wtd_update),
    (r"/wtd/delete", wtd_delete),
    (r"/wtd/attachment", wtd_attachment),
    (r"/wtd/attachment/number", wtd_attachment_number),
    (r"/get_order_env", get_order_env),
    (r"/get_order_type", get_order_type),
    (r"/get_order_status", get_order_status),
    (r"/get_order_handler", get_order_handler),
    # online order
    (r"/online/save", prod_online_save),
    (r"/online/update", prod_online_update),
    (r"/online/delete", prod_online_delete),
    (r"/online/audit", prod_online_audit),
    (r"/online/audit_canal", prod_online_audit_canal),
    (r"/online/order_number", prod_online_order_number),
    (r"/online/_query", online_query),
    (r"/online/detail", online_detail),
    (r"/online/ver/desc", online_ver_desc),
]
