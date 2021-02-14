#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import traceback
import requests

from web.utils.common      import format_sql
from web.utils.common      import current_rq
from web.utils.mysql_async import async_processer

async def query_monitor_index(index_code):
    v_where=' '
    if index_code != '':
        v_where = " where a.index_code like '%{0}%' or a.index_name like '%{1}%'".format(index_code,index_code)
    sql = """SELECT
                 id,  
                 index_code,
                 index_name,                 
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_type=b.dmm AND b.dm='23') AS index_type,
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_db_type=b.dmm AND b.dm='02') AS index_db_type,  
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.index_threshold_type=b.dmm AND b.dm='24') AS index_threshold_type,     
                 case when a.index_threshold_type='1' or a.index_threshold_type='3' then
                    index_threshold
                 else
                    concat(index_threshold_day,'^',index_threshold_times)                   
                 end as    index_threshold,
                 concat(trigger_time,'^',trigger_times),
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_monitor_index a {0} order by a.index_type,a.id""".format(v_where)
    return await async_processer.query_list(sql)

async def save_index(p_index):
    val=check_index(p_index)
    if val['code']=='-1':
        return val
    try:
        sql="""insert into t_monitor_index(
                           index_name,index_code,index_type,index_db_type,index_threshold_type,
                           index_threshold_day,index_threshold_times,index_threshold,status,trigger_time,trigger_times)
               values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(p_index['index_name'],p_index['index_code'],p_index['index_type'],p_index['index_db_type'],
                       p_index['index_val_type'],p_index['index_threshold_day'],p_index['index_threshold_times'],
                       p_index['index_threshold'],p_index['index_status'],
                       p_index['index_trigger_time'],p_index['index_trigger_times']
                     )
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def upd_index(p_index):
    val = check_index(p_index)
    if  val['code'] == '-1':
        return val
    try:
        sql="""update t_monitor_index  set  
                      index_name            ='{0}',
                      index_code            ='{1}',
                      index_type            ='{2}', 
                      index_db_type         ='{3}',
                      index_threshold_type  ='{4}',
                      index_threshold       ='{5}', 
                      index_threshold_day   ='{6}',
                      index_threshold_times ='{7}',
                      status                ='{8}',                      
                      trigger_time          ='{9}',
                      trigger_times         ='{10}'                      
                where id='{11}'
            """.format(p_index['index_name'],p_index['index_code'],p_index['index_type'], p_index['index_db_type'],
                       p_index['index_val_type'], p_index['index_threshold'],p_index['index_threshold_day'],
                       p_index['index_threshold_times'],p_index['index_status'],
                       p_index['index_trigger_time'],p_index['index_trigger_times'],p_index['index_id'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}

async def del_index(p_index_code):
    try:
        sql="delete from t_monitor_index  where index_code='{0}'".format(p_index_code)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}

async def query_threshold():
    sql = "SELECT index_code,index_threshold FROM t_monitor_index WHERE index_threshold_type IN(1,3)"
    v_dict = {}
    for r in await async_processer.query_list(sql):
        v_dict[r[0]]=r[1]
    return v_dict

async def del_task(p_task_tag):
    try:
        sql="delete from t_monitor_task  where task_tag='{0}'".format(p_task_tag)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}

async def get_index_by_index_code(p_index_code):
    sql = """SELECT  index_name,index_code,index_type,index_db_type,index_threshold,status FROM t_monitor_index where index_code='{0}'""".format(p_index_code)
    return await async_processer.query_dict_one(sql)

async def get_index_by_index_id(p_id):
    sql = """SELECT  index_name,index_code,index_type,index_db_type,index_threshold,status  FROM t_monitor_index where id='{0}'""".format(p_id)
    return await async_processer.query_dict_one(sql)

async def get_monitor_indexes():
    return await async_processer.query_list("SELECT  id,index_name FROM t_monitor_index WHERE STATUS='1'")

async def get_monitor_indexes2(p_type):
    if p_type=='':
        sql = """SELECT  index_code,index_name FROM t_monitor_index  WHERE STATUS='1' order by index_type,id"""
    else:
        sql = """SELECT  index_code,index_name FROM t_monitor_index  WHERE STATUS='1' and index_type='{0}' order by index_type,id """.format(p_type)
    return await async_processer.query_list(sql)

async def query_monitor_templete(templete_code):
    v_where=' '
    if templete_code != '':
        v_where = " where a.code like '%{0}%' or a.code like '%{1}%'".format(templete_code,templete_code)
    sql = """SELECT  
                 code,name,
                 (SELECT dmmc FROM t_dmmx b 
                    WHERE a.type=b.dmm AND b.dm='23') AS templete_type,     
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag, 
                 creator, date_format(creation_date,'%Y-%m-%d')  creation_date,
                 updator, date_format(last_update_date,'%Y-%m-%d') last_update_date
            FROM t_monitor_templete a {0} """.format(v_where)
    return await async_processer.query_list(sql)

async def get_monitor_sys_indexes(p_templete_code):
    sql = """SELECT  id,index_name FROM t_monitor_index 
                   WHERE STATUS='1' and id not in(select index_id from t_monitor_templete_index 
                                             where templete_id=(select id from t_monitor_templete where code='{0}'))""".format(p_templete_code)
    return await async_processer.query_list(sql)

async def get_monitor_indexes_by_type(p_index_type,p_db_id):
    if p_db_id =='':
        sql = """SELECT  index_code,index_name FROM t_monitor_index  WHERE STATUS='1' AND  index_type = '{0}'""".format(p_index_type)
    else:
        sql = """SELECT  index_code,index_name FROM t_monitor_index  
                  WHERE STATUS='1' AND  index_type = '{0}' AND index_db_type =(SELECT db_type FROM t_db_source WHERE id='{1}') """.format(p_index_type,p_db_id)
    return await async_processer.query_list(sql)

async def get_monitor_templete_indexes(p_templete_code):
    sql = """SELECT  id,index_name FROM t_monitor_index 
              WHERE STATUS='1'  and id in(select index_id from t_monitor_templete_index
                                          where templete_id=(select id from t_monitor_templete where code='{0}'))""".format(p_templete_code)
    return await async_processer.query_list(sql)

async def get_templeteid():
    sql = "select ifnull(max(id),0)+1 from t_monitor_templete"
    return (await async_processer.query_one(sql))[0]

async def get_templeteid_by_code(p_code):
    sql="select id from t_monitor_templete where code='{0}'".format(p_code)
    return (await async_processer.query_one(sql))[0]

async def save_templete_indexes(p_templete_id,p_indexes):
    try:
        for id in p_indexes.split(','):
            sql="""insert into t_monitor_templete_index(templete_id,index_id,creation_date,creator,last_update_date,updator) 
                     values({0},'{1}','{2}','{3}','{4}','{5}')""".format(p_templete_id,id,current_rq(),'DBA',current_rq(),'DBA')
            async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def upd_templete_indexes(p_templete_id,p_indexes):
    try:
        await async_processer.exec_sql("delete from t_monitor_templete_index where  templete_id='{0}'".format(p_templete_id))
        for id in p_indexes.split(','):
             sql="""insert into t_monitor_templete_index(templete_id,index_id,creation_date,creator,last_update_date,updator) 
                       values({0},'{1}','{2}','{3}','{4}','{5}')""".format(p_templete_id,id,current_rq(),'DBA',current_rq(),'DBA')
             await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def save_templete(p_templete):
    val = check_templete(p_templete)
    if val['code']=='-1':
        return val
    try:
        templete_id = await get_templeteid()
        result  = {}
        sql ="""insert into t_monitor_templete(id,name,code,type,status,creation_date,creator,last_update_date,updator)  values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
             """.format(templete_id,p_templete['templete_name'],p_templete['templete_code'],p_templete['templete_type'], p_templete['templete_status'],current_rq(), 'DBA', current_rq(), 'DBA')
        await async_processer.exec_sql(sql)
        await save_templete_indexes(templete_id,p_templete['templete_indexes'])
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def upd_templete(p_templete):
    val = check_templete(p_templete)
    if  val['code'] == '-1':
        return val
    try:
        templete_id = await get_templeteid_by_code(p_templete['templete_code'])
        sql         = """update t_monitor_templete  set  
                            name    ='{0}',
                            type    ='{1}',
                            status  ='{2}',
                            updator ='{3}',
                            last_update_date ='{4}' 
                         where code='{5}'
                      """.format(p_templete['templete_name'],p_templete['templete_type'],p_templete['templete_status'], 'DBA',current_rq(),p_templete['templete_code'])
        await async_processer.exec_sql(sql)
        await upd_templete_indexes(templete_id, p_templete['templete_indexes'])
        return {'code': '0', 'message': '更新成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}

async def del_templete(p_templete_code):
    try:
        await async_processer.exec_sql("delete from t_monitor_templete_index where templete_id =(select id from t_monitor_templete where code='{0}')".format(p_templete_code))
        await async_processer.exec_sql("delete from t_monitor_templete  where code='{0}'".format(p_templete_code))
        return {'code': '0', 'message': '删除成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}

async def get_templetes_by_templete_id(p_templeteid):
    sql = """SELECT  name FROM t_monitor_templete where status='1' and instr('{0}',id)>0""".format(p_templeteid)
    rs = await async_processer.query_list(sql)
    t=''
    for i in range(len(rs)):
       t=t+rs[i][0]+','
    return t[0:-1]

async def get_monitor_task_by_tag(p_tag):
    sql = """SELECT  * FROM t_monitor_task where task_tag='{0}'""".format(p_tag)
    return (await async_processer.query_one(sql))[0]

async def query_task(p_task_tag):
    v_where=' '
    if p_task_tag != '':
       v_where = " and ( a.task_tag like '%{0}%' or a.comments like '%{1}%' or b.server_ip like '%{2}%')".format(p_task_tag,p_task_tag,p_task_tag)
    sql = """SELECT  
                 task_tag,comments,
                 CONCAT(b.server_ip,':',b.server_port) AS sync_server,             
                 templete_id,run_time,api_server,
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  AS  flag
            FROM t_monitor_task a,t_server b
            where a.server_id=b.id {0}""".format(v_where)
    v_list = []
    for r in await async_processer.query_list(sql):
        v_temp = list(r)
        v_temp.insert(4,await get_templetes_by_templete_id(v_temp[3]))
        v_list.append(v_temp)
    return v_list

async def save_gather_task(p_task):
    val=check_task(p_task)
    if val['code']=='-1':
        return val
    try:
        sql ="""insert into t_monitor_task (task_tag,comments,server_id,db_id,templete_id,run_time,script_path,script_file,python3_home,api_server,status)
                      values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
             """.format(p_task['add_gather_task_tag'],
                        p_task['add_gather_task_desc'],
                        p_task['add_gather_server'],
                        p_task['add_gather_task_db_server'],
                        p_task['add_gather_task_templete_name'],
                        p_task['add_gather_task_run_time'],
                        format_sql(p_task['add_gather_task_script_base']),
                        format_sql(p_task['add_gather_task_script_name']),
                        format_sql(p_task['add_gather_task_python3_home']),
                        p_task['add_gather_task_api_server'],
                        p_task['add_gather_task_status'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def save_monitor_task(p_task):
    val = check_task(p_task)
    if val['code']=='-1':
        return val
    try:
        sql ="""insert into t_monitor_task(task_tag,comments,server_id,run_time,script_path,script_file,python3_home,api_server,status)
                  values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
            """.format(p_task['add_monitor_task_tag'], p_task['add_monitor_task_desc'],
                        p_task['add_monitor_server'], p_task['add_monitor_task_run_time'],
                        format_sql(p_task['add_monitor_task_script_base']),
                        format_sql(p_task['add_monitor_task_script_name']),
                        format_sql(p_task['add_monitor_task_python3_home']),
                        p_task['add_monitor_task_api_server'],
                        p_task['add_monitor_task_status'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def upd_gather_task(p_task):
    val = check_task(p_task)
    if val['code']=='-1':
        return val
    try:
        sql ="""update t_monitor_task
                  set  run_time='{}',
                       script_path='{}',
                       script_file='{}',
                       python3_home='{}',
                       api_server='{}',
                       status='{}',
                       db_id ='{}'
                 where task_tag='{}'
             """.format(p_task['upd_gather_task_run_time'],
                        format_sql(p_task['upd_gather_task_script_base']),
                        format_sql(p_task['upd_gather_task_script_name']),
                        format_sql(p_task['upd_gather_task_python3_home']),
                        p_task['upd_gather_task_api_server'],
                        p_task['upd_gather_task_status'],
                        p_task['upd_gather_task_db_server'],
                        p_task['upd_gather_task_tag'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def upd_monitor_task(p_task):
    val = check_task(p_task)
    if val['code'] == '-1':
        return val
    try:
        sql = """update t_monitor_task
                     set  run_time='{}',
                          script_path='{}',
                          script_file='{}',
                          python3_home='{}',
                          api_server='{}',
                          status='{}'
                    where task_tag='{}'
                """.format( p_task['upd_monitor_task_run_time'],
                            p_task['upd_monitor_task_script_base'],
                            p_task['upd_monitor_task_script_name'],
                            p_task['upd_monitor_task_python3_home'],
                            p_task['upd_monitor_task_api_server'],
                            p_task['upd_monitor_task_status'],
                            p_task['upd_monitor_task_tag']
                        )
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def query_monitor_templete_type(p_templete_id):
    sql = """select dmm,dmmc  from t_dmmx 
               where dm='23'  and dmm=(select type from t_monitor_templete where id='{0}')""".format(p_templete_id)
    return await async_processer.query_list(sql)

async def query_monitor_log_analyze(server_id,db_id,index_code,begin_date,end_date):
    v_where = ' where 1=1 '
    sql = ''
    if server_id != '':
        v_where = v_where + " and a.server_id='{0}'\n".format(server_id)
    if db_id != '':
        v_where = v_where + " and a.db_id='{0}'\n".format(db_id)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')
    if index_code=='cpu_total_usage':
       sql = """SELECT cast(a.create_date as char) as create_date,a.cpu_total_usage FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
             """.format(v_where)
    elif index_code=='cpu_core_usage':
       sql = """SELECT cast(a.create_date as char) as create_date,a.cpu_core_usage  FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
             """.format(v_where)
    elif index_code=='mem_usage':
       sql = """SELECT cast(a.create_date as char) as create_date,a.mem_usage  FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
             """.format(v_where)
    elif index_code == 'disk_usage':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_usage FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'disk_read':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_read  FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'disk_write':
        sql = """SELECT cast(a.create_date as char) as create_date,a.disk_write FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'net_out':
        sql = """SELECT cast(a.create_date as char) as create_date,a.net_out  FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code == 'net_in':
        sql = """SELECT cast(a.create_date as char) as create_date,a.net_in  FROM t_monitor_task_server_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code in('mysql_total_connect','mssql_total_connect','oracle_total_connect'):
        sql = """SELECT cast(a.create_date as char) as create_date,a.total_connect  FROM t_monitor_task_db_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code in('mysql_qps','mssql_qps','oracle_qps'):
        sql = """SELECT cast(a.create_date as char) as create_date,a.db_qps  FROM t_monitor_task_db_log a {0} and a.db_qps is not null and a.db_qps!='' ORDER BY a.create_date
              """.format(v_where)
    elif index_code in('mysql_tps','mssql_tps','oracle_tps'):
        sql = """SELECT cast(a.create_date as char) as create_date,a.db_tps  FROM t_monitor_task_db_log a {0} and a.db_tps is not null and a.db_tps!='' ORDER BY a.create_date
              """.format(v_where)
    elif index_code in ('mysql_active_connect','mssql_active_connect','oracle_active_connect') :
        sql = """SELECT cast(a.create_date as char) as create_date,a.active_connect FROM t_monitor_task_db_log a {0} ORDER BY a.create_date
              """.format(v_where)
    elif index_code in('mysql_available','mssql_available','oracle_available','es_available','redis_available','mongo_available'):
        sql = """SELECT cast(a.create_date as char) as create_date,a.db_available FROM t_monitor_task_db_log a {0} ORDER BY a.create_date 
              """.format(v_where)
    elif index_code == 'oracle_tablespace':
        sql = """SELECT cast(a.create_date as char) as create_date,a.db_tbs_usage FROM t_monitor_task_db_log a {0}  and a.db_tbs_usage is not null and a.db_tbs_usage!='' ORDER BY a.create_date 
              """.format(v_where)
    else:
        pass
    return await async_processer.query_list(sql)

async def query_monitor_sys(env,search_text):
    if env == 'hst-dev':
         vw = " and b.server_desc like '%合生通开发%'"
    elif env == 'hst-test':
         vw = " and b.server_desc like '%合生通测试%'"
    elif env == 'hst-pre':
         vw = " and b.server_desc like '%合生通预生产%'"
    elif env == 'hst-prod':
         vw = " and b.server_desc like '%合生通生产%'"
    elif env == 'hst-proj':
         vw = " and b.server_desc like '%同步服务器%'"
    elif env == 'easylife-dev':
        vw = " and b.server_desc like '%好房开发%'"
    elif env == 'easylife-test':
        vw = " and b.server_desc like '%好房测试%'"
    elif env == 'easylife-gray':
         vw = " and b.server_desc like '%好房灰度%'"
    elif env == 'easylife-prod':
         vw = " and b.server_desc like '%好房生产%'"
    elif env == 'sg-prod':
         vw = " and b.server_desc like '%商管%'"
    elif env == 'platform-prod':
         vw = " and b.server_desc like '%平台组生产%'"
    else:
         vw =''

    if search_text != '':
        vw = vw + " and b.server_desc like '%{}%'".format(search_text)

    sql = """SELECT b.server_desc,
                    concat(b.server_ip,':',b.server_port) as server,
                    concat(a.cpu_total_usage,'%') as cpu_total_usage,
                    concat(a.mem_usage,'%')  as mem_usage,
                    a.disk_usage,
                    CONCAT(ROUND(a.disk_read/1000,1),'kb/s')  AS disk_read,
                    CONCAT(ROUND(a.disk_write/1000,1),'kb/s') AS disk_write,
                    CONCAT(ROUND(a.net_in/1000,1),'kb/s')     AS net_in,
                    CONCAT(ROUND(a.net_out/1000,1),'kb/s')    AS net_out,
                    DATE_FORMAT(a.create_date,'%Y-%m-%d %H:%i:%s')     AS cjrq,
                    CASE WHEN TIMESTAMPDIFF(MINUTE, a.create_date, NOW())>10 THEN '0' ELSE '100' END  AS STATUS
            FROM t_monitor_task_server_log a  LEFT JOIN t_server b ON a.server_id=b.id 
            WHERE (a.server_id,a.create_date) IN(SELECT server_id,MAX(create_date) FROM `t_monitor_task_server_log` GROUP BY server_id) {}  ORDER BY STATUS, b.server_desc
          """.format(vw)
    v_list = []
    for r in await async_processer.query_list(sql):
        v_temp =list(r)
        v_temp[4] =get_max_disk_usage(json.loads(v_temp[4]))
        v_list.append(v_temp)
    return  {'data': v_list, 'index': await query_threshold()}

async def query_monitor_svr(env,search_text):
    if env == 'hst-dev':
        vw = " and server_desc like '%合生通开发%'"
    elif env == 'hst-test':
        vw = " and server_desc like '%合生通测试%'"
    elif env == 'hst-pre':
        vw = " and server_desc like '%合生通预生产%'"
    elif env == 'hst-prod':
        vw = " and server_desc like '%合生通生产%'"
    elif env == 'hst-proj':
        vw = " and server_desc like '%同步服务器%'"
    elif env == 'easylife-dev':
        vw = " and server_desc like '%好房开发%'"
    elif env == 'easylife-test':
        vw = " and server_desc like '%好房测试%'"
    elif env == 'easylife-gray':
        vw = " and server_desc like '%好房灰度%'"
    elif env == 'easylife-prod':
        vw = " and server_desc like '%好房生产%'"
    elif env == 'sg-prod':
        vw = " and server_desc like '%商管%'"
    elif env == 'platform-prod':
         vw = " and server_desc like '%平台组生产%'"
    else:
        vw = ''

    if search_text != '':
        vw = vw + " and server_desc like '%{}%'".format(search_text)
    sql1 = """SELECT server_desc, mysql_proj,mssql_park,mssql_flow, mssql_car,mssql_dldf, mssql_sg, oracle_sg,redis, mongo,es
              FROM t_monitor_service
                WHERE (mysql_proj<>'' OR mssql_park<>''  OR mssql_flow<>''  OR mssql_car<>''  OR mssql_dldf<>'' 
                     OR mssql_sg<>'' OR oracle_sg<>'' OR redis<>''  OR mongo<>''  OR es<>'')  {}  ORDER BY server_desc,sxh""".format(vw)

    sql2= """SELECT server_desc, mysql_proj,mssql_park,mssql_flow, mssql_car,mssql_dldf, mssql_sg, oracle_sg,redis, mongo,es
                   FROM t_monitor_service
                    where instr(mysql_proj,'0@')>0 or instr(mssql_park,'0@')>0   or instr(mssql_flow,'0@')>0 
                       or instr(mssql_car,'0@')>0   or instr(mssql_dldf,'0@')>0 or instr(mssql_sg,'0@')>0  
                         or instr(oracle_sg,'0@')>0   or instr(redis,'0@')>0  or instr(mongo,'0@')>0 
                          or instr(es,'0@')>0 ORDER BY server_desc,sxh"""
    return {'data': await async_processer.query_list(sql1), 'warning': await async_processer.query_list(sql2)}

def get_max_disk_usage(d_disk):
    n_max_val =0.0
    for key in d_disk:
        if n_max_val <= float (d_disk[key]):
           n_max_val = float (d_disk[key])
    result = str(n_max_val)+'%'
    return result

def check_templete(p_index):
    result = {}

    if p_index["templete_name"]=="":
        result['code']='-1'
        result['message']='模板名称不能为空！'
        return result

    if p_index["templete_code"] == "":
        result['code'] = '-1'
        result['message'] = '模板代码不能为空！'
        return result

    if p_index["templete_indexes"]=="":
        result['code']='-1'
        result['message']='模板指标不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def check_task(p_task):
    result = {}
    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def push_monitor_task(p_tag,p_api):
    url = 'http://{}/push_script_remote_monitor'.format(p_api)
    res = requests.post(url, data={'tag': p_tag})
    jres = res.json()
    v = ''
    for c in jres['msg']['crontab'].split('\n'):
        if c.count(p_tag) > 0:
            v = v + "<span class='warning'>" + c + "</span>"
        else:
            v = v + c
        v = v + '<br>'
    jres['msg']['crontab'] = v
    return jres

def run_monitor_task(p_tag,p_api):
    url = 'http://{}/run_script_remote_archive'.format(p_api)
    res = requests.post(url, data={'tag': p_tag})
    jres = res.json()
    return jres

def stop_monitor_task(p_tag,p_api):
    url = 'http://{}/stop_script_remote_archive'.format(p_api)
    res = requests.post(url, data={'tag': p_tag})
    jres = res.json()
    return jres

def check_index(p_index):
    result = {}

    if p_index["index_name"]=="":
        result['code']='-1'
        result['message']='指标名称不能为空！'
        return result

    if p_index["index_code"] == "":
        result['code'] = '-1'
        result['message'] = '指标代码不能为空！'
        return result

    if p_index["index_type"]=="":
        result['code']='-1'
        result['message']='指标类型不能为空！'
        return result

    if p_index["index_type"]=='2':
        if p_index["index_db_type"]=="":
            result['code']='-1'
            result['message']='数据库类型不能为空！'
            return result

    if p_index["index_val_type"] == "":
        result['code'] = '-1'
        result['message'] = '阀值类型不能为空！'
        return result

    if p_index["index_val_type"] == "1":
        if p_index["index_threshold"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(百分比)不能为空！'
            return result
    elif p_index["index_val_type"] == "3":
        if p_index["index_threshold"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(布尔值)不能为空！'
            return result
    else:
        if p_index["index_threshold_day"] == "" or p_index["index_threshold_times"] == "":
            result['code'] = '-1'
            result['message'] = '指标阀值(计算)不能为空！'
            return result

    if p_index["index_status"] == "":
        result['code'] = '-1'
        result['message'] = '指标状态不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result