#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据库备份管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_user import get_users
from   web.model.t_port import query_port,save_port,get_port_by_portid,upd_port,del_port,imp_port,exp_port
from   web.utils.basehandler import basehandler
from   web.model.t_dmmx  import get_dmm_from_dm

class portquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./port_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),)

class port_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        market_id  = self.get_argument("market_id")
        v_list    = query_port(market_id)
        v_json    = json.dumps(v_list)
        self.write(v_json)

class portadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./port_add.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_mapping_type=get_dmm_from_dm('35'),
                   )

class portadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        result=save_port(d_port)
        self.write({"code": result['code'], "message": result['message']})

class portchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./port_change.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    )

class portedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        port_id  = self.get_argument("port_id")
        d_port   = get_port_by_portid(port_id)
        self.render("./port_edit.html",
                    p_port=d_port,
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_mapping_type=get_dmm_from_dm('35'))

class portedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
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
        result=upd_port(d_port)
        self.write({"code": result['code'], "message": result['message']})

class portedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        port_id  = self.get_argument("port_id")
        result   = del_port(port_id)
        self.write({"code": result['code'], "message": result['message']})

class portedit_imp(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        user_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas  = self.request.files["file"]
        try:
            for meta in file_metas:
                file_path = static_path + '/' + 'uploads/port/'
                file_name = meta['filename'].split(' ')[-1]
                print('file_path=', file_path)
                print('file_name=', file_name)
                with open(file_path + '/' + file_name, 'wb') as up:
                    up.write(meta['body'])
            result = imp_port(file_path+file_name,user_name)
            self.write({"code": result['code'], "message": result['message']})
        except Exception as e:
            print(e)
            self.write({"code": -1, "message": '导入失败' + str(e)})


class portedit_exp(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = exp_port(static_path)
        print('portedit_exp=', zipfile)
        self.write({"code": 0, "message": zipfile})