#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm
from web.services.sql          import orderquery,order_query
from web.services.sql          import wtd_save,wtd_release,wtd_update,wtd_delete,get_order_no,wtd_query,wtd_detail,get_order_env,get_order_type,get_order_status,get_order_handler,wtd_save_uploadImage,wtd_attachment,wtd_attachment_number

# 功能：我的工单API
wtd = [

        (r"/order/query", orderquery),
        (r"/order/_query", order_query),
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
]