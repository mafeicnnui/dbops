#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/2/7 8:45
# @Author : maf.fei
# @File : mysql_async.py.py
# @Software: PyCharm

import asyncio
from  aiomysql import create_pool,DictCursor,connect
from functools import partial

db  = {
    "db_ip"        : "10.2.39.17",
    "db_port"      : "23306",
    "db_user"      : "puppet",
    "db_pass"      : "Puppet@123",
    "db_service"   : "puppet",
    "db_charset"   : "utf8"
}

class async_processer:

    pool = create_pool(host=db['db_ip'],
                       port=int(db['db_port']),
                       user=db['db_user'],
                       password=db['db_pass'],
                       db=db['db_service'],
                       autocommit=True)

    def  get_pool_by_ds(p_ds):
         pool = create_pool(host=p_ds['ip'],
                            port=int(p_ds['port']),
                            user=p_ds['user'],
                            password=p_ds['password'],
                            db=p_ds['service'],
                            autocommit=True)
         return pool

    async def query_list(p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(list(r))
        return v_list

    async def query_one(p_sql):
        async with create_pool(host=db['db_ip'],
                               port=int(db['db_port']),
                               user=db['db_user'],
                               password=db['db_pass'],
                               db=db['db_service'],
                               autocommit=True) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs

    async def query_dict_one(p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs

    async def exec_sql(p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)

    async def query_dict_list(p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(r)
        return v_list

    async def query_one_by_ds(p_ds, p_sql):
        async with async_processer.get_pool_by_ds(p_ds) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs

    async def query_dict_list_by_ds(p_ds, p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    v_list = []
                    rs = await cur.fetchall()
                    for r in rs:
                        v_list.append(r)
        return v_list

class async_processer2:

    __connection    = None
    __config        = db

    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_ds = None

    @staticmethod
    async def get_connection():
        if async_processer2.__connection == None:
            conn = await connect(
                    host       = async_processer2.__config['db_ip'],
                    port       = int(async_processer2.__config['db_port']),
                    user       = async_processer2.__config['db_user'],
                    password   = async_processer2.__config['db_pass'],
                    db         = async_processer2.__config['db_service'],
                    autocommit = True)
            if conn:
                async_processer.__connection = conn
                return conn
            else:
                raise ("create mysql connect error! ")
        else:
            return async_processer.__connection

    async def execute(self):
       cr = await async_processer2.get_connection()

async def query_list():
      rs = await async_processer.query_list("select * from t_user")
      return rs

async def query_one():
    rs = await async_processer.query_one("select * from t_user where id=138")
    print('await complete!')
    return rs

def callback(url,future):
    print(url)
    print('send mail success!')

async def query_dict_one(loop):
    task2 = loop.create_task(async_processer.query_dict_one("select * from t_user where id=138"))
    rs = await task2
    for key in rs:
       print(key,'=',rs[key])

async def query_dict_list(loop):
    task1 = loop.create_task(async_processer.query_dict_list("select * from t_user"))
    rs = await task1
    for i in rs:
        print(i)

if __name__ == '__main__':
    import time
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(query_list())
    #loop.run_until_complete(query_dict_list())
    loop.run_until_complete(query_one())
    time.sleep(1)
    loop.run_until_complete(query_one())
    # loop.run_until_complete(query_dict_one(loop))
    # tasks = [query_one() for i in range(10)]
    # print(tasks)

    # get_furture = asyncio.ensure_future(query_one())
    # loop.run_until_complete(get_furture)
    # print(get_furture.result())

    # task = loop.create_task(query_one())
    # task.add_done_callback(partial(callback,"www.baidu.com"))
    # loop.run_until_complete(task)
    # print(task.result())
