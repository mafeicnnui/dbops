#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
import tornado.web
from   web.model.t_archive import query_archive_detail
from   web.utils.basehandler import basehandler

class dict_gen(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_query.html")


class redis_migrate(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archive_id")
        v_list      = query_archive_detail(archive_id)
        v_json      = json.dumps(v_list)
        print('archive_query_detail=',v_json)
        self.write({"code": 0, "message": v_json})
