#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/17 9:35
# @Author : 马飞
# @File : t_dmmx.py
# @Software: PyCharm

import traceback
from web.utils.mysql_async import async_processer
from web.utils.mysql_sync import sync_processer

async def get_dmm_from_dm(p_dm):
    sql = "select dmm,dmmc from t_dmmx where dm='{0}'".format(p_dm)
    return await async_processer.query_list(sql)

async def get_dmm_from_dm_cipher(p_dm):
    sql = "select dmm,dmmc from t_dmmx where dm='{0}' and dmm in('1','2','3','4')".format(p_dm)
    return await async_processer.query_list(sql)

async def get_dmm_from_dm2(p_dm,p_dmm):
    sql = "select dmm,dmmc from t_dmmx where dm='{0}' and instr('{1}',dmm)>0".format(p_dm,p_dmm)
    return await async_processer.query_list(sql)

async def get_dmlx_from_dm_bbgl():
    sql = "select dm,mc from t_bbgl_dmlx order by mc"
    return await async_processer.query_list(sql)

async def get_dmm_from_dm_bbgl(p_dm):
    sql = "select dmm,dmmc from t_bbgl_dmmx where dm='{0}'".format(p_dm)
    return await async_processer.query_list(sql)

async def get_dmmc_from_dm(p_dm,p_dmm):
    sql = "select dmmc from t_dmmx where dm='{0}' and dmm={1}".format(p_dm,p_dmm)
    return await async_processer.query_one(sql)

def get_dmmc_from_dm_sync(p_dm,p_dmm):
    sql = "select dmmc from t_dmmx where dm='{0}' and dmm={1}".format(p_dm,p_dmm)
    return  sync_processer.query_one(sql)

async def get_users_from_proj(p_userid):
    sql = """select id,concat(name,'(',wkno,')') from t_user 
              where project_group=(select project_group from t_user where id='{0}')""".format(p_userid)
    return await async_processer.query_list(sql)

async def get_users(p_username):
    if p_username=='admin':
       sql = """select login_name,concat(name,'(',wkno,')') from t_user order by id """
    else:
       sql = """select login_name,concat(name,'(',wkno,')') from t_user where login_name='{}' order by id """.format(p_username)
    return await async_processer.query_list(sql)

async def get_users_by_query_grants(p_username):
    if p_username=='admin':
       sql = """select id,concat(name,'(',wkno,')') from t_user order by id """
    else:
       sql = """select id,concat(name,'(',wkno,')') from t_user where login_name='{}' order by id """.format(p_username)
    return await async_processer.query_list(sql)

async def get_sys_dmlx():
    sql = "select dm,mc from t_dmlx where flag='1' order by dm"
    return await async_processer.query_list(sql)

async def get_sys_dmlx_from_dm(p_dm):
    sql = "select dm,mc from t_dmlx where flag='1' and dm='{}' order by dm".format(p_dm)
    return await async_processer.query_list(sql)

async def get_backup_server():
    sql = "select id,server_desc from t_server WHERE server_type=1 order by market_id"
    return  await async_processer.query_list(sql)

async def get_sync_server():
    sql = "select id,server_desc from t_server WHERE server_type=2 order by market_id"
    return await async_processer.query_list(sql)

async def get_gather_server():
    sql = "select id,server_desc from t_server WHERE status='1' order by market_id,server_desc"
    return await async_processer.query_list(sql)

async def get_templete_names():
    sql = "select id,name from t_monitor_templete WHERE status='1' order by id"
    return await async_processer.query_list(sql)

async def get_gather_tasks():
    sql = "select id,comments from t_monitor_task WHERE status='1' order by id"
    return await async_processer.query_list(sql)

async def get_slow_dbs_names(p_env):
    if p_env == '':
        sql = "SELECT a.ds_id,b.db_desc FROM t_slow_log a,t_db_source b WHERE  a.ds_id=b.id AND a.STATUS='1' order by b.db_desc"
    else:
        sql = "SELECT a.ds_id,b.db_desc FROM t_slow_log a,t_db_source b WHERE  a.ds_id=b.id AND a.STATUS='1' and b.db_env='{}' order by b.db_desc".format(p_env)
    return await async_processer.query_list(sql)

async def get_slow_inst_names(p_env):
    if p_env == '':
        sql = "SELECT a.inst_id, b.inst_name FROM t_slow_log a,t_db_inst b WHERE  a.inst_id=b.id AND a.STATUS='1' order by b.inst_name"
    else:
        sql = "SELECT a.inst_id, b.inst_name FROM t_slow_log a,t_db_inst b WHERE  a.inst_id=b.id AND a.STATUS='1'  and b.inst_env='{}'  order by b.inst_name".format(p_env)
    return await async_processer.query_list(sql)

async def get_db_server():
    sql = "SELECT id,db_desc FROM t_db_source WHERE  db_type in(0,1,2,3,4,5,6) AND STATUS=1 ORDER BY id"
    return await async_processer.query_list(sql)

async def get_db_backup_server():
    sql = """SELECT id,db_desc FROM t_db_source 
             WHERE  (db_type in(0)  and user in('puppet','easylife','apptong') or db_type not in (0))
                and STATUS=1 ORDER BY db_desc,db_type"""
    return await async_processer.query_list(sql)

async def get_db_backup_tags():
    sql = """SELECT db_tag,comments FROM t_db_config  WHERE STATUS=1  ORDER BY db_type,db_id"""
    return await async_processer.query_list(sql)

async def get_minio_tags():
    sql = """SELECT sync_tag,comments FROM t_minio_config  WHERE STATUS=1  ORDER BY sync_tag """
    return await async_processer.query_list(sql)

async def get_db_sync_tags():
    sql = """SELECT sync_tag,comments FROM t_db_sync_config  WHERE STATUS=1  ORDER BY sync_ywlx,comments"""
    return await async_processer.query_list(sql)

async def get_datax_sync_tags():
    sql = """SELECT sync_tag,comments FROM t_datax_sync_config  WHERE STATUS=1  ORDER BY comments"""
    return await async_processer.query_list(sql)

async def get_db_sync_tags_by_market_id(market_id):
    if market_id=='':
        sql = """SELECT sync_tag,comments FROM t_db_sync_config  WHERE STATUS=1   ORDER BY sync_col_val,comments"""
    else:
        sql = """SELECT sync_tag,comments FROM t_db_sync_config  
                    WHERE STATUS=1  and INSTR(sync_col_val,'{0}')>0  ORDER BY sync_col_val,comments 
              """.format(market_id)
    return  await async_processer.query_list(sql)

async def get_db_sync_ywlx_by_market_id(market_id):
    if market_id=='':
        sql = """SELECT dmm,dmmc FROM t_dmmx WHERE dm='08' ORDER BY dmm """
    else:
        sql = """SELECT a.dmm,a.dmmc FROM t_dmmx a 
                 WHERE dm='08' 
                   AND EXISTS(SELECT 1 FROM t_db_sync_config b
                               WHERE b.status='1'
                                 AND b.sync_ywlx=a.dmm
                                 AND b.sync_col_val='{0}')
                 ORDER BY a.dmm 
              """.format(market_id)
    return await async_processer.query_list(sql)

async def get_db_sync_ywlx():
    sql = """SELECT dmm,dmmc FROM t_dmmx WHERE dm='08' ORDER BY dmm"""
    return await async_processer.query_list(sql)

async def get_db_backup_tags_by_env_type(p_env,p_type):
    v_where = ''
    if p_type != '':
        v_where=v_where+" and c.db_type='{0}'\n".format(p_type)

    if p_env != '':
        v_where=v_where+" and c.db_env='{0}'\n".format(p_env)

    sql = """SELECT a.db_tag,a.comments
             FROM t_db_config a ,t_server b,t_db_source c
               WHERE a.STATUS=1 AND a.server_id=b.id AND a.db_id=c.id
               {0}
             ORDER BY c.db_type,a.db_id
          """.format(v_where)
    return await async_processer.query_list(sql)


async def get_sync_db_server():
    sql = """SELECT id,db_desc FROM t_db_source 
            WHERE  db_type in(0,1,2,3,4,5,6) and db_env in(1,2,3,4,5,6)  and STATUS=1  ORDER BY db_desc,db_type"""
    return await async_processer.query_list(sql)

async def get_bbtj_db_server():
    sql = """SELECT id,db_desc FROM t_db_source 
              WHERE  id in(16,19,191,49,69,84,93) ORDER BY db_desc,db_type"""
    return await async_processer.query_list(sql)

async def get_sync_db_mysql_server():
    sql = """SELECT id,db_desc FROM t_db_source 
            WHERE  db_type in(0) and db_env in(1,2,3,4,5,6)  and STATUS=1  ORDER BY db_desc,db_type"""
    return await async_processer.query_list(sql)


async def get_db_moitor_templates():
    sql = """SELECT t.id,t.name FROM t_monitor_templete t WHERE t.type='2' AND t.name LIKE '%监控%';"""
    return await async_processer.query_list(sql)


async def get_sync_db_server_by_type(p_type):
    try:
        result = {}
        sql = """SELECT cast(id as char) id,db_desc FROM t_db_source 
                    WHERE  db_type ='{0}' and db_env in(1,2,3,4) 
                       and status=1  and user!='puppet'  ORDER BY db_desc,db_type""".format(p_type)
        result['code'] = '0'
        result['message'] = await async_processer.query_list(sql)
        return result
    except :
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '获取数据库名失败！'
        return result


async def get_datax_sync_db_server():
    sql = """select id,db_desc from t_db_source  where  db_type in(0) and db_env in(1,2,3,4) 
                and STATUS=1 and user!='puppet' order by db_desc,db_type"""
    return await async_processer.query_list(sql)

async def get_datax_sync_db_server_doris():
    sql = """select id,db_desc from t_db_source  where  db_type in(8) and db_env in(1,2,3,4) 
                and STATUS=1 and user!='puppet' order by db_desc,db_type"""
    return await async_processer.query_list(sql)

async def get_datax_real_sync_db_server():
    sql = """select id,db_desc from t_db_source  where  db_type in(0,8,9,10) and db_env in(1,2,3,4) 
                and STATUS=1  order by db_desc,db_type"""
    return await async_processer.query_list(sql)


async def get_compare_db_server():
    sql = """select id,db_desc from t_db_source  where  db_type in(0,8,9) and db_env in(1,2,3,4) 
                and STATUS=1 and user!='puppet' order by db_type,db_desc"""
    return await async_processer.query_list(sql)
