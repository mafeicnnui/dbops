#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.dbtools      import dict_gen,redis_migrate

# 功能：数据库工具API
tools = [

        (r"/dict/gen", dict_gen),
        (r"/redis/migrate", redis_migrate),
]