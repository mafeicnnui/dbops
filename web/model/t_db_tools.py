#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/14 14:02
# @Author : ma.fei
# @File : t_db_tools.py.py
# @Software: PyCharm

from web.model.t_ds import get_ds_by_dsid_by_cdb
from web.model.t_sql import get_ck_proxy_result, get_ck_result
from web.utils.common import format_sql, current_rq
from web.utils.mysql_async import async_processer
import xlwt
import os,zipfile
import traceback


async def save_db(dsid,dres):
    desc = 'insert into t_db_compare(`dsid`,'
    for r in dres[0:1]:
          for key, value in r.items():
                desc = desc + '`{}`,'.format(key)
    desc = desc[0:-1]+') values '

    vals = ''
    for r in dres:
          val = '{},'.format(dsid)
          for key,value in r.items():
                 val = val + "'{}',".format(format_sql(str(value)))
          vals = vals +'({}),'.format(val[0:-1])
    await async_processer.exec_sql(desc + vals[0:-1])

async def db_stru_compare(sour_db_server,sour_schema,desc_db_server,desc_schema,sour_tab):
      vvv = " and instr(table_name,'{}')>0".format(sour_tab) if sour_tab!='' else ''
      sds = await get_ds_by_dsid_by_cdb(sour_db_server,sour_schema)
      dds = await get_ds_by_dsid_by_cdb(desc_db_server,desc_schema)
      sql  = """SELECT  
                table_schema,
                table_name,
                column_name,
                is_nullable,
                data_type,
                column_default,
                character_maximum_length,
                numeric_precision,
                character_set_name,
                collation_name,
                column_type,
                column_key,
                extra,
                column_comment
            FROM information_schema.columns 
            WHERE table_schema='{}' {} ORDER BY table_name,ordinal_position"""

      sres = await async_processer.query_dict_list_by_ds(sds,sql.format(sour_schema,vvv))
      dres = await async_processer.query_dict_list_by_ds(dds, sql.format(desc_schema,vvv))

      await async_processer.exec_sql('truncate table t_db_compare')
      await save_db(sour_db_server,sres)
      await save_db(desc_db_server,dres)

      sql = """
            SELECT a.table_schema,
                   a.table_name,
                   a.column_name,
                   a.is_nullable,
                   a.column_type,
                   a.column_default,
                   a.character_set_name,
                   a.collation_name,
                   a.column_key,
                   a.column_comment,
                   a.extra
            FROM t_db_compare a
            WHERE dsid={} AND not exists(
                 select 1 FROM t_db_compare b
                    WHERE b.dsid={} 
                      AND b.`table_name`=a.`table_name`
                      AND b.`column_name`=a.`column_name`
                      AND b.`is_nullable` = a.`is_nullable`
                      AND b.`data_type` = a.`data_type`
                      AND b.`column_default` = a.`column_default`
                      AND b.`character_maximum_length` = a.`character_maximum_length`
                      AND b.`numeric_precision` = a.`numeric_precision`
                      AND b.`character_set_name` = a.`character_set_name`
                      AND b.`column_type` = a.`column_type`
                      AND b.`column_key` = a.`column_key`
                      AND b.`extra` = a.`extra`
                      AND b.`column_comment` = a.`column_comment`)"""
      res = await async_processer.query_list(sql.format(sour_db_server,desc_db_server))
      return res

async def db_stru_compare_idx(sour_db_server,sour_schema, desc_db_server, desc_schema, sour_tab):
    vvv = " and instr(table_name,'{}')>0".format(sour_tab) if sour_tab != '' else ''
    sds = await get_ds_by_dsid_by_cdb(sour_db_server, sour_schema)
    dds = await get_ds_by_dsid_by_cdb(desc_db_server, desc_schema)
    sql = """SELECT  table_schema,table_name
             FROM information_schema.tables 
             WHERE table_schema='{}' {} ORDER BY table_name"""

    sres = await async_processer.query_dict_list_by_ds(sds, sql.format(sour_schema, vvv))
    dres = await async_processer.query_dict_list_by_ds(dds, sql.format(desc_schema, vvv))

    await async_processer.exec_sql('truncate table t_db_compare_idx')

    for s in sres:
        rs = await async_processer.query_dict_list_by_ds(sds,'show index from {}'.format(s['table_name']))
        for r in rs:
            st = """insert into t_db_compare_idx
                     (dsid,table_schema,`table_name`,is_unique,index_name,seq_in_index,`column_name`,`nullable`,index_type) 
                     values({},'{}','{}','{}','{}','{}','{}','{}','{}')
                 """.format(sour_db_server,sour_schema, r['table'], r['non_unique'],r['key_name'],
                            r['seq_in_index'],r['column_name'],r['null'],r['index_type'])
            await async_processer.exec_sql(st)

    for s in dres:
        rs = await async_processer.query_dict_list_by_ds(dds, 'show index from {}'.format(s['table_name']))
        for r in rs:
            st = """insert into t_db_compare_idx
                       (dsid,table_schema,`table_name`,is_unique,index_name,seq_in_index,`column_name`,`nullable`,index_type) 
                       values({},'{}','{}','{}','{}','{}','{}','{}','{}')
                   """.format(desc_db_server, desc_schema, r['table'], r['non_unique'], r['key_name'],
                              r['seq_in_index'], r['column_name'], r['null'], r['index_type'])
            await async_processer.exec_sql(st)

    sql = """ SELECT   a.table_schema,
                       a.table_name,
                       a.index_name,
                       a.index_type,
                       case when a.is_unique =0 then '唯一' else  '非唯一' end is_unique,
                       a.column_name,
                       a.nullable 
                FROM v_db_compare_idx a
                WHERE dsid={} AND NOT EXISTS(
                 SELECT 1 FROM v_db_compare_idx b
                    WHERE b.dsid={}
                      AND b.`table_name` = a.`table_name`
                      AND b.`index_name` = a.`index_name`
                      AND b.`index_type` = a.`index_type`
                      AND b.`is_unique`  = a.`is_unique`
                      AND b.`column_name` = a.`column_name`
                      AND b.`nullable` = a.`nullable`)"""
    res = await async_processer.query_list(sql.format(sour_db_server, desc_db_server))
    return res

def get_sync_sql(sres,dres,desc_schema=''):
    if dres is None:
        st = """ALTER TABLE `{}`.`{}` ADD `{}` `{}` {} {} {} {} {};
             """.format(desc_schema,
                    sres['table_name'],
                    sres['column_name'],
                    sres['column_type'],
                    ' CHARSET ' + sres['character_set_name']  if sres['character_set_name'] is not None and sres['character_set_name'] != '' else '',
                    'COLLATE ' + sres['collation_name'] if sres['collation_name'] is not None and sres['collation_name'] != '' else '',
                    'DEFAULT ' + sres['column_default'] if sres['column_default'] is not None and sres['column_default'] != '' else '',
                    'NOT NULL '  if sres['is_nullable'] == 'YES' is not None else '',
                    "COMMENT '"+sres['column_comment']+"'" if sres['column_comment'] is not None and sres['column_comment'] != '' else '')

    else:
        st = """ALTER TABLE `{}`.`{}` CHANGE `{}` `{}` {} {} {} {} {} {};
             """.format(dres['table_schema'],
                        dres['table_name'],
                        sres['column_name'],
                        sres['column_name'],
                        sres['column_type'],
                        ' CHARSET ' + sres['character_set_name']
                                    if sres['character_set_name'] is not None and sres['character_set_name'] !='' else '',
                        'COLLATE ' + sres['collation_name']
                                    if sres['collation_name'] is not None and sres['collation_name'] !='' else '',
                        'DEFAULT ' + sres['column_default']
                                    if sres['column_default'] is not None and sres['column_default'] !='' else '',
                        'NOT NULL ' if sres['is_nullable'] == 'YES' is not None else '',
                        "COMMENT '{}'".format(sres['column_comment'])
                                    if sres['column_comment'] is not None and sres['column_comment'] !=''  else '')
    return st

def get_sync_sql_idx(sres,dres,desc_schema=''):
    if dres is None:
        if sres['index_name'] =='PRIMARY':
           st = """ALTER TABLE `{}`.`{}` ADD  PRIMARY KEY (`{}`);
                """.format(desc_schema,sres['table_name'],sres['column_name'],sres['column_name'])
        elif sres['is_unique'] == '0':
           st = """ALTER TABLE `{}`.`{}` ADD  UNIQUE `{}` (`{}`);
                """.format(desc_schema, sres['table_name'], sres['column_name'], sres['column_name'])
        else:
           st = """ALTER TABLE `{}`.`{}` ADD  INDEX `{}` (`{}`);
                """.format(desc_schema, sres['table_name'], sres['index_name'],sres['column_name'])

    else:
        if sres['index_name'] =='PRIMARY':
           st = """ALTER TABLE `{}`.`{}` DROP PRIMARY KEY (`{}`);\n\nALTER TABLE `{}`.`{}` ADD  PRIMARY KEY (`{}`);
                """.format(desc_schema,sres['table_name'],sres['column_name'],sres['column_name'],
                           desc_schema,sres['table_name'],sres['column_name'],sres['column_name'])
        elif sres['is_unique'] == '0':
           st = """ALTER TABLE `{}`.`{}` DROP UNIQUE `{}` (`{}`);\n\nALTER TABLE `{}`.`{}` ADD  UNIQUE `{}` (`{}`);
                """.format(desc_schema, sres['table_name'], sres['column_name'], sres['column_name'],
                           desc_schema, sres['table_name'], sres['column_name'], sres['column_name'])
        else:
           st = """ALTER TABLE `{}`.`{}` DROP INDEX `{}` (`{}`);\n\nALTER TABLE `{}`.`{}` ADD  INDEX `{}` (`{}`);
                """.format(desc_schema, sres['table_name'], sres['index_name'],sres['column_name'],
                           desc_schema, sres['table_name'], sres['index_name'],sres['column_name'])
    return st

async def db_stru_compare_detail(sour_db_server,sour_schema,desc_db_server,desc_schema,table,column):
    sql = """SELECT   a.table_schema,
                      a.table_name,
                      a.column_name,
                      a.is_nullable,
                      a.column_type,
                      a.column_default,
                      a.column_key,
                      a.character_set_name,
                      a.collation_name,
                      a.column_comment,
                      a.extra
               FROM t_db_compare a
               WHERE  a.dsid={} 
                  and a.`table_schema`='{}' 
                  and a.`table_name`='{}' 
                  and a.`column_name`='{}'"""
    sres = await async_processer.query_dict_one(sql.format(sour_db_server,sour_schema,table,column))
    dres = await async_processer.query_dict_one(sql.format(desc_db_server,desc_schema,table,column))
    print('sres=',sres)
    print('dres=',dres)

    await async_processer.exec_sql('truncate table t_db_compare_detail')
    for k,v in sres.items():
        if dres is None:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                              format_sql(get_sync_sql(sres, dres))))
        elif sres[k] != dres[k]:
            await async_processer.exec_sql(
             """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                values('{}','{}','{}','{}','{}')""".format(k,sres[k],dres[k],'1',format_sql(get_sync_sql(sres,dres))))
        else:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))

    return await  async_processer.query_list("""select 
                                                     property_name,
                                                     sour_property_value,
                                                     desc_property_value,
                                                     case when status ='1' then '<span style="color:red">×</span>' 
                                                     else '<span style="color:green">√</span>' end result,
                                                     statement,
                                                     status
                                                 from t_db_compare_detail order by id""")

async def db_stru_compare_statement(sour_db_server,sour_schema,desc_db_server,desc_schema,table,column):
    sql = """SELECT   a.table_schema,
                      a.table_name,
                      a.column_name,
                      a.is_nullable,
                      a.column_type,
                      a.column_default,
                      a.column_key,
                      a.character_set_name,
                      a.collation_name,
                      a.column_comment,
                      a.extra
               FROM t_db_compare a
               WHERE  a.dsid={} 
                  and a.`table_schema`='{}' 
                  and a.`table_name`='{}' 
                  and a.`column_name`='{}'"""
    sres = await async_processer.query_dict_one(sql.format(sour_db_server,sour_schema,table,column))
    dres = await async_processer.query_dict_one(sql.format(desc_db_server,desc_schema,table,column))

    await async_processer.exec_sql('truncate table t_db_compare_detail')
    for k,v in sres.items():
        if dres is None:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                              format_sql(get_sync_sql(sres, dres))))
            break
        elif sres[k] != dres[k]:
            await async_processer.exec_sql(
             """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                values('{}','{}','{}','{}','{}')""".format(k,sres[k],dres[k],'1',format_sql(get_sync_sql(sres,dres))))
        else:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))

    return await  async_processer.query_list(
                    """select statement from t_db_compare_detail where status='1' order by id""")

async def db_stru_compare_statement_idx(sour_db_server,sour_schema,desc_db_server,desc_schema,table,index):
    sql = """SELECT     a.table_schema,
                        a.table_name,
                        a.index_name,
                        a.index_type,
                        a.is_unique,
                        a.nullable,
                        a.visible ,
                        a.column_name 
               FROM v_db_compare_idx a
               WHERE  a.dsid={} 
                  and a.`table_schema`='{}' 
                  and a.`table_name`='{}' 
                  and a.`index_name`='{}'"""
    sres = await async_processer.query_dict_one(sql.format(sour_db_server,sour_schema,table,index))
    dres = await async_processer.query_dict_one(sql.format(desc_db_server,desc_schema,table,index))
    print('sres=',sres)
    print('dres=',dres)

    await async_processer.exec_sql('truncate table t_db_compare_detail')
    for k,v in sres.items():
        if dres is None:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                              format_sql(get_sync_sql_idx(sres, dres,desc_schema))))
            break
        elif sres[k] != dres[k]:
            await async_processer.exec_sql(
             """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                values('{}','{}','{}','{}','{}')""".format(k,sres[k],dres[k],'1',format_sql(get_sync_sql_idx(sres,dres,desc_schema))))
            break
        else:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))

    return await  async_processer.query_list(
                    """select statement from t_db_compare_detail where status='1' order by id""")

async def db_stru_batch_gen_statement(sour_db_server,sour_schema,desc_db_server,desc_schema,table):
    # table
    res = await db_stru_compare(sour_db_server,sour_schema,desc_db_server,desc_schema,table)
    sql = """SELECT  a.table_schema,
                     a.table_name,
                     a.column_name,
                     a.is_nullable,
                     a.column_type,
                     a.column_default,
                     a.column_key,
                     a.character_set_name,
                     a.collation_name,
                     a.column_comment,
                     a.extra
              FROM t_db_compare a
              WHERE  a.dsid={}
                 and a.`table_schema`='{}'
                 and a.`table_name`='{}'
                 and a.`column_name`='{}'"""

    await async_processer.exec_sql('truncate table t_db_compare_detail')
    for r in res:
        sres = await async_processer.query_dict_one(sql.format(sour_db_server,r[0],r[1],r[2]))
        dres = await async_processer.query_dict_one(sql.format(desc_db_server,r[0],r[1],r[2]))
        for k,v in sres.items():
            if dres is None:
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                                  format_sql(get_sync_sql(sres, dres,desc_schema))))
                break
            elif sres.get(k) != dres.get(k):
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k,sres[k],dres[k],'1',format_sql(get_sync_sql(sres,dres))))
                break
            else:
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))
    # index
    res = await db_stru_compare_idx(sour_db_server, sour_schema, desc_db_server, desc_schema, table)
    sql = """SELECT   a.table_schema,
                      a.table_name,
                      a.index_name,
                      a.index_type,
                      a.is_unique,
                      a.nullable,
                      a.visible ,
                      a.column_name 
             FROM v_db_compare_idx a
             WHERE  a.dsid={} 
                and a.`table_schema`='{}' 
                and a.`table_name`='{}' 
                and a.`index_name`='{}'"""
    for r in res:
        sres = await async_processer.query_dict_one(sql.format(sour_db_server, r[0], r[1], r[2]))
        dres = await async_processer.query_dict_one(sql.format(desc_db_server, r[0], r[1], r[2]))
        for k, v in sres.items():
            if dres is None:
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                                  format_sql(get_sync_sql_idx(sres, dres, desc_schema))))
                break
            elif sres[k] != dres[k]:
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '1',
                                                                  format_sql(get_sync_sql_idx(sres, dres,desc_schema))))
                break
            else:
                await async_processer.exec_sql(
                    """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                       values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))


    return await  async_processer.query_dict_list("""select
                                                     property_name,
                                                     sour_property_value,
                                                     desc_property_value,
                                                     statement,
                                                     status
                                                   from t_db_compare_detail where status='1' order by id""")

async def db_stru_compare_detail_idx(sour_db_server,sour_schema,desc_db_server,desc_schema,table,index):
    sql = """SELECT  table_schema,
                     table_name,
                     index_name,
                     index_type,
                     is_unique,
                     nullable,
                     visible ,
                     column_name 
            FROM v_db_compare_idx a
            WHERE a.dsid={}
              AND a.`table_schema`='{}' 
              AND a.`table_name`='{}' 
              AND a.`index_name`='{}'"""
    sres = await async_processer.query_dict_one(sql.format(sour_db_server,sour_schema,table,index))
    dres = await async_processer.query_dict_one(sql.format(desc_db_server,desc_schema,table,index))
    print('sres_idx=',sres)
    print('dres_idx=',dres)

    await async_processer.exec_sql('truncate table t_db_compare_detail')
    for k,v in sres.items():
        if dres is None:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], '', '1',
                                                              format_sql(get_sync_sql_idx(sres, dres))))
        elif sres[k] != dres[k]:
            await async_processer.exec_sql(
             """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                values('{}','{}','{}','{}','{}')""".format(k,sres[k],dres[k],'1',format_sql(get_sync_sql_idx(sres,dres))))
        else:
            await async_processer.exec_sql(
                """insert into t_db_compare_detail(property_name,sour_property_value,desc_property_value,status,statement)
                   values('{}','{}','{}','{}','{}')""".format(k, sres[k], dres[k], '0', ''))

    return await  async_processer.query_list("""select 
                                                     property_name,
                                                     sour_property_value,
                                                     desc_property_value,
                                                     case when status ='1' then '<span style="color:red">×</span>' 
                                                     else '<span style="color:green">√</span>' end result,
                                                     statement,
                                                     status
                                                 from t_db_compare_detail order by id""")

async def get_ck_query_result(ds,sql,curdb):
    print('ds=',ds)
    if ds['proxy_status'] == '1':
       res = get_ck_proxy_result(ds, sql, curdb)
    else:
       res = await get_ck_result(ds, sql, curdb)
    return res

async def db_stru_compare_ck_data(sour_db_server,sour_schema,desc_db_server,desc_schema):
    sds = await get_ds_by_dsid_by_cdb(sour_db_server, sour_schema)
    dds = await get_ds_by_dsid_by_cdb(desc_db_server, desc_schema)
    sql = """select  lower(database) as db_name,
                     lower(name) as table_name
             from system.tables  where database='{}' order by 2 """

    if dds['db_type'] == '9':
        dres = await get_ck_query_result(dds,sql.format(desc_schema),desc_schema)
        await async_processer.exec_sql('truncate table t_db_compare_data')
        for d in dres['data']:
            rs2 = await get_ck_query_result(dds,'select count(0) as rec from `{}`.`{}`'.format(desc_schema, d[1]),desc_schema)
            try:
                rs1 = await async_processer.query_dict_one_by_ds(sds,
                        'select count(0) as rec from `{}`.`{}`'.format(sour_schema, d[1]))
            except:
                rs1 = {'rec': 0}

            st = """insert into t_db_compare_data
                              (sour_dsid,dest_dsid,sour_schema,dest_schema,dest_table,sour_rows,dest_rows) 
                             values('{}','{}','{}','{}','{}','{}','{}')
                            """.format(sour_db_server, desc_db_server,
                                       sour_schema, desc_schema,
                                       d[1], rs1['rec'], rs2['data'][0][0])
            await async_processer.exec_sql(st)

        sql = """ SELECT   
                           (select db_desc from t_db_source where id=a.sour_dsid) as sour_desc,
                           sour_schema,
                           (select db_desc from t_db_source where id=a.dest_dsid) as dest_desc,
                           dest_schema,
                           dest_table,
                           sour_rows,
                           dest_rows,
                           case when dest_rows!=sour_rows then '<span style="color:red">×</span>' 
                           else '<span style="color:green">√</span>' end result
                       FROM t_db_compare_data a order by id"""
        res = await async_processer.query_list(sql)
        return res

async def db_stru_compare_data(sour_db_server,sour_schema,desc_db_server,desc_schema):
    sds = await get_ds_by_dsid_by_cdb(sour_db_server, sour_schema)
    dds = await get_ds_by_dsid_by_cdb(desc_db_server, desc_schema)

    if dds['db_type'] == '9':
        return await db_stru_compare_ck_data(sour_db_server,sour_schema,desc_db_server,desc_schema)
    else:
        sql = """SELECT  table_schema,table_name
                     FROM information_schema.tables 
                     WHERE table_schema='{}' ORDER BY table_name"""

        dres = await async_processer.query_dict_list_by_ds(dds, sql.format(desc_schema))
        await async_processer.exec_sql('truncate table t_db_compare_data')

        for d in dres:
            rs1 = await async_processer.query_dict_one_by_ds(dds, 'select count(0) as rec from `{}`.`{}`'.format(desc_schema,d['table_name']))
            try:
              rs2 = await async_processer.query_dict_one_by_ds(sds, 'select count(0) as rec from `{}`.`{}`'.format(sour_schema, d['table_name']))
            except:
              print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
              traceback.print_exc()
              rs2 = { 'rec' :-1 }
            st = """insert into t_db_compare_data
                       (sour_dsid,dest_dsid,sour_schema,dest_schema,dest_table,sour_rows,dest_rows) 
                      values('{}','{}','{}','{}','{}','{}','{}')
                     """.format(sour_db_server, desc_db_server,
                                sour_schema, desc_schema,
                                d['table_name'], rs2['rec'],rs1['rec'])
            await async_processer.exec_sql(st)

        sql = """ SELECT   
                    (select db_desc from t_db_source where id=a.sour_dsid) as sour_desc,
                    sour_schema,
                    (select db_desc from t_db_source where id=a.dest_dsid) as dest_desc,
                    dest_schema,
                    dest_table,
                    sour_rows,
                    dest_rows,
                    case when dest_rows!=sour_rows then '<span style="color:red">×</span>' 
                    else '<span style="color:green">√</span>' end result
                FROM t_db_compare_data a order by id"""
        res = await async_processer.query_list(sql)
        return res

async def db_gen_dict(db_server,db_schema):
    ds = await get_ds_by_dsid_by_cdb(db_server, db_schema)
    st = """SELECT      
                table_name,
                column_name,
                column_type,
                is_nullable,
                column_default,
                character_set_name,
                collation_name,
                column_key,
                extra,
                CASE WHEN LENGTH(column_comment)>20 THEN
                   CONCAT(SUBSTR(column_comment,1,20),'...') 
                ELSE
                   column_comment
                    END AS column_comment
                FROM information_schema.columns 
                WHERE table_schema='{}'  ORDER BY table_name,ordinal_position""".format(db_schema)
    rs = await async_processer.query_list_by_ds(ds,st)
    return rs

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

async def exp_dict(static_path,db_server, db_schema):
    row_data  = 0
    workbook  = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('dict')
    header_styles = set_header_styles(45,1)
    os.system('cd {0}'.format(static_path + '/downloads/dict'))
    file_name   = static_path + '/downloads/dict/exp_dict_{0}.xls'.format(db_schema)
    file_name_s = 'exp_dict_{0}.xls'.format(db_schema)
    ds          = await get_ds_by_dsid_by_cdb(db_server, db_schema)
    st          = """SELECT      
                        table_name as '表名',
                        column_name as '列名',
                        column_type  as '列类型',
                        is_nullable as '是否可空',
                        column_default as '默认值',
                        character_set_name as '字符集',
                        collation_name as '校对规则',
                        column_key as '主键',
                        extra  as '附加',
                        CASE WHEN LENGTH(column_comment)>20 THEN
                           CONCAT(SUBSTR(column_comment,1,20),'...') 
                        ELSE
                           column_comment
                            END AS '注释'
                        FROM information_schema.columns 
                    WHERE table_schema='{}'  ORDER BY table_name,ordinal_position""".format(db_schema)

    # 写表头
    desc = await async_processer.query_one_desc_by_ds(ds,st)
    for k in range(len(desc)):
        worksheet.write(row_data, k, desc[k][0], header_styles)

    # 写单元格
    row_data = row_data + 1
    rs3 = await async_processer.query_list_by_ds(ds,st)
    for i in rs3:
        for j in range(len(i)):
            if i[j] is None:
                worksheet.write(row_data, j, '')
            else:
                worksheet.write(row_data, j, str(i[j]))
        row_data = row_data + 1

    workbook.save(file_name)
    print("{0} export complete!".format(file_name))

    # 生成压缩文件
    zip_file = static_path + '/downloads/dict/exp_dict_{0}.zip'.format(current_rq())
    rzip_file = '/static/downloads/dict/exp_dict_{0}.zip'.format(current_rq())

    # 若文件存在则删除
    if os.path.exists(zip_file):
        os.system('rm -f {0}'.format(zip_file))

    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    z.write(file_name, arcname=file_name_s)
    z.close()

    # 删除json文件
    os.system('rm -f {0}'.format(file_name))
    return rzip_file