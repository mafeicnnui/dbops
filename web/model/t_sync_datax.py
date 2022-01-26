#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_sync_datax.py
# @Software: PyCharm

import requests
import traceback
import os,json,zipfile

from web.model.t_sql import get_mysql_proxy_result
from web.utils.common    import aes_decrypt
from web.model.t_ds       import get_ds_by_dsid
from web.utils.mysql_async import async_processer
from web.utils.mysql_sync import  sync_processer

def get_sync_incr_where(p_sync):
    v_rq_col=p_sync['sour_incr_col']
    v_expire_time=p_sync['sync_gap']
    if p_sync['sync_time_type']=='day':
       v = "{0} >= DATE_SUB(NOW(),INTERVAL {1} DAY)".format(v_rq_col,v_expire_time)
    elif p_sync['sync_time_type']=='hour':
       v = "{0} >= DATE_SUB(NOW(),INTERVAL {1} HOUR)".format(v_rq_col, v_expire_time)
    elif p_sync['sync_time_type'] == 'min':
       v = "{0} >= DATE_SUB(NOW(),INTERVAL {1} MINUTE)".format(v_rq_col, v_expire_time)
    else:
       v = ''
    if v_rq_col=='' or v_rq_col is None:
       return ''
    else:
       return v

def get_hbase_rowkey(p_sync):
    v_row_key = ''
    for idx in range(len(p_sync['sync_hbase_rowkey'].split(','))):
        print('get_hbase_rowkey=',idx,p_sync['sync_hbase_rowkey_separator'],len(p_sync['sync_hbase_rowkey'].split(',')))
        if idx<len(p_sync['sync_hbase_rowkey'].split(','))-1:
            v_row_key=v_row_key+'''
{{
  "index":{0},
  "type":"string"
}},
{{
  "index":-1,
  "type":"string",
  "value":"{1}"
}},'''.format(idx,p_sync['sync_hbase_rowkey_separator'])
        else:
            v_row_key = v_row_key + '''
{{
  "index":{0},
  "type":"string"
}}'''.format(idx, p_sync['sync_hbase_rowkey_separator'])
    return v_row_key

def get_mysql_columns(p_sync):
    v = '''"{0}",'''.format(p_sync['sync_hbase_rowkey_sour'])
    for i in p_sync['sync_columns'].split(','):
       v=v+'''"{}",'''.format(i)
    return v[0:-1]

def get_mysql_columns_doris(p_sync):
    v = ''
    for i in p_sync['sync_columns'].split(','):
       v=v+'''"{}",'''.format(i)
    return v[0:-1]

async def query_datax_sync(sync_tag,sync_ywlx,sync_type,sync_env):
    v_where=' and  1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.sync_tag like '%{0}%'\n".format(sync_tag)
    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)
    if sync_type != '':
        v_where = v_where + " and a.sync_type='{0}'\n".format(sync_type)
    if sync_env == 'prod':
        v_where = v_where + " and a.zk_hosts='192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181'\n"
    elif sync_env == "dev":
        v_where = v_where + " and a.zk_hosts='10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181'\n"
    elif sync_env == "uat":
        v_where = v_where + " and a.zk_hosts='10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181'\n"
    else:
        pass

    if sync_env == 'doris_prod':
        v_where = v_where + """  and doris_id in (SELECT doris_id FROM t_datax_sync_config 
                                                 where doris_id in(select id FROM t_db_source
                                                                   where db_type='8' AND  db_env='1'))"""
    if sync_env == "doris_dev_test":
        v_where = v_where + """  and doris_id in (SELECT doris_id FROM t_datax_sync_config 
                                                 where doris_id in(select id FROM t_db_source 
                                                                    where db_type='8' AND  db_env in('2','3')))"""

    sql = """SELECT  a.id,
                     concat(substr(sync_tag,1,40),'...') as sync_tag1,
                     sync_tag,
		             CONCAT(SUBSTR(a.comments,1,30),'...'),
                     CONCAT(b.server_ip,':',b.server_port) AS sync_server,
                     d.dmmc AS  sync_type,
                     a.run_time,
                     a.api_server,
                     CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
             FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d
            WHERE a.server_id=b.id AND b.status='1' 
              AND c.dm='08' AND d.dm='09' AND a.sync_ywlx=c.dmm AND a.sync_type=d.dmm  {0}""".format(v_where)
    return await async_processer.query_list(sql)

async def query_datax_sync_detail(sync_id):
    sql = """SELECT
                 a.sync_tag,
                 b.server_desc AS sync_server,
                 e.db_desc     AS sync_db_server,  
                 a.sync_schema,
                 a.sync_table,
                 a.sync_columns,
                 a.sync_incr_col,  
                 (SELECT dmmc FROM t_dmmx  WHERE dm='15' AND dmm=a.zk_hosts ) AS zk_hosts, 
                 c.dmmc AS  sync_ywlx,
                 d.dmmc AS  sync_type,
                 a.script_path,
                 a.run_time, 
                 a.comments,
                 a.datax_home,
                 CASE  a.sync_time_type when 'day' THEN '天' WHEN 'hour' THEN '小时' WHEN 'min' THEN '分' END as sync_time_type,
                 a.sync_gap,
                 a.api_server,
                 CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS,
                 a.sync_hbase_table,
                 a.sync_hbase_rowkey_sour,
                 a.python3_home,
                 a.hbase_thrift,
                 a.es_service,
                 a.es_index_name,
                 a.es_type_name,                      
                 a.sync_type ,
                 a.doris_id,
                 a.doris_db_name,
                 a.doris_tab_name,
                 a.doris_batch_size           
            FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d,t_db_source e
            WHERE a.server_id=b.id AND b.status='1' 
            AND a.sour_db_id=e.id
            AND c.dm='08' AND d.dm='09' 
            AND a.sync_ywlx=c.dmm
            AND a.sync_type=d.dmm
            AND a.id='{0}'
         """.format(sync_id)
    return await async_processer.query_one(sql)

async def query_datax_by_id(sync_id):
    sql = """SELECT
                 a.sync_tag,
                 a.server_id,
                 a.sour_db_id,
                 a.sync_schema,
                 a.sync_table,
                 a.sync_incr_col,
                 e.user,
                 e.password,
                 a.sync_columns,
                 a.sync_table,
                 CONCAT(e.ip,':',e.port,'/',a.sync_schema) AS mysql_url,
                 a.zk_hosts,
                 a.sync_hbase_table,
                 a.sync_hbase_rowkey,
                 a.sync_hbase_rowkey_sour,
                 a.sync_hbase_rowkey_separator,
                 a.sync_hbase_columns,
                 a.sync_incr_where,
                 a.sync_ywlx,
                 a.sync_type,
                 a.script_path,
                 a.run_time,
                 a.comments,
                 a.datax_home,
                 a.sync_time_type,
                 a.sync_gap,
                 a.api_server,
                 a.status,
                 a.python3_home,
                 a.hbase_thrift,
                 a.es_service,
                 a.es_index_name,
                 a.es_type_name,
                 a.sync_es_columns,
                 a.doris_id,
                 (select user from t_db_source x where x.id=a.doris_id) as doris_user,
                 (select password from t_db_source x where x.id=a.doris_id) as doris_password,
                 (select stream_load from t_db_source x where x.id=a.doris_id) as doris_stream_load,
                 (select concat(x.ip,':',x.port) from t_db_source x where x.id=a.doris_id) as doris_jbdc_url,
                 a.doris_db_name,
                 a.doris_tab_name,
                 a.doris_batch_size,
                 a.doris_jvm,
                 a.doris_tab_config,
                 a.doris_sync_type
            FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d,t_db_source e
            WHERE a.server_id=b.id AND b.status='1' 
            AND a.sour_db_id=e.id
            AND c.dm='08' AND d.dm='09'
            AND a.sync_ywlx=c.dmm
            AND a.sync_type=d.dmm
            AND a.id='{0}'
         """.format(sync_id)
    return await async_processer.query_dict_one(sql)

async def process_templete(p_sync_id,p_templete):
    v_templete = p_templete
    p_sync = await query_datax_by_id(p_sync_id)
    #replace full templete
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$',p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$PASSWORD$$',await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$ZK_HOSTS', p_sync['zk_hosts'])
    v_templete['full'] = v_templete['full'].replace('$$HBASE_TABLE_NAME$$', p_sync['sync_hbase_table'])
    v_templete['full'] = v_templete['full'].replace('$$HBASE_ROWKEY$$', p_sync['sync_hbase_rowkey'])
    v_templete['full'] = v_templete['full'].replace('$$HBASE_COLUMN_NAMES$$', p_sync['sync_hbase_columns'])
    #replacre incr templete
    v_templete['incr'] = v_templete['incr'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['incr'] = v_templete['incr'].replace('$$PASSWORD$$', await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['incr'] = v_templete['incr'].replace('$$ZK_HOSTS', p_sync['zk_hosts'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_TABLE_NAME$$', p_sync['sync_hbase_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_ROWKEY$$', p_sync['sync_hbase_rowkey'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_COLUMN_NAMES$$', p_sync['sync_hbase_columns'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_WHERE$$', p_sync['sync_incr_where'])
    return v_templete

async def process_templete_es(p_sync_id,p_templete):
    v_templete = p_templete
    p_sync = await query_datax_by_id(p_sync_id)
    #replace full templete
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$',p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$PASSWORD$$',await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$ES_SERVICE$$', p_sync['es_service'])
    v_templete['full'] = v_templete['full'].replace('$$ES_INDEX_NAME$$', p_sync['es_index_name'])
    v_templete['full'] = v_templete['full'].replace('$$ES_TYPE_NAME$$', p_sync['es_type_name'])
    v_templete['full'] = v_templete['full'].replace('$$ES_COLUMN_NAMES$$', p_sync['sync_es_columns'])
    #replacre incr templete
    v_templete['incr'] = v_templete['incr'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['incr'] = v_templete['incr'].replace('$$PASSWORD$$', await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_WHERE$$', p_sync['sync_incr_where'])
    v_templete['incr'] = v_templete['incr'].replace('$$ES_SERVICE$$', p_sync['zk_hosts'])
    v_templete['incr'] = v_templete['incr'].replace('$$ES_INDEX_NAME$$', p_sync['sync_hbase_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$ES_TYPE_NAME$$', p_sync['sync_hbase_rowkey'])
    v_templete['incr'] = v_templete['incr'].replace('$$ES_COLUMN_NAMES$$', p_sync['sync_es_columns'])
    return v_templete

async def process_templete_doris(p_sync_id,p_templete):
    v_templete = p_templete
    p_sync = await query_datax_by_id(p_sync_id)
    #replace full templete
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$',p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$PASSWORD$$',await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns_doris(p_sync))
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['full'] = v_templete['full'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_FE_LOAD_URL$$', p_sync['doris_stream_load'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_JDBC_URL$$', p_sync['doris_jbdc_url'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_DATABASE$$', p_sync['doris_db_name'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_TABLE$$', p_sync['doris_tab_name'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_USER$$', p_sync['doris_user'])
    v_templete['full'] = v_templete['full'].replace('$$DORIS_PASSWORD$$', await aes_decrypt(p_sync['doris_password'],p_sync['doris_user']))
    v_templete['full'] = v_templete['full'].replace('$$MAX_BATCH_ROWS$$', p_sync['doris_batch_size'])

    #replacre incr templete
    v_templete['incr'] = v_templete['incr'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['incr'] = v_templete['incr'].replace('$$PASSWORD$$', await aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns_doris(p_sync))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_WHERE$$', p_sync['sync_incr_where'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_FE_LOAD_URL$$', p_sync['doris_stream_load'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_JDBC_URL$$', p_sync['doris_jbdc_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_DATABASE$$', p_sync['doris_db_name'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_TABLE$$', p_sync['doris_tab_name'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_USER$$', p_sync['doris_user'])
    v_templete['incr'] = v_templete['incr'].replace('$$DORIS_PASSWORD$$', await aes_decrypt(p_sync['doris_password'],p_sync['doris_user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MAX_BATCH_ROWS$$', p_sync['doris_batch_size'])
    return v_templete

async def query_datax_sync_dataxTemplete(sync_id):
    templete = {}
    p_sync   = await query_datax_by_id(sync_id)
    sql_full = 'select contents from t_templete where templete_id=1'
    sql_incr = 'select contents from t_templete where templete_id=2'
    templete['full'] = (await async_processer.query_one(sql_full))[0]
    templete['incr'] = (await async_processer.query_one(sql_incr))[0]
    v_templete = await process_templete(sync_id,templete)
    v_templete['incr_col'] = p_sync['sync_incr_col']
    return v_templete

async def query_datax_sync_es_dataxTemplete(sync_id):
    templete = {}
    p_sync   = await query_datax_by_id(sync_id)
    sql_full = 'select contents from t_templete where templete_id=3'
    sql_incr = 'select contents from t_templete where templete_id=4'
    templete['full'] = (await async_processer.query_one(sql_full))[0]
    templete['incr'] = (await async_processer.query_one(sql_incr))[0]
    v_templete = await process_templete_es(sync_id,templete)
    v_templete['incr_col'] = p_sync['sync_incr_col']
    return v_templete

async def query_datax_sync_doris_dataxTemplete(sync_id):
    templete = {}
    p_sync   = await query_datax_by_id(sync_id)
    sql_full = 'select contents from t_templete where templete_id=5'
    sql_incr = 'select contents from t_templete where templete_id=6'
    templete['full'] = (await async_processer.query_one(sql_full))[0]
    templete['incr'] = (await async_processer.query_one(sql_incr))[0]
    v_templete = await process_templete_doris(sync_id,templete)
    print('query_datax_sync_doris_dataxTemplete=',v_templete['incr'])
    v_templete['incr_col'] = p_sync['sync_incr_col']
    return v_templete

async def downloads_datax_sync_dataxTemplete(sync_id,static_path):
    sync_obj  = await query_datax_by_id(sync_id)
    sync_tag  = sync_obj['sync_tag']

    #获取模板内容至templete字典中
    if sync_obj['sync_type'] == '5':
        templete = await query_datax_sync_dataxTemplete(sync_id)
    elif sync_obj['sync_type'] == '6':
        templete = await query_datax_sync_es_dataxTemplete(sync_id)
    elif sync_obj['sync_type'] == '7':
        templete = await query_datax_sync_doris_dataxTemplete(sync_id)
    else:
        pass

    #切换工作目录
    os.system('cd {0}'.format(static_path+'/downloads/datax'))

    #生成全量json模板文件
    v_datax_full_file = static_path + '/downloads/datax/{0}_full.json'.format(sync_tag)
    v_datax_full_s_file = 'Datax_{0}_full.json'.format(sync_tag)
    with open(v_datax_full_file, 'w') as f:
        f.write(templete['full'])

    #生成增量json模板文件
    v_datax_incr_file = static_path + '/downloads/datax/{0}_incr.json'.format(sync_tag)
    v_datax_incr_s_file = 'Datax_{0}_incr.json'.format(sync_tag)
    with open(v_datax_incr_file, 'w') as f:
        f.write(templete['incr'])

    #生成zip压缩文件
    zip_file = static_path + '/downloads/datax/{0}.zip'.format(sync_tag)
    rzip_file = '/static/downloads/datax/{0}.zip'.format(sync_tag)

    #若文件存在则删除
    if os.path.exists(zip_file):
       os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED,allowZip64=True)
    z.write(v_datax_full_file,arcname=v_datax_full_s_file)
    z.write(v_datax_incr_file,arcname=v_datax_incr_s_file)
    z.close()
    print('downloads_datax_sync_dataxTemplete=',zip_file)

    #删除json文件
    os.system('rm -f {0}'.format(v_datax_full_file))
    os.system('rm -f {0}'.format(v_datax_incr_file))
    return rzip_file

async def query_datax_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date):
    v_where=' and 1=1 '
    if sync_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(sync_tag)
    if market_id != '':
        v_where = v_where + " and a.sync_col_val='{0}'\n".format(market_id)
    if sync_ywlx != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_ywlx)
    if begin_date != '':
        v_where = v_where + " and b.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    else:
        v_where = v_where + " and b.create_date>=DATE_ADD(NOW(),INTERVAL -1 hour)\n"
    if end_date != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(end_date+' 23:59:59')
    sql = """SELECT b.id,
                    c.dmmc as market_name,
                    a.comments,
                    b.sync_tag,
                    cast(b.create_date as char),
                    b.duration,
                    b.amount
            FROM  t_db_sync_config a,t_db_sync_tasks_log b,t_dmmx c
            WHERE a.sync_tag=b.sync_tag  and c.dm='05' 
              and a.sync_col_val=c.dmm  and a.status='1' {0} """.format(v_where)
    return await async_processer.query_list(sql)

async def query_datax_sync_log_analyze(market_id,tagname,begin_date,end_date):
    v_where = ' where 1=1 '
    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(market_id)
    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')
    sql1 = "SELECT cast(a.create_date as char) as create_date,a.duration FROM t_db_sync_tasks_log a {0} ORDER BY a.create_date".format(v_where)
    sql2 = "SELECT cast(a.create_date as char) as create_date,a.amount FROM t_db_sync_tasks_log a {0}  ORDER BY a.create_date".format(v_where)
    return await async_processer.query_list(sql1),await async_processer.query_list(sql2)

async def query_datax_sync_log_analyze2(market_id,sync_type,begin_date,end_date):
    v_where = ' where 1=1 '
    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(market_id)
    if sync_type != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_type)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')
    sql1 = """SELECT cast(a.create_date as char) as create_date,a.duration FROM t_db_sync_tasks_log a {0} ORDER BY a.create_date""".format(v_where)
    sql2 = """SELECT cast(a.create_date as char) as create_date,a.amount FROM t_db_sync_tasks_log a  {0} ORDER BY a.create_date""".format(v_where)
    return await async_processer.query_list(sql1),await async_processer.query_list(sql2)

async def query_datax_sync_log_detail(p_tag,p_sync_rqq,p_sync_rqz):
    v_where = ' and 1=1 '
    if p_tag != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(p_tag)
    if p_sync_rqq != '':
       v_where = v_where + " and b.create_date>='{0}' \n".format(p_sync_rqq+' 0:0:0')
    if p_sync_rqz != '':
        v_where = v_where + " and b.create_date<='{0}'\n".format(p_sync_rqz+' 23:59:59')
    sql = """SELECT 
                 a.comments,
                 b.sync_tag,
                 b.sync_table,
                 CAST(b.create_date AS CHAR), 
                 b.sync_amount,
                 b.duration 
                FROM 
                  t_db_sync_config a,t_db_sync_tasks_log_detail b
                WHERE  a.sync_tag=b.sync_tag  AND a.status='1' {0}""".format(v_where)
    return await async_processer.query_list(sql)

async def get_hbase_columns(p_sync):
    p_ds = await get_ds_by_dsid(p_sync['sour_db_server'])
    n_len= len(p_sync['sync_hbase_rowkey'].split(','))-1
    sql = """
SELECT 
 CONCAT('
 {{
    "index":',cast((@rowNum:=@rowNum+1) as char),',
    "name": "info:',column_name,'",
    "type": "string"
 }},') AS json
 FROM information_schema.columns a,(SELECT (@rowNum:={0})) b
 WHERE a.table_schema='{1}' 
   AND a.table_name='{2}'
   AND instr('{3}',a.column_name)>0
 ORDER BY a.ordinal_position
""".format(str(n_len),p_sync['sour_db_name'],p_sync['sour_tab_name'],p_sync['sour_tab_cols'])
    rs = await async_processer.query_list_by_ds(p_ds,sql)
    v=''
    for i in rs:
        v=v+str(i[0])
    return v[0:-1]

async def get_es_columns(p_sync):
    p_ds = await get_ds_by_dsid(p_sync['sour_db_server'])
    sql = """
SELECT 
	CASE WHEN column_name = 'doc_id' THEN
		 CONCAT('
		 {{
		    "name": "',column_name,'",
		    "type": "id"
		 }},')

	ELSE 
		 CONCAT('
		 {{
		    "name": "',column_name,'",
		    "type": "keyword"
		 }},') 
	 END  AS json
 FROM information_schema.columns a
 WHERE a.table_schema='{0}' 
   AND a.table_name='{1}'
   AND instr('{2}',a.column_name)>0
 ORDER BY CASE WHEN column_name = 'doc_id' THEN 0 ELSE a.ordinal_position END 
""".format(p_sync['sour_db_name'],p_sync['sour_tab_name'],p_sync['sour_tab_cols'])
    rs = await async_processer.query_list_by_ds(p_ds,sql)
    v=''
    for i in rs:
        v=v+str(i[0])
    return v[0:-1]

async def check_tab_exists_pk(cfg):
    ds = await get_ds_by_dsid(cfg['sour_db_server'])
    ds['service'] = cfg['sour_db_name']
    st = """select count(0) from information_schema.columns
              where table_schema='{}' and table_name='{}' and column_key='PRI'""".format(cfg['sour_db_name'],cfg['doris_tab_name'])
    rs = await async_processer.query_one_by_ds(ds,st)
    return rs[0]

async def save_datax_sync(p_sync):
    val  = await check_datax_sync(p_sync,'add')
    if val['code']=='-1':
        return val
    try:
        result                 = {}
        sync_tag               = p_sync['sync_tag']
        sync_server            = p_sync['sync_server']
        sour_db_server         = p_sync['sour_db_server']
        sour_db_name           = p_sync['sour_db_name']
        sour_tab_name          = p_sync['sour_tab_name']
        sour_tab_cols          = p_sync['sour_tab_cols']
        sour_incr_col          = p_sync['sour_incr_col']
        zk_hosts               = p_sync['zk_hosts']
        hbase_thrift           = p_sync['hbase_thrift']
        sync_ywlx              = p_sync['sync_ywlx']
        sync_data_type         = p_sync['sync_data_type']
        python3_home           = p_sync['python3_home']
        script_base            = p_sync['script_base']
        run_time               = p_sync['run_time']
        task_desc              = p_sync['task_desc']
        datax_home             = p_sync['datax_home']
        sync_time_type         = p_sync['sync_time_type']
        sync_gap               = p_sync['sync_gap']
        api_server             = p_sync['api_server']
        status                 = p_sync['status']
        sync_hbase_table       = p_sync['sync_hbase_table']
        sync_hbase_rowkey_sour = p_sync['sync_hbase_rowkey']
        if p_sync['sync_data_type'] == '5':
            sync_hbase_rowkey = get_hbase_rowkey(p_sync)
            sync_hbase_columns = await get_hbase_columns(p_sync)
        else:
            sync_hbase_rowkey = ''
            sync_hbase_columns = ''

        sync_hbase_rowkey_separator = p_sync['sync_hbase_rowkey_separator']
        es_service             = p_sync['es_service']
        es_index_name          = p_sync['es_index_name']
        es_type_name           = p_sync['es_type_name']
        sync_incr_where        = get_sync_incr_where(p_sync)
        if p_sync['sync_data_type'] == '6':
            sync_es_columns    = await get_es_columns(p_sync)
        else:
            sync_es_columns    = ''

        db_doris               = p_sync['db_doris']
        doris_db_name          = p_sync['doris_db_name']
        doris_tab_name         = p_sync['doris_tab_name']
        doris_batch_size       = p_sync['doris_batch_size']
        doris_jvm              = p_sync['doris_jvm']
        doris_tab_config       = p_sync['doris_tab_config']
        doris_sync_type        = p_sync['doris_sync_type']

        sql="""insert into t_datax_sync_config(
                       sync_tag,server_id,sour_db_id,sync_schema,sync_table,
                       sync_columns,sync_incr_col,zk_hosts,sync_ywlx,sync_type,
                       script_path,run_time,comments,datax_home,sync_time_type,
                       sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                       sync_hbase_rowkey_separator,sync_hbase_columns,sync_hbase_rowkey_sour,sync_incr_where,python3_home,
                       hbase_thrift,es_service,es_index_name,es_type_name,sync_es_columns,
                       doris_id,doris_db_name,doris_tab_name,doris_batch_size,doris_jvm,doris_tab_config,doris_sync_type)
               values('{0}','{1}','{2}','{3}','{4}',
                      '{5}','{6}','{7}','{8}','{9}',
                      '{10}','{11}','{12}','{13}','{14}',
                      '{15}','{16}','{17}','{18}','{19}',
                      '{20}','{21}','{22}','{23}','{24}',
                      '{25}','{26}','{27}','{28}','{29}',
                      '{30}','{31}','{32}','{33}','{34}',
                      '{35}','{36}')
            """.format(sync_tag,sync_server,sour_db_server,sour_db_name,sour_tab_name,
                       sour_tab_cols,sour_incr_col,zk_hosts,sync_ywlx,sync_data_type,
                       script_base,run_time,task_desc,datax_home,sync_time_type,
                       sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                       sync_hbase_rowkey_separator,sync_hbase_columns,sync_hbase_rowkey_sour,sync_incr_where,python3_home,
                       hbase_thrift,es_service,es_index_name,es_type_name,sync_es_columns,
                       db_doris,doris_db_name,doris_tab_name,doris_batch_size,doris_jvm,
                       doris_tab_config,doris_sync_type)
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='保存成功!'
        return result
    except:
        result = {}
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '保存失败!'
        return result

async def upd_datax_sync(p_sync):
    result={}
    val = await check_datax_sync(p_sync,'edit')
    if  val['code'] == '-1':
        return val
    try:
        sync_id                = p_sync['sync_id']
        sync_tag               = p_sync['sync_tag']
        sync_server            = p_sync['sync_server']
        sour_db_server         = p_sync['sour_db_server']
        sour_db_name           = p_sync['sour_db_name']
        sour_tab_name          = p_sync['sour_tab_name']
        sour_tab_cols          = p_sync['sour_tab_cols']
        sour_incr_col          = p_sync['sour_incr_col']
        zk_hosts               = p_sync['zk_hosts']
        hbase_thrift           = p_sync['hbase_thrift']
        sync_ywlx              = p_sync['sync_ywlx']
        sync_data_type         = p_sync['sync_data_type']
        script_base            = p_sync['script_base']
        run_time               = p_sync['run_time']
        task_desc              = p_sync['task_desc']
        datax_home             = p_sync['datax_home']
        sync_time_type         = p_sync['sync_time_type']
        sync_gap               = p_sync['sync_gap']
        api_server             = p_sync['api_server']
        status                 = p_sync['status']
        sync_hbase_table       = p_sync['sync_hbase_table']
        if p_sync['sync_data_type'] == '5' :
            sync_hbase_rowkey  = get_hbase_rowkey(p_sync)
            sync_hbase_columns = await get_hbase_columns(p_sync)
        else:
            sync_hbase_rowkey = ''
            sync_hbase_columns = ''
        sync_hbase_rowkey_sp   = p_sync['sync_hbase_rowkey_separator']
        sync_hbase_rowkey_sour = p_sync['sync_hbase_rowkey']
        sync_incr_where        = get_sync_incr_where(p_sync)
        python3_home           = p_sync['python3_home']
        es_service             = p_sync['es_service']
        es_index_name          = p_sync['es_index_name']
        es_type_name           = p_sync['es_type_name']
        if p_sync['sync_data_type'] == '6':
           sync_es_columns        = await get_es_columns(p_sync)
        else:
           sync_es_columns = ''
        db_doris               = p_sync['db_doris']
        doris_db_name          = p_sync['doris_db_name']
        doris_tab_name         = p_sync['doris_tab_name']
        doris_batch_size       = p_sync['doris_batch_size']
        doris_jvm              = p_sync['doris_jvm']
        doris_tab_config       = p_sync['doris_tab_config']
        doris_sync_type        = p_sync['doris_sync_type']

        sql="""update t_datax_sync_config 
                  set  
                      sync_tag                     ='{0}',
                      server_id                    ='{1}',     
                      sour_db_id                   ='{2}',
                      sync_schema                  ='{3}',
                      sync_table                   ='{4}',                      
                      sync_columns                 ='{5}',
                      sync_incr_col                ='{6}',
                      zk_hosts                     ='{7}',
                      sync_ywlx                    ='{8}',
                      sync_type                    ='{9}',                                            
                      script_path                  ='{10}',
                      run_time                     ='{11}',
                      comments                     ='{12}',
                      datax_home                   ='{13}',
                      sync_time_type               ='{14}',                                            
                      sync_gap                     ='{15}',
                      api_server                   ='{16}',
                      status                       ='{17}',
                      sync_hbase_table             ='{18}',
                      sync_hbase_rowkey            ='{19}',                      
                      sync_hbase_rowkey_separator  ='{20}',
                      sync_hbase_columns           ='{21}',
                      sync_hbase_rowkey_sour       ='{22}',
                      sync_incr_where              ='{23}',
                      python3_home                 ='{24}',
                      hbase_thrift                 ='{25}',
                      es_service                   ='{26}',
                      es_index_name                ='{27}',
                      es_type_name                 ='{28}',
                      sync_es_columns              ='{29}',
                      doris_id                     ='{30}',
                      doris_db_name                ='{31}',
                      doris_tab_name               ='{32}',
                      doris_batch_size             ='{33}',
                      doris_jvm                    ='{34}',
                      doris_tab_config             ='{35}',
                      doris_sync_type              ='{36}'
                where id={37}""".format(sync_tag,sync_server,sour_db_server,sour_db_name,sour_tab_name,
                                        sour_tab_cols,sour_incr_col,zk_hosts,sync_ywlx,sync_data_type,
                                        script_base,run_time,task_desc,datax_home,sync_time_type,
                                        sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                                        sync_hbase_rowkey_sp,sync_hbase_columns,sync_hbase_rowkey_sour,
                                        sync_incr_where,python3_home,hbase_thrift,es_service,
                                        es_index_name,es_type_name,sync_es_columns,
                                        db_doris, doris_db_name, doris_tab_name,doris_batch_size,
                                        doris_jvm,doris_tab_config,doris_sync_type,
                                        sync_id)
        print(sql)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='更新成功!'
        return result
    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result

async def del_datax_sync(p_syncid):
    try:
        sql="delete from t_datax_sync_config  where id='{0}'".format(p_syncid)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='删除成功!'
        return result
    except :
        result = {}
        result['code'] = '-1'
        result['message'] = '删除失败!'
        return result

async def get_datax_sync_by_syncid(p_syncid):
    sql = """select server_id,
                    sour_db_id as sour_db_server,
                    desc_db_id as desc_db_server,
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
                    batch_size_incr as sync_batch_size,
                    sync_gap,
                    sync_col_name,
                    sync_col_val,
                    sync_time_type,
                    api_server,
                    status
             from t_db_sync_config where id={0}
          """.format(p_syncid)
    return await async_processer.query_dict_one(sql)

async def query_sync_log_analyze(sync_env,tagname,begin_date,end_date):
    v_where = ' where 1=1 '
    if sync_env == 'prod':
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181'
                                         and  sync_tag='{0}')""".format(tagname)
    if sync_env == "dev":
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181'
                                         and  sync_tag='{0}')""".format(tagname)
    if sync_env == "uat":
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181'
                                         and  sync_tag='{0}')""".format(tagname)

    if sync_env == 'doris_prod':
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                           where doris_id in(select id FROM t_db_source
                                                             where db_type='8' AND  db_env='1'))
                            """
    if sync_env == "doris_dev_test":
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                           where doris_id in(select id FROM t_db_source 
                                                              where db_type='8' AND  db_env in('2','3')))"""


    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)
    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')
    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')
    sql1 = """SELECT cast(a.create_date as char) as create_date,a.duration FROM t_datax_sync_log a {0} ORDER BY a.create_date""".format(v_where)
    sql2 = """SELECT cast(a.create_date as char) as create_date,a.amount  FROM t_datax_sync_log a {0} ORDER BY a.create_date""".format(v_where)

    print('sql1=',sql1)
    print('sql2=',sql2)

    return await async_processer.query_list(sql1),await async_processer.query_list(sql2)

async def get_datax_sync_tags_by_env(p_env):
    v_where=''
    if p_env == 'prod':
        v_where = v_where + " and a.zk_hosts='192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181'\n"
    if p_env == "dev":
        v_where = v_where + " and a.zk_hosts='10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181'\n"
    if p_env == "uat":
        v_where = v_where + " and a.zk_hosts='10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181'\n"

    if p_env == 'doris_prod':
        v_where = v_where + """  and doris_id in (SELECT doris_id FROM t_datax_sync_config 
                                              where doris_id in(select id FROM t_db_source
                                                                where db_type='8' AND  db_env='1'))"""
    if p_env == "doris_dev_test":
        v_where = v_where + """  and doris_id in (SELECT doris_id FROM t_datax_sync_config 
                                              where doris_id in(select id FROM t_db_source 
                                                                 where db_type='8' AND  db_env in('2','3')))"""

    if p_env=='':
        sql = """SELECT a.sync_tag,a.comments FROM t_datax_sync_config a  WHERE STATUS=1   ORDER BY comments"""
    else:
        sql = """SELECT a.sync_tag,a.comments FROM t_datax_sync_config a  WHERE STATUS=1 {0}  ORDER BY comments""".format(v_where)

    print('sql=',sql)
    return await async_processer.query_list(sql)

async def check_sync_tag(p_sync):
    st = "SELECT count(0) as rec FROM t_datax_sync_config  WHERE sync_tag='{}'".format(p_sync['sync_tag'])
    return (await async_processer.query_dict_one(st))['rec']



async def check_datax_sync(p_sync,p_flag):
    print('check_datax_sync=',p_sync)
    result = {}
    if p_sync["sync_tag"]=="":
        result['code']='-1'
        result['message']='同步标识号不能为空!'
        return result
    if p_flag != 'edit':
        if await check_sync_tag(p_sync) >0 :
            result['code'] = '-1'
            result['message'] = '同步标识已存在!'
            return result

    if p_sync["sync_server"]=="":
        result['code']='-1'
        result['message']='同步服务器不能为空!'
        return result

    if p_sync["sour_db_server"]=="":
        result['code']='-1'
        result['message']='源端数据库不能为空!'
        return result

    if p_sync["sour_db_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库名称不能为空!'
        return result

    if p_sync["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库表名不能为空！'
        return result

    if p_sync["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '选择同步列名不能为空！'
        return result

    if p_sync["zk_hosts"]=="" and p_sync['sync_data_type'] == '5':
        result['code']='-1'
        result['message']='zookeeper地址不能为空！'
        return result

    if p_sync["hbase_thrift"]=="" and p_sync['sync_data_type'] == '5':
        result['code']='-1'
        result['message']='hbase_thrift地址不能为空！'
        return result

    if p_sync["sync_hbase_table"] == "" and p_sync['sync_data_type'] == '5':
        result['code'] = '-1'
        result['message'] = 'hbase表名不能为空！'
        return result

    if p_sync["sync_hbase_rowkey"] == "" and p_sync['sync_data_type'] == '5':
        result['code'] = '-1'
        result['message'] = 'hbase行键不能为空！'
        return result

    if p_sync["es_service"]=="" and p_sync['sync_data_type'] == '6':
        result['code']='-1'
        result['message']='ElasticSearch服务不能为空！'
        return result

    if p_sync["es_index_name"] == "" and p_sync['sync_data_type'] == '6':
        result['code'] = '-1'
        result['message'] = 'ElasticSearch索引名不能为空！'
        return result

    if p_sync["es_type_name"] == "" and p_sync['sync_data_type'] == '6':
        result['code'] = '-1'
        result['message'] = 'ElasticSearch类型名不能为空！'
        return result

    if p_sync["sync_ywlx"] == "":
        result['code'] = '-1'
        result['message'] = '同步业务类型不能为空！'
        return result

    if p_sync["sync_data_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步数据方向不能为空！'
        return result

    if p_sync["script_base"] == "":
        result['code'] = '-1'
        result['message'] = 'dataX脚本目录不能为空！'
        return result

    if p_sync["run_time"] == "":
        result['code'] = '-1'
        result['message'] = '运行时间不能为空！'
        return result

    if p_sync["task_desc"] == "":
        result['code'] = '-1'
        result['message'] = '任务描述不能为空！'
        return result

    if p_sync["datax_home"] == "":
        result['code'] = '-1'
        result['message'] = 'datax主目录不能为空！'
        return result

    if p_sync["sync_time_type"] == "":
        result['code'] = '-1'
        result['message'] = '同步时间类型不能为空！'
        return result

    if p_sync["sync_gap"] == "":
        result['code'] = '-1'
        result['message'] = '同步间隔不能为空！'
        return result


    if p_sync["api_server"] == "":
        result['code'] = '-1'
        result['message'] = 'API服务器不能为空！'
        return result

    if p_sync["status"] == "":
        result['code'] = '-1'
        result['message'] = '任务状态不能为空！'
        return result

    if p_sync['sync_data_type'] == '7':

        if p_sync["db_doris"] == "":
            result['code'] = '-1'
            result['message'] = 'doris数据源为空!'
            return result

        if p_sync["doris_db_name"] == "":
            result['code'] = '-1'
            result['message'] = 'doris数据库不能为空!'
            return result

        if p_sync["doris_tab_name"] == "":
            result['code'] = '-1'
            result['message'] = 'doris表名不能为空!'
            return result

        if p_sync["doris_sync_type"] == "":
            result['code'] = '-1'
            result['message'] = 'doris同步类型不能为空!'
            return result
        try:
            if (await check_tab_exists_pk(p_sync)) == 0:
               result['code'] = '-1'
               result['message'] = '表`{}`无主键!'.format(p_sync['doris_tab_name'])
               return result
        except:
            pass


    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def push_datax_sync_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/push_datax_remote_sync'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    v = ''
    for c in jres['msg']:
        if c.count(p_tag) > 0:
            v = v + "<span class='warning'>" + c + "</span>"
        else:
            v = v + c
        v = v + '<br>'
    jres['msg'] = v
    return jres

def pushall_datax_sync_task(p_tags):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'
        for p in p_tags[0:-1].split(','):
            v_tag = p.split('$$')[0]
            v_api = p.split('$$')[1]
            v_cmd = "curl -XPOST {0}/push_datax_remote_sync -d 'tag={1}'".format(v_api,v_tag)
            r = os.popen(v_cmd).read()
            d = json.loads(r)
            if d['code'] != 200:
               traceback.print_exc()
               result['code'] = '-1'
               result['message'] = '推送失败!'
               return result
        return result
    except Exception as e:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '推送失败!'
        return result

def run_datax_sync_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/run_datax_remote_sync'.format(p_api)
    res = requests.post(url, data=data)
    jres = res.json()
    v = ''
    for c in jres['msg'].split('\n'):
        if c.count(p_tag) > 0:
            v = v + "<span class='warning'>" + c + "</span>"
        else:
            v = v + c
        v = v + '<br>'
    jres['msg'] = v
    return jres

def stop_datax_sync_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/stop_datax_remote_sync'.format(p_api)
    res = requests.post(url, data=data)
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

def update_datax_sync_status():
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        r = os.system("curl -XPOST {0}/update_backup_status".format(get_api_server()))
        if r == 0:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '执行失败！'
            return result
    except:
        result['code'] = '-1'
        result['message'] = '执行失败！'
        return result


async def get_datax_sync_db_names_doris(dbid):
    pds = await get_ds_by_dsid(dbid)
    sql = """select schema_name,schema_name FROM information_schema.`SCHEMATA` 
                where schema_name NOT IN('information_schema','mysql','performance_schema') order by schema_name"""
    try:
        res = await async_processer.query_list_by_ds(pds,sql)
        return res
    except:
        try:
            print('from agent server:{} get db name!'.format(pds['proxy_server']))
            res = get_mysql_proxy_result(pds, sql, 'information_schema')
            return res['data']
        except:
            traceback.print_exc()
            return {'message':['获取数据库名失败!']}
