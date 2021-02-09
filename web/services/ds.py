#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据源管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_ds    import get_ds_by_dsid,query_ds,save_ds,upd_ds,del_ds,check_ds_valid
from   web.model.t_dmmx  import get_dmm_from_dm,get_sync_db_server_by_type
from   web.utils.basehandler import basehandler

class dsquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./ds_query.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_env_type=get_dmm_from_dm('03'))

class ds_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsname     = self.get_argument("dsname")
        market_id  = self.get_argument("market_id")
        db_env     = self.get_argument("db_env")
        ds_type    = self.get_argument("ds_type")
        v_list     = query_ds(dsname,market_id,db_env,ds_type)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class ds_query_id(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsid       = self.get_argument("dsid")
        v_list     = get_ds_by_dsid(dsid)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class dsadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./ds_add.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_db_type=get_dmm_from_dm('02'),
                    dm_inst_type=get_dmm_from_dm('07'),
                    dm_env_type=get_dmm_from_dm('03'),
                    dm_ds_proxy=get_dmm_from_dm('26')
                    )

class dsadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_ds={}
        d_ds['market_id']    = self.get_argument("market_id")
        d_ds['db_type']      = self.get_argument("db_type")
        d_ds['db_env']       = self.get_argument("db_env")
        d_ds['db_desc']      = self.get_argument("db_desc")
        d_ds['inst_type']    = self.get_argument("inst_type")
        d_ds['ip']           = self.get_argument("ip")
        d_ds['port']         = self.get_argument("port")
        d_ds['service']      = self.get_argument("service")
        d_ds['user']         = self.get_argument("user")
        d_ds['pass']         = self.get_argument("pass")
        d_ds['status']       = self.get_argument("status")
        d_ds['proxy_status'] = self.get_argument("proxy_status")
        d_ds['proxy_server'] = self.get_argument("proxy_server")
        result=save_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})

class dschange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./ds_change.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_env_type=get_dmm_from_dm('03'))

class dsedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        dsid   = self.get_argument("dsid")
        d_ds   = get_ds_by_dsid(dsid)
        self.render("./ds_edit.html",
                     dsid         = d_ds['dsid'],
                     market_id    = d_ds['market_id'],
                     inst_type    = d_ds['inst_type'],
                     db_type      = d_ds['db_type'],
                     db_env       = d_ds['db_env'],
                     dm_db_type   = get_dmm_from_dm('02'),
                     dm_db_env    = get_dmm_from_dm('03'),
                     dm_inst_type = get_dmm_from_dm('07'),
                     dm_proj_type = get_dmm_from_dm('05'),
                     dm_ds_proxy  = get_dmm_from_dm('26'),
                     db_desc      = d_ds['db_desc'],
                     ip           = d_ds['ip'],
                     port         = d_ds['port'],
                     service      = d_ds['service'],
                     user         = d_ds['user'],
                     password     = d_ds['password'],
                     status       = d_ds['status'],
                     proxy_status = d_ds['proxy_status'],
                     proxy_server = d_ds['proxy_server'],
                    )

class dsedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_ds={}
        d_ds['dsid']         = self.get_argument("dsid")
        d_ds['market_id']    = self.get_argument("market_id")
        d_ds['inst_type']    = self.get_argument("inst_type")
        d_ds['db_type']      = self.get_argument("db_type")
        d_ds['db_env']       = self.get_argument("db_env")
        d_ds['db_desc']      = self.get_argument("db_desc")
        d_ds['ip']           = self.get_argument("ip")
        d_ds['port']         = self.get_argument("port")
        d_ds['service']      = self.get_argument("service")
        d_ds['user']         = self.get_argument("user")
        d_ds['pass']         = self.get_argument("pass")
        d_ds['status']       = self.get_argument("status")
        d_ds['proxy_status'] = self.get_argument("proxy_status")
        d_ds['proxy_server'] = self.get_argument("proxy_server")
        result=upd_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})


class dsclone(basehandler):
    @tornado.web.authenticated
    def get(self):
        dsid=self.get_argument("dsid")
        d_ds      =get_ds_by_dsid(dsid)
        self.render("./ds_clone.html",
                     market_id    = d_ds['market_id'],
                     inst_type    = d_ds['inst_type'],
                     db_type      = d_ds['db_type'],
                     db_env       = d_ds['db_env'],
                     dm_db_type   =  get_dmm_from_dm('02'),
                     dm_db_env    =  get_dmm_from_dm('03'),
                     dm_inst_type = get_dmm_from_dm('07'),
                     dm_proj_type = get_dmm_from_dm('05'),
                     dm_ds_proxy  = get_dmm_from_dm('26'),
                     db_desc      = d_ds['db_desc'],
                     ip           = d_ds['ip'],
                     port         = d_ds['port'],
                     service      = d_ds['service'],
                     user         = d_ds['user'],
                     password     = d_ds['password'],
                     status       = d_ds['status'],
                     proxy_status = d_ds['proxy_status'],
                     proxy_server = d_ds['proxy_server'],
                    )

class dsclone_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_ds={}
        d_ds['market_id']    = self.get_argument("market_id")
        d_ds['inst_type']    = self.get_argument("inst_type")
        d_ds['db_type']      = self.get_argument("db_type")
        d_ds['db_env']       = self.get_argument("db_env")
        d_ds['db_desc']      = self.get_argument("db_desc")
        d_ds['ip']           = self.get_argument("ip")
        d_ds['port']         = self.get_argument("port")
        d_ds['service']      = self.get_argument("service")
        d_ds['user']         = self.get_argument("user")
        d_ds['pass']         = self.get_argument("pass")
        d_ds['status']       = self.get_argument("status")
        d_ds['proxy_status'] = self.get_argument("proxy_status")
        d_ds['proxy_server'] = self.get_argument("proxy_server")
        result=save_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})


class dsedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsid  = self.get_argument("dsid")
        result=del_ds(dsid)
        self.write({"code": result['code'], "message": result['message']})

class dstest(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./ds_test.html",
                    dm_proj_type=get_dmm_from_dm('05'),
                    dm_env_type=get_dmm_from_dm('03')
                    )

class ds_check_valid(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       result = check_ds_valid(id)
       self.write({"code": result['code'], "message": result['message']})

class get_db_by_type(basehandler):
    @tornado.web.authenticated
    def post(self):
        db_type  = self.get_argument("db_type")
        result = get_sync_db_server_by_type(db_type)
        self.write({"code": result['code'], "message": result['message']})
