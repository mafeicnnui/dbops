#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.model.t_dmmx  import get_sync_db_server
from   web.model.t_bbgl  import save_bbgl,save_bbgl_header,query_bbgl_header
from   web.model.t_bbgl  import save_bbgl_filter,query_bbgl_filter
from   web.model.t_bbgl  import save_bbgl_preprocess,query_bbgl_preprocess
from   web.model.t_bbgl  import save_bbgl_statement,query_bbgl_statement
from   web.model.t_bbgl  import query_bbgl_data,get_bbgl_bbdm,get_filter,get_config
from   web.model.t_bbgl  import update_bbgl_header,delete_bbgl_header
from   web.model.t_bbgl  import update_bbgl_filter,delete_bbgl_filter

from   web.utils import base_handler
from   web.model.t_dmmx    import get_dmm_from_dm
from   web.utils.common import DateEncoder

class bbgl_query(base_handler.TokenHandler):
   async def get(self):
        self.render("./bbgl/bbgl_query.html",
                    dm_bbdm = await get_bbgl_bbdm())

class bbgl_query_data (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm   = self.get_argument("bbdm")
        param  = self.get_argument("param")
        param  = json.loads(param)
        v_list = await query_bbgl_data(bbdm,param)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_filter(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await get_filter(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)

class bbgl_config(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await get_config(bbdm)
        v_json = json.dumps(v_list,cls=DateEncoder)
        self.write(v_json)


class bbgl_add(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_add.html",
                    db_server = await get_sync_db_server(),
                    dm_filter = await get_dmm_from_dm('42'),
              )

class bbgl_add_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        bbmc        = self.get_argument("bbmc")
        dsid        = self.get_argument("dsid")
        v_list      = await save_bbgl(bbdm,bbmc,dsid,self.userid)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_add_header_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        name        = self.get_argument("name")
        width       = self.get_argument("width")
        v_list      = await save_bbgl_header(bbdm,name,width)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_add_filter_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm         = self.get_argument("bbdm")
        filter_name  = self.get_argument("name")
        filter_code  = self.get_argument("code")
        filter_type  = self.get_argument("type")
        v_list       = await save_bbgl_filter(bbdm,filter_name,filter_code,filter_type)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class bbgl_add_preprocess_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm         = self.get_argument("bbdm")
        statement    = self.get_argument("statement")
        description  = self.get_argument("description")

        print('bbgl_add_preprocess_save=', bbdm, statement, description)
        print('bbgl_add_preprocess_save2=', bbdm)
        print('bbgl_add_preprocess_save3=', statement)
        print('bbgl_add_preprocess_save=4', description)



        v_list       = await save_bbgl_preprocess(bbdm,statement,description)
        v_json       = json.dumps(v_list)
        self.write(v_json)

class bbgl_add_statement_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm         = self.get_argument("bbdm")
        statement    = self.get_argument("statement")
        v_list       = await save_bbgl_statement(bbdm,statement)
        v_json       = json.dumps(v_list)
        self.write(v_json)


class bbgl_header_query (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await query_bbgl_header(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_filter_query (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await query_bbgl_filter(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_preprocess_query (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await query_bbgl_preprocess(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_statement_query (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await query_bbgl_statement(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_header (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm      = self.get_argument("bbdm")
        xh        = self.get_argument("xh")
        name      = self.get_argument("name")
        width     = self.get_argument("width")
        v_list    = await update_bbgl_header(bbdm,xh,name,width)
        v_json    = json.dumps(v_list)
        self.write(v_json)

class bbgl_delete_header (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh        = self.get_argument("xh")
        v_list      = await delete_bbgl_header(bbdm,xh)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_filter (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        v_list      = await update_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_delete_filter (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        v_list      = await delete_bbgl_filter(bbdm,xh)
        v_json      = json.dumps(v_list)
        self.write(v_json)



class bbgl_query_preprocess (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        v_list      = await update_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_update_preprocess (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        v_list      = await update_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_delete_preprocess (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        v_list      = await delete_bbgl_filter(bbdm,xh)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_statement (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        v_list      = await update_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type)
        v_json      = json.dumps(v_list)
        self.write(v_json)
