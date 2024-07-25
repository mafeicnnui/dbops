#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/2/7 8:45
# @Author : maf.fei
# @File : mysql_async.py.py
# @Software: PyCharm

import json
import logging
import re
import datetime
from  aiomysql import create_pool,DictCursor

def read_json(file):
    with open(file, 'r') as f:
         cfg = json.loads(f.read())
    return cfg

def capital_to_lower(dict_info):
    new_dict = {}
    for i, j in dict_info.items():
        if j is None:
            new_dict[i.lower()] = ''
        else:
            new_dict[i.lower()] = j
    return new_dict

def datetime2str(dict_info):
    new_dict = {}
    for i, j in dict_info.items():
        if j is None:
            new_dict[i] = ''
        else:
            if isinstance(j, datetime.datetime):
               new_dict[i] = str(j)
            else:
               new_dict[i] = j
    return new_dict

db = read_json('./config/config.json')

class async_processer:
    async def query_list(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(list(r))
        return v_list

    async def query_list_by_ds(p_ds, p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(list(r))
        return v_list

    async def query_one(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs

    async def query_one_desc(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    desc = cur.description
        return desc

    async def query_one_by_ds(p_ds, p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs

    async def query_one_desc_by_ds(p_ds, p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    desc = cur.description
        return desc

    async def exec_sql(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)

    async def exec_ins_sql(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    id =  conn.insert_id()
        return id

    async def exec_sql_by_ds(p_ds,p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)

    async def exec_sql_by_ds_new(p_ds, p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),
                               user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=False) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
                    await cur.execute('FLUSH TABLES WITH READ LOCK')
                    await cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ')
                    await cur.execute('START TRANSACTION /*!40100 WITH CONSISTENT SNAPSHOT */')
                    await cur.execute('show master status')
                    await cur.execute('UNLOCK TABLES')
                    binlog_file, start_position = (await cur.fetchone())[0:2]
                    await cur.execute(p_sql)
                    await cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
                    await cur.execute('FLUSH TABLES WITH READ LOCK')
                    await cur.execute('show master status')
                    _, stop_position = (await cur.fetchone())[0:2]
                    await cur.execute('UNLOCK TABLES')
                await conn.commit()
        return binlog_file, start_position, stop_position

    # match execute
    async def exec_sql_by_ds_multi(p_ds,p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),
                               user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                  #await cur.fetchone()
                  for st in reReplace(p_sql):
                       print('>>>>>>>>>>>>>>>>>:::',st)
                       await cur.execute(st)
                await conn.commit()

    async def exec_sql_by_ds_multi_new(p_ds,p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),
                               user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=False) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
                    await cur.execute('FLUSH TABLES WITH READ LOCK')
                    await cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ')
                    await cur.execute('START TRANSACTION /*!40100 WITH CONSISTENT SNAPSHOT */')
                    await cur.execute('show master status')
                    binlog_file, start_position = (await cur.fetchone())[0:2]
                    await cur.execute('UNLOCK TABLES')
                    for st in reReplace(p_sql):
                       await cur.execute(st)
                    await cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
                    await cur.execute('FLUSH TABLES WITH READ LOCK')
                    await cur.execute('show master status')
                    _, stop_position = (await cur.fetchone())[0:2]
                    await cur.execute('UNLOCK TABLES')
                await conn.commit()
        return binlog_file, start_position, stop_position

        # match execute

    async def exec_sql_by_ds_batch(p_ds, p_sql,p_data):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),
                               user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                     await cur.executemany(p_sql,p_data)
                await conn.commit()

    async def query_dict_list(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(capital_to_lower(r))
        return v_list

    async def query_dict_list_by_ds(p_ds, p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(capital_to_lower(r))
        return v_list

    async def query_dict_one(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        if rs is not None:
           return capital_to_lower(rs)
        else:
           return None

    async def query_dict_one2(p_sql):
        async with create_pool(host=db['db_ip'], port=int(db['db_port']), user=db['db_user'], password=db['db_pass'],
                               db=db['db_service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        if rs is not None:
            return datetime2str(capital_to_lower(rs))
        else:
            return None

    async def query_dict_one_by_ds(p_ds,p_sql):
        async with create_pool(host=p_ds['ip'], port=int(p_ds['port']), user=p_ds['user'], password=p_ds['password'],
                               db=p_ds['service'], autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return capital_to_lower(rs)

def preProcesses(matched):
    value = matched.group(0)
    return value.replace(';','^^^')

def preProcesses2(matched):
    value = matched.group(0)
    return value.replace(';',',')

def reReplace(p_sql):
    p_sql_pre=p_sql
    pattern1 = re.compile(r'(COMMENT\s+\'[^\']*;[^\']*\')')
    if pattern1.findall(p_sql) != []:
       logging.info('一: 将comment中的;替换为^^^ ...')
       p_sql_pre = re.sub(pattern1,preProcesses,p_sql)
       logging.info(('1:',str(p_sql_pre)))

    pattern2 = re.compile(r'(\s*\)\s*;\s*)')
    if pattern2.findall(p_sql_pre)!=[]:
       logging.info('二: 将);替换为)$$$ ...')
       p_sql_pre = re.sub(pattern2, ')$$$', p_sql_pre)
       logging.info(('2:', str(p_sql_pre)))

    pattern3 = re.compile(r'(\s*\'\s*;\s*)')
    if pattern3.findall(p_sql_pre) != []:
       logging.info('三: 将\';替换为\'$$$ ...')
       p_sql_pre = re.sub(pattern3, "'$$$", p_sql_pre)
       logging.info(('3:', str(p_sql_pre)))

    pattern4 = re.compile(r'(comment\s*\'.*;.*\')')
    if pattern4.findall(p_sql_pre) != []:
       logging.info('四: 将comment中的;替换为, ...')
       p_sql_pre = re.sub(pattern4, preProcesses2, p_sql_pre)
       logging.info(('4:', str(p_sql_pre)))

    pattern5 = re.compile(r'(\s*;\s*)')
    if pattern5.findall(p_sql_pre) != []:
        logging.info('五: 将;替换为$$$')
        p_sql_pre = re.sub(pattern5, "$$$\n", p_sql_pre)
        logging.info(('5:', str(p_sql_pre)))

    logging.info('六: 通过$$$将p_sql_pre处理为列表...')
    p_sql_pre = [i for i in p_sql_pre.split('$$$') if (i != '' and i!='\n')]
    logging.info(('6=', str(p_sql_pre)))
    logging.info(('6-len=', len(p_sql_pre)))

    logging.info(('七: 将列表中每个语句comment中的^^^替为;...'))
    p_sql_pre = [i.replace('^^^', ';') for i in p_sql_pre]
    logging.info(('7=', str(p_sql_pre)))
    logging.info(('7-len=', len(p_sql_pre)))

    if len(p_sql_pre) == 1:
       return [p_sql]
    else:
       return  p_sql_pre