#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.model.t_dmmx  import get_sync_db_server
from   web.model.t_bbgl  import save_bbgl,save_bbgl_header,query_bbgl_header
from   web.utils import base_handler

class bbgl_add(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_add.html",
                    db_server=await get_sync_db_server(),
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


class bbgl_header_query (base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm        = self.get_argument("bbdm")
        v_list      = await query_bbgl_header(bbdm)
        v_json      = json.dumps(v_list)
        self.write(v_json)


