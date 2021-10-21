#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.model.t_ds    import get_ds_by_dsid,query_ds,save_ds,upd_ds,del_ds,check_ds_valid,get_dss_sql_query,exe_query
from   web.model.t_dmmx  import get_dmm_from_dm,get_sync_db_server_by_type,get_sync_db_server
from web.utils           import base_handler

class dsquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./ds/ds_query.html",
                    dm_proj_type=await get_dmm_from_dm('05'),
                    dm_env_type=await get_dmm_from_dm('03'))

class ds_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsname     = self.get_argument("dsname")
        market_id  = self.get_argument("market_id")
        db_env     = self.get_argument("db_env")
        ds_type    = self.get_argument("ds_type")
        v_list     = await query_ds(dsname,market_id,db_env,ds_type)
        v_json     = json.dumps(v_list)
        self.write(v_json)

class ds_sql_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dsid   = self.get_argument("dsid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       result = await exe_query(self.userid,dsid,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)


class ds_query_id(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsid    = self.get_argument("dsid")
        v_list  = await get_ds_by_dsid(dsid)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class dsadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./ds/ds_add.html",
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_db_type   = await get_dmm_from_dm('02'),
                    dm_inst_type = await get_dmm_from_dm('07'),
                    dm_env_type  = await get_dmm_from_dm('03'),
                    dm_ds_proxy  = await get_dmm_from_dm('26'),
                    db_server    = await get_sync_db_server(),
                    )

class dsadd_save(base_handler.TokenHandler):
    async def post(self):
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
        d_ds['read_db']      = self.get_argument("read_db")
        d_ds['stream_load']  = self.get_argument("stream_load")
        result = await save_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})

class dschange(base_handler.TokenHandler):
    async def get(self):
        self.render("./ds/ds_change.html",
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_env_type = await get_dmm_from_dm('03'))

class dsconsole(base_handler.TokenHandler):
    async def get(self):
        dsid = self.get_argument("dsid")
        dss = await get_ds_by_dsid(dsid)
        self.render("./ds/ds_console.html", dss = dss)

class dsedit(base_handler.TokenHandler):
    async def get(self):
        dsid   = self.get_argument("dsid")
        d_ds   = await get_ds_by_dsid(dsid)
        print('ds=',d_ds)
        self.render("./ds/ds_edit.html",
                     dsid         = d_ds['dsid'],
                     market_id    = d_ds['market_id'],
                     inst_type    = d_ds['inst_type'],
                     db_type      = d_ds['db_type'],
                     db_env       = d_ds['db_env'],
                     dm_db_type   = await get_dmm_from_dm('02'),
                     dm_db_env    = await get_dmm_from_dm('03'),
                     dm_inst_type = await get_dmm_from_dm('07'),
                     dm_proj_type = await get_dmm_from_dm('05'),
                     dm_ds_proxy  = await get_dmm_from_dm('26'),
                     db_server    = await get_sync_db_server(),
                     db_desc      = d_ds['db_desc'],
                     ip           = d_ds['ip'],
                     port         = d_ds['port'],
                     service      = d_ds['service'],
                     user         = d_ds['user'],
                     password     = d_ds['password'],
                     status       = d_ds['status'],
                     proxy_status = d_ds['proxy_status'],
                     proxy_server = d_ds['proxy_server'],
                     read_db      = d_ds['id_ro'],
                     stream_load  = d_ds['stream_load'],
                    )

class dsedit_save(base_handler.TokenHandler):
    async def post(self):
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
        d_ds['read_db']      = self.get_argument("read_db")
        d_ds['stream_load']  = self.get_argument("stream_load")
        result = await upd_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})

class dsclone(base_handler.TokenHandler):
    async def get(self):
        dsid = self.get_argument("dsid")
        d_ds = await get_ds_by_dsid(dsid)
        self.render("./ds/ds_clone.html",
                     market_id    = d_ds['market_id'],
                     inst_type    = d_ds['inst_type'],
                     db_type      = d_ds['db_type'],
                     db_env       = d_ds['db_env'],
                     dm_db_type   = await get_dmm_from_dm('02'),
                     dm_db_env    = await get_dmm_from_dm('03'),
                     dm_inst_type = await get_dmm_from_dm('07'),
                     dm_proj_type = await get_dmm_from_dm('05'),
                     dm_ds_proxy  = await get_dmm_from_dm('26'),
                     db_desc      = d_ds['db_desc'],
                     ip           = d_ds['ip'],
                     port         = d_ds['port'],
                     service      = d_ds['service'],
                     user         = d_ds['user'],
                     password     = d_ds['password'],
                     status       = d_ds['status'],
                     proxy_status = d_ds['proxy_status'],
                     proxy_server = d_ds['proxy_server'],
                     stream_load  = d_ds['stream_load'],
                    )


class dsclone_save(base_handler.TokenHandler):
    async def post(self):
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
        d_ds['stream_load']  = self.get_argument("stream_load")
        result = await save_ds(d_ds)
        self.write({"code": result['code'], "message": result['message']})

class dsedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dsid   = self.get_argument("dsid")
        result = await del_ds(dsid)
        self.write({"code": result['code'], "message": result['message']})

class dstest(base_handler.TokenHandler):
    async def get(self):
        self.render("./ds/ds_test.html",
                    dm_proj_type = await get_dmm_from_dm('05'),
                    dm_env_type  = await get_dmm_from_dm('03')
                    )

class ds_check_valid(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       result = await check_ds_valid(id)
       self.write({"code": result['code'], "message": result['message']})

class get_db_by_type(base_handler.TokenHandler):
    async def post(self):
        db_type = self.get_argument("db_type")
        result  = await get_sync_db_server_by_type(db_type)
        self.write({"code": result['code'], "message": result['message']})
