#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/14 14:02
# @Author : ma.fei
# @File : t_db_tools.py.py
# @Software: PyCharm

from web.model.t_ds import get_ds_by_dsid_by_cdb
from web.utils.common import format_sql
from web.utils.mysql_async import async_processer


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