#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import traceback

import requests

from web.utils.common import format_sql
from web.utils.mysql_async import async_processer


async def query_sync(sync_tag, market_id, sync_ywlx, sync_type, task_status):
    v_where = ' and  1=1 '
    if sync_tag != '':
        v_where = v_where + " and ( a.sync_tag like '%{}%' or lower(sync_table) LIKE '%{}%' OR lower(sync_schema) LIKE '%{}%') \n".format(
            sync_tag, sync_tag, sync_tag)
    if market_id != '':
        v_where = v_where + " and instr(a.sync_col_val,'{0}')>0\n".format(market_id)
    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)
    if sync_type != '':
        v_where = v_where + " and a.sync_type='{0}'\n".format(sync_type)
    if task_status != '':
        v_where = v_where + " and a.status='{0}'\n".format(task_status)
    sql = """SELECT  a.id,
                     concat(substr(a.sync_tag,1,40),'...') as sync_tag_,             
                     a.sync_tag,
                     concat(substr(a.comments,1,30),'...') as comments,
                     CONCAT(b.server_ip,':',b.server_port) AS sync_server,
                     c.dmmc AS  sync_ywlx,
                     a.run_time,
                     CASE WHEN INSTR(api_server,',')>0 THEN 
                        SUBSTR(a.api_server,1,INSTR(a.api_server,',')-1)
                     ELSE                         
                        a.api_server
                     END AS api_server ,
                     a.api_server as back_api_server,
                     CASE a.status WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS,
                     CASE a.task_status 
                       WHEN '1' THEN 
                      CONCAT('<span style=''color: red''>运行中(',TIMESTAMPDIFF(SECOND,a.task_create_time,NOW()),'s)</span>')
                       WHEN '0' THEN '停止' END  STATUS
             FROM t_db_sync_config a,t_server b ,t_dmmx c,t_dmmx d
            WHERE a.server_id=b.id AND b.status='1' 
              AND c.dm='08' AND d.dm='09'
              AND a.sync_ywlx=c.dmm
              AND a.sync_type=d.dmm {0} """.format(v_where)
    return await async_processer.query_list(sql)


async def query_sync_tab(sync_tag, sync_tab):
    sql = """SELECT  
                    a.id,
                    a.db_name,
                    a.schema_name,
                    a.tab_name,
                    a.sync_cols,
                    a.sync_incr_col,
                    a.sync_time
             FROM t_db_sync_tab_config a
            WHERE a.sync_tag='{}' 
             and  instr(a.tab_name,'{}')>0
            order by 1
              """.format(sync_tag, sync_tab)
    print(sql)
    return await async_processer.query_list(sql)


async def query_sync_id(sync_id):
    sql = """SELECT * FROM t_db_sync_config a WHERE a.id='{}'""".format(sync_id)
    print(sql)
    return await async_processer.query_dict_one2(sql)


async def query_sync_tab_real(sync_tag, sync_tab):
    sql = """SELECT  
                    a.id,
                    a.db_name,
                    a.tab_name,
                    a.sync_incr_col,
                    a.schema_name,
                    a.status
             FROM t_db_sync_tab_config a
            WHERE a.sync_tag='{}' 
             and  (instr(a.tab_name,'{}')>0 or instr(a.db_name,'{}')>0  or instr(a.sync_incr_col,'{}')>0 )
            order by 1
              """.format(sync_tag, sync_tab, sync_tab, sync_tab)
    print('query_sync_tab_real=', sql)
    return await async_processer.query_list(sql)


async def query_sync_tab_cfg(sync_tag):
    sql = """SELECT  
                GROUP_CONCAT(
                    CONCAT(    
                       IF (a.schema_name='',a.tab_name,CONCAT(a.schema_name,'.',a.tab_name)),   
                       ':',
                       a.sync_incr_col,
                       ':',
                       a.sync_time)) AS sync_tab
             FROM t_db_sync_tab_config a
            WHERE a.sync_tag='{}' 
            order by 1
          """.format(sync_tag)
    rs = await async_processer.query_one(sql)
    if rs[0] is None:
        return 'None'
    else:
        return rs[0]


# async def query_sync_tab_cfg_real(sync_tag):
#     sql = """SELECT
#                 GROUP_CONCAT(CONCAT(a.db_name,'.',a.tab_name,'$',a.schema_name)) AS sync_tab
#              FROM t_db_sync_tab_config a
#             WHERE a.sync_tag='{}'  and a.status='1'
#             order by 1
#           """.format(sync_tag)
#     rs = await async_processer.query_one(sql)
#     if rs[0] is None :
#        return 'None'
#     else:
#        return rs[0]

async def query_sync_tab_cfg_real(sync_tag):
    sql = """SELECT  
                CONCAT(a.db_name,'.',a.tab_name,'.',a.sync_incr_col,'$',a.schema_name) 
             FROM t_db_sync_tab_config a
            WHERE a.sync_tag='{}'  and a.status='1'
            order by 1
          """.format(sync_tag)
    print('query_sync_tab_cfg_real=', sql)
    rs = await async_processer.query_list(sql)
    v = ''
    for r in rs:
        v = v + r[0] + ','
    return v[0:-1]


async def query_sync_tag_by_id(sync_id):
    sql = "select sync_tag FROM t_db_sync_tab_config where id='{}'".format(sync_id)
    return (await async_processer.query_dict_one(sql))['sync_tag']


async def query_sync_log(sync_tag, market_id, sync_ywlx, begin_date, end_date):
    v_where = ' and 1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(sync_tag)
    if market_id != '':
        v_where = v_where + " and a.sync_col_val='{0}'\n".format(market_id)
    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)
    if begin_date != '':
        v_where = v_where + " and b.create_date>='{0}'\n".format(begin_date + ' 0:0:0')
    else:
        v_where = v_where + " and b.create_date>=DATE_ADD(NOW(),INTERVAL -1 hour)\n"
    if end_date != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(end_date + ' 23:59:59')
    sql = """SELECT b.id,
                    c.dmmc as market_name,
                    a.comments,
                    b.sync_tag,
                    cast(b.create_date as char),
                    b.duration,
                    b.amount
            FROM  t_db_sync_config a,t_db_sync_tasks_log b,t_dmmx c
            WHERE a.sync_tag=b.sync_tag 
              and c.dm='05' 
              and instr(a.sync_col_val,c.dmm)>0
              and a.status='1'  {0}""".format(v_where)
    return await async_processer.query_list(sql)


async def query_sync_log_analyze(market_id, tagname, begin_date, end_date):
    v_where = ' where 1=1 '
    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and instr(b.sync_col_val,'{0}')>0) \n".format(
            market_id)
    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date + ' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date + ' 23:59:59')
    if tagname.count('logger') == 0 and tagname.count('executer') == 0:
        sql1 = """SELECT  cast(a.create_date as char) as create_date,a.duration  FROM t_db_sync_tasks_log a  {0}  ORDER BY a.create_date """.format(
            v_where)
        sql2 = """SELECT  cast(a.create_date as char) as create_date,a.amount FROM t_db_sync_tasks_log a {0}  ORDER BY a.create_date""".format(
            v_where)
        return await async_processer.query_list(sql1), await async_processer.query_list(sql2), []
    else:
        sql1 = """SELECT  cast(a.create_date as char) as create_date,a.event_amount  FROM t_db_sync_real_log a  {0}  ORDER BY a.create_date """.format(
            v_where)
        return [], [], await async_processer.query_list(sql1)


async def query_sync_log_analyze2(market_id, sync_type, begin_date, end_date):
    v_where = ' where 1=1 '
    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(
            market_id)
    if sync_type != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_type)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date + ' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date + ' 23:59:59')
    sql1 = """SELECT  cast(a.create_date as char) as create_date,a.duration  FROM t_db_sync_tasks_log a {0} ORDER BY a.create_date""".format(
        v_where)
    sql2 = """SELECT cast(a.create_date as char) as create_date,a.amount  FROM t_db_sync_tasks_log a {0}  ORDER BY a.create_date""".format(
        v_where)
    return await async_processer.query_list(sql1), await async_processer.query_list(sql2)


async def query_sync_log_detail(p_tag, p_sync_rqq, p_sync_rqz):
    v_where = ' and 1=1 '
    if p_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(p_tag)
    if p_sync_rqq != '':
        v_where = v_where + " and b.create_date>='{0}' \n".format(p_sync_rqq + ' 0:0:0')
    if p_sync_rqz != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(p_sync_rqz + ' 23:59:59')
    sql = """SELECT 
                 a.comments,
                 b.sync_tag,
                 b.sync_table,
                 CAST(b.create_date AS CHAR), 
                 b.sync_amount,
                 b.duration 
                FROM 
                 t_db_sync_config a,t_db_sync_tasks_log_detail b
                WHERE  a.sync_tag=b.sync_tag 
                   AND a.status='1' {0} """.format(v_where)
    return await async_processer.query_list(sql)


async def save_sync(p_backup):
    val = await check_sync(p_backup, 'add')
    if val['code'] == '-1':
        return val
    try:
        result = {}
        sync_server = p_backup['sync_server']
        sour_db_server = p_backup['sour_db_server']
        desc_db_server = p_backup['desc_db_server']
        sync_tag = p_backup['sync_tag']
        sync_ywlx = p_backup['sync_ywlx']
        sync_type = p_backup['sync_data_type']
        script_base = p_backup['script_base']
        script_name = p_backup['script_name']
        run_time = p_backup['run_time']
        task_desc = p_backup['task_desc']
        python3_home = p_backup['python3_home']
        sync_schema = p_backup['sync_schema']
        sync_schema_dest = p_backup['sync_schema_dest']
        sync_tables = p_backup['sync_tables']
        sync_batch_size = p_backup['sync_batch_size']
        sync_batch_size_incr = p_backup['sync_batch_size_incr']
        sync_gap = p_backup['sync_gap']
        sync_col_name = p_backup['sync_col_name']
        sync_col_val = format_sql(p_backup['sync_col_val'])
        sync_time_type = p_backup['sync_time_type']
        sync_repair_day = p_backup['sync_repair_day']
        api_server = p_backup['api_server']
        status = p_backup['status']
        if sync_schema_dest == '':
            sql = """insert into t_db_sync_config(
                                  sour_db_id,desc_db_id,server_id,
                                  sync_tag,sync_ywlx,sync_type,
                                  comments,run_time,sync_table,sync_schema,
                                  batch_size,batch_size_incr,sync_gap,
                                  script_path,script_file,python3_home,api_server,
                                  sync_col_name,sync_col_val,sync_time_type,status,sync_schema_dest,sync_repair_day)
                          values('{0}','{1}','{2}',
                                 '{3}','{4}','{5}',
                                 '{6}','{7}','{8}','{9}',
                                 '{10}','{11}','{12}',
                                 '{13}','{14}','{15}','{16}',
                                 '{17}','{18}','{19}','{20}',null,'{21}')
                       """.format(sour_db_server, desc_db_server, sync_server,
                                  sync_tag, sync_ywlx, sync_type,
                                  task_desc, run_time, sync_tables, sync_schema,
                                  sync_batch_size, sync_batch_size_incr, sync_gap,
                                  script_base, script_name, python3_home, api_server,
                                  sync_col_name, sync_col_val, sync_time_type, status, sync_repair_day)

        else:
            sql = """insert into t_db_sync_config(
                           sour_db_id,desc_db_id,server_id,
                           sync_tag,sync_ywlx,sync_type,
                           comments,run_time,sync_table,sync_schema,
                           batch_size,batch_size_incr,sync_gap,
                           script_path,script_file,python3_home,api_server,
                           sync_col_name,sync_col_val,sync_time_type,status,sync_schema_dest,sync_repair_day)
                   values('{0}','{1}','{2}',
                          '{3}','{4}','{5}',
                          '{6}','{7}','{8}','{9}',
                          '{10}','{11}','{12}',
                          '{13}','{14}','{15}','{16}',
                          '{17}','{18}','{19}','{20}','{21}','{22}')
                """.format(sour_db_server, desc_db_server, sync_server,
                           sync_tag, sync_ywlx, sync_type,
                           task_desc, run_time, sync_tables, sync_schema,
                           sync_batch_size, sync_batch_size_incr, sync_gap,
                           script_base, script_name, python3_home, api_server,
                           sync_col_name, sync_col_val, sync_time_type, status, sync_schema_dest, sync_repair_day)
        await async_processer.exec_sql(sql)
        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def save_sync_real(p_backup):
    val = await check_sync_real(p_backup, 'add')
    if val['code'] == '-1':
        return val
    try:
        result = {}
        sync_server = p_backup['sync_server']
        sour_db_server = p_backup['sour_db_server']
        desc_db_server = p_backup['desc_db_server']
        sour_db_log_server = p_backup['sour_db_log_server']
        log_db_name = p_backup['log_db_name']
        sync_tag = p_backup['sync_tag']
        sync_ywlx = p_backup['sync_ywlx']
        sync_type = p_backup['sync_data_type']
        script_base = p_backup['script_base']
        script_name = p_backup['script_name']
        run_time = p_backup['run_time']
        task_desc = p_backup['task_desc']
        python3_home = p_backup['python3_home']
        sync_tables = p_backup['sync_tables']
        sync_batch_size = p_backup['sync_batch_size']
        sync_batch_size_incr = p_backup['sync_batch_size_incr']
        sync_gap = p_backup['sync_gap']
        process_num = p_backup['process_num']
        apply_timeout = p_backup['apply_timeout']
        api_server = p_backup['api_server']
        status = p_backup['status']
        desc_db_prefix = p_backup['desc_db_prefix']
        ch_cluster_name = p_backup['ch_cluster_name']
        real_sync_status = p_backup['real_sync_status']

        st = """insert into t_db_sync_config(
                          sour_db_id,desc_db_id,server_id,sync_tag,sync_ywlx,sync_type,
                          comments,run_time,sync_table,batch_size,batch_size_incr,script_path,
                          script_file,python3_home,api_server,status,
                          sync_gap,process_num,desc_db_prefix,apply_timeout,log_db_id,log_db_name,ch_cluster_name,real_sync_status)
                  values('{0}','{1}','{2}','{3}','{4}','{5}',
                         '{6}','{7}','{8}','{9}','{10}','{11}',
                         '{12}','{13}','{14}','{15}',
                         '{16}','{17}','{18}','{19}',
                         '{20}','{21}','{22}','{23}')
               """.format(sour_db_server, desc_db_server, sync_server, sync_tag, sync_ywlx, sync_type,
                          task_desc, run_time, sync_tables, sync_batch_size, sync_batch_size_incr, script_base,
                          script_name, python3_home, api_server, status,
                          sync_gap, process_num, desc_db_prefix, apply_timeout,
                          sour_db_log_server, log_db_name, ch_cluster_name, real_sync_status)
        await async_processer.exec_sql(st)

        # st = """insert into t_db_sync_tab_config(sync_tag,db_name,schema_name,tab_name,STATUS)
        #         select sync_tag,db_name,schema_name,tab_name,status
        #         from t_db_sync_tab_config
        #         where sync_tag='{}')
        #      """.format(sync_tag,sync_tag)
        # await async_processer.exec_sql(st)

        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def save_sync_clone_real(p_backup):
    val = await check_sync_real(p_backup, 'clone')
    if val['code'] == '-1':
        return val
    try:
        result = {}
        sync_id = p_backup['sync_id']
        sync_server = p_backup['sync_server']
        sour_db_server = p_backup['sour_db_server']
        desc_db_server = p_backup['desc_db_server']
        sour_db_log_server = p_backup['sour_db_log_server']
        log_db_name = p_backup['log_db_name']
        sync_tag = p_backup['sync_tag']
        sync_ywlx = p_backup['sync_ywlx']
        sync_type = p_backup['sync_data_type']
        script_base = p_backup['script_base']
        script_name = p_backup['script_name']
        run_time = p_backup['run_time']
        task_desc = p_backup['task_desc']
        python3_home = p_backup['python3_home']
        sync_tables = p_backup['sync_tables']
        sync_batch_size = p_backup['sync_batch_size']
        sync_batch_size_incr = p_backup['sync_batch_size_incr']
        sync_gap = p_backup['sync_gap']
        process_num = p_backup['process_num']
        apply_timeout = p_backup['apply_timeout']
        api_server = p_backup['api_server']
        status = p_backup['status']
        desc_db_prefix = p_backup['desc_db_prefix']
        ch_cluster_name = p_backup['ch_cluster_name']
        real_sync_status = p_backup['real_sync_status']

        st = """insert into t_db_sync_config(
                          sour_db_id,desc_db_id,server_id,sync_tag,sync_ywlx,sync_type,
                          comments,run_time,sync_table,batch_size,batch_size_incr,script_path,
                          script_file,python3_home,api_server,status,
                          sync_gap,process_num,desc_db_prefix,apply_timeout,log_db_id,log_db_name,
                          ch_cluster_name,real_sync_status)
                  values('{0}','{1}','{2}','{3}','{4}','{5}',
                         '{6}','{7}','{8}','{9}','{10}','{11}',
                         '{12}','{13}','{14}','{15}',
                         '{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}')
               """.format(sour_db_server, desc_db_server, sync_server, sync_tag, sync_ywlx, sync_type,
                          task_desc, run_time, sync_tables, sync_batch_size, sync_batch_size_incr, script_base,
                          script_name, python3_home, api_server, status,
                          sync_gap, process_num, desc_db_prefix, apply_timeout, sour_db_log_server, log_db_name,
                          ch_cluster_name, real_sync_status)
        await async_processer.exec_sql(st)

        st = """delete from t_db_sync_tab_config where sync_tag='{}'""".format(sync_tag)
        await async_processer.exec_sql(st)
        st = """insert into t_db_sync_tab_config(sync_tag,db_name,schema_name,tab_name,sync_incr_col,STATUS)
                select '{}',db_name,schema_name,tab_name,sync_incr_col,status
                from t_db_sync_tab_config
                where sync_tag=(select sync_tag from t_db_sync_config where id='{}')
             """.format(sync_tag, sync_id)
        print('st=', st)
        await async_processer.exec_sql(st)

        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def check_sync_tab(p_sync_id):
    st = "select count(0) from t_db_sync_tab_config where id={}".format(p_sync_id)
    rs = await async_processer.query_one(st)
    return rs[0]


async def save_sync_tab(p_sync):
    try:
        result = {}
        sync_id = p_sync['sync_id']
        sync_tag = p_sync['sync_tag']
        db_name = p_sync['db_name']
        schema_name = p_sync['schema_name']
        tab_name = p_sync['tab_name']
        sync_cols = p_sync['sync_cols']
        sync_incr_col = p_sync['sync_incr_col']
        sync_time = p_sync['sync_time']
        tab_status = p_sync['tab_status']

        if await check_sync_tab(sync_id) == 0:
            sql = """insert into t_db_sync_tab_config(sync_tag,db_name,schema_name,tab_name, sync_cols, sync_incr_col,sync_time,status,create_date)
                       values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',now())
                  """.format(sync_tag, db_name, schema_name, tab_name, sync_cols, sync_incr_col, sync_time, tab_status)
            result['code'] = '0'
            result['message'] = '保存成功!'
        else:
            sql = """update t_db_sync_tab_config 
                       set sync_tag      = '{}',
                           db_name       = '{}',
                           schema_name   = '{}',
                           tab_name      = '{}',
                           sync_cols     = '{}',
                           sync_incr_col = '{}',
                           sync_time     = '{}',
                           update_date   = now(),
                           status        = '{}'
                       where id = '{}'""".format(sync_tag, db_name, schema_name, tab_name, sync_cols, sync_incr_col,
                                                 sync_time, tab_status, sync_id)

            print('sql=', sql)
            result['code'] = '0'
            result['message'] = '更新成功!'
        print('save_sync_tab=', sql)
        await async_processer.exec_sql(sql)

        await async_processer.exec_sql("update t_db_sync_config set sync_table='{}' where sync_tag='{}'".
                                       format(await query_sync_tab_cfg_real(sync_tag), sync_tag))
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败！'
        return result


async def del_sync_tab(p_sync_id):
    try:
        result = {}
        sync_tag = await query_sync_tag_by_id(p_sync_id)

        st = "delete from t_db_sync_tab_config where id={}".format(p_sync_id)
        await async_processer.exec_sql(st)

        st = """update t_db_sync_config set sync_table='{}' where sync_tag='{}'""". \
            format(await query_sync_tab_cfg_real(sync_tag), sync_tag)
        await async_processer.exec_sql(st)

        result['code'] = '0'
        result['message'] = '删除成功！'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '删除失败！'
        return result


async def upd_sync(p_sync):
    result = {}
    val = await check_sync(p_sync, 'upd')
    if val['code'] == '-1':
        return val
    try:
        sync_server = p_sync['sync_server']
        sour_db_server = p_sync['sour_db_server']
        desc_db_server = p_sync['desc_db_server']
        sync_tag = p_sync['sync_tag']
        sync_ywlx = p_sync['sync_ywlx']
        sync_type = p_sync['sync_data_type']
        script_base = p_sync['script_base']
        script_name = p_sync['script_name']
        run_time = p_sync['run_time']
        task_desc = p_sync['task_desc']
        python3_home = p_sync['python3_home']
        sync_schema = p_sync['sync_schema']
        sync_schema_dest = p_sync['sync_schema_dest']
        sync_tables = p_sync['sync_tables']
        sync_batch_size = p_sync['sync_batch_size']
        sync_batch_size_incr = p_sync['sync_batch_size_incr']
        sync_gap = p_sync['sync_gap']
        sync_col_name = p_sync['sync_col_name']
        sync_col_val = format_sql(p_sync['sync_col_val'])
        sync_time_type = p_sync['sync_time_type']
        sync_repair_day = p_sync['sync_repair_day']
        api_server = p_sync['api_server']
        status = p_sync['status']
        sync_id = p_sync['sync_id']
        if sync_schema_dest == '':
            sql = """update t_db_sync_config 
                      set server_id         ='{0}',
                          sour_db_id        ='{1}',     
                          desc_db_id        ='{2}',
                          sync_tag          ='{3}',
                          sync_ywlx         ='{4}',
                          sync_type         ='{5}',
                          comments          ='{6}',
                          run_time          ='{7}',
                          sync_table        ='{8}',
                          sync_schema       ='{9}',
                          batch_size        ='{10}',
                          batch_size_incr   ='{11}',
                          sync_gap          ='{12}',
                          script_path       ='{13}',
                          script_file       ='{14}',
                          python3_home      ='{15}',
                          api_server        ='{16}',
                          sync_col_name     ='{17}',
                          sync_col_val      ='{18}',
                          sync_time_type    ='{19}',
                          status            ='{20}',
                          sync_schema_dest  = null,
                          sync_repair_day   = '{21}'
                    where id={22}""".format(sync_server, sour_db_server, desc_db_server,
                                            sync_tag, sync_ywlx, sync_type,
                                            task_desc, run_time, sync_tables,
                                            sync_schema, sync_batch_size, sync_batch_size_incr,
                                            sync_gap, script_base, script_name,
                                            python3_home, api_server, sync_col_name,
                                            sync_col_val, sync_time_type, status, sync_repair_day, sync_id)
        else:
            sql = """update t_db_sync_config 
                         set server_id         ='{0}',
                             sour_db_id        ='{1}',     
                             desc_db_id        ='{2}',
                             sync_tag          ='{3}',
                             sync_ywlx         ='{4}',
                             sync_type         ='{5}',
                             comments          ='{6}',
                             run_time          ='{7}',
                             sync_table        ='{8}',
                             sync_schema       ='{9}',
                             batch_size        ='{10}',
                             batch_size_incr   ='{11}',
                             sync_gap          ='{12}',
                             script_path       ='{13}',
                             script_file       ='{14}',
                             python3_home      ='{15}',
                             api_server        ='{16}',
                             sync_col_name     ='{17}',
                             sync_col_val      ='{18}',
                             sync_time_type    ='{19}',
                             status            ='{20}',
                             sync_schema_dest  ='{21}',
                             sync_repair_day   ='{22}'
                       where id={23}""".format(sync_server, sour_db_server, desc_db_server,
                                               sync_tag, sync_ywlx, sync_type,
                                               task_desc, run_time, sync_tables,
                                               sync_schema, sync_batch_size, sync_batch_size_incr,
                                               sync_gap, script_base, script_name,
                                               python3_home, api_server, sync_col_name,
                                               sync_col_val, sync_time_type, status,
                                               sync_schema_dest, sync_repair_day, sync_id)
        await async_processer.exec_sql(sql)
        result = {}
        result['code'] = '0'
        result['message'] = '更新成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '更新失败！'
        return result


async def upd_sync_real(p_sync):
    result = {}
    val = await check_sync(p_sync, 'upd')
    if val['code'] == '-1':
        return val
    try:
        sync_server = p_sync['sync_server']
        sour_db_server = p_sync['sour_db_server']
        desc_db_server = p_sync['desc_db_server']
        sour_db_log_server = p_sync['sour_db_log_server']
        log_db_name = p_sync['log_db_name']
        sync_tag = p_sync['sync_tag']
        sync_ywlx = p_sync['sync_ywlx']
        sync_type = p_sync['sync_data_type']
        script_base = p_sync['script_base']
        script_name = p_sync['script_name']
        run_time = p_sync['run_time']
        task_desc = p_sync['task_desc']
        python3_home = p_sync['python3_home']
        sync_tables = p_sync['sync_tables']
        sync_batch_size = p_sync['sync_batch_size']
        sync_batch_size_incr = p_sync['sync_batch_size_incr']
        sync_gap = p_sync['sync_gap']
        process_num = p_sync['process_num']
        apply_timeout = p_sync['apply_timeout']
        api_server = p_sync['api_server']
        status = p_sync['status']
        sync_id = p_sync['sync_id']
        desc_db_prefix = p_sync['desc_db_prefix']
        ch_cluster_name = p_sync['ch_cluster_name']
        real_sync_status = p_sync['real_sync_status']

        sql = """update t_db_sync_config 
                     set server_id         ='{0}',
                         sour_db_id        ='{1}',
                         desc_db_id        ='{2}',
                         sync_tag          ='{3}',
                         sync_ywlx         ='{4}',
                         sync_type         ='{5}', 
                         comments          ='{6}',
                         run_time          ='{7}',
                         sync_table        ='{8}',
                         batch_size        ='{9}',
                         batch_size_incr   ='{10}',
                         sync_gap          ='{11}',
                         script_path       ='{12}',
                         script_file       ='{13}',
                         python3_home      ='{14}',
                         api_server        ='{15}',
                         status            ='{16}',
                         process_num       ='{17}',
                         apply_timeout     ='{18}',
                         desc_db_prefix    ='{19}',
                         log_db_id         ='{20}',
                         log_db_name       ='{21}',
                         ch_cluster_name   ='{22}',
                         real_sync_status  ='{23}'                             
                   where id={24}""".format(sync_server, sour_db_server, desc_db_server,
                                           sync_tag, sync_ywlx, sync_type,
                                           task_desc, run_time, sync_tables,
                                           sync_batch_size, sync_batch_size_incr, sync_gap,
                                           script_base, script_name, python3_home,
                                           api_server, status, process_num,
                                           apply_timeout, desc_db_prefix, sour_db_log_server, log_db_name,
                                           ch_cluster_name, real_sync_status, sync_id)
        print(sql)
        await async_processer.exec_sql(sql)
        result = {}
        result['code'] = '0'
        result['message'] = '更新成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '更新失败！'
        return result


async def del_sync(p_syncid):
    try:
        sql = "delete from t_db_sync_config  where id='{0}'".format(p_syncid)
        await async_processer.exec_sql(sql)
        result = {}
        result['code'] = '0'
        result['message'] = '删除成功!'
        return result
    except:
        result = {}
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result


async def check_sync_repeat(p_sync):
    result = {}
    sql = """select count(0) from t_db_sync_config where sync_tag='{0}' """.format(p_sync["sync_tag"])
    rs1 = await async_processer.query_one(sql)
    sql = """select count(0) from t_db_sync_config where comments='{0}' """.format(p_sync["task_desc"])
    rs2 = await async_processer.query_one(sql)
    if rs1[0] > 0:
        result['code'] = True
        result['message'] = '数据标识不能重复!'
    elif rs2[0] > 0:
        result['code'] = True
        result['message'] = '同步描述不能重复!'
    else:
        result['code'] = False
        result['message'] = '!'
    return result


async def check_sync(p_server, p_flag):
    result = {}
    if p_server["sync_server"] == "":
        result['code'] = '-1'
        result['message'] = '同步服务器不能为空！'
        return result

    if p_server["sour_db_server"] == "":
        result['code'] = '-1'
        result['message'] = '源端数据库不能为空！'
        return result

    if p_server["desc_db_server"] == "":
        result['code'] = '-1'
        result['message'] = '目标数据库不能为空！'
        return result

    if p_server["sync_tag"] == "":
        result['code'] = '-1'
        result['message'] = '同步标识号不能为空！'
        return result

    if p_server["sync_ywlx"] == "":
        result['code'] = '-1'
        result['message'] = '同步业务类型不能为空！'
        return result

    if p_server["sync_data_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步数据方向不能为空！'
        return result

    if p_server["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '脚本主目录不能为空！'
        return result

    if p_server["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '备份脚本名不能为空！'
        return result

    if p_server["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '运行时间不能为空！'
        return result

    if p_server["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_server["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_server["sync_ywlx"] not in ('21'):
        if p_server["sync_schema"] == "":
            result['code'] = '-1'
            result['message'] = '同步数据库名不能为空！'
            return result

    if p_server["sync_tables"] == "":
        result['code'] = '-1'
        result['message'] = '同步表列表不能为空！'
        return result

    if p_server["sync_batch_size"] == "":
        result['code'] = '-1'
        result['message'] = '全量批大小不能为空！'
        return result

    if p_server["sync_batch_size_incr"] == "":
        result['code'] = '-1'
        result['message'] = '增量批大小不能为空！'
        return result

    if p_server["sync_gap"] == "":
        result['code'] = '-1'
        result['message'] = '同步间隔不能为空！'
        return result

    if p_server["sync_ywlx"] not in ('21'):

        if p_server["sync_col_name"] == "":
            result['code'] = '-1'
            result['message'] = '新增同步列名不能为空！'
            return result

        if p_server["sync_col_val"] == "":
            result['code'] = '-1'
            result['message'] = '新增同步列值不能为空！'
            return result

        if p_server["sync_time_type"] == "":
            result['code'] = '-1'
            result['message'] = '同步时间类型不能为空！'
            return result

    if p_server["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_server["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    if p_flag == 'add':
        v = await  check_sync_repeat(p_server)
        if v['code']:
            result['code'] = '-1'
            result['message'] = v['message']
            return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result


async def check_sync_real(p_server, p_flag):
    result = {}
    if p_server["sync_server"] == "":
        result['code'] = '-1'
        result['message'] = '同步服务器不能为空！'
        return result

    if p_server["sour_db_server"] == "":
        result['code'] = '-1'
        result['message'] = '源端数据库不能为空！'
        return result

    if p_server["desc_db_server"] == "":
        result['code'] = '-1'
        result['message'] = '目标数据库不能为空！'
        return result

    if p_server["sync_tag"] == "":
        result['code'] = '-1'
        result['message'] = '同步标识号不能为空！'
        return result

    if p_server["sync_ywlx"] == "":
        result['code'] = '-1'
        result['message'] = '同步业务类型不能为空！'
        return result

    if p_server["sync_data_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步数据方向不能为空！'
        return result

    if p_server["script_base"] == "":
        result['code'] = '-1'
        result['message'] = '脚本主目录不能为空！'
        return result

    if p_server["script_name"] == "":
        result['code'] = '-1'
        result['message'] = '备份脚本名不能为空！'
        return result

    if p_server["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '检测时间不能为空！'
        return result

    if p_server["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_server["python3_home"] == "":
        result['code'] = '-1'
        result['message'] = 'PYTHON3主目录不能为空！'
        return result

    if p_server["sync_tables"] == "":
        result['code'] = '-1'
        result['message'] = '同步表列表不能为空！'
        return result

    if p_server["sync_batch_size"] == "":
        result['code'] = '-1'
        result['message'] = '全量批大小不能为空！'
        return result

    if p_server["sync_batch_size_incr"] == "":
        result['code'] = '-1'
        result['message'] = '增量批大小不能为空！'
        return result

    if p_server["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_server["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    if p_flag == 'add':
        v = await  check_sync_repeat(p_server)
        if v['code']:
            result['code'] = '-1'
            result['message'] = v['message']
            return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result


async def get_sync_by_syncid(p_syncid):
    sql = """select server_id,
                    sour_db_id  as sour_db_server,
                    desc_db_id  as desc_db_server,
                    sync_tag,
                    sync_ywlx,
                    sync_type   as sync_data_type,
                    script_path as script_base,
                    script_file as script_name,
                    run_time,
                    comments    as task_desc,
                    python3_home,
                    sync_schema,
                    sync_table  as sync_tables,
                    batch_size  as sync_batch_size,
                    batch_size_incr as sync_batch_size_incr,
                    sync_gap,
                    sync_col_name,
                    sync_col_val,
                    sync_time_type,
                    api_server,
                    status,
                    ifnull(sync_schema_dest,'') as sync_schema_dest,
                    sync_repair_day,
                    apply_timeout,
                    process_num,
                    desc_db_prefix,
                    log_db_id,
                    log_db_name,
                    ch_cluster_name,
                    real_sync_status
             from t_db_sync_config where id={0}""".format(p_syncid)
    return await async_processer.query_dict_one(sql)


async def get_sync_by_sync_tag(p_sync_tag):
    sql = "select * from t_db_sync_config where sync_tag='{0}'".format(p_sync_tag)
    return await async_processer.query_dict_one(sql)


def get_health_api_server(api_servers):
    api_status = {}
    for api in api_servers.split(','):
        req = 'http://{}/health'.format(api)
        try:
            res = requests.head(req, timeout=3)
            api_status[api] = res.status_code
        except:
            api_status[api] = 500

    print('api server status:', api_status)
    for key in api_status:
        if api_status[key] == 200:
            print('health api server:', key)
            return key
    return None


def push_sync_task(p_tag, p_api):
    data = {
        'tag': p_tag,
    }

    url = 'http://{}/push_script_remote_sync'.format(get_health_api_server(p_api))
    print('url=', url)
    res = requests.post(url, data=data)
    print('res=', res, data)
    try:
        jres = res.json()
        print('jres=', jres)
        v = ''
        for c in jres['msg']:
            if c.count(p_tag) > 0:
                v = v + "<span class='warning'>" + c + "</span>"
            else:
                v = v + c
            v = v + '<br>'
        print('v=', v)
        jres['msg'] = v
        return jres
    except:
        traceback.print_exc()


def run_sync_task(p_tag, p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/run_script_remote_sync'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    return jres


def stop_sync_task(p_tag, p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/stop_script_remote_sync'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    return jres


async def query_sync_park():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='3' AND b.status='1'           
              AND (a.sync_tag,a.create_date) IN(
                SELECT a.sync_tag, MAX(a.create_date)
                 FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 3 DAY)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_park_real_time():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='4' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 3 HOUR)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_flow():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='1' AND b.status='1'           
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 DAY)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_flow_real_time():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='2' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 HOUR)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_flow_device():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<30 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='5' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 HOUR)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_park_charge():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(MINUTE,a.create_date,NOW())<60 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='7' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 1 DAY)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


async def query_sync_bi():
    sql = """SELECT 
                 b.sync_col_val,  
                 b.comments,
                 date_format(a.create_date,'%Y-%m-%d %H:%i:%s') as create_date,
                 concat(a.duration,''),
                 concat(a.amount,''),
                 CASE WHEN TIMESTAMPDIFF(HOUR,a.create_date,NOW())<3 THEN '√' ELSE '×' END AS flag
            FROM t_db_sync_tasks_log a,t_db_sync_config b
            WHERE a.sync_tag = b.sync_tag 
              AND b.sync_ywlx='18' AND b.status='1'
              AND (a.sync_tag,a.create_date) IN(
                SELECT 
                     a.sync_tag,
                     MAX(a.create_date)
                FROM t_db_sync_tasks_log a
                WHERE a.create_date>DATE_SUB(DATE(NOW()),INTERVAL 2 DAY)
                GROUP BY a.sync_tag)"""
    return await async_processer.query_list(sql)


def get_sync_num(r):
    flow_flag = r[2]
    flow_real_flag = r[3]
    flow_device_flag = r[4]
    park_flag = r[5]
    park_real_flag = r[6]
    sales_dldf_flag = r[7]
    i_success_time = 0
    i_failure_time = 0
    if flow_flag != '':
        for i in flow_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    if flow_real_flag != '':
        for i in flow_real_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    if flow_device_flag != '':
        for i in flow_device_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    if park_flag != '':
        for i in park_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    if park_real_flag != '':
        for i in park_real_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    if sales_dldf_flag != '':
        for i in sales_dldf_flag.split(','):
            if i[0] == '0':
                i_success_time = i_success_time + 1
            else:
                i_failure_time = i_failure_time + 1

    return i_success_time, i_failure_time


async def query_sync_case():
    sql = """ SELECT 
                  market_id,
                  market_name,
                  flow_flag,
                  flow_real_flag,
                  flow_device_flag,
                  park_flag,
                  park_real_flag,
                  sales_dldf_flag,
                  date_format(create_date,'%Y-%m-%d %H:%i') as create_date
                FROM t_db_sync_monitor
                  ORDER BY CASE WHEN market_name LIKE '%北京%' THEN 1 
                               WHEN market_name LIKE '%上海%' THEN 2 
                               WHEN market_name LIKE '%成都%' THEN 3
                               WHEN market_name LIKE '%广州%' THEN 4
                               ELSE 5 END"""
    v_list = await async_processer.query_list(sql)
    n_succ_num = 0
    n_fail_num = 0
    for r in v_list:
        s, f = get_sync_num(r)
        n_succ_num = n_succ_num + s
        n_fail_num = n_fail_num + f
    result = {}
    result['data'] = v_list
    result['success'] = n_succ_num
    result['failure'] = n_fail_num
    return result


async def query_sync_case_log(p_tag):
    res = {}
    sql = """ SELECT 
                date_format(create_date,'%H:%i') as create_date,
                amount
              FROM `t_db_sync_tasks_log` 
              WHERE create_date>=DATE_ADD(NOW(),INTERVAL -3 HOUR)
               AND sync_tag='{}'ORDER BY create_date""".format(p_tag.split(',')[0])
    x = []
    y = []
    for r in await async_processer.query_list(sql):
        x.append(r[0])
        y.append(r[1])
    res['amount'] = {}
    res['amount']['x'] = x
    res['amount']['y'] = y
    res['amount']['t'] = p_tag
    return res


async def query_db_active_num(p_db_id, p_begin_date, p_end_date):
    res = {}
    sql = """SELECT 
                   DATE_FORMAT(create_date,'%Y-%m-%d %H') AS rq,
                   ROUND(AVG(total_connect),2) AS val_total,
                   ROUND(AVG(active_connect),2) AS val_active,
                   ROUND(AVG(db_qps),2) AS val_qps,
                   ROUND(AVG(db_tps),2) AS val_tps
               FROM `t_monitor_task_db_log`
               WHERE db_id={}
                 AND create_date >= '{}'
                 AND create_date <= '{}'
                 group by DATE_FORMAT(create_date,'%Y-%m-%d %H')
               ORDER BY 1 """.format(p_db_id, p_begin_date, p_end_date)
    x = []
    y = []
    x_total = []
    y_total = []
    x_qps = []
    y_qps = []
    x_tps = []
    y_tps = []
    for r in await async_processer.query_list(sql):
        x_total.append(r[0])
        y_total.append(r[1])
        x.append(r[0])
        y.append(r[2])
        x_qps.append(r[0])
        y_qps.append(r[3])
        x_tps.append(r[0])
        y_tps.append(r[4])
    res['amount'] = {}
    res['amount']['x'] = x
    res['amount']['y'] = y
    res['amount']['x_total'] = x_total
    res['amount']['y_total'] = y_total
    res['amount']['x_qps'] = x_qps
    res['amount']['y_qps'] = y_qps
    res['amount']['x_tps'] = x_tps
    res['amount']['y_tps'] = y_tps
    return res


async def query_db_real_sync(p_sync_tag, p_max_id):
    res = []
    if p_max_id == 1:
        sql = """SELECT MAX(id) AS max_id FROM t_db_sync_real_log WHERE sync_tag='{}'""".format(p_sync_tag)
        mid = (await async_processer.query_dict_one(sql))['max_id']

        if mid == '':
            return {'max_id': p_max_id, 'data': [], 'binlogfile': '', 'binlogpos': '', 'c_binlogfile': '',
                    'c_binlogpos': ''}

        sql = """SELECT DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s') AS create_date,cast(avg(event_amount) as SIGNED)
                 FROM t_db_sync_real_log WHERE sync_tag='{}' AND id >={} AND id<={} 
                 Group by DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s')
                 ORDER BY 1 limit 50""".format(p_sync_tag, mid - 1000, mid)

        for r in await async_processer.query_list(sql):
            res.append({
                'name': r[0],
                'value': [r[0], r[1]]
            })

        sql = """SELECT binlogfile,
                        binlogpos,
                        c_binlogfile,
                        c_binlogpos
                  FROM t_db_sync_real_log WHERE sync_tag='{}'   ORDER BY create_date DESC LIMIT 1
              """.format(p_sync_tag)
        bin = await async_processer.query_dict_one(sql)
        return {'max_id': mid, 'data': res,
                'binlogfile': bin['binlogfile'], 'binlogpos': bin['binlogpos'],
                'c_binlogfile': bin['c_binlogfile'], 'c_binlogpos': bin['c_binlogpos']}
    else:
        sql = """SELECT count(0) AS rec FROM t_db_sync_real_log WHERE sync_tag='{}' and id >={} limit 1""".format(
            p_sync_tag, p_max_id)
        rec = (await async_processer.query_dict_one(sql))['rec']
        if rec == 0:
            return {'max_id': p_max_id, 'data': [], 'binlogfile': '', 'binlogpos': ''}
        else:
            sql = """SELECT max(id) AS max_id FROM t_db_sync_real_log WHERE sync_tag='{}' and id >={} limit 1""".format(
                p_sync_tag, p_max_id)
            mid = (await async_processer.query_dict_one(sql))['max_id']
            sql = """SELECT DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s') AS create_date,cast(avg(event_amount) as SIGNED)
                     FROM t_db_sync_real_log WHERE sync_tag='{}' AND id >={} 
                     Group by DATE_FORMAT(create_date,'%Y-%m-%d %H:%i:%s')
                     limit 1""".format(p_sync_tag, p_max_id, mid)
            for r in await async_processer.query_list(sql):
                res.append({
                    'name': r[0],
                    'value': [r[0], r[1]]
                })
            sql = """SELECT binlogfile,
                            binlogpos,
                            c_binlogfile,
                            c_binlogpos
                      FROM t_db_sync_real_log WHERE sync_tag='{}'  ORDER BY create_date DESC LIMIT 1
                  """.format(p_sync_tag)
            bin = await async_processer.query_dict_one(sql)
            return {
                'max_id': mid,
                'data': res,
                'binlogfile': bin['binlogfile'],
                'binlogpos': bin['binlogpos'],
                'c_binlogfile': bin['c_binlogfile'],
                'c_binlogpos': bin['c_binlogpos']
            }


async def query_db_order_num():
    res = {}
    sql = """
            SELECT 
               a.rq,
               (SELECT COUNT(0) FROM `t_sql_release` b WHERE dbid=16 AND DATE_FORMAT(b.creation_date,'%Y-%m-%d')=a.rq) AS num_hst,
               (SELECT COUNT(0) FROM `t_sql_release` b WHERE dbid=84 AND DATE_FORMAT(b.creation_date,'%Y-%m-%d')=a.rq) AS num_hft,
               (SELECT COUNT(0) FROM `t_sql_release` b WHERE dbid=245 AND DATE_FORMAT(b.creation_date,'%Y-%m-%d')=a.rq) AS num_dev
            FROM (SELECT DATE_FORMAT(DATE_ADD(NOW(),INTERVAL -t.help_topic_id DAY),'%Y-%m-%d') AS 'rq'  
            FROM (SELECT DISTINCT help_topic_id AS help_topic_id  FROM help_topic) t WHERE t.help_topic_id<=10 ORDER BY 1) a"""
    x = []
    y_hst = []
    y_hft = []
    y_wutong = []

    for r in await async_processer.query_list(sql):
        x.append(r[0])
        y_hst.append(r[1])
        y_hft.append(r[2])
        y_wutong.append(r[3])

    res['amount'] = {}
    res['amount']['x'] = x
    res['amount']['y'] = [y_hst, y_hft, y_wutong]
    return res


async def query_db_slow_num(p_inst_id, p_ds_id, p_begin_date, p_end_date):
    res = {}
    if p_begin_date != '' or p_end_date != '':
        sql = """SELECT DATE_FORMAT(finish_time,'%Y-%m-%d %H') AS rq,
                           COUNT(0) as val
                    FROM t_slow_detail 
                     WHERE {}={} 
                       AND finish_time >= '{}'
                       AND finish_time <= '{}'
                       AND query_time>3
                       GROUP BY DATE_FORMAT(finish_time,'%Y-%m-%d %H')  ORDER BY 1
               """.format('db_id' if p_inst_id == p_ds_id else 'inst_id',
                          p_ds_id if p_inst_id == p_ds_id else p_inst_id,
                          p_begin_date,
                          p_end_date)
    else:
        sql = """SELECT DATE_FORMAT(finish_time,'%H') AS rq,
                              COUNT(0) as val
                       FROM t_slow_detail 
                        WHERE {}={} 
                          AND finish_time >= CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 0:0:0')
                          AND finish_time <= CONCAT(DATE_FORMAT(NOW(),'%Y-%m-%d'),' 23:59:59')
                          AND query_time>3
                          GROUP BY DATE_FORMAT(finish_time,'%H')  ORDER BY 1
                  """.format('db_id' if p_inst_id == p_ds_id else 'inst_id',
                             p_ds_id if p_inst_id == p_ds_id else p_inst_id,
                             p_begin_date,
                             p_end_date)

    print(sql)
    x = []
    y = []
    for r in await async_processer.query_list(sql):
        x.append(r[0])
        y.append(r[1])
    res['amount'] = {}
    res['amount']['x'] = x
    res['amount']['y'] = y
    return res


def get_max_disk_usage(d_disk):
    n_max_val = 0.0
    for key in d_disk:
        if n_max_val <= float(d_disk[key]):
            n_max_val = float(d_disk[key])
    result = n_max_val
    return result


async def query_sys_stats_num(p_server_id, p_begin_date, p_end_date):
    res = {}
    sql = """SELECT  
                    DATE_FORMAT(a.create_date,'%Y-%m-%d %H') AS rq,
                    ROUND(AVG(a.cpu_total_usage),2) AS cpu_usage,
                    ROUND(AVG(a.mem_usage),2)       AS mem_usage,
                    MAX(a.disk_usage)               AS disk_usage,
                    ROUND(AVG(a.disk_read/1000),2)  AS disk_read,
                    ROUND(AVG(a.disk_write/1000),2) AS disk_write,
                    ROUND(AVG(a.net_in/1000),2)     AS net_in,
                    ROUND(AVG(a.net_out/1000),2)    AS net_out
                FROM t_monitor_task_server_log a
                WHERE a.server_id={}
                  AND a.create_date >= '{}'
                  AND a.create_date <= '{}'
                GROUP BY DATE_FORMAT(a.create_date,'%Y-%m-%d %H')""".format(p_server_id, p_begin_date, p_end_date)
    rq = []
    cpu_usage = []
    mem_usage = []
    disk_usage = []
    disk_read = []
    disk_write = []
    net_in = []
    net_out = []
    for r in await async_processer.query_dict_list(sql):
        rq.append(r['rq'])
        cpu_usage.append(r['cpu_usage'])
        mem_usage.append(r['mem_usage'])
        disk_usage.append(get_max_disk_usage(json.loads(r['disk_usage'])))
        disk_read.append(r['disk_read'])
        disk_write.append(r['disk_write'])
        net_in.append(r['net_in'])
        net_out.append(r['net_out'])
    res['rq'] = rq
    res['cpu_usage'] = cpu_usage
    res['mem_usage'] = mem_usage
    res['disk_usage'] = disk_usage
    res['disk_read'] = disk_read
    res['disk_write'] = disk_write
    res['net_in'] = net_in
    res['net_out'] = net_out
    return res


async def query_sys_stats_idx():
    res = {}
    sql = "SELECT idx_name,idx_sql FROM t_sys_stats_idx ORDER BY id"
    rs2 = await async_processer.query_dict_list(sql)
    for r in await async_processer.query_dict_list(sql):
        rs = await async_processer.query_dict_one(r['idx_sql'])
        res[r['idx_name']] = rs['val']
    return res


def get_mssql_tables_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
    }
    url = 'http://{}/get_mssql_tables'.format(proxy_server)
    res = requests.post(url, data=data, timeout=300)
    res = json.loads(res.text)
    return res


def get_mysql_tables_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
    }
    url = 'http://{}/get_mysql_tables'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_mysql_databases_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
    }
    url = 'http://{}/get_mysql_databases'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_ck_databases_list(db_ip, db_port, db_service, db_user, db_pass, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
    }
    url = 'http://{}/get_ck_databases'.format(proxy_server)
    print('url=', url)
    print('data=', data)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_mssql_columns_list(db_ip, db_port, db_service, db_user, db_pass, db_tab, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
        'db_tab': db_tab,
    }
    url = 'http://{}/get_mssql_columns'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_mysql_columns_list(db_ip, db_port, db_service, db_user, db_pass, db_tab, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
        'db_tab': db_tab,
    }
    url = 'http://{}/get_mysql_columns'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_mssql_incr_columns_list(db_ip, db_port, db_service, db_user, db_pass, db_tab, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
        'db_tab': db_tab,
    }
    url = 'http://{}/get_mssql_incr_columns'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res


def get_mysql_incr_columns_list(db_ip, db_port, db_service, db_user, db_pass, db_tab, proxy_server):
    data = {
        'db_ip': db_ip,
        'db_port': db_port,
        'db_service': db_service,
        'db_user': db_user,
        'db_pass': db_pass,
        'db_tab': db_tab,
    }
    url = 'http://{}/get_mysql_incr_columns'.format(proxy_server)
    res = requests.post(url, data=data)
    res = json.loads(res.text)
    return res
