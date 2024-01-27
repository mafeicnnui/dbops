#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 13:18
# @Author  : 马飞
# @File    : t_sql.py
# @Software: PyCharm

import sqlparse
import traceback,re
import logging
import datetime
import json
import xlrd,xlwt
import os,zipfile
from xpinyin import Pinyin

from web.model.t_sql_online     import check_online
from web.utils.common           import current_time, send_message, send_message_sync, current_rq
from web.model.t_user           import get_user_by_loginame
from web.model.t_ds             import get_ds_by_dsid,get_ds_by_dsid_sync
from web.model.t_dmmx           import get_dmmc_from_dm, get_dmmc_from_dm_sync, get_dmm_from_dm2
from web.model.t_sql_check      import check_mysql_ddl
from web.utils.common           import send_mail,send_mail_param,get_sys_settings,get_sys_settings_sync
from web.utils.common           import format_sql as fmt_sql
from web.model.t_user           import get_user_by_userid,get_user_by_loginame_sync
from web.utils.mysql_async      import async_processer
from web.utils.mysql_sync       import sync_processer
from web.utils.mysql_rollback   import write_rollback,delete_rollback
from web.model.t_sql_check      import check_statement_count

async def get_sqlid():
    sql="select ifnull(max(id),0)+1 from t_sql_release"
    rs = await async_processer.query_one(sql)
    return rs[0]

async def get_sql_release(p_id):
    sql="select * from t_sql_release where id={}".format(p_id)
    return await async_processer.query_dict_one(sql)

def get_sql_release_sync(p_id):
    sql="select * from t_sql_release where id={}".format(p_id)
    return sync_processer.query_dict_one(sql)

async def get_sql_by_sqlid(p_sql_id):
    sql="select sqltext from t_sql_release where id={0}".format(p_sql_id)
    rs = await async_processer.query_one(sql)
    return rs[0]

def get_sql_by_sqlid_sync(p_sql_id):
    sql="select sqltext from t_sql_release where id={0}".format(p_sql_id)
    rs = sync_processer.query_one(sql)
    return rs[0]

async def query_audit(p_name,p_dsid,p_creator,p_userid,p_username,p_reason):
    print('p_creator=',p_creator,'p_userid',p_username)
    v_where = ''
    if p_name != '':
        v_where = v_where + " and (a.sqltext like '%{}%' or a.db like '%{}%')\n".format(p_name,p_name,p_name)

    if p_reason != '':
        v_where = v_where + " and a.reason like '%{}%'\n".format(p_reason)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)
    else:
        v_where = v_where + """ and exists(select 1 from t_user_proj_privs x 
                                           where x.proj_id=b.id and x.user_id='{0}' and priv_id='3')""".format(p_userid)
    if p_creator != '':
        v_where = v_where + " and a.creator='{0}'\n".format(p_creator)

    if p_username != 'admin':
        v_where = v_where + " and a.creator='{0}'\n".format(p_username)

    sql = """SELECT  a.id, 
                     a.message,
                      CASE a.status 
                           WHEN '0' THEN '已发布'
                           WHEN '1' THEN '已审核'
                           WHEN '2' THEN '审核失败'
                           WHEN '3' THEN '执行中'
                           WHEN '4' THEN '执行成功'
                           WHEN '5' THEN '执行失败'
                           WHEN '6' THEN '已驳回'
                           WHEN '7' THEN '准备执行'
                     END  STATUS,
                     CASE  WHEN a.run_time IS NOT NULL and a.run_time !='' THEN
                        CONCAT(c.dmmc,'(<span style="color:red">定时</span>)')
                     ELSE
                        c.dmmc 
                     END AS 'type',
                     b.db_desc,
                     a.db,
                     (SELECT NAME FROM t_user d WHERE d.login_name=a.creator) creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %H:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%Y-%m-%d %H:%i:%s')   audit_date   
            FROM t_sql_release a,t_db_source b,t_dmmx c
            WHERE a.dbid=b.id
              AND c.dm='13'
              AND a.type=c.dmm
              {0}
            order by a.creation_date desc
          """.format(v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def query_run(p_name,p_dsid,p_creator,p_userid,p_username,p_reason):
    v_where = ''
    if p_name != '':
        v_where = v_where + " and (a.sqltext like '%{}%' or a.db like '%{}%')\n".format(p_name, p_name, p_name)

    if p_reason != '':
        v_where = v_where + " and a.reason like '%{}%'\n".format(p_reason)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)
    else:
        v_where = v_where + """ and exists(select 1 from t_user_proj_privs x 
                                   where x.proj_id=b.id and x.user_id='{0}' and priv_id='4')""".format(p_userid)
    if p_creator != '':
        v_where = v_where + " and a.creator='{0}'\n".format(p_creator)

    if p_username != 'admin':
        v_where = v_where + " and a.creator='{0}'\n".format(p_username)

    sql = """SELECT  a.id, 
                     a.message,
                     CASE a.status 
                           WHEN '0' THEN '已发布'
                           WHEN '1' THEN '已审核'
                           WHEN '2' THEN '审核失败'
                           WHEN '3' THEN '执行中'
                           WHEN '4' THEN '执行成功'
                           WHEN '5' THEN '执行失败'
                           WHEN '6' THEN '已驳回'
                           WHEN '7' THEN '准备执行'
                     END  STATUS,
                     CASE  WHEN a.run_time IS NOT NULL and a.run_time !='' THEN
                        CONCAT(c.dmmc,'(<span style="color:red">定时</span>)')
                     ELSE
                        c.dmmc 
                     END AS 'type',
                     b.db_desc,
                     a.db,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.creator) creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %H:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%Y-%m-%d %H:%i:%s')   audit_date,
                     IFNULL(error,'')  as error   
            FROM t_sql_release a,t_db_source b,t_dmmx c
            WHERE a.dbid=b.id
              AND c.dm='13'
              AND a.type=c.dmm
              {0} order by a.creation_date desc
          """.format(v_where)
    return await async_processer.query_list(sql)

async def query_order(p_name,p_dsid,p_creator,p_username,p_reason):
    v_where=''
    if p_username != 'admin':
        if p_creator != '':
            v_where = v_where + " and a.creator='{0}'\n".format(p_creator)
        else:
            v_where = "  and  a.creator='{0}'".format(p_username)
    else:
        if p_creator != '':
            v_where = v_where + " and a.creator='{0}'\n".format(p_creator)

    if p_name != '':
        v_where = v_where + " and (a.sqltext like '%{}%' or a.db like '%{}%')\n".format(p_name, p_name, p_name)

    if p_reason != '':
        v_where = v_where + " and a.reason like '%{}%'\n".format(p_reason)

    if p_dsid != '':
        v_where = v_where + " and a.dbid='{0}'\n".format(p_dsid)

    sql = """SELECT  a.id, 
                     a.message,
                      CASE a.status 
                           WHEN '0' THEN '已发布'
                           WHEN '1' THEN '已审核'
                           WHEN '2' THEN '审核失败'
                           WHEN '3' THEN '执行中'
                           WHEN '4' THEN '执行成功'
                           WHEN '5' THEN '执行失败'
                           WHEN '6' THEN '已驳回'
                           WHEN '7' THEN '准备执行'
                     END  STATUS,                     
                     CASE  WHEN a.run_time IS NOT NULL and a.run_time !='' THEN
                        CONCAT(c.dmmc,'(<span style="color:red">定时</span>)')
                     ELSE
                        c.dmmc 
                     END AS 'type',
                     b.db_desc,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.creator) creator,
                     DATE_FORMAT(a.creation_date,'%Y-%m-%d %h:%i:%s')  creation_date,
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.auditor) auditor,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date,
                     error
            FROM t_sql_release a,t_db_source b,t_dmmx c
            WHERE a.dbid=b.id
              AND c.dm='13'
              AND a.type=c.dmm
              {0} order by a.creation_date desc
          """.format(v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def query_wtd(p_userid):
    sql = """SELECT 
                 order_no,
                 (SELECT db_desc FROM t_db_source WHERE  id=a.order_env) AS order_env,
                 (SELECT dmmc FROM t_dmmx WHERE dm='17' AND dmm=a.order_type) AS order_type,
                 (SELECT dmmc FROM t_dmmx WHERE dm='19' AND dmm=a.order_status) AS order_status,                
                 (SELECT NAME FROM t_user WHERE id=a.creator) AS creator,
                 date_format(a.create_date,'%Y-%m-%d') as  create_date,
                 (SELECT NAME FROM t_user WHERE id=a.order_handler) AS order_handler,
                 date_format(a.handler_date,'%Y-%m-%d') as  handler_date                
           FROM t_wtd a
           where a.creator='{0}' or a.order_handler='{1}'
          """.format(p_userid,p_userid)
    return await async_processer.query_list(sql)

async def get_order_attachment_number(p_wtd_no):
    sql = """SELECT  attachment_path FROM t_wtd a where order_no='{0}'""".format(p_wtd_no)
    rs = await async_processer.query_one(sql)
    if rs is None or rs == (None,) or rs ==('',):
       return 0
    else:
       return rs[0].count(',')+1

async def query_wtd_detail(p_wtd_no,p_userid):
    sql = """SELECT 
                 order_no,
                 order_env,
                 order_type,
                 order_status,                
                 creator,
                 date_format(a.create_date,'%Y-%m-%d') as  create_date,
                 order_handler,
                 date_format(a.handler_date,'%Y-%m-%d') as  handler_date,
                 (SELECT db_desc FROM t_db_source WHERE id=a.order_env) AS order_env_name,
                 (SELECT dmmc FROM t_dmmx WHERE dm='17' AND dmm=a.order_type) AS order_type_name,
                 (SELECT dmmc FROM t_dmmx WHERE dm='19' AND dmm=a.order_status) AS order_status_name,                
                 (SELECT NAME FROM t_user WHERE id=a.creator) AS creator_name,
                 (SELECT NAME FROM t_user WHERE id=a.order_handler) AS order_handler_name,             
                 order_desc,
                 attachment_path,
                 attachment_name,
                 '{0}' as curr_user
                FROM t_wtd a where order_no='{1}'""".format(p_userid,p_wtd_no)
    rs = await async_processer.query_dict_one(sql)
    return rs

async def query_order_no():
    sql = '''SELECT 
                   CASE WHEN (COUNT(0)+1)<10 THEN 
                      CONCAT('0',CAST(COUNT(0)+1 AS CHAR))
                   ELSE
                      CAST(COUNT(0)+1 AS CHAR)
                   END AS order_no   
               FROM t_wtd FOR UPDATE'''
    rs = await async_processer.query_one(sql)
    return rs[0]

async def save_order(order_number,order_env,order_type,order_status,order_handle,order_desc,p_user,p_attachment_path,p_attachment_name):
    result = {}
    try:
        sql = '''insert into t_wtd(order_no,order_env,order_type,order_status,order_handler,order_desc,creator,create_date,attachment_path,attachment_name)
                  values('{0}','{1}','{2}','{3}','{4}','{5}','{6}',now(),'{7}','{8}')
              '''.format(order_number,order_env,order_type,order_status,order_handle,order_desc,p_user,p_attachment_path,p_attachment_name)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='保存成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败!'
        return result

async def upd_order(order_number, order_env, order_type, order_status,order_handler, order_desc, p_attachment_path, p_attachment_name):
    result = {}
    try:
        sql = '''update t_wtd set                     
                      order_env          = '{0}',
                      order_type         = '{1}',
                      order_status       = '{2}',
                      order_handler      = '{3}',
                      order_desc         = '{4}',
                      attachment_path    = '{5}',
                      attachment_name    = '{6}'
                 where order_no ='{7}'
              '''.format(order_env, order_type, order_status, order_handler, order_desc,
                         p_attachment_path, p_attachment_name,order_number)
        await async_processer.exec_sql(sql)
        result['code'] = '0'
        result['message'] = '更新成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def delete_wtd(order_number):
    result = {}
    try:
        sql = "delete from t_wtd  where order_no='{0}'".format(order_number)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='删除成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result

async def delete_order(p_release_id):
    result = {}
    try:
        release = await get_sql_release(p_release_id)
        if release['status'] in('1','3','4','5'):
            result['code'] = '-1'
            result['message'] = '不能删除已审核工单!'
            return result
        sql = "delete from t_sql_release  where id='{0}'".format(p_release_id)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='删除成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result

async def update_order(p_release_id,p_run_time):
    result = {}
    try:
        release = await get_sql_release(p_release_id)
        if release['status'] in('3','4','5'):
            result['code'] = '-1'
            result['message'] = '不能更新已执行工单!'
            return result
        sql = "update  t_sql_release set run_time='{}' where id='{}'".format(p_run_time,p_release_id)
        print(sql)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='更新成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def release_order(p_order_no,p_userid):
    result = {}
    try:
        user = await get_user_by_userid(p_userid)
        sql  = """update t_wtd set order_status='2' where order_no='{0}'""".format(p_order_no)
        await async_processer.exec_sql(sql)
        v_handle  = await query_wtd_detail(p_order_no,p_userid)['order_handler']
        v_email   = await get_user_by_userid(v_handle)['email']
        v_content ='{}发布了问题单，编号：{},请尽时处理!'.format(user['username'],p_order_no)
        send_mail('190343@lifeat.cn', 'Hhc5HBtAuYTPGHQ8',v_email , '发布工单', v_content)
        result['code']='0'
        result['message']='发布成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '发布失败!'
        return result

async def get_order_xh(p_type,p_rq,p_dbid):
    result = {}
    try:
        st ="""SELECT MAX(a.message)  as xh FROM t_sql_release a
                    WHERE a.dbid={} 
                      and a.TYPE='{}' 
                      and a.creation_date=(SELECT MAX(creation_date) 
                                           FROM t_sql_release b 
                                           WHERE b.dbid=a.dbid 
                                             and b.TYPE=a.type
                                             and DATE_FORMAT(b.creation_date,'%Y%m%d')='{}')
                     """.format(p_dbid,p_type,p_rq)
        res = await async_processer.query_dict_one(st)
        print(st)
        result['code']='0'
        if res['xh']=='':
           result['message'] = 1
        else:
           print('xh=',res['xh'])
           result['message']=int(res['xh'].split('-')[-1])+1
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = traceback.format_exc()
        return result

async def check_order_xh(p_message):
    result = {}
    try:
        st ="""SELECT COUNT(0) as xh FROM t_sql_release WHERE message='{}'""".format(p_message)
        res = await async_processer.query_dict_one(st)
        print(st)
        result['code']='0'
        result['message']=res['xh']
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = traceback.format_exc()
        return result

async def query_audit_sql(id):
    res = {}
    st = """select a.id,a.message,a.sqltext,a.error,a.run_time,a.db,a.dbid,a.run_result,reason from t_sql_release a where a.id={0}""".format(id)
    rs = await async_processer.query_dict_one(st)
    st = """select rollback_statement FROM `t_sql_backup` WHERE release_id={} order by id desc """.format(id)
    rs['rollback'] =  await async_processer.query_dict_list(st)
    if rs['run_result'] is not None and rs['run_result'] !='' :
       rs['run_result'] = json.loads(rs.get('run_result'))
    else:
       rs['run_result'] = {}
    ds = await get_ds_by_dsid(rs['dbid'])
    ds['service'] = rs['db']
    rs['ds'] = ds
    res['code'] = '0'
    res['message'] = rs
    print('query_audit_sql=',rs)
    return res

async def query_rollback(release_id):
    st = """select rollback_statement
                FROM `t_sql_backup` WHERE release_id={} order by id desc """.format(release_id)
    rs = await async_processer.query_dict_list(st)
    return rs

async def exp_rollback(static_path,release_id):
    os.system('cd {0}'.format(static_path + '/downloads/log'))
    file_name = static_path + '/downloads/log/exp_log_{0}.sql'.format(release_id)
    file_name_ext = 'exp_log_{0}.sql'.format(release_id)

    res = await query_rollback(release_id)
    with open(file_name, 'w') as f:
        for r in res:
            f.write(r['rollback_statement']+'\n')

    # 生成zip压缩文件
    zip_file = static_path + '/downloads/log/exp_log_{0}.zip'.format(release_id)
    rzip_file = '/static/downloads/log/exp_log_{0}.zip'.format(release_id)

    # 若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_ext)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file

async def save_sql(p_dbid,p_sql,desc,logon_user):
    result = {}
    try:
        if p_dbid == '':
            result['code'] = '1'
            result['message'] = '请选择数据源!'
            return result

        p_ds = await get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] == '0':
            val = check_mysql_ddl(p_dbid, p_sql,logon_user)

        if val['code']!='0':
           return val
        sql="""insert into t_sql_release(id,dbid,sqltext,status,message,creation_date,creator,last_update_date,updator) 
                values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}','{8}')""".format(get_sqlid(),p_dbid,p_sql,'0',desc,current_time(),'DBA',current_time(),'DBA');
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='发布成功！'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '发布失败！'
        return result

async def check_sql(p_dbid,p_cdb,p_sql,desc,logon_user,type):
    result = {}
    result['code'] = '0'
    result['message'] = '发布成功！'
    try:
        if p_dbid == '':
            result['code'] = '1'
            result['message'] = '请选择数据源!'
            return result

        p_ds = await get_ds_by_dsid(p_dbid)
        if p_ds['db_type'] in('0','11'):
            val = await check_mysql_ddl(p_dbid,p_cdb, p_sql,logon_user,type)

        if val == False:
            result['code'] = '1'
            result['message'] = '发布失败!'
            return result
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '发布失败！'
        return result

async def save_sql(p_dbid,p_cdb,p_sql,desc,p_user,type,time,p_username,p_host,p_reason):
    result = {}
    try:
        if check_validate(p_dbid,p_cdb,p_sql,desc,p_user,type)['code']!='0':
           return check_validate(p_dbid,p_cdb,p_sql,desc,p_user,type)

        p_ds = await get_ds_by_dsid(p_dbid)
        p_sqlid = await get_sqlid()

        if p_ds['db_type'] in('0','11') :
            val = check_mysql_ddl(p_dbid,p_cdb, p_sql,p_user,type)

        if val == False:
            result['code'] = '1'
            result['message'] = '发布失败!'
            return result

        sql="""insert into t_sql_release(id,dbid,db,sqltext,status,message,creation_date,creator,last_update_date,updator,type,run_time,reason) 
                 values('{0}','{1}',"{2}",'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')
            """.format(p_sqlid,p_dbid,p_cdb,fmt_sql(p_sql),'0',desc,current_time(),p_user['login_name'],current_time(),p_user['login_name'],type,time,p_reason)

        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='发布成功！'

        # 2021.09.09 add send mail
        p_ds['service'] = p_cdb
        sql = await get_sql_by_sqlid(p_sqlid)
        email = (await get_user_by_loginame(p_username))['email']
        settings = await get_sys_settings()
        wkno = await get_sql_release(p_sqlid)
        v_title = '工单发布情况[{}]'.format(wkno['message'])
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator = (await get_user_by_loginame(wkno['creator']))['name']
        otype   = (await get_dmmc_from_dm('13', wkno['type']))[0]
        status  = (await get_dmmc_from_dm('41', wkno['status']))[0]

        if p_host=="124.127.103.190":
           p_host = "124.127.103.190:65482"
        elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
           p_host = '{}:81'.format(p_host)
        else:
           p_host = p_host

        # send success mail
        v_content = get_html_contents_release()
        v_content = v_content.replace('$$TIME$$', nowTime)
        v_content = v_content.replace('$$DBINFO$$',  p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$TYPE$$', otype)
        v_content = v_content.replace('$$STATUS$$', status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host,p_sqlid))
        v_content = v_content.replace('$$ERROR$$', '')
        send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'), email,
                        settings.get('CC'), v_title, v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',  p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', creator)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', '')
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sqlid)
        await send_message(p_user['wkno'],v_title,v_content_wx,v_detail_url)
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '发布失败!'
        return result

async def upd_sql(p_sqlid,p_user,p_status,p_message,p_host):
    result={}
    try:
        sql="""update t_sql_release 
                  set  status ='{}' ,
                       last_update_date =now(),
                       updator='{}',
                       audit_date =now() ,
                       auditor='{}',
                       audit_message='{}'
                where id='{}'""".format(p_status,p_user['login_name'],p_user['login_name'],p_message,p_sqlid)
        await async_processer.exec_sql(sql)

        wkno = await get_sql_release(p_sqlid)
        p_ds = await get_ds_by_dsid(wkno['dbid'])
        p_ds['service'] = wkno['db']
        email     = p_user['email']
        settings  = await get_sys_settings()
        v_title   = '工单审核情况[{}]'.format(wkno['message'])
        nowTime   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator   = (await get_user_by_loginame(wkno['creator']))['name']
        cmail     =  (await get_user_by_loginame(wkno['creator']))['email']
        auditor   = (await get_user_by_loginame(wkno['auditor']))['name']
        otype     = (await get_dmmc_from_dm('13', wkno['type']))[0]
        status    = (await get_dmmc_from_dm('41', wkno['status']))[0]

        if p_host=="124.127.103.190":
           p_host = "124.127.103.190:65482"
        elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
           p_host = '{}:81'.format(p_host)
        else:
           p_host = p_host

        # send audit mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$', nowTime)
        v_content = v_content.replace('$$DBINFO$$',p_ds['url'] + p_ds['service']
                                                   if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor)
        v_content = v_content.replace('$$TYPE$$', otype)
        v_content = v_content.replace('$$STATUS$$', status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host,p_sqlid))
        v_content = v_content.replace('$$ERROR$$', '')
        send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'), email,
                        cmail, v_title, v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                            p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                            p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', auditor)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', '')
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sqlid)
        await send_message('{}|{}'.format(p_user['wkno'],
                                          (await get_user_by_loginame(wkno['creator']))['wkno']),
                           v_title,
                           v_content_wx,
                           v_detail_url)

        result['code']='0'
        result['message']='审核成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '审核异常!'
        return result

async def upd_sql_canal(p_id,p_user):
    result={}
    try:
        sql="""update t_sql_release 
                  set  status ='0' ,
                       last_update_date =now(),
                       updator='{}',
                       audit_date =null ,
                       auditor=null,
                       audit_message=null,
                       error=null
                where id='{}'""".format(p_user['login_name'],p_id)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='取消审核成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '取消审核异常!'
        return result

async def upd_sql_contents(p_id,p_contents,p_run_time,p_user):
    result={}
    try:
        res= await get_sql_release(p_id)
        print('res=',res)
        ds = await get_ds_by_dsid(res['dbid'])
        if ds['db_type'] == '0':
            print('check_mysql_ddl..')
            val = await check_mysql_ddl(res['dbid'],
                                  res['db'],
                                  p_contents,
                                  p_user,
                                  res['type'])
            print('val=',val)
            if val == False:
                result['code'] = '1'
                result['message'] = '检测失败!'
                return result

        st="""update t_sql_release 
                set  sqltext ='{}',
                     run_time='{}' 
                where id='{}'""".format(fmt_sql(p_contents),p_run_time,p_id)
        print('upd_sql_contents=',st)
        await async_processer.exec_sql(st)
        result['code']='0'
        result['message']='更新成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def upd_sql_run_status(p_sqlid,p_user):
    result={}
    try:
        sql="""update t_sql_release  set  status ='7' ,last_update_date =now(),executor='{}' where id='{}'""".format(p_user,p_sqlid)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='已在后台运行!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '设置运行状态异常!'
        return result

async def upd_run_status(p_sqlid,p_flag,p_err=None,binlog_file=None,start_pos=None,stop_pos=None):
    try:
        if p_flag == 'before':
            sql = """update t_sql_release set  status ='3',last_update_date ='{0}',exec_start ='{1}' where id='{2}'""".format(current_time(),current_time(),str(p_sqlid))
        elif p_flag =='after':
            sql = """update t_sql_release set status ='4',last_update_date ='{0}',exec_end ='{1}',binlog_file='{2}',start_pos='{3}',stop_pos='{4}', error = '',executor='admin' where id='{5}'""".format(current_time(), current_time(),binlog_file,start_pos,stop_pos,str(p_sqlid))
        elif p_flag=='error':
            sql = """update t_sql_release set  status ='5',last_update_date ='{0}',exec_end ='{1}',error = '{2}',failure_times=failure_times+1 where id='{3}'""".format(current_time(), current_time(), p_err,str(p_sqlid))
        else:
           pass
        logging.info(("upd_run_status:",sql))
        await async_processer.exec_sql(sql)
    except :
        logging.error((traceback.format_exc()))
        traceback.print_exc()

def upd_run_status_sync(p_sqlid,p_flag,p_err=None,binlog_file=None,start_pos=None,stop_pos=None):
    try:
        if p_flag == 'before':
            sql = """update t_sql_release set  status ='3',last_update_date ='{0}',exec_start ='{1}' where id='{2}'""".format(current_time(),current_time(),str(p_sqlid))
        elif p_flag =='after':
            sql = """update t_sql_release set status ='4',last_update_date ='{0}',exec_end ='{1}',binlog_file='{2}',start_pos='{3}',stop_pos='{4}', error = '' where id='{5}'""".format(current_time(), current_time(),binlog_file,start_pos,stop_pos,str(p_sqlid))
        elif p_flag=='error':
            sql = """update t_sql_release set  status ='5',last_update_date ='{0}',exec_end ='{1}',error = '{2}',failure_times=failure_times+1 where id='{3}'""".format(current_time(), current_time(), p_err,str(p_sqlid))
        else:
           pass
        logging.info(("upd_run_status:",sql))
        sync_processer.exec_sql(sql)
    except :
        logging.error((traceback.format_exc()))
        traceback.print_exc()

def get_html_contents_release():
    v_html='''<html>
		<head>
		   <style type="text/css">
			   .xwtable {width: 90%;border-collapse: collapse;border: 1px solid #ccc;}
			   .xwtable thead td {font-size: 12px;color: #333333;
					      text-align: center;background: url(table_top.jpg) repeat-x top center;
				              border: 1px solid #ccc; font-weight:bold;}
			   .xwtable thead th {font-size: 12px;color: #333333;
				              text-align: center;background: url(table_top.jpg) repeat-x top center;
					      border: 1px solid #ccc; font-weight:bold;}
			   .xwtable tbody tr {background: #fff;font-size: 12px;color: #666666;}
			   .xwtable tbody tr.alt-row {background: #f2f7fc;}
			   .xwtable td{line-height:20px;text-align: left;padding:4px 10px 3px 10px;height: 18px;border: 1px solid #ccc;}
		   </style>
		</head>
		<body>
              <table class='xwtable'>
                  <tr><td width="20%">发送时间</td><td width="80%">$$TIME$$</td></tr>
                  <tr><td>数据库名</td><td>$$DBINFO$$</td></tr>
                  <tr><td>提交人员</td><td>$$CREATOR$$</td></tr>
                  <tr><td>工单类型</td><td>$$TYPE$$</td></tr>
                  <tr><td>工单状态</td><td>$$STATUS$$</td></tr>
                  <tr><td>工单详情</td><td>$$DETAIL$$</td></tr>
              </table>    
		</body>
	    </html>'''
    return v_html

def get_html_contents_release_wx():
    v_wx='''发送时间:$$TIME$$
数据库名:$$DBINFO$$
提交人员:$$CREATOR$$
工单类型:$$TYPE$$
工单状态:$$STATUS$$'''
    return v_wx

def get_html_contents():
    v_html='''<html>
		<head>
		   <style type="text/css">
			   .xwtable {width: 90%;border-collapse: collapse;border: 1px solid #ccc;}
			   .xwtable thead td {font-size: 12px;color: #333333;
					      text-align: center;background: url(table_top.jpg) repeat-x top center;
				              border: 1px solid #ccc; font-weight:bold;}
			   .xwtable thead th {font-size: 12px;color: #333333;
				              text-align: center;background: url(table_top.jpg) repeat-x top center;
					      border: 1px solid #ccc; font-weight:bold;}
			   .xwtable tbody tr {background: #fff;font-size: 12px;color: #666666;}
			   .xwtable tbody tr.alt-row {background: #f2f7fc;}
			   .xwtable td{line-height:20px;text-align: left;padding:4px 10px 3px 10px;height: 18px;border: 1px solid #ccc;}
		   </style>
		</head>
		<body>
              <table class='xwtable'>
                  <tr><td width="20%">发送时间</td><td width="80%">$$TIME$$</td></tr>
                  <tr><td>数据库名</td><td>$$DBINFO$$</td></tr>
                  <tr><td>提交人员</td><td>$$CREATOR$$</td></tr>
                  <tr><td>审核人员</td><td>$$AUDITOR$$</td></tr>
                  <tr><td>工单类型</td><td>$$TYPE$$</td></tr>
                  <tr><td>工单状态</td><td>$$STATUS$$</td></tr>
                  <tr><td>工单详情</td><td>$$DETAIL$$</td></tr>
              </table>    
		</body>
	    </html>'''
    return v_html

async def exe_sql(p_dbid, p_db_name,p_sql_id,p_username,p_host):
    res = {}
    p_ds = await get_ds_by_dsid(p_dbid)
    p_ds['service'] = p_db_name
    await upd_run_status(p_sql_id,'before')
    sql   = await get_sql_by_sqlid(p_sql_id)
    email = (await get_user_by_loginame(p_username))['email']
    settings = await get_sys_settings()

    try:
        # get binlog ,start_position
        # await async_processer.exec_sql_by_ds(p_ds, 'FLUSH /*!40101 LOCAL */ TABLES')
        # await async_processer.exec_sql_by_ds(p_ds, 'FLUSH TABLES WITH READ LOCK')
        # rs1 = await async_processer.query_one_by_ds(p_ds, 'show master status')
        # binlog_file=rs1[0]
        # start_position=rs1[1]
        #
        # logging.info(('check_statement_count(sql)=',check_statement_count(sql)))
        # if check_statement_count(sql) == 1:
        #     logging.info(('exec single statement:'))
        #     logging.info(('-----------------------------------------'))
        #     logging.info(('statement:', sql))
        #     await async_processer.exec_sql_by_ds(p_ds, sql)
        # elif check_statement_count(sql) > 1:
        #     logging.info(('exec multi statement:'))
        #     logging.info(('-----------------------------------------'))
        #     #await async_processer.exec_sql_by_ds_multi(p_ds, sql)
        #     for st in reReplace(sql):
        #         logging.info(('statement=',st))
        #         await async_processer.exec_sql_by_ds(p_ds, st)
        # else:
        #     pass
        #
        # # get stop_position
        # rs2 = await async_processer.query_one_by_ds(p_ds, 'show master status')
        # stop_position=rs2[1]

        if check_statement_count(sql) == 1:
            binlog_file,start_position,stop_position = await async_processer.exec_sql_by_ds_new(p_ds, sql)

        if check_statement_count(sql) > 1:
            binlog_file,start_position,stop_position = await async_processer.exec_sql_by_ds_multi_new(p_ds, sql)

        logging.info('binlog:{},{},{}'.format(binlog_file,str(start_position),str(stop_position)))
        await upd_run_status(p_sql_id, 'after',None,binlog_file,start_position,stop_position)

        # write rollback statement
        write_rollback(p_sql_id,p_ds,binlog_file,start_position,stop_position)

        # send success mail
        wkno  = await get_sql_release(p_sql_id)
        if wkno['run_time'] is not None and wkno['run_time'] !='':
            v_title = '定时工单执行情况[{}]'.format(wkno['message'])
        else:
            v_title = '工单执行情况[{}]'.format(wkno['message'])
        nowTime   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator   = (await get_user_by_loginame(wkno['creator']))['name']
        auditor   = (await get_user_by_loginame(wkno['auditor']))['name']
        otype     = (await get_dmmc_from_dm('13',wkno['type']))[0]
        status    = (await get_dmmc_from_dm('41',wkno['status']))[0]

        # if p_host == "124.127.103.190":
        #     p_host = "124.127.103.190:65482"
        # elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
        #     p_host = '{}:81'.format(p_host)
        # else:
        #     p_host = p_host

        # send mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$',   nowTime)
        v_content = v_content.replace('$$DBINFO$$',  p_ds['url']+p_ds['service'] if p_ds['url'].find(p_ds['service'])<0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor )
        v_content = v_content.replace('$$TYPE$$',    otype)
        v_content = v_content.replace('$$STATUS$$',  status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host,p_sql_id))
        v_content = v_content.replace('$$ERROR$$','')
        send_mail_param(settings.get('send_server'), settings.get('sender'), settings.get('sendpass'), email,settings.get('CC'), v_title,v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                             p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                             p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', creator)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', '')
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id)
        to_user ='{}|{}|{}'.format((await get_user_by_loginame(wkno['executor']))['wkno'],
                                   (await get_user_by_loginame(wkno['creator']))['wkno'],
                                   (await get_user_by_loginame(wkno['auditor']))['wkno'])
        await send_message(to_user, v_title, v_content_wx, v_detail_url)

        res['code'] = '0'
        res['message'] = '执行成功!'
        return res
    except Exception as e:
        from web.utils.common import format_sql as fmt_sql
        error = fmt_sql(traceback.format_exc())
        res['code'] = '-1'
        res['message'] = '执行失败!'
        logging.error(traceback.format_exc())
        await upd_run_status(p_sql_id,'error', error)
        delete_rollback(p_sql_id)

        # send error mail
        wkno    = await get_sql_release(p_sql_id)
        v_title = '工单执行情况[{}]'.format(wkno['message'])
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator = (await get_user_by_loginame(wkno['creator']))['name']
        auditor = (await get_user_by_loginame(wkno['auditor']))['name']
        otype   = (await get_dmmc_from_dm('13', wkno['type']))[0]
        status  = (await get_dmmc_from_dm('41', wkno['status']))[0]

        # if p_host == "124.127.103.190":
        #     p_host = "124.127.103.190:65482"
        # elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
        #     p_host = '{}:81'.format(p_host)
        # else:
        #     p_host = p_host

        # send mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$', nowTime)
        v_content = v_content.replace('$$DBINFO$$',
                                      p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor)
        v_content = v_content.replace('$$TYPE$$',    otype)
        v_content = v_content.replace('$$STATUS$$',  status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id))
        send_mail_param(settings.get('send_server'), settings.get('sender'),
                        settings.get('sendpass'), email,settings.get('CC'), v_title,v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                            p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                            p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', creator)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', error)
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id)
        to_user = '{}|{}|{}'.format((await get_user_by_loginame(wkno['executor']))['wkno'],
                                    (await get_user_by_loginame(wkno['creator']))['wkno'],
                                    (await get_user_by_loginame(wkno['auditor']))['wkno'])
        await send_message(to_user, v_title, v_content_wx, v_detail_url)
        return res

def exe_sql_sync(p_dbid, p_db_name,p_sql_id,p_username,p_host):
    res  = {}
    p_ds = get_ds_by_dsid_sync(p_dbid)
    p_ds['service'] = p_db_name
    upd_run_status_sync(p_sql_id,'before')
    sql   = get_sql_by_sqlid_sync(p_sql_id)
    email = get_user_by_loginame_sync(p_username)['email']
    settings = get_sys_settings_sync()

    try:
        # get binlog ,start_position，one session execute
        # sync_processer.exec_sql_by_ds(p_ds, 'FLUSH /*!40101 LOCAL */ TABLES')
        # sync_processer.exec_sql_by_ds(p_ds, 'FLUSH TABLES WITH READ LOCK')
        # rs1 = sync_processer.query_one_by_ds(p_ds, 'show master status')
        # binlog_file=rs1[0]
        # start_position=rs1[1]
        #
        # logging.info(('check_statement_count(sql)=',check_statement_count(sql)))
        # if check_statement_count(sql) == 1:
        #    sync_processer.exec_sql_by_ds(p_ds, sql)
        #
        # if check_statement_count(sql) > 1:
        #    sync_processer.exec_sql_by_ds_multi(p_ds, sql)
        #
        # # get stop_position
        # rs2 = sync_processer.query_one_by_ds(p_ds, 'show master status')
        # stop_position=rs2[1]
        # sync_processer.exec_sql_by_ds(p_ds, 'UNLOCK TABLES')

        logging.info(('check_statement_count(sql)=', check_statement_count(sql)))
        if p_ds['db_type'] == '11':
            if check_statement_count(sql) == 1:
                 sync_processer.exec_sql_by_ds(p_ds, sql)
            if check_statement_count(sql) > 1:
                sync_processer.exec_sql_by_ds_multi(p_ds, sql)
            upd_run_status_sync(p_sql_id, 'after')
        else:
            if check_statement_count(sql) == 1:
                binlog_file, start_position, stop_position = sync_processer.exec_sql_by_ds_new(p_ds, sql)
            if check_statement_count(sql) > 1:
                binlog_file, start_position, stop_position = sync_processer.exec_sql_by_ds_multi_new(p_ds, sql)
            logging.info('binlog:{},{},{}'.format(binlog_file,str(start_position),str(stop_position)))
            upd_run_status_sync(p_sql_id, 'after',None,binlog_file,start_position,stop_position)
            # write rollback
            write_rollback(p_sql_id,p_ds,binlog_file,start_position,stop_position)

        # send success mail
        wkno      =  get_sql_release_sync(p_sql_id)
        v_title   = '工单执行情况[{}]'.format(wkno['message'])
        nowTime   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator   = get_user_by_loginame_sync(wkno['creator'])['name']
        auditor   = get_user_by_loginame_sync(wkno['auditor'])['name']
        otype     = get_dmmc_from_dm_sync('13',wkno['type'])[0]
        status    = get_dmmc_from_dm_sync('41',wkno['status'])[0]

        if p_host == "124.127.103.190":
            p_host = "124.127.103.190:65482"
        elif p_host in('10.2.39.18','10.2.39.20','10.2.39.21'):
            p_host = '{}:81'.format(p_host)
        else:
            p_host = p_host

        # send mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$',    nowTime)
        v_content = v_content.replace('$$DBINFO$$',  p_ds['url']+p_ds['service'] if p_ds['url'].find(p_ds['service'])<0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor )
        v_content = v_content.replace('$$TYPE$$',    otype)
        v_content = v_content.replace('$$STATUS$$',  status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host,p_sql_id))
        v_content = v_content.replace('$$ERROR$$','')
        send_mail_param(settings.get('send_server'),
                        settings.get('sender'),
                        settings.get('sendpass'),
                        email,settings.get('CC'),
                        v_title,
                        v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                            p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                            p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', creator)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', '')
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id)
        to_user = '{}|{}|{}'.format(get_user_by_loginame_sync(wkno['executor'])['wkno'],
                                    get_user_by_loginame_sync(wkno['creator'])['wkno'],
                                    get_user_by_loginame_sync(wkno['auditor'])['wkno'])
        send_message_sync(to_user, v_title, v_content_wx, v_detail_url)

        res['code'] = '0'
        res['message'] = '工单:{}执行成功!'.format(wkno['message'])
        return res
    except :
        from web.utils.common import format_sql as fmt_sql
        error = fmt_sql(traceback.format_exc())
        logging.error(traceback.format_exc())
        upd_run_status_sync(p_sql_id, 'error', error)
        delete_rollback(p_sql_id)

        wkno    =  get_sql_release_sync(p_sql_id)
        v_title = '工单执行情况[{}]'.format(wkno['message'])
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        creator = get_user_by_loginame_sync(wkno['creator'])['name']
        auditor = get_user_by_loginame_sync(wkno['auditor'])['name']
        otype   = get_dmmc_from_dm_sync('13', wkno['type'])[0]
        status  = get_dmmc_from_dm_sync('41', wkno['status'])[0]

        if p_host == "124.127.103.190":
            p_host = "124.127.103.190:65482"
        elif p_host in ('10.2.39.18', '10.2.39.20', '10.2.39.21'):
            p_host = '{}:81'.format(p_host)
        else:
            p_host = p_host

        # send mail
        v_content = get_html_contents()
        v_content = v_content.replace('$$TIME$$', nowTime)
        v_content = v_content.replace('$$DBINFO$$',
                                       p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else p_ds['url'])
        v_content = v_content.replace('$$CREATOR$$', creator)
        v_content = v_content.replace('$$AUDITOR$$', auditor)
        v_content = v_content.replace('$$TYPE$$',    otype)
        v_content = v_content.replace('$$STATUS$$',  status)
        v_content = v_content.replace('$$DETAIL$$', 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id))
        send_mail_param(settings.get('send_server'),
                        settings.get('sender'),
                        settings.get('sendpass'),
                        email,settings.get('CC'),
                        v_title,
                        v_content)

        # send to wx 2022.03.07
        v_content_wx = get_html_contents_release_wx()
        v_content_wx = v_content_wx.replace('$$TIME$$', nowTime)
        v_content_wx = v_content_wx.replace('$$DBINFO$$',
                                            p_ds['url'] + p_ds['service'] if p_ds['url'].find(p_ds['service']) < 0 else
                                            p_ds['url'])
        v_content_wx = v_content_wx.replace('$$CREATOR$$', creator)
        v_content_wx = v_content_wx.replace('$$TYPE$$', otype)
        v_content_wx = v_content_wx.replace('$$STATUS$$', status)
        v_content_wx = v_content_wx.replace('$$ERROR$$', error)
        v_detail_url = 'http://{}/sql/detail?release_id={}'.format(p_host, p_sql_id)
        to_user = '{}|{}|{}'.format(get_user_by_loginame_sync(wkno['executor'])['wkno'],
                                    get_user_by_loginame_sync(wkno['creator'])['wkno'],
                                    get_user_by_loginame_sync(wkno['auditor'])['wkno'])
        send_message_sync(to_user, v_title, v_content_wx, v_detail_url)

        res['code'] = '-1'
        res['message'] = '工单执行失败!'
        return res

def check_validate(p_dbid,p_cdb,p_sql,desc,logon_user,type):
    result = {}
    result['code'] = '0'
    result['message'] = '发布成功！'

    if p_dbid == '':
       result['code'] = '1'
       result['message'] = '请选择数据源!'
       return result

    if p_cdb == '':
       result['code'] = '1'
       result['message'] = '当前数据库不能为空!'
       return result

    if desc == '':
       result['code'] = '1'
       result['message'] = '请输入工单描述!'
       return result

    if type == '':
       result['code'] = '1'
       result['message'] = '工单类型不能为空!'
       return result

    return result

def format_sql(p_sql):
    result = {}
    result['code'] = '0'
    v_sql_list=sqlparse.split(p_sql)
    v_ret=''
    for v in v_sql_list:
        v_sql = sqlparse.format(v, reindent=True, keyword_case='upper')
        if v_sql.upper().count('CREATE') > 0 or v_sql.upper().count('ALTER') > 0:
            v_tmp = re.sub(' {5,}', '  ', v_sql).strip()
        else:
            v_tmp = re.sub('\n{2,}', '\n\n', v_sql).strip(' ')
        v_ret=v_ret+v_tmp+'\n\n'
    result['message'] = v_ret[0:-2]
    return result

def set_header_styles(p_fontsize,p_color):
    header_borders = xlwt.Borders()
    header_styles  = xlwt.XFStyle()
    # add table header style
    header_borders.left   = xlwt.Borders.THIN
    header_borders.right  = xlwt.Borders.THIN
    header_borders.top    = xlwt.Borders.THIN
    header_borders.bottom = xlwt.Borders.THIN
    header_styles.borders = header_borders
    header_pattern = xlwt.Pattern()
    header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    header_pattern.pattern_fore_colour = p_color
    # add font
    font = xlwt.Font()
    font.name = u'微软雅黑'
    font.bold = True
    font.size = p_fontsize
    header_styles.font = font
    #add alignment
    header_alignment = xlwt.Alignment()
    header_alignment.horz = xlwt.Alignment.HORZ_CENTER
    header_alignment.vert = xlwt.Alignment.VERT_CENTER
    header_styles.alignment = header_alignment
    header_styles.borders = header_borders
    header_styles.pattern = header_pattern
    return header_styles

def set_row_styles(p_fontsize,p_color):
    cell_borders   = xlwt.Borders()
    cell_styles    = xlwt.XFStyle()

    # add font
    font = xlwt.Font()
    font.name = u'微软雅黑'
    font.bold = True
    font.size = p_fontsize
    cell_styles.font = font

    #add col style
    cell_borders.left     = xlwt.Borders.THIN
    cell_borders.right    = xlwt.Borders.THIN
    cell_borders.top      = xlwt.Borders.THIN
    cell_borders.bottom   = xlwt.Borders.THIN

    row_pattern           = xlwt.Pattern()
    row_pattern.pattern   = xlwt.Pattern.SOLID_PATTERN
    row_pattern.pattern_fore_colour = p_color

    # add alignment
    cell_alignment        = xlwt.Alignment()
    cell_alignment.horz   = xlwt.Alignment.HORZ_LEFT
    cell_alignment.vert   = xlwt.Alignment.VERT_CENTER

    cell_styles.alignment = cell_alignment
    cell_styles.borders   = cell_borders
    cell_styles.pattern   = row_pattern
    cell_styles.font      = font
    return cell_styles

async def exp_sql_xls(static_path,p_month,p_market_id):
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('kpi')
    header_styles = set_header_styles(45,1)
    os.system('cd {0}'.format(static_path + '/downloads/kpi'))
    file_name   = static_path + '/downloads/port/exp_kpi_{0}.xls'.format(current_rq())
    file_name_s = 'exp_kpi_{0}.xls'.format(current_rq())

    v_where = ' '
    if p_market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(p_market_id)

    sql_header = """select date_format(a.bbrq,'%Y-%m-%d') as "报表日期",
                       a.month                 as "报表月",
                       a.market_id             as "项目编码	",
                       a.market_name           as "项目名称",
                       a.item_code             as "指标编码",
                       a.item_name             as "指标名称",
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as "指标说明",
                       a.goal                  as "月度指标",
                       a.actual_completion     as "月度完成",
                       a.completion_rate       as "月度完成率",
                       a.`annual_target`       as "年度指标",
                       a.completion_sum_finish as "年度完成	",
                       a.completion_sum_rate   as "年度完成率"
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0 limit 1""".format(p_month, v_where)


    sql_content = """select 
                       date_format(a.bbrq,'%Y-%m-%d') as bbrq,
                       a.month,
                       a.market_id,a.market_name,
                       a.item_code,a.item_name,
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as item_type,
                       a.goal,a.actual_completion,a.completion_rate,
                       a.`annual_target`,a.completion_sum_finish,a.completion_sum_rate
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0""".format(p_month, v_where)

    # 写表头
    desc = await async_processer.query_one_desc(sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k in (3, 5):
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #循环项目写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list(sql_content)
    for i in rs3:
        for j in range(len(i)):
            cell_styles = set_row_styles(45, 1)
            if i[j] is None:
                worksheet.write(row_data, j, '')
            else:
                worksheet.write(row_data, j, str(i[j]))
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    #生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_kpi_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_kpi_{0}.zip'.format(current_rq())

    #若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file

async def exp_sql_pdf(static_path,p_month,p_market_id):
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('kpi')
    header_styles = set_header_styles(45,1)
    os.system('cd {0}'.format(static_path + '/downloads/kpi'))
    file_name   = static_path + '/downloads/port/exp_kpi_{0}.xls'.format(current_rq())
    file_name_s = 'exp_kpi_{0}.xls'.format(current_rq())

    v_where = ' '
    if p_market_id != '':
        v_where = v_where + " and a.market_id='{0}'\n".format(p_market_id)

    sql_header = """select date_format(a.bbrq,'%Y-%m-%d') as "报表日期",
                       a.month                 as "报表月",
                       a.market_id             as "项目编码	",
                       a.market_name           as "项目名称",
                       a.item_code             as "指标编码",
                       a.item_name             as "指标名称",
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as "指标说明",
                       a.goal                  as "月度指标",
                       a.actual_completion     as "月度完成",
                       a.completion_rate       as "月度完成率",
                       a.`annual_target`       as "年度指标",
                       a.completion_sum_finish as "年度完成	",
                       a.completion_sum_rate   as "年度完成率"
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0 limit 1""".format(p_month, v_where)


    sql_content = """select 
                       date_format(a.bbrq,'%Y-%m-%d') as bbrq,
                       a.month,
                       a.market_id,a.market_name,
                       a.item_code,a.item_name,
                       (select case when type=1 then '当月考核' else '累计考核' end  from kpi_item x where x.code=a.item_code) as item_type,
                       a.goal,a.actual_completion,a.completion_rate,
                       a.`annual_target`,a.completion_sum_finish,a.completion_sum_rate
               from kpi_po_hz a,kpi_po b ,kpi_item_sql c
               WHERE a.market_id=b.market_id  AND a.`item_code`=c.`item_code`
                 and a.item_code not in('9','13','2.1','2.2','12.1','12.2') 
                 and a.month='{}' {}
                   ORDER BY b.sxh,a.item_code+0""".format(p_month, v_where)

    # 写表头
    desc = await async_processer.query_one_desc(sql_header)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)
        if k in (3, 5):
            worksheet.col(k).width = 8000
        else:
            worksheet.col(k).width = 4000

    #循环项目写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list(sql_content)
    for i in rs3:
        for j in range(len(i)):
            cell_styles = set_row_styles(45, 1)
            if i[j] is None:
                worksheet.write(row_data, j, '')
            else:
                worksheet.write(row_data, j, str(i[j]))
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    #生成zip压缩文件
    zip_file = static_path + '/downloads/port/exp_kpi_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/port/exp_kpi_{0}.zip'.format(current_rq())

    #若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file

async def save_order_prod(order_env,order_number,order_ver,order_type,order_status,order_script,p_user):
    result = {}
    try:
        rs = await check_online(order_env,order_type,order_script)
        if not rs['code'] :
            result['code'] = '-1'
            result['message'] = rs['msg']
            return result

        if await check_online_order(order_number):
            result['code'] = '-2'
            result['message'] = '操作失败(工单已存在)!'
            return result
        else:
           st = '''insert into t_sql_online(order_number,order_ver,order_type,order_status,sqltext,creator,create_date,order_env)
                   values('{0}','{1}','{2}','{3}','{4}','{5}',now(),'{6}')
                '''.format(order_number,order_ver,order_type,order_status,fmt_sql(order_script),p_user,order_env)
        print(st)
        await async_processer.exec_sql(st)
        result['code']='0'
        result['message']='操作成功!'
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '操作失败!'
        return result

async def update_order_prod(order_env,order_number,order_ver,order_type,order_status,order_script,p_user):
    result = {}
    try:
        if await check_online_order(order_number):

           rs = await check_online(order_env, order_type, order_script)
           if not rs['code']:
              result['code'] = '-1'
              result['message'] = rs['msg']
              return result

           st = '''update t_sql_online set 
                          order_ver= '{}',
                          order_type = '{}',
                          order_status = replace('{}','2','0'),
                          sqltext = '{}',
                          updator = '{}',
                          last_update_date = now(),
                          order_env = '{}'
                   where order_number='{}'
                '''.format(order_ver,order_type,order_status,fmt_sql(order_script),p_user,order_env,order_number)
           await async_processer.exec_sql(st)
           result['code']='0'
           result['message']='操作成功!'
           return result
        else:
            result['code'] = '-2'
            result['message'] = '操作失败(工单不存在)!'
            return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '操作失败!'
        return result

async def get_prod_order_number(p_order_type,p_userid,p_username):
    result = {}
    try:
        py = Pinyin()
        xm = await async_processer.query_dict_one('select name from t_user where id = {}'.format(p_userid))
        rs = py.get_pinyin(xm['name']).split('-')
        sp = ''.join(i[0].upper() for i in rs)
        tp = await async_processer.query_dict_one("select dmmc2 from t_dmmx where dm='46' and dmm='{}'".format(p_order_type))
        st ="""SELECT lpad(COUNT(0)+1,3,0)  as xh FROM t_sql_online a
                WHERE a.creator='{}'  and a.order_type='{}' """.format(p_username,p_order_type)
        print('get_prod_order_number=',st)
        xh = await async_processer.query_dict_one(st)
        result['code']='0'
        result['message']=sp+'_'+tp['dmmc2']+'_'+str(xh['xh'])
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = traceback.format_exc()
        return result

async def query_online_order(p_name,p_creator,p_username,p_order_ver,p_order_env):
    v_where=''
    if p_username != 'admin':
        if p_creator != '':
            v_where = v_where + " and a.creator='{0}'\n".format(p_creator)
        else:
            v_where = "  and  a.creator='{0}'".format(p_username)
    else:
        if p_creator != '':
            v_where = v_where + " and a.creator='{0}'\n".format(p_creator)

    if p_name != '':
       v_where = v_where + " and a.sqltext like '%{0}%'\n".format(p_name)

    if p_order_ver != '':
        v_where = v_where + " and a.order_ver='{0}'\n".format(p_order_ver)

    if p_order_env != '':
        v_where = v_where + " and a.order_env='{0}'\n".format(p_order_env)

    sql = """SELECT  
                     (select dmmc from t_dmmx f where f.dm='12' and f.dmm=a.order_ver) as order_ver,
                     (select flag1 from t_db_source f where f.id=a.order_env) as order_env,
                     a.order_number,
                     c.dmmc AS 'order_type',
                     CASE a.order_status 
                           WHEN '0' THEN '已发布'
                           WHEN '1' THEN '已审核'
                           WHEN '2' THEN '审核失败'
                     END  order_status,  
                     
                     (SELECT NAME FROM t_user e WHERE e.login_name=a.creator) creator,
                     DATE_FORMAT(a.create_date,'%Y-%m-%d %h:%i:%s')  create_date,
                     DATE_FORMAT(a.last_update_date,'%Y-%m-%d %h:%i:%s')  last_update_date,
                     DATE_FORMAT(a.audit_date,'%y-%m-%d %h:%i:%s')   audit_date,
                     '{}'
            FROM t_sql_online a, t_dmmx c
            WHERE  c.dm='46'
              AND a.order_type=c.dmm
              {} order by a.create_date desc
          """.format(p_username,v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def query_online_detail(p_order_number,p_userid):
    sql = """SELECT 
                 order_env,
                 order_number,
                 order_type,
                 order_ver,
                 (select dmmc2 from t_dmmx b where b.dm=12 and b.dmm=a.order_ver) as order_ver_desc,
                 order_status,                
                 creator,
                 date_format(a.create_date,'%Y-%m-%d') as  create_date,
                 updator,
                 date_format(a.last_update_date,'%Y-%m-%d %H:%i:%s') as  last_update_date,
                 auditor,
                 date_format(a.audit_date,'%Y-%m-%d %H:%i:%s') as  audit_date,
                 (SELECT dmmc FROM t_dmmx WHERE dm='13' AND dmm=a.order_type) AS order_type_name,
                 (SELECT dmmc FROM t_dmmx WHERE dm='41' AND dmm=a.order_status) AS order_status_name,       
                 (SELECT dmmc FROM t_dmmx WHERE dm='12' AND dmm=a.order_ver) AS order_ver_name,             
                 (SELECT NAME FROM t_user WHERE login_name=a.creator) AS creator_name,
                 (SELECT NAME FROM t_user WHERE login_name=a.auditor) AS auditor_name,
                 (select flag1 from t_db_source f where f.id=a.order_env) as order_env_name,
                 sqltext,
                 audit_message,
                 '{0}' as curr_user
                FROM t_sql_online a where order_number='{1}'""".format(p_userid,p_order_number)
    rs = await async_processer.query_dict_one(sql)
    print('query_online_detail=',rs)
    return rs

async def query_online_ver_desc(p_dmm):
    try:
        sql = "SELECT  dmmc2 FROM t_dmmx WHERE dm=12 and dmm='{}'".format(p_dmm)
        rs = await async_processer.query_dict_one(sql)
        return rs
    except:
        return {'dmmc2': ''}


async def check_online_order(p_ver):
    try:
        st ="""SELECT COUNT(0) as xh FROM t_sql_online WHERE order_number='{}'""".format(p_ver)
        rs = await async_processer.query_dict_one(st)
        if rs['xh']>0:
           return True
        else:
           return False
    except:
        traceback.print_exc()
        return False

async def delete_online_order(p_order_number):
    result = {}
    try:
        order = await query_online_detail(p_order_number,'')
        if order['order_status'] =='1':
            result['code'] = '-1'
            result['message'] = '不能删除已审核工单!'
            return result
        sql = "delete from t_sql_online  where order_number='{0}'".format(p_order_number)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='删除成功!'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result

async def audit_online_order(p_order_number,audit_status,audit_message,p_username):
    result = {}
    try:
        if await check_online_order(p_order_number):
            sql = """update t_sql_online 
                         set order_status='{}',
                             auditor='{}',
                             audit_message='{}',
                             audit_date=now()
                         where order_number='{}'""".format(audit_status,p_username,audit_message,p_order_number)
            await async_processer.exec_sql(sql)
            result['code']='0'
            result['message']='审核成功!'
            return result
        else:
            result['code'] = '-1'
            result['message'] = '`{}`工单不存在!'.format(p_order_number)
            return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '审核失败!'
        return result

async def audit_canal_online_order(p_order_number):
    result = {}
    try:
        if await check_online_order(p_order_number):
            sql = "update t_sql_online set order_status='0',auditor='',audit_date=null where order_number='{0}'".format(p_order_number)
            await async_processer.exec_sql(sql)
            result['code']='0'
            result['message']='取消审核成功!'
            return result
        else:
            result['code'] = '-1'
            result['message'] = '`{}`工单不存在!'.format(p_order_number)
            return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '审核失败!'
        return result