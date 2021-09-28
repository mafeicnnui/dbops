#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
import traceback
import tornado.web
from   web.model.t_port      import query_port,save_port,get_port_by_portid,upd_port,del_port,imp_port,exp_port
from   web.model.t_dmmx      import get_dmm_from_dm
from web.utils               import base_handler

class portquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./port/port_query.html",
                    dm_proj_type= await get_dmm_from_dm('05'),)

class port_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        v_list     = await query_port(market_id)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class portadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./port/port_add.html",
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_mapping_type = await get_dmm_from_dm('35'),
                   )

class portadd_save(base_handler.TokenHandler):
    async def post(self):
        d_port  = {}
        d_port['market_id']      = self.get_argument("market_id")
        d_port['market_name']    = self.get_argument("market_name")
        d_port['app_desc']       = self.get_argument("app_desc")
        d_port['local_ip']       = self.get_argument("local_ip")
        d_port['local_port']     = self.get_argument("local_port")
        d_port['mapping_port']   = self.get_argument("mapping_port")
        d_port['mapping_domain'] = self.get_argument("mapping_domain")
        d_port['mapping_type']   = self.get_argument("mapping_type")
        d_port['creater']        = str(self.get_secure_cookie("username"), encoding="utf-8")
        result = await save_port(d_port)
        self.write({"code": result['code'], "message": result['message']})

class portchange(base_handler.TokenHandler):
    async def get(self):
        self.render("./port/port_change.html",
                    dm_proj_type = await get_dmm_from_dm('05'))

class portedit(base_handler.TokenHandler):
    async def get(self):
        port_id  = self.get_argument("port_id")
        d_port   = await get_port_by_portid(port_id)
        self.render("./port/port_edit.html",
                    p_port=d_port,
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_mapping_type = await get_dmm_from_dm('35'))

class portedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_port = {}
        d_port['port_id']          = self.get_argument("port_id")
        d_port['market_id']        = self.get_argument("market_id")
        d_port['market_name']      = self.get_argument("market_name")
        d_port['app_desc']         = self.get_argument("app_desc")
        d_port['local_ip']         = self.get_argument("local_ip")
        d_port['local_port']       = self.get_argument("local_port")
        d_port['mapping_port']     = self.get_argument("mapping_port")
        d_port['mapping_domain']   = self.get_argument("mapping_domain")
        d_port['mapping_type']     = self.get_argument("mapping_type")
        result = await upd_port(d_port)
        self.write({"code": result['code'], "message": result['message']})

class portedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        port_id  = self.get_argument("port_id")
        result   = await del_port(port_id)
        self.write({"code": result['code'], "message": result['message']})

class portedit_imp(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        user_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas  = self.request.files["file"]
        try:
            for meta in file_metas:
                file_path = static_path + '/' + 'uploads/port/'
                file_name = meta['filename'].split(' ')[-1]
                with open(file_path + '/' + file_name, 'wb') as up:
                    up.write(meta['body'])
            result = await imp_port(file_path+file_name,user_name)
            self.write({"code": result['code'], "message": result['message']})
        except :
            traceback.print_exc()
            self.write({"code": -1, "message": '导入失败!'})


class portedit_exp(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = await exp_port(static_path)
        self.write({"code": 0, "message": zipfile})