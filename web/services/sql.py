#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:14
# @Author : ma.fei
# @File : initialize.py
# @Software: PyCharm

import json
import tornado.web
import threading
import traceback

from web.model.t_sql           import exe_query
from web.model.t_sql_check     import query_check_result
from web.model.t_sql_release   import upd_sql,exe_sql,upd_sql_run_status,save_sql,query_audit,query_run,query_order,query_audit_sql,check_sql,format_sql,get_sql_release,get_order_xh,check_order_xh,update_order
from web.model.t_sql_release   import query_order_no,save_order,delete_order,query_wtd,query_wtd_detail,release_order,get_order_attachment_number,upd_order,delete_wtd
from web.model.t_ds            import get_dss_sql_query,get_dss_sql_run,get_dss_order,get_dss_sql_release,get_dss_sql_audit
from web.model.t_user          import get_user_by_loginame
from web.model.t_xtqx          import get_tab_ddl_by_tname,get_tab_idx_by_tname,get_tree_by_dbid,get_tree_by_dbid_mssql
from web.model.t_xtqx          import get_db_name,get_tab_name,get_tab_columns,get_tab_structure,get_tab_keys,get_tab_incr_col,query_ds
from web.model.t_xtqx          import get_tree_by_dbid_proxy,get_tree_by_dbid_mssql_proxy
from web.model.t_dmmx          import get_dmm_from_dm,get_users_from_proj,get_users
from web.utils.basehandler     import basehandler
from web.model.t_ds            import get_ds_by_dsid
from web.utils.common          import DateEncoder

class sqlquery(basehandler):
   @tornado.web.authenticated
   async def get(self):
       name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./order/sql_query.html", dss= await get_dss_sql_query(name))

class sql_query(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid   = self.get_argument("dbid")
       sql    = self.get_argument("sql")
       curdb  = self.get_argument("cur_db")
       print(curdb,dbid,sql)
       result = await exe_query(dbid,sql,curdb)
       v_dict = {"data": result['data'],"column":result['column'],"status":result['status'],"msg":result['msg']}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sql_detail(basehandler):
   async def get(self):
       release_id = self.get_argument("release_id")
       wkno = await get_sql_release(release_id)
       roll = await query_audit_sql(release_id)
       ds  = await get_ds_by_dsid(wkno['dbid'])
       ds['service'] = wkno['db']
       self.render("./order/sql_detail.html",
                   wkno= json.loads(json.dumps(wkno,cls=DateEncoder)),
                   roll = json.loads(json.dumps(roll,cls=DateEncoder)),
                   dbinfo= ds['db_desc']+' ('+(ds['url']+ds['service'] if ds['url'].find(ds['service'])<0 else ds['url'])+')'
       )


class sqlrelease(basehandler):
    @tornado.web.authenticated
    async def get(self):
       name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./order/sql_release.html",
                   dss    = await get_dss_sql_release(name),
                   vers   = await get_dmm_from_dm('12'),
                   orders = await get_dmm_from_dm('13'),
                   )

class sql_release(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       name       = str(self.get_secure_cookie("username"), encoding="utf-8")
       user       = await get_user_by_loginame(name)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       type       = self.get_argument("type")
       time       = self.get_argument("time")
       result     = await save_sql(dbid,cdb,sql,desc,user,type,time,name,self.request.host)
       self.write({"code": result['code'], "message": result['message']})

class sql_check(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       name       = str(self.get_secure_cookie("username"), encoding="utf-8")
       user       = await get_user_by_loginame(name)
       dbid       = self.get_argument("dbid")
       cdb        = self.get_argument("cur_db")
       sql        = self.get_argument("sql")
       desc       = self.get_argument("desc")
       type       = self.get_argument("type")
       result     = await check_sql(dbid,cdb,sql,desc,user,type)
       self.write({"code": result['code'], "message": result['message']})

class sql_format(basehandler):
   @tornado.web.authenticated
   def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       sql   = self.get_argument("sql")
       res   = format_sql(sql)
       self.write({"code": res['code'], "message": res['message']})

class sql_check_result(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       name = str(self.get_secure_cookie("username"), encoding="utf-8")
       user   = await get_user_by_loginame(name)
       v_list = await query_check_result(user)
       v_dict = {"data": v_list}
       v_json = json.dumps(v_dict)
       self.write(v_json)

class sqlaudit(basehandler):
   @tornado.web.authenticated
   async def get(self):
       name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./order/sql_audit.html",
                   audit_dss = await get_dss_sql_audit(name),
                   creater = await get_users(name)
                   )

class sql_audit(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       name     = str(self.get_secure_cookie("username"), encoding="utf-8")
       sqlid    = self.get_argument("sqlid")
       status   = self.get_argument("status")
       message  = self.get_argument("message")
       result   = await upd_sql(sqlid,name,status,message,self.request.host)
       self.write({"code": result['code'], "message": result['message']})

class sqlrun(basehandler):
   @tornado.web.authenticated
   async def get(self):
       name = str(self.get_secure_cookie("username"), encoding="utf-8")
       self.render("./order/sql_run.html",
                   run_dss = await get_dss_sql_run(name),
                   creater = await get_users(name))


class sql_run(basehandler):
   @tornado.web.authenticated
   async def post(self):
       self.set_header("Content-Type", "application/json; charset=UTF-8")
       dbid    = self.get_argument("dbid")
       db_name = self.get_argument("db_name")
       sql_id  = self.get_argument("sql_id")
       print('request.host=',self.request.host,self.request.path)
       # result = await exe_sql(dbid, db_name, sql_id, name,self.request.host)
       result = await upd_sql_run_status(sql_id)
       self.write({"code": result['code'], "message": result['message']})


class sql_audit_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname   = self.get_argument("qname")
        dsid    = self.get_argument("dsid")
        creater = self.get_argument("creater")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        username= str(self.get_secure_cookie("username"), encoding="utf-8")
        v_list  = await query_audit(qname,dsid,creater,userid,username)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class sql_run_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        creater= self.get_argument("creater")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        username= str(self.get_secure_cookie("username"), encoding="utf-8")
        v_list = await query_run(qname,dsid,creater,userid,username)
        v_json = json.dumps(v_list)
        self.write(v_json)


class sql_audit_detail(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = await query_audit_sql(id)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_tree_by_sql(basehandler):
    @tornado.web.authenticated
    async def post(self):
        dbid   = self.get_argument("dbid")
        msg    = self.get_argument("msg")
        p_ds   = await get_ds_by_dsid(dbid)
        result = {}
        if p_ds['db_type'] == '0':
            if p_ds['proxy_status'] == '1':
                result = await get_tree_by_dbid_proxy(dbid)
            else:
                result = await get_tree_by_dbid(dbid,msg)
        elif p_ds['db_type'] == '2':
            if p_ds['proxy_status'] == '1':
                result = await get_tree_by_dbid_mssql_proxy(dbid)
            else:
                result = await get_tree_by_dbid_mssql(dbid)
        self.write({"code": result['code'], "message": result['message'], "url": result['db_url'],"desc":result['desc']})


class get_tab_ddl(basehandler):
    async def post(self):
        dbid    = self.get_argument("dbid")
        cur_db  = self.get_argument("cur_db")
        tab     = self.get_argument("tab")
        result  = await get_tab_ddl_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_tab_idx(basehandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        cur_db = self.get_argument("cur_db")
        tab    = self.get_argument("tab")
        result = await get_tab_idx_by_tname(dbid,tab,cur_db)
        self.write({"code": result['code'], "message": result['message']})

class get_database(basehandler):
    async def post(self):
        dbid   = self.get_argument("dbid")
        result = await get_db_name(dbid)
        self.write({"code": result['code'], "message": result['message']})

class get_tables(basehandler):
    async def post(self):
        dbid    = self.get_argument("dbid")
        db_name = self.get_argument("db_name")
        result  = await get_tab_name(dbid,db_name)
        self.write({"code": result['code'], "message": result['message']})

class get_dmm_dm(basehandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dm     = self.get_argument("dm")
        v_list = await get_dmm_from_dm(dm)
        v_json = json.dumps(v_list)
        self.write(v_json)

class get_columns(basehandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_columns(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})

class get_ds(basehandler):
    async def post(self):
        dsid   = self.get_argument("dsid")
        result = await query_ds(dsid)
        self.write({"code": result['code'], "message": result['message']})

class get_keys(basehandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_keys(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})

class get_incr_col(basehandler):
    async def post(self):
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        result   = await get_tab_incr_col(dbid,db_name,tab_name)
        self.write({"code": result['code'], "message": result['message']})


class get_tab_stru(basehandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dbid     = self.get_argument("dbid")
        db_name  = self.get_argument("db_name")
        tab_name = self.get_argument("tab_name")
        v_list   = await get_tab_structure(dbid,db_name,tab_name)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class orderquery(basehandler):
    @tornado.web.authenticated
    async def get(self):
        user_name = str(self.get_secure_cookie("username"), encoding="utf-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        self.render("./order/order_query.html",
                    order_dss     = await get_dss_order(user_name),
                    vers          = await get_dmm_from_dm('12'),
                    order_types   = await get_dmm_from_dm('17'),
                    order_handles = await get_users_from_proj(userid),
                    order_status  = await get_dmm_from_dm('19'),
                    creater = await get_users(user_name))

class order_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        username = str(self.get_secure_cookie("username"), encoding="utf-8")
        qname  = self.get_argument("qname")
        dsid   = self.get_argument("dsid")
        creater = self.get_argument("creater")
        v_list = await query_order(qname,dsid,creater,username)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_query(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_list = await query_wtd(userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class wtd_detail(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid   = str(self.get_secure_cookie("userid"), encoding="utf-8")
        v_wtd_no = self.get_argument("wtd_no")
        v_list   = await query_wtd_detail(v_wtd_no,userid)
        v_json   = json.dumps(v_list)
        self.write(v_json)

class get_order_no(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        v_no = await query_order_no()
        self.write(v_no)

class get_order_env(basehandler):
    @tornado.web.authenticated
    async def post(self):
        name    = str(self.get_secure_cookie("username"), encoding="utf-8")
        result  = await get_dss_order(name)
        self.write({"message": result})

class get_order_type(basehandler):
    @tornado.web.authenticated
    async def post(self):
        result = await get_dmm_from_dm('17')
        self.write({"message": result})

class get_order_status(basehandler):
    @tornado.web.authenticated
    async def post(self):
        result = await get_dmm_from_dm('19')
        self.write({"message": result})

class get_order_handler(basehandler):
    @tornado.web.authenticated
    async def post(self):
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        result = await get_users_from_proj(userid),
        self.write({"message": result})

class wtd_save(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid          = str(self.get_secure_cookie("userid"), encoding="utf-8")
        order_number    = self.get_argument("order_number")
        order_env       = self.get_argument("order_env")
        order_type      = self.get_argument("order_type")
        order_status    = self.get_argument("order_status")
        order_handle    = self.get_argument("order_handle")
        order_desc      = self.get_argument("order_desc")
        attachment_path = self.get_argument("attachment_path")
        attachment_name = self.get_argument("attachment_name")
        v_list          = await save_order(order_number,order_env,order_type,order_status,order_handle,order_desc,userid,attachment_path,attachment_name)
        v_json          = json.dumps(v_list)
        self.write(v_json)


class wtd_save_uploadImage(basehandler):
    @tornado.web.authenticated
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


class wtd_release(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await release_order(wtd_no,userid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class order_query_xh(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        tp     = self.get_argument("type")
        rq     = self.get_argument("rq")
        dbid   = self.get_argument("dbid")
        v_list = await get_order_xh(tp, rq,dbid)
        v_json = json.dumps(v_list)
        self.write(v_json)

class order_check_xh(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        message = self.get_argument("message")
        v_list  = await check_order_xh(message)
        v_json  = json.dumps(v_list)
        self.write(v_json)

class wtd_update(basehandler):
    @tornado.web.authenticated
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

class wtd_delete(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await delete_wtd(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)


class order_delete(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        release_id = self.get_argument("release_id")
        v_list = await delete_order(release_id)
        v_json = json.dumps(v_list)
        self.write(v_json)


class order_update(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        release_id = self.get_argument("release_id")
        run_time   = self.get_argument("run_time")
        v_list     = await update_order(release_id,run_time)
        v_json     = json.dumps(v_list)
        self.write(v_json)


class wtd_attachment(basehandler):
    @tornado.web.authenticated
    async def get(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        userid = str(self.get_secure_cookie("userid"), encoding="utf-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await query_wtd_detail(wtd_no, userid)
        v_attach = []
        for i in  range(len(v_list['attachment_path'].split(','))):
            v_attach.append([i+1,'http://10.2.39.17:8300'+v_list['attachment_path'].split(',')[i]+'/'+v_list['attachment_name'].split(',')[i]])
        self.render("./order/order_attachment.html", order_attachments=v_attach)

class wtd_attachment_number(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        wtd_no = self.get_argument("wtd_no")
        v_list = await get_order_attachment_number(wtd_no)
        v_json = json.dumps(v_list)
        self.write(v_json)

class query_sql_release(basehandler):
    @tornado.web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id     = self.get_argument("id")
        v_list = await get_sql_release(id)
        v_json = json.dumps(v_list, cls=DateEncoder)
        self.write(v_json)

