#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/2/7 8:45
# @Author : maf.fei
# @File : mysql_async.py.py
# @Software: PyCharm

import json

from  aiomysql import create_pool,DictCursor,connect

def read_json(file):
    with open(file, 'r') as f:
         cfg = json.loads(f.read())
    return cfg

db = read_json('./config/config.json')

async def query_list(p_sql):
    print('query_list=',p_sql)
    async with create_pool(host=db['db_ip'], port=int(db['db_port']),user=db['db_user'], password=db['db_pass'],db=db['db_service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(p_sql)
                v_list = []
                rs = await cur.fetchall()
                for r in rs:
                    v_list.append(list(r))
    return v_list

async def query_one(p_sql):
    print('query_one=',p_sql)
    async with create_pool(host=db['db_ip'], port=int(db['db_port']),user=db['db_user'], password=db['db_pass'],db=db['db_service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(p_sql)
                rs = await cur.fetchone()
                print('rs=',rs)
    return rs

async def query_one_by_ds(p_ds,p_sql):
    print('query_one_by_ds=',p_sql)
    async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),user=p_ds['user'], password=p_ds['password'],db=p_ds['service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(p_sql)
                rs = await cur.fetchone()
                print('rs=',rs)
    return rs

async def exec_sql(p_sql):
    print('exec_sql=',p_sql)
    async with create_pool(host=db['db_ip'], port=int(db['db_port']),user=db['db_user'], password=db['db_pass'],db=db['db_service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(p_sql)


async def query_dict_list(p_sql):
    print('query_list=',p_sql)
    async with create_pool(host=db['db_ip'], port=int(db['db_port']),user=db['db_user'], password=db['db_pass'],db=db['db_service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(p_sql)
                v_list = []
                rs = await cur.fetchall()
                for r in rs:
                    v_list.append(list(r))
    return v_list

async def query_dict_list_by_ds(p_ds,p_sql):
    print('p_ds=', p_ds)
    print('query_list=',p_sql)
    async with create_pool(host=p_ds['ip'], port=int(p_ds['port']),user=p_ds['user'], password=p_ds['password'],db=p_ds['service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(p_sql)
                v_list = []
                rs = await cur.fetchall()
                for r in rs:
                    v_list.append(r)
    return v_list


async def query_dict_one(p_sql):
    print('query_one_dict=',p_sql)
    async with create_pool(host=db['db_ip'], port=int(db['db_port']),user=db['db_user'], password=db['db_pass'],db=db['db_service'], autocommit=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(p_sql)
                rs = await cur.fetchone()
    return rs


class async_processer:
    __connection    = None
    __connection_ds = None
    __config        = read_json('./config/config.json')

    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_ds = None

    @staticmethod
    async def get_connection():
        if async_processer.__connection == None:
            conn = await connect(
                    host       = async_processer.__config['db_ip'],
                    port       = int(async_processer.__config['db_port']),
                    user       = async_processer.__config['db_user'],
                    password   = async_processer.__config['db_pass'],
                    db         = async_processer.__config['db_service'],
                    autocommit = True)
            if conn:
                async_processer.__connection = conn
                return conn
            else:
                raise ("create mysql connect error! ")
        else:
            return async_processer.__connection

    @staticmethod
    async def get_connection_ds(p_ds):
        if async_processer.__connection_ds == None:
            conn = await connect(
                    host       = p_ds['ip'],
                    port       = int(p_ds['port']),
                    user       = p_ds['user'],
                    password   = p_ds['password'],
                    db         = p_ds['service'],
                    autocommit = True)
            if conn:
                async_processer.__connection_ds = conn
                return conn
            else:
                raise ("create mysql ds connect error! ")
        else:
            return async_processer.__connection_ds


    async def query_list(self,p_sql):
        self.cursor = await self.connection.cursor()
        await self.connection.ping()
        await self.cursor.execute(p_sql)
        v_list = []
        rs = await self.cursor.fetchall()
        for r in rs:
            v_list.append(list(r))
        return v_list

    async def query_one(self,p_sql):
        self.cursor = await self.connection.cursor()
        await self.connection.ping()
        await self.cursor.execute(p_sql)
        rs = await self.cursor.fetchone()
        return rs


    async def query_one_by_ds(self,p_ds, p_sql):
        self.cursor = await self.connection.cursor()
        await self.connection.ping()
        await self.cursor.execute(p_sql)
        rs = await self.cursor.fetchone()
        return rs


        async with async_processer.get_pool_by_ds(p_ds) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
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
                        v_list.append(list(r))
        return v_list

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

    async def query_dict_one(p_sql):
        async with async_processer.pool as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(p_sql)
                    rs = await cur.fetchone()
        return rs
