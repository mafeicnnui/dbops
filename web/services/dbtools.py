#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
import tornado.web
from   web.model.t_archive import query_archive_detail
from web.model.t_db_tools import db_stru_compare, db_stru_compare_detail, db_stru_compare_statement, \
    db_stru_batch_gen_statement, db_stru_compare_idx
from web.model.t_dmmx import get_sync_db_mysql_server
from web.utils import base_handler

class dict_gen(base_handler.TokenHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_query.html")

class redis_migrate(base_handler.TokenHandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archive_id")
        v_list      = query_archive_detail(archive_id)
        v_json      = json.dumps(v_list)
        print('archive_query_detail=',v_json)
        self.write({"code": 0, "message": v_json})

class db_compare(base_handler.TokenHandler):
    async def get(self):
        self.render("./tools/db_compare.html",
                    db_server=await get_sync_db_mysql_server(),
                    )

class _db_compare(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server  = self.get_argument("sour_db_server")
        sour_schema     = self.get_argument("sour_schema")
        desc_db_server  = self.get_argument("desc_db_server")
        desc_schema     = self.get_argument("desc_schema")
        sour_tab        = self.get_argument("sour_tab")
        v_list          = await db_stru_compare(sour_db_server,sour_schema,desc_db_server,desc_schema,sour_tab)
        self.write({"code": 0, "message": v_list})


class _db_compare_idx(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server  = self.get_argument("sour_db_server")
        sour_schema     = self.get_argument("sour_schema")
        desc_db_server  = self.get_argument("desc_db_server")
        desc_schema     = self.get_argument("desc_schema")
        sour_tab        = self.get_argument("sour_tab")
        v_list          = await db_stru_compare_idx(sour_db_server,sour_schema,desc_db_server,desc_schema,sour_tab)
        self.write({"code": 0, "message": v_list})


class _db_compare_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server = self.get_argument("sour_db_server")
        sour_schema    = self.get_argument("sour_schema")
        desc_db_server = self.get_argument("desc_db_server")
        desc_schema    = self.get_argument("desc_schema")
        table          = self.get_argument("table")
        column         = self.get_argument("column")
        v_list         = await db_stru_compare_detail(sour_db_server,sour_schema,desc_db_server,desc_schema,table,column)
        self.write({"code": 0, "message": v_list})


class _db_compare_statement(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server = self.get_argument("sour_db_server")
        sour_schema    = self.get_argument("sour_schema")
        desc_db_server = self.get_argument("desc_db_server")
        desc_schema    = self.get_argument("desc_schema")
        table          = self.get_argument("table")
        column         = self.get_argument("column")
        v_list         = await db_stru_compare_statement(sour_db_server,sour_schema,desc_db_server,desc_schema,table,column)
        self.write({"code": 0, "message": v_list})

class _db_compare_gen_statement(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server = self.get_argument("sour_db_server")
        sour_schema    = self.get_argument("sour_schema")
        desc_db_server = self.get_argument("desc_db_server")
        desc_schema    = self.get_argument("desc_schema")
        table          = self.get_argument("sour_tab")
        v_list         = await db_stru_batch_gen_statement(sour_db_server,sour_schema,desc_db_server,desc_schema,table)
        print('_db_compare_gen_statement=',v_list)
        self.write({"code": 0, "message": v_list})
