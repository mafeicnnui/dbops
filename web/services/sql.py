#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : ma.fei
# @File : initialize.py
# @Software: PyCharm

import json
import traceback

from web.model.t_redis import query_redis, get_redis_db
from web.model.t_sql import exe_query, exe_query_aio
from web.model.t_sql_check     import query_check_result
from web.model.t_sql_release import upd_sql, exe_sql, upd_sql_run_status, save_sql, query_audit, query_run, query_order, \
    query_audit_sql, check_sql, format_sql, get_sql_release, get_order_xh, check_order_xh, update_order, query_rollback, \
    exp_rollback
from web.model.t_sql_release   import query_order_no,save_order,delete_order,query_wtd,query_wtd_detail,release_order,get_order_attachment_number,upd_order,delete_wtd,exp_sql_xls,exp_sql_pdf
from web.model.t_ds import get_dss_sql_query, get_dss_sql_run, get_dss_order, get_dss_sql_release, get_dss_sql_audit, \
    get_ds_by_dsid_by_cdb, get_dss_sql_query_type
from web.model.t_user          import get_user_by_loginame
from web.model.t_xtqx import get_tab_ddl_by_tname, get_tab_idx_by_tname, get_tree_by_dbid, get_tree_by_dbid_mssql, \
    get_tree_by_dbid_ck_proxy, get_tree_by_dbid_ck
from web.model.t_xtqx          import get_db_name,get_tab_name,get_tab_columns,get_tab_structure,get_tab_keys,get_tab_incr_col,query_ds
from web.model.t_xtqx          import get_tree_by_dbid_proxy,get_tree_by_dbid_mssql_proxy
from web.model.t_dmmx          import get_dmm_from_dm,get_users_from_proj,get_users
from web.model.t_ds            import get_ds_by_dsid
from web.utils.common          import DateEncoder,get_server
from web.utils                 import base_handler
from web.model.t_sql_export import exp_data, query_export, delete_export, save_exp_sql, export_query, update_exp_sql, \
    upd_exp_sql, query_exp_audit, del_export, get_download, export_data, query_exp_task

from web.model.t_es import get_indexes, query_es, query_es_mapping


class sqlquery(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/sql_query.html", dss= await get_dss_sql_query(self.username))

class sql_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       print('settings=', self.settings)
       #result = await exe_query(dbid,sql,curdb)
       result = await exe_query_aio(dbid, sql, curdb,self.settings['event_loop'])

       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sql_detail(base_handler.BaseHandler):
   async def get(self):
       release_id = self.get_argument("release_id")
       wkno = await get_sql_release(release_id)
       roll = await query_audit_sql(release_id)
       ds  =  await get_ds_by_dsid(wkno['dbid'])
       ds['service'] = wkno['db']
       self.render("./order/sql_detail.html",
                   wkno= json.loads(json.dumps(wkno,cls=DateEncoder)),
                   roll = json.loads(json.dumps(roll,cls=DateEncoder)),
                   dbinfo= ds['db_desc']+' ('+(ds['url']+ds['service'] if ds['url'].find(ds['service'])<0 else ds['url'])+')'
       )

class sqlrelease(base_handler.TokenHandler):
    async def get(self):
       self.render("./order/sql_release.html",
                   dss    = await get_dss_sql_release(self.username),
                   vers   = await get_dmm_from_dm('12'),
                   orders = await get_dmm_from_dm('13'),
                   )

class sql_release(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user       = await get_user_by_loginame(self.username)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       type       = self.get_argument("type")
       time       = self.get_argument("time")
       result     = await save_sql(dbid,cdb,sql,desc,user,type,time,self.username,self.request.host)
       self.write({"code": result['code'], "message": result['message']})

class sql_check(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user   = await get_user_by_loginame(self.username)
       dbid   = self.get_argument("dbid")
       cdb    = self.get_argument("cur_db")
       sql    = self.get_argument("sql")
       desc   = self.get_argument("desc")
       type   = self.get_argument("type")
       result = await check_sql(dbid,cdb,sql,desc,user,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_format(base_handler.TokenHandler):
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sql = self.get_argument("sql")
       res = format_sql(sql)
       self.write({"code": res['code'], "message": res['message']})

class sql_check_result(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user   = await get_user_by_loginame(self.username)
       v_list = await query_check_result(user)
       v_dict = {"data": v_list}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sqlaudit(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/sql_audit.html",
                   audit_dss = await get_dss_sql_audit(self.username),
                   creater = await get_users(self.username)
                   )

class sql_audit(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sqlid    = self.get_argument("sqlid")
       status   = self.get_argument("status")
       message  = self.get_argument("message")
       user     = await get_user_by_loginame(self.username)
       result   = await upd_sql(sqlid,user,status,message,self.request.host)
       self.write({"code": result['code'], "message": result['message']})

class sqlrun(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/sql_run.html",
                   run_dss = await get_dss_sql_run(self.username),
                   creater = await get_users(self.username))


class sql_run(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid    = self.get_argument("dbid")
       db_name = self.get_argument("db_name")
       sql_id  = self.get_argument("sql_id")
       result = await upd_sql_run_status(sql_id,self.username)
       self.write({"code": result['code'], "message": result['message']})


class sql_audit_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname   = self.get_argument("qname")
        dsid    = self.get_argument("dsid")
        creater = self.get_argument("creater")
        v_list  = await query_audit(qname,dsid,creater,self.userid,self.username)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class sql_run_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        creater= self.get_argument("creater")
        v_list = await query_run(qname,dsid,creater,self.userid,self.username)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sql_audit_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = await query_audit_sql(id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_tree_by_sql(base_handler.TokenHandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        msg    = self.get_argument("msg")
        p_ds   = await get_ds_by_dsid(dbid)
        result = {}
        if p_ds['db_type'] in('0','8'):
            if p_ds['proxy_status'] == '1':
                result = await get_tree_by_dbid_proxy(dbid)
            else:
                result = await get_tree_by_dbid(dbid,msg)
        elif p_ds['db_type'] == '2':
            if p_ds['proxy_status'] == '1':
                result = await get_tree_by_dbid_mssql_proxy(dbid)
            else:
                result = await get_tree_by_dbid_mssql(dbid)
        elif p_ds['db_type'] == '9':
            if p_ds['proxy_status'] == '1':
                result = await get_tree_by_dbid_ck_proxy(dbid)
            else:
                result = await get_tree_by_dbid_ck(dbid)
        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})


class get_tab_ddl(base_handler.BaseHandler):
    async def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result  = await get_tab_ddl_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_tab_idx(base_handler.BaseHandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = await get_tab_idx_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_database(base_handler.BaseHandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        result = await get_db_name(dbid)
        self.write({"code": result['code'], "message": result['message']})

class get_tables(base_handler.BaseHandler):
    async def post(self):
        dbid    = self.get_argument("dbid")
        db_name = self.get_argument("db_name")
        result  = await get_tab_name(dbid,db_name)
        self.write({"code": result['code'], "message": result['message']})

class get_dmm_dm(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dm     = self.get_argument("dm")
        v_list = await get_dmm_from_dm(dm)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_columns(base_handler.BaseHandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_columns(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})

class get_ds(base_handler.BaseHandler):
    async def post(self):
        dsid   = self.get_argument("dsid")
        result = await query_ds(dsid)
        self.write({"code": result['code'], "message": result['message']})

class get_keys(base_handler.BaseHandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_keys(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})

class get_incr_col(base_handler.BaseHandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_incr_col(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})


class get_tab_stru(base_handler.BaseHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        v_list   = await get_tab_structure(dbid,db_name,tab_name)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class orderquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./order/order_query.html",
                    order_dss     = await get_dss_order(self.username),
                    vers          = await get_dmm_from_dm('12'),
                    order_types   = await get_dmm_from_dm('17'),
                    order_handles = await get_users_from_proj(self.userid),
                    order_status  = await get_dmm_from_dm('19'),
                    creater = await get_users(self.username))

class order_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        creater = self.get_argument("creater")
        v_list = await query_order(qname,dsid,creater,self.username)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = await query_wtd(self.userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_wtd_no = self.get_argument("wtd_no")
        v_list   = await query_wtd_detail(v_wtd_no,self.userid)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class get_order_no(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        v_no = await query_order_no()
        self.write(v_no)

class get_order_env(base_handler.TokenHandler):
    async def post(self):
        name    = str(self.get_secure_cookie("username"), encoding="utf-8")
        result  = await get_dss_order(name)
        self.write({"message": result})

class get_order_type(base_handler.TokenHandler):
    async def post(self):
        result = await get_dmm_from_dm('17')
        self.write({"message": result})

class get_order_status(base_handler.TokenHandler):
    async def post(self):
        result = await get_dmm_from_dm('19')
        self.write({"message": result})

class get_order_handler(base_handler.TokenHandler):
    async def post(self):
        result = await get_users_from_proj(self.userid),
        self.write({"message": result})

class wtd_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        order_number    = self.get_argument("order_number")
        order_env       = self.get_argument("order_env")
        order_type      = self.get_argument("order_type")
        order_status    = self.get_argument("order_status")
        order_handle    = self.get_argument("order_handle")
        order_desc      = self.get_argument("order_desc")
        attachment_path = self.get_argument("attachment_path")
        attachment_name = self.get_argument("attachment_name")
        v_list          = await save_order(order_number,order_env,order_type,order_status,order_handle,order_desc,self.userid,attachment_path,attachment_name)
        v_json          = json.dumps(v_list)
        self.write(v_json)


class wtd_save_uploadImage(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path  = self.get_template_path().replace("templates", "static")
        file_metas   = self.request.files["file"]
        order_number = self.get_argument("order_number")
        try:
            i_sxh = 1
            v_path = []
            v_name = []
            for meta in file_metas:
                file_path = static_path+'/'+'assets/images/wtd'
                file_name=order_number+'_'+str(i_sxh)+'.'+meta['filename'].split('.')[-1]
                with open(file_path+'/'+file_name, 'wb') as up:
                    up.write(meta['body'])
                v_path.append('/'+'/'.join(file_path.split('/')[11:]))
                v_name.append(file_name)
                i_sxh =i_sxh +1
            self.write({"code": 0, "file_path": ','.join(v_path),"file_name":','.join(v_name)})
        except :
            traceback.print_exc()
            self.write({"code": -1, "message": '保存图片失败!'})


class wtd_release(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await release_order(wtd_no,self.userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class order_query_xh(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tp     = self.get_argument("type")
        rq     = self.get_argument("rq")
        dbid   = self.get_argument("dbid")
        v_list = await get_order_xh(tp, rq,dbid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class order_check_xh(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        message = self.get_argument("message")
        v_list  = await check_order_xh(message)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class wtd_update(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        order_number    = self.get_argument("order_number")
        order_env       = self.get_argument("order_env")
        order_type      = self.get_argument("order_type")
        order_status    = self.get_argument("order_status")
        order_handle    = self.get_argument("order_handle")
        order_desc      = self.get_argument("order_desc")
        attachment_path = self.get_argument("attachment_path")
        attachment_name = self.get_argument("attachment_name")
        v_list          = await upd_order(order_number,order_env,order_type,order_status,order_handle,order_desc,attachment_path,attachment_name)
        v_json          = json.dumps(v_list)
        self.write(v_json)

class wtd_delete(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await delete_wtd(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)


class order_delete(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        release_id = self.get_argument("release_id")
        v_list = await delete_order(release_id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class order_update(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        release_id = self.get_argument("release_id")
        run_time   = self.get_argument("run_time")
        v_list     = await update_order(release_id,run_time)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class wtd_attachment(base_handler.TokenHandler):
    async def get(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await query_wtd_detail(wtd_no, self.userid)
        v_attach = []
        for i in  range(len(v_list['attachment_path'].split(','))):
            v_attach.append([i+1,'http://{}'.format(get_server(self.request.host))+v_list['attachment_path'].split(',')[i]+'/'+v_list['attachment_name'].split(',')[i]])
        self.render("./order/order_attachment.html", order_attachments=v_attach)

class wtd_attachment_number(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await get_order_attachment_number(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)

class query_sql_release(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = await get_sql_release(id)
        v_json = json.dumps(v_list, cls=DateEncoder)
        self.write(v_json)

class sql_exp_xls(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month = self.get_argument("month")
        market_id = self.get_argument("market_id")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = await exp_sql_xls(static_path,month,market_id)
        self.write({"code": 0, "message": zipfile})

class sql_exp_pdf(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month = self.get_argument("month")
        market_id = self.get_argument("market_id")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = await exp_sql_pdf(static_path,month,market_id)
        self.write({"code": 0, "message": zipfile})


class sql_rollback_exp(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        release_id = self.get_argument("release_id")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = await exp_rollback(static_path, release_id)
        self.write({"code": 0, "message": zipfile})

'''
  SQL导出API
'''

class sql_exp_query(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/sql_export.html",
                   dss= await get_dss_sql_query(self.username),
                   creater = await get_users(self.username))

class _sql_exp_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       creater= self.get_argument("creater")
       key    = self.get_argument("key")
       v_list = await export_query(dbid,creater,key,self.username)
       v_json = json.dumps(v_list)
       self.write(v_json)

class _sql_exp_save(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user       = await get_user_by_loginame(self.username)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cdb")
       sql        = self.get_argument("sql")
       flag       = self.get_argument("flag")
       result     = await save_exp_sql(dbid,cdb,sql,flag,user)
       self.write({"code": result['code'], "message": result['message']})

class _sql_exp_update(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user = await get_user_by_loginame(self.username)
       dbid = self.get_argument("dbid")
       cdb  = self.get_argument("cdb")
       sql  = self.get_argument("sql")
       flag = self.get_argument("flag")
       id   = self.get_argument("id")
       res = await update_exp_sql(dbid,cdb,sql,flag,user,id)
       self.write({"code": res['code'], "message": res['message']})

class _sql_exp_delete(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id    = self.get_argument("id")
       res   = await delete_export(id)
       self.write({"code": res['code'], "message": res['message']})

class _sql_exp_export(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id    = self.get_argument("id")
       exp   = await query_export(id)
       path  = self.get_template_path().replace("templates", "static")
       ds    = await get_ds_by_dsid_by_cdb(exp['dbid'],exp['db'])
       res   = await exp_data(path,ds,exp['sqltext'])
       self.write({"code": res['code'], "message": res['message']})

class _sql_exp_detail(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = await query_export(id)
        v_json = json.dumps(v_list)
        print('v_json=',v_json)
        self.write(v_json)


class expaudit(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/exp_audit.html",
                   audit_dss = await get_dss_sql_audit(self.username),
                   creater = await get_users(self.username)
                   )

class exp_audit(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id    = self.get_argument("id")
       status   = self.get_argument("status")
       message  = self.get_argument("message")
       user     = await get_user_by_loginame(self.username)
       result   = await upd_exp_sql(id,user,status,message,self.request.host)
       self.write({"code": result['code'], "message": result['message']})

class exp_detail(base_handler.BaseHandler):
   async def get(self):
       release_id = self.get_argument("release_id")
       wkno = await get_sql_release(release_id)
       roll = await query_audit_sql(release_id)
       ds  =  await get_ds_by_dsid(wkno['dbid'])
       ds['service'] = wkno['db']
       self.render("./order/exp_detail.html",
                   wkno= json.loads(json.dumps(wkno,cls=DateEncoder)),
                   roll = json.loads(json.dumps(roll,cls=DateEncoder)),
                   dbinfo= ds['db_desc']+' ('+(ds['url']+ds['service'] if ds['url'].find(ds['service'])<0 else ds['url'])+')'
       )

class exp_audit_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname   = self.get_argument("qname")
        dsid    = self.get_argument("dsid")
        creater = self.get_argument("creater")
        v_list  = await query_exp_audit(qname,dsid,creater,self.userid,self.username)
        v_json  = json.dumps(v_list)
        self.write(v_json)


class sql_exp_task(base_handler.TokenHandler):
   async def get(self):
        self.render("./order/exp_task.html",
                    dss = await get_dss_sql_audit(self.username),
                    creater = await get_users(self.username))

class _sql_exp_task(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid    = self.get_argument("dbid")
       creater = self.get_argument("creater")
       key     = self.get_argument("key")
       res = await query_exp_task(dbid, creater,key)
       self.write(json.dumps(res))


class exp_export_data(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       user  = await get_user_by_loginame(self.username)
       id    = self.get_argument("id")
       path  = self.get_template_path().replace("templates", "static")
       res   = await export_data(id,user,path)
       self.write(json.dumps(res))

class exp_download(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id   = self.get_argument("id")
       res = await get_download(id)
       v_json = json.dumps(res,cls=DateEncoder)
       print(v_json)
       self.write(v_json)

class exp_export_data_delete(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       id = self.get_argument("id")
       res = await del_export(id)
       v_json = json.dumps(res, cls=DateEncoder)
       print(v_json)
       self.write(v_json)


class esquery(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/es_query.html", dss= await get_dss_sql_query_type('4'))

class es_index(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       result = await get_indexes(dbid)
       v_dict = {"code":result['code'],"data": result['data'],'message':result['message']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class es_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       index_name  = self.get_argument("index_name")
       body = self.get_argument("body")
       result = await query_es(dbid,index_name,body)
       v_dict = {"code":result['code'],"data": result['data'],'message':result['message']}
       v_json = json.dumps(v_dict,
                  cls=DateEncoder,
                  ensure_ascii=False,
                  indent=4,
                  separators=(',', ':')) + '\n'
       self.write(v_json)

class es_query_mapping(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       index_name  = self.get_argument("index_name")
       result = await query_es_mapping(dbid,index_name)
       v_dict = {"code":result['code'],"data": result['data'],'message':result['message']}
       v_json = json.dumps(v_dict,
                  cls=DateEncoder,
                  ensure_ascii=False,
                  indent=4,
                  separators=(',', ':')) + '\n'
       self.write(v_json)

class redisquery(base_handler.TokenHandler):
   async def get(self):
       self.render("./order/redis_query.html", dss= await get_dss_sql_query_type('5'))

class redis_query(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       db_name  = self.get_argument("db_name")
       key_name = self.get_argument("key_name")
       result = await query_redis(dbid,db_name,key_name)
       v_dict = {"code":result['code'],"data": result['data'],'message':result['message']}
       v_json = json.dumps(v_dict,
                           cls=DateEncoder,
                           ensure_ascii=False,
                           indent=4,
                           separators=(',', ':')) + '\n'
       self.write(v_json)

class redis_db(base_handler.TokenHandler):
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       result = await get_redis_db(dbid)
       v_dict = {"code":result['code'],"data": result['data'],'message':result['message']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

