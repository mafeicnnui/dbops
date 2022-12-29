#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.utils   import base_handler
from web.model.t_dmmx import get_dmm_from_dm, get_dmlx_from_dm_bbgl, get_dmm_from_dm_bbgl
from   web.utils.common  import DateEncoder

from   web.model.t_dmmx  import get_bbtj_db_server
from   web.model.t_bbgl  import save_bbgl,save_bbgl_header,query_bbgl_header
from   web.model.t_bbgl  import save_bbgl_filter,query_bbgl_filter
from   web.model.t_bbgl  import save_bbgl_preprocess,query_bbgl_preprocess
from   web.model.t_bbgl  import save_bbgl_statement,query_bbgl_statement
from   web.model.t_bbgl  import query_bbgl_data,get_bbgl_bbdm,get_filter,get_config
from   web.model.t_bbgl  import update_bbgl_header,delete_bbgl_header
from   web.model.t_bbgl  import update_bbgl_filter,delete_bbgl_filter
from   web.model.t_bbgl  import query_bbgl_preprocess_detail,update_bbgl_preprocess,delete_bbgl_preprocess
from   web.model.t_bbgl  import update_bbgl_statement,query_bbgl_config,delete_bbgl,export_bbgl_data,get_download,query_bbgl_export,del_export

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
        print('param=',param)
        v_list = await query_bbgl_data(bbdm,param)
        v_json = json.dumps(v_list)
        self.write(v_json)

class bbgl_query_dm (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dm   = self.get_argument("dm")
        print('dm=',dm)
        v_list = await get_dmm_from_dm_bbgl(dm)
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
        bbdm   = self.get_argument("bbdm")
        v_list = await get_config(bbdm)
        print('v_list=',v_list,type(v_list))
        v_json = json.dumps(v_list,cls=DateEncoder)
        self.write(v_json)


class bbgl_add(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_add.html",
                    db_server = await get_bbtj_db_server(),
                    dm_filter = await get_dmm_from_dm('42'),
                    dm_select_cfg = await get_dmlx_from_dm_bbgl(),
              )


class bbgl_add_save (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        bbmc        = self.get_argument("bbmc")
        dsid        = self.get_argument("dsid")
        db          = self.get_argument("db")
        v_list      = await save_bbgl(bbdm,bbmc,dsid,db,self.userid)
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
        item         = self.get_argument("item")
        v_list       = await save_bbgl_filter(bbdm,filter_name,filter_code,filter_type,item)
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
        item        = self.get_argument("item")
        cfg         = self.get_argument("cfg")
        notnull     = self.get_argument("notnull")
        is_range    = self.get_argument("is_range")
        rq_range    = self.get_argument("rq_range")
        v_list      = await update_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type,item,cfg,notnull,is_range,rq_range)
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
        v_list      = await query_bbgl_preprocess_detail(bbdm,xh)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_update_preprocess (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        statement   = self.get_argument("statement")
        description = self.get_argument("description")
        v_list      = await update_bbgl_preprocess(bbdm,xh,statement,description)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_delete_preprocess (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        xh          = self.get_argument("xh")
        v_list      = await delete_bbgl_preprocess(bbdm,xh)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_statement (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        statement = self.get_argument("statement")
        v_list      = await update_bbgl_statement(bbdm,statement)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class bbgl_change(base_handler.TokenHandler):
   async def get(self):
        self.render("./bbgl/bbgl_change.html",
                    dm_bbdm = await get_bbgl_bbdm())


class bbgl_query_config(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       bbdm   = self.get_argument("bbdm")
       v_list = await query_bbgl_config(bbdm)
       v_json = json.dumps(v_list,cls=DateEncoder)
       print('v_json=',v_json)
       self.write(v_json)

class bbgl_query_export(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       bbdm   = self.get_argument("bbdm")
       v_list = await query_bbgl_export(bbdm)
       v_json = json.dumps(v_list,cls=DateEncoder)
       print('v_json=',v_json)
       self.write(v_json)


class bbgl_edit(base_handler.TokenHandler):
   async def get(self):
        bbdm = self.get_argument("bbdm")
        print('bbgl_edit=',bbdm)
        self.render("./bbgl/bbgl_edit.html",
                    bbdm = bbdm,
                    db_server=await get_bbtj_db_server(),
                    dm_filter=await get_dmm_from_dm('42')
                    )

class bbgl_delete (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await delete_bbgl(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class bbgl_export(base_handler.TokenHandler):
   async def get(self):
        self.render("./bbgl/bbgl_export.html",
                    dm_bbdm = await get_bbgl_bbdm())

class bbgl_export_data(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       bbdm   = self.get_argument("bbdm")
       param  = self.get_argument("param")
       param  = json.loads(param)
       path   = self.get_template_path().replace("templates", "static")
       res = await export_bbgl_data(bbdm, param,self.userid,path)
       self.write(json.dumps(res))

class bbgl_download(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id   = self.get_argument("id")
       res = await get_download(id)
       v_json = json.dumps(res,cls=DateEncoder)
       print(v_json)
       self.write(v_json)

class bbgl_delete_export(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       res = await del_export(id)
       v_json = json.dumps(res, cls=DateEncoder)
       print(v_json)
       self.write(v_json)



