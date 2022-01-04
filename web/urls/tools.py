#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.dbtools      import dict_gen,redis_migrate,db_compare,_db_compare,_db_compare_detail,_db_compare_statement,_db_compare_gen_statement,_db_compare_idx

tools = [

        (r"/dict/gen", dict_gen),
        (r"/redis/migrate", redis_migrate),
        (r"/dbtools/compare", db_compare),
        (r"/dbtools/_compare", _db_compare),
        (r"/dbtools/_compare/idx", _db_compare_idx),
        (r"/dbtools/_compare/detail", _db_compare_detail),
        (r"/dbtools/_compare/statement", _db_compare_statement),
        (r"/dbtools/_compare/gen", _db_compare_gen_statement),



]