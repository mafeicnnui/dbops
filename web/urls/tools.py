#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.dbtools      import dict_gen,redis_migrate,db_compare,_db_compare,_db_compare_detail

tools = [

        (r"/dict/gen", dict_gen),
        (r"/redis/migrate", redis_migrate),
        (r"/dbtools/compare", db_compare),
        (r"/dbtools/_compare", _db_compare),
        (r"/dbtools/_compare/detail", _db_compare_detail),

]