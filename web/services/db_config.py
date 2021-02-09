#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/9 10:19
# @Author : 马飞
# @File : db_inst.py.py
# @Software: PyCharm

import tornado.web
import json
from  web.utils.basehandler   import basehandler
from  web.model.t_db_inst     import query_inst_list
from  web.model.t_db_config   import query_db_config,update_db_config
from  web.model.t_dmmx        import get_dmm_from_dm,get_inst_names


class dbinstcfgquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./db_inst_cfg_query.html",
                    dm_env_type     = get_dmm_from_dm('03'),
                    dm_inst_names   = get_inst_names(''),
                 )

class db_inst_cfg_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        inst_env   = self.get_argument("inst_env")
        inst_id    = self.get_argument("inst_id")
        v_list     = query_db_config(inst_env,inst_id)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class db_inst_cfg_update(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_db_para = {}
        d_db_para['para_id']    = self.get_argument("para_id")
        d_db_para['para_name']  = self.get_argument("para_name")
        d_db_para['para_val']   = self.get_argument("para_val")
        print('db_inst_cfg_update=',d_db_para)
        result = update_db_config(d_db_para)
        self.write({"code": result['code'], "message": result['message']})
