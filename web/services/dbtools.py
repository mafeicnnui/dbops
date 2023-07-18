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
    db_stru_batch_gen_statement, db_stru_compare_idx, db_stru_compare_detail_idx, db_stru_compare_statement_idx, \
    db_stru_compare_data, db_gen_dict, exp_dict
from web.model.t_dmmx import get_sync_db_mysql_server, get_datax_sync_db_server_doris, get_compare_db_server, \
    get_dmm_from_dm, get_dmm_from_dm_cipher
from web.model.t_ds import db_decrypt, db_encrypt
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

class _db_compare_detail_idx(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server = self.get_argument("sour_db_server")
        sour_schema    = self.get_argument("sour_schema")
        desc_db_server = self.get_argument("desc_db_server")
        desc_schema    = self.get_argument("desc_schema")
        table          = self.get_argument("table")
        index         = self.get_argument("index")
        v_list         = await db_stru_compare_detail_idx(sour_db_server,sour_schema,desc_db_server,desc_schema,table,index)
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

class _db_compare_statement_idx(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server = self.get_argument("sour_db_server")
        sour_schema    = self.get_argument("sour_schema")
        desc_db_server = self.get_argument("desc_db_server")
        desc_schema    = self.get_argument("desc_schema")
        table          = self.get_argument("table")
        index          = self.get_argument("index")
        v_list         = await db_stru_compare_statement_idx(sour_db_server, sour_schema, desc_db_server, desc_schema,
                                                 table, index)
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


class db_compare_data(base_handler.TokenHandler):
    async def get(self):
        self.render("./tools/db_compare_data.html",
                    db_server=await get_sync_db_mysql_server(),
                    db_doris_server=await get_compare_db_server()
                    )

class _db_compare_data(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sour_db_server  = self.get_argument("sour_db_server")
        sour_schema     = self.get_argument("sour_schema")
        desc_db_server  = self.get_argument("desc_db_server")
        desc_schema     = self.get_argument("desc_schema")
        v_list          = await db_stru_compare_data(sour_db_server,sour_schema,desc_db_server,desc_schema)
        self.write({"code": 0, "message": v_list})

class db_dict(base_handler.TokenHandler):
    async def get(self):
        self.render("./tools/db_dict.html",
                    db_server=await get_sync_db_mysql_server(),
                    )

class _db_dict(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_server  = self.get_argument("db_server")
        db_schema  = self.get_argument("db_schema")
        v_list     = await db_gen_dict(db_server,db_schema)
        self.write({"code": 0, "message": v_list})


class _db_dict_exp(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_server = self.get_argument("db_server")
        db_schema = self.get_argument("db_schema")
        static_path = self.get_template_path().replace("templates", "static")
        v_list = await exp_dict(static_path,db_server, db_schema)
        self.write({"code": 0, "message": v_list})



class db_cipher(base_handler.TokenHandler):
    async def get(self):
        self.render("./tools/db_cipher.html",
                    dm_env_type  = await get_dmm_from_dm_cipher('03'),
                    )

class db_cipher_encrypt(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_env  = self.get_argument("db_env")
        plain_text  = self.get_argument("plain_text")
        res  = await db_encrypt(db_env,plain_text,self.userid)
        self.write(res)


class db_cipher_decrypt(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        db_env = self.get_argument("db_env")
        cipher_text = self.get_argument("cipher_text")
        res = await db_decrypt(db_env,cipher_text,self.userid)
        print('db_cipher_decrypt res=>',res)
        self.write(res)