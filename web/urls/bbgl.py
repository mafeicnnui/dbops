#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.bbgl  import bbgl_add,bbgl_add_save,bbgl_add_header_save,bbgl_header_query

bbgl = [
        (r"/bbgl/add", bbgl_add),
        (r"/bbgl/add/save", bbgl_add_save),
        (r"/bbgl/add/header/save", bbgl_add_header_save),
        (r"/bbgl/header/query", bbgl_header_query),

 ]
