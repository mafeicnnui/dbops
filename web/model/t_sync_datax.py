#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common    import exception_info,get_connection,get_connection_dict,get_connection_ds,aes_decrypt
from web.model.t_ds      import get_ds_by_dsid
import os,json,zipfile
import requests

def query_datax_sync(sync_tag,sync_ywlx,sync_type,sync_env):
    db = get_connection()
    cr = db.cursor()
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

    sql = """SELECT  a.id,
                     concat(substr(sync_tag,1,40),'...') as sync_tag1,
                     sync_tag,
		             CONCAT(SUBSTR(a.comments,1,30),'...'),
                     CONCAT(b.server_ip,':',b.server_port) AS sync_server,
                     -- c.dmmc AS  sync_ywlx,
                     d.dmmc AS  sync_type,
                     a.run_time,
                     a.api_server,
                     CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
             FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d
            WHERE a.server_id=b.id AND b.status='1' 
              AND c.dm='08' AND d.dm='09'
              AND a.sync_ywlx=c.dmm
              AND a.sync_type=d.dmm
              {0}
         """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_datax_sync_detail(sync_id):
    db = get_connection()
    cr = db.cursor()
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
                 a.sync_type             
            FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d,t_db_source e
            WHERE a.server_id=b.id AND b.status='1' 
            AND a.sour_db_id=e.id
            AND c.dm='08' AND d.dm='09' 
            AND a.sync_ywlx=c.dmm
            AND a.sync_type=d.dmm
            AND a.id='{0}'
         """.format(sync_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    v_list=list(rs)
    cr.close()
    db.commit()
    return v_list

def query_datax_by_id(sync_id):
    db = get_connection_dict()
    cr = db.cursor()
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
                 a.sync_es_columns
            FROM t_datax_sync_config a,t_server b ,t_dmmx c,t_dmmx d,t_db_source e
            WHERE a.server_id=b.id AND b.status='1' 
            AND a.sour_db_id=e.id
            AND c.dm='08' AND d.dm='09'
            AND a.sync_ywlx=c.dmm
            AND a.sync_type=d.dmm
            AND a.id='{0}'
         """.format(sync_id)
    print(sql)
    cr.execute(sql)
    rs=cr.fetchone()
    #v_list=list(rs)
    cr.close()
    db.commit()
    return rs

def process_templete(p_sync_id,p_templete):
    v_templete = p_templete
    p_sync = query_datax_by_id(p_sync_id)
    print('process_templete->p_sync=',p_sync)
    print('process_templete->p_templete=',p_templete)
    #replace full templete
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$',p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$PASSWORD$$',aes_decrypt(p_sync['password'],p_sync['user']))
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
    v_templete['incr'] = v_templete['incr'].replace('$$PASSWORD$$', aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$USERNAME$$', p_sync['user'])
    v_templete['incr'] = v_templete['incr'].replace('$$ZK_HOSTS', p_sync['zk_hosts'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_TABLE_NAME$$', p_sync['sync_hbase_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_ROWKEY$$', p_sync['sync_hbase_rowkey'])
    v_templete['incr'] = v_templete['incr'].replace('$$HBASE_COLUMN_NAMES$$', p_sync['sync_hbase_columns'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_WHERE$$', p_sync['sync_incr_where'])
    print('process_templete->v_templete=', v_templete)
    return v_templete

def process_templete_es(p_sync_id,p_templete):
    v_templete = p_templete
    p_sync = query_datax_by_id(p_sync_id)
    print('process_templete_es->p_sync=',p_sync)
    print('process_templete_es->p_templete=',p_templete)
    #replace full templete
    v_templete['full'] = v_templete['full'].replace('$$USERNAME$$',p_sync['user'])
    v_templete['full'] = v_templete['full'].replace('$$PASSWORD$$',aes_decrypt(p_sync['password'],p_sync['user']))
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
    v_templete['incr'] = v_templete['incr'].replace('$$PASSWORD$$', aes_decrypt(p_sync['password'],p_sync['user']))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_COLUMN_NAMES$$', get_mysql_columns(p_sync))
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_TABLE_NAME$$', p_sync['sync_table'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_URL$$', p_sync['mysql_url'])
    v_templete['incr'] = v_templete['incr'].replace('$$MYSQL_WHERE$$', p_sync['sync_incr_where'])
    v_templete['full'] = v_templete['full'].replace('$$ES_SERVICE$$', p_sync['zk_hosts'])
    v_templete['full'] = v_templete['full'].replace('$$ES_INDEX_NAME$$', p_sync['sync_hbase_table'])
    v_templete['full'] = v_templete['full'].replace('$$ES_TYPE_NAME$$', p_sync['sync_hbase_rowkey'])
    v_templete['full'] = v_templete['full'].replace('$$ES_COLUMN_NAMES$$', p_sync['sync_es_columns'])
    print('process_templete_es->v_templete=', v_templete)
    return v_templete

def query_datax_sync_dataxTemplete(sync_id):
    templete = {}
    p_sync   = query_datax_by_id(sync_id)
    db       = get_connection()
    cr       = db.cursor()
    sql_full = 'select contents from t_templete where templete_id=1'
    print(sql_full)
    cr.execute(sql_full)
    rs=cr.fetchone()
    templete['full']=rs[0]
    sql_incr = 'select contents from t_templete where templete_id=2'
    print(sql_incr)
    cr.execute(sql_incr)
    rs = cr.fetchone()
    templete['incr'] = rs[0]
    cr.close()
    db.commit()
    v_templete=process_templete(sync_id,templete)
    v_templete['incr_col'] = p_sync['sync_incr_col']
    print('query_datax_sync_dataxTemplete=', v_templete)
    return v_templete

def query_datax_sync_es_dataxTemplete(sync_id):
    templete = {}
    p_sync   = query_datax_by_id(sync_id)
    db       = get_connection()
    cr       = db.cursor()
    sql_full = 'select contents from t_templete where templete_id=3'
    print(sql_full)
    cr.execute(sql_full)
    rs=cr.fetchone()
    templete['full']=rs[0]
    sql_incr = 'select contents from t_templete where templete_id=4'
    print(sql_incr)
    cr.execute(sql_incr)
    rs = cr.fetchone()
    templete['incr'] = rs[0]
    cr.close()
    db.commit()
    v_templete=process_templete_es(sync_id,templete)
    v_templete['incr_col'] = p_sync['sync_incr_col']
    print('query_datax_sync_es_dataxTemplete=', v_templete)
    return v_templete

def downloads_datax_sync_dataxTemplete(sync_id,static_path):

    sync_tag = query_datax_by_id(sync_id)['sync_tag']

    #获取模板内容至templete字典中
    templete = query_datax_sync_dataxTemplete(sync_id)

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

def query_datax_sync_log(sync_tag,market_id,sync_ywlx,begin_date,end_date):
    db = get_connection()
    cr = db.cursor()

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
            WHERE a.sync_tag=b.sync_tag 
              and c.dm='05' 
              and a.sync_col_val=c.dmm
              and a.status='1'
              {0}
            -- order by b.create_date desc,b.sync_tag 
        """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_datax_sync_log_analyze(market_id,tagname,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = ' where 1=1 '

    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(market_id)

    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                  cast(a.create_date as char) as create_date,a.duration
              FROM t_db_sync_tasks_log a
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    sql2 = """SELECT 
                  cast(a.create_date as char) as create_date,a.amount
              FROM t_db_sync_tasks_log a 
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    print(sql1)
    print(sql2)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2

def query_datax_sync_log_analyze2(market_id,sync_type,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = ' where 1=1 '

    if market_id != '':
        v_where = v_where + " and exists(select 1 from t_db_sync_config b where a.sync_tag=b.sync_tag and b.sync_col_val='{0}')\n".format(market_id)

    if sync_type != '':
        v_where = v_where + " and a.sync_ywlx='{0}'\n".format(sync_type)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                  cast(a.create_date as char) as create_date,a.duration
              FROM t_db_sync_tasks_log a
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    sql2 = """SELECT 
                  cast(a.create_date as char) as create_date,a.amount
              FROM t_db_sync_tasks_log a 
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    print(sql1)
    print(sql2)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2

def query_datax_sync_log_detail(p_tag,p_sync_rqq,p_sync_rqz):
    db = get_connection()
    cr = db.cursor()
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
                WHERE  a.sync_tag=b.sync_tag 
                   AND a.status='1'
                  {0}
                """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

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

    print(v_row_key)
    return v_row_key

def get_mysql_columns(p_sync):
    v = '''"{0}",'''.format(p_sync['sync_hbase_rowkey_sour'])
    for i in p_sync['sync_columns'].split(','):
       v=v+'''"{}",'''.format(i)
    print('get_mysql_columns=',v)
    return v[0:-1]

def get_hbase_columns(p_sync):
    print('p_sync=',p_sync)
    p_ds = get_ds_by_dsid(p_sync['sour_db_server'])
    n_len= len(p_sync['sync_hbase_rowkey'].split(','))-1
    db   = get_connection_ds(p_ds)
    cr   = db.cursor()
    print('get_hbase_columns.para=',p_sync['sour_db_name'],p_sync['sour_tab_name'],p_sync['sour_tab_cols'],p_sync['sync_hbase_rowkey'])
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
    print('get_hbase_columns.sql=',sql)
    cr.execute(sql)
    rs = cr.fetchall()
    print('rs=',rs)
    v=''
    for i in rs:
        v=v+str(i[0])
    print('------------------------------')
    print(v)
    return v[0:-1]

def get_es_columns(p_sync):
    print('p_sync=',p_sync)
    p_ds = get_ds_by_dsid(p_sync['sour_db_server'])
    db   = get_connection_ds(p_ds)
    cr   = db.cursor()
    print('get_es_columns.para=',p_sync['sour_db_name'],p_sync['sour_tab_name'],p_sync['sour_tab_cols'])
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
    print('get_es_columns.sql=',sql)
    cr.execute(sql)
    rs = cr.fetchall()
    print('rs=',rs)
    v=''
    for i in rs:
        v=v+str(i[0])
    print('------------------------------')
    print(v)
    return v[0:-1]

def get_sync_incr_where(p_sync):
    print('get_sync_incr_where=',p_sync)
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

def save_datax_sync(p_sync):
    result = {}
    val    = check_datax_sync(p_sync)
    if val['code']=='-1':
        return val
    try:
        db                   = get_connection()
        cr                   = db.cursor()
        result               = {}
        sync_tag             = p_sync['sync_tag']
        sync_server          = p_sync['sync_server']
        sour_db_server       = p_sync['sour_db_server']
        sour_db_name         = p_sync['sour_db_name']
        sour_tab_name        = p_sync['sour_tab_name']
        sour_tab_cols        = p_sync['sour_tab_cols']
        sour_incr_col        = p_sync['sour_incr_col']
        zk_hosts             = p_sync['zk_hosts']
        hbase_thrift         = p_sync['hbase_thrift']
        sync_ywlx            = p_sync['sync_ywlx']
        sync_data_type       = p_sync['sync_data_type']
        python3_home         = p_sync['python3_home']
        script_base          = p_sync['script_base']
        run_time             = p_sync['run_time']
        task_desc            = p_sync['task_desc']
        datax_home           = p_sync['datax_home']
        sync_time_type       = p_sync['sync_time_type']
        sync_gap             = p_sync['sync_gap']
        api_server           = p_sync['api_server']
        status               = p_sync['status']
        sync_hbase_table     = p_sync['sync_hbase_table']
        sync_hbase_rowkey_sour = p_sync['sync_hbase_rowkey']
        sync_hbase_rowkey    = get_hbase_rowkey(p_sync)
        sync_hbase_columns   = get_hbase_columns(p_sync)
        sync_hbase_rowkey_separator = p_sync['sync_hbase_rowkey_separator']
        es_service           = p_sync['es_service']
        es_index_name        = p_sync['es_index_name']
        es_type_name         = p_sync['es_type_name']
        sync_incr_where      = get_sync_incr_where(p_sync)
        sync_es_columns      = get_es_columns(p_sync)

        sql="""insert into t_datax_sync_config(
                           sync_tag,server_id,sour_db_id,sync_schema,sync_table,
                           sync_columns,sync_incr_col,zk_hosts,sync_ywlx,sync_type,
                           script_path,run_time,comments,datax_home,sync_time_type,
                           sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                           sync_hbase_rowkey_separator,sync_hbase_columns,sync_hbase_rowkey_sour,
                           sync_incr_where,python3_home,hbase_thrift,es_service,es_index_name,es_type_name,sync_es_columns)
                   values('{0}','{1}','{2}','{3}','{4}',
                          '{5}','{6}','{7}','{8}','{9}',
                          '{10}','{11}','{12}','{13}','{14}',
                          '{15}','{16}','{17}','{18}','{19}',
                          '{20}','{21}','{22}','{23}','{24}','{25}','{26}')
            """.format(sync_tag,sync_server,sour_db_server,sour_db_name,sour_tab_name,
                       sour_tab_cols,sour_incr_col,zk_hosts,sync_ywlx,sync_data_type,
                       script_base,run_time,task_desc,datax_home,sync_time_type,
                       sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                       sync_hbase_rowkey_separator,sync_hbase_columns,sync_hbase_rowkey_sour,
                       sync_incr_where,python3_home,hbase_thrift,es_service,es_index_name,es_type_name,sync_es_columns)

        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_datax_sync(p_sync):
    result={}
    val = check_datax_sync(p_sync)
    if  val['code'] == '-1':
        return val
    try:
        db = get_connection()
        cr = db.cursor()
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
        sync_hbase_rowkey      = get_hbase_rowkey(p_sync)
        sync_hbase_columns     = get_hbase_columns(p_sync)
        sync_hbase_rowkey_sp   = p_sync['sync_hbase_rowkey_separator']
        sync_hbase_rowkey_sour = p_sync['sync_hbase_rowkey']
        sync_incr_where        = get_sync_incr_where(p_sync)
        python3_home           = p_sync['python3_home']
        es_service             = p_sync['es_service']
        es_index_name          = p_sync['es_index_name']
        es_type_name           = p_sync['es_type_name']
        sync_es_columns        = get_es_columns(p_sync)

        sql="""update t_datax_sync_config 
                  set  
                      sync_tag            ='{0}',
                      server_id           ='{1}',     
                      sour_db_id          ='{2}',
                      sync_schema         ='{3}',
                      sync_table          ='{4}',                      
                      sync_columns        ='{5}',
                      sync_incr_col       ='{6}',
                      zk_hosts            ='{7}',
                      sync_ywlx           ='{8}',
                      sync_type           ='{9}',                                            
                      script_path         ='{10}',
                      run_time            ='{11}',
                      comments            ='{12}',
                      datax_home          ='{13}',
                      sync_time_type      ='{14}',                                            
                      sync_gap            ='{15}',
                      api_server          ='{16}',
                      status              ='{17}',
                      sync_hbase_table    ='{18}',
                      sync_hbase_rowkey   ='{19}',                      
                      sync_hbase_rowkey_separator  ='{20}',
                      sync_hbase_columns           ='{21}',
                      sync_hbase_rowkey_sour       ='{22}',
                      sync_incr_where              ='{23}',
                      python3_home                 ='{24}',
                      hbase_thrift                 ='{25}',
                      es_service                   ='{26}',
                      es_index_name                ='{27}',
                      es_type_name                 ='{28}',
                      sync_es_columns              ='{29}'                                            
                where id={30}""".format(sync_tag,sync_server,sour_db_server,sour_db_name,sour_tab_name,
                                        sour_tab_cols,sour_incr_col,zk_hosts,sync_ywlx,sync_data_type,
                                        script_base,run_time,task_desc,datax_home,sync_time_type,
                                        sync_gap,api_server,status,sync_hbase_table,sync_hbase_rowkey,
                                        sync_hbase_rowkey_sp,sync_hbase_columns,sync_hbase_rowkey_sour,
                                        sync_incr_where,python3_home,hbase_thrift,es_service,
                                        es_index_name,es_type_name,sync_es_columns,sync_id)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except Exception as e:
        print('upd_datax_sync.ERROR:',str(e))
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_datax_sync(p_syncid):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        sql="delete from t_datax_sync_config  where id='{0}'".format(p_syncid)
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
    except :
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def check_datax_sync(p_sync):
    result = {}

    if p_sync["sync_tag"]=="":
        result['code']='-1'
        result['message']='同步标识号不能为空！'
        return result

    if p_sync["sync_server"]=="":
        result['code']='-1'
        result['message']='同步服务器不能为空！'
        return result

    if p_sync["sour_db_server"]=="":
        result['code']='-1'
        result['message']='源端数据库不能为空！'
        return result

    if p_sync["sour_db_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库名称不能为空！'
        return result

    if p_sync["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '源数据库表名不能为空！'
        return result

    if p_sync["sour_tab_name"] == "":
        result['code'] = '-1'
        result['message'] = '选择同步列名不能为空！'
        return result

    if p_sync["zk_hosts"]=="" and p_sync['sync_data_type'] == 5:
        result['code']='-1'
        result['message']='zookeeper地址不能为空！'
        return result

    if p_sync["hbase_thrift"]=="" and p_sync['sync_data_type'] == 5:
        result['code']='-1'
        result['message']='hbase_thrift地址不能为空！'
        return result

    if p_sync["sync_hbase_table"] == "" and p_sync['sync_data_type'] == 5:
        result['code'] = '-1'
        result['message'] = 'hbase表名不能为空！'
        return result

    if p_sync["sync_hbase_rowkey"] == "" and p_sync['sync_data_type'] == 5:
        result['code'] = '-1'
        result['message'] = 'hbase行键不能为空！'
        return result

    if p_sync["es_service"]=="" and p_sync['sync_data_type'] == 6:
        result['code']='-1'
        result['message']='ElasticSearch服务不能为空！'
        return result

    if p_sync["es_index_name"] == "" and p_sync['sync_data_type'] == 6:
        result['code'] = '-1'
        result['message'] = 'ElasticSearch索引名不能为空！'
        return result

    if p_sync["es_type_name"] == "" and p_sync['sync_data_type'] == 6:
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

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

def get_datax_sync_by_syncid(p_syncid):
    db = get_connection()
    cr = db.cursor()
    sql = """select server_id,sour_db_id,desc_db_id,
                    sync_tag,sync_ywlx,sync_type,
                    script_path,script_file,run_time,
                    comments,python3_home,sync_schema,
                    sync_table,batch_size,batch_size_incr,
                    sync_gap,sync_col_name,sync_col_val,
                    sync_time_type,api_server,status
             from t_db_sync_config where id={0}
          """.format(p_syncid)
    cr.execute(sql)
    rs = cr.fetchall()
    d_sync = {}
    d_sync['server_id']      = rs[0][0]
    d_sync['sour_db_server'] = rs[0][1]
    d_sync['desc_db_server'] = rs[0][2]
    d_sync['sync_tag']       = rs[0][3]
    d_sync['sync_ywlx']      = rs[0][4]
    d_sync['sync_data_type'] = rs[0][5]
    d_sync['script_base']    = rs[0][6]
    d_sync['script_name']    = rs[0][7]
    d_sync['run_time']       = rs[0][8]
    d_sync['task_desc']       = rs[0][9]
    d_sync['python3_home']   = rs[0][10]
    d_sync['sync_schema']    = rs[0][11]
    d_sync['sync_tables']    = rs[0][12]
    d_sync['sync_batch_size'] = rs[0][13]
    d_sync['sync_batch_size_incr'] = rs[0][14]
    d_sync['sync_gap']       = rs[0][15]
    d_sync['sync_col_name']  = rs[0][16]
    d_sync['sync_col_val']   = rs[0][17]
    d_sync['sync_time_type'] = rs[0][18]
    d_sync['api_server']     = rs[0][19]
    d_sync['status']         = rs[0][20]
    cr.close()
    db.commit()
    print(d_sync)
    return d_sync

def push_datax_sync_task(p_tag,p_api):
    data = {
        'tag': p_tag,
    }
    url = 'http://{}/push_datax_remote_sync'.format(p_api)
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



def pushall_datax_sync_task(p_tags):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '推送成功！'

        print('pushall_datax_sync_task=',p_tags[0:-1])
        for p in p_tags[0:-1].split(','):
            print('p=',p)
            v_tag = p.split('$$')[0]
            v_api = p.split('$$')[1]
            v_cmd="curl -XPOST {0}/push_datax_remote_sync -d 'tag={1}'".format(v_api,v_tag)
            print('pushall_datax_sync_task.cmd=',v_cmd)
            r=os.popen(v_cmd).read()
            d=json.loads(r)
            if d['code']!=200:
               result['code'] = '-1'
               result['message'] = '{0}!'.format(d['msg'])
               return result
        return result
    except Exception as e:
        result['code'] = '-1'
        result['message'] = '{0}!'.format(str(e))
        return result

def run_datax_sync_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/run_datax_remote_sync -d 'tag={1}'".format(p_api,p_tag)
        print('v_cmd=', v_cmd)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result

    except Exception as e:
          result['code'] = '-1'
          result['message'] = '{0}!'.format(str(e))
          return result

def stop_datax_sync_task(p_tag,p_api):
    try:
        result = {}
        result['code'] = '0'
        result['message'] = '执行成功！'
        v_cmd = "curl -XPOST {0}/stop_datax_remote_sync -d 'tag={1}'".format(p_api,p_tag)
        r = os.popen(v_cmd).read()
        d = json.loads(r)
        if d['code'] == 200:
            return result
        else:
            result['code'] = '-1'
            result['message'] = '{0}!'.format(d['msg'])
            return result

    except Exception as e:
         result['code'] = '-1'
         result['message'] = '{0!'.format(str(e))
         return result

def update_datax_sync_status():
    try:
        #通过p_tag自动获取api_server地址
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

def query_sync_log_analyze(sync_env,tagname,begin_date,end_date):
    db  = get_connection()
    cr  = db.cursor()
    v_where = ' where 1=1 '
    if sync_env == 'prod':
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181'
                                         and  sync_tag='{0}' 
                                        ) 
                            """.format(tagname)
    elif sync_env == "dev":
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181'
                                         and  sync_tag='{0}' 
                                        ) 
                            """.format(tagname)
    elif sync_env == "uat":
        v_where = v_where + """  and exists(SELECT 1 FROM t_datax_sync_config 
                                        where zk_hosts='10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181'
                                         and  sync_tag='{0}' 
                                        ) 
                            """.format(tagname)
    else:
        pass

    if tagname != '':
        v_where = v_where + " and a.sync_tag='{0}'\n".format(tagname)

    if begin_date != '':
        v_where = v_where + " and a.create_date>='{0}'\n".format(begin_date+' 0:0:0')

    if end_date != '':
        v_where = v_where + " and a.create_date<='{0}'\n".format(end_date+' 23:59:59')

    sql1 = """SELECT 
                  cast(a.create_date as char) as create_date,a.duration
              FROM t_datax_sync_log a
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    sql2 = """SELECT 
                  cast(a.create_date as char) as create_date,a.amount
              FROM t_datax_sync_log a 
              {0}
              ORDER BY a.create_date
             """.format(v_where)

    print(sql1)
    print(sql2)

    cr.execute(sql1)
    v_list1 = []
    for r in cr.fetchall():
        v_list1.append(list(r))

    cr.execute(sql2)
    v_list2 = []
    for r in cr.fetchall():
        v_list2.append(list(r))

    cr.close()
    db.commit()
    return v_list1,v_list2

def get_datax_sync_tags_by_env(p_env):
    db = get_connection()
    cr = db.cursor()
    v_where=''
    if p_env == 'prod':
        v_where = v_where + " and a.zk_hosts='192.168.100.63:2181,192.168.100.64:2181,192.168.100.69:2181'\n"
    elif p_env == "dev":
        v_where = v_where + " and a.zk_hosts='10.2.39.165:2181,10.2.39.166:2181,10.2.39.182:2181'\n"
    elif p_env == "uat":
        v_where = v_where + " and a.zk_hosts='10.2.39.84:2181,10.2.39.89:2181,10.2.39.67:2181'\n"
    else:
        pass

    if p_env=='':
        sql = """SELECT a.sync_tag,a.comments FROM t_datax_sync_config a  WHERE STATUS=1   ORDER BY comments"""
    else:
        sql = """SELECT a.sync_tag,a.comments FROM t_datax_sync_config a  WHERE STATUS=1 {0}  ORDER BY comments""".format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    return v_list