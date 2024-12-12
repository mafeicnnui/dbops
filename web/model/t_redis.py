#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/10/18 14:21
# @Author : ma.fei
# @File : t_es.py.py
# @Software: PyCharm

'''
1.单key查询，例：card:detail:129
2.支持一次查询多个key,key间用逗号隔开，例：card:detail:129,card:detail:130,card:receive:rule:128
3.目前只支持key类型为string,set,hash,list
'''

import traceback

from redis import StrictRedis

from web.model.t_ds import get_ds_by_dsid


def get_ds_redis(p_ip, p_port, p_password, p_db):
    if p_password is not None:
        if p_db is not None:
            conn = StrictRedis(host=p_ip, port=p_port, password=p_password, db=p_db, encoding='utf8',
                               decode_responses=True)
        else:
            conn = StrictRedis(host=p_ip, port=p_port, password=p_password, encoding='utf8', decode_responses=True)
    else:
        if p_db is not None:
            conn = StrictRedis(host=p_ip, port=p_port, encoding='utf8', db=p_db, decode_responses=True)
        else:
            conn = StrictRedis(host=p_ip, port=p_port, encoding='utf8', decode_responses=True)
    return conn


async def get_redis_db(p_dbid):
    try:
        ds = await get_ds_by_dsid(p_dbid)
        redis = get_ds_redis(ds['ip'], ds['port'], ds['password'], p_dbid)
        info = redis.info()
        db_names = [k for k in info.keys() if k[0:2] == 'db']
        return {'code': 0, 'data': db_names, 'message': ''}
    except:
        traceback.print_exc()
        return {'code': -1, 'data': [], 'message': traceback.format_exc()}


async def query_redis(p_dbid, p_db_name, p_key_name):
    try:
        ds = await  get_ds_by_dsid(p_dbid)
        print(p_db_name, p_db_name.replace('db', ''))
        redis = get_ds_redis(ds['ip'], ds['port'], ds['password'], p_db_name.replace('db', ''))
        res = []
        for k in p_key_name.split(','):
            typ = redis.type(k)
            if typ == 'string':
                res.append({'key': k, 'type': typ, 'value': redis.get(k)})
            elif typ == 'hash':
                res.append({'key': k, 'type': typ, 'value': redis.hgetall(k)})
            elif typ == 'set':
                res.append({'key': k, 'type': typ, 'value': redis.getset(k)})
            elif typ == 'list':
                res.append({'key': k, 'type': typ, 'value': redis.getrange(0, 1000)})
        print('query_redis=', res)
        return {'code': 0, 'data': res, 'message': ''}
    except:
        traceback.print_exc()
        return {'code': -1, 'data': [], 'message': traceback.format_exc()}


async def query_redis_keys(p_dbid, p_db_name, p_key_name):
    try:
        ds = await  get_ds_by_dsid(p_dbid)
        print(p_db_name, p_db_name.replace('db', ''))
        redis = get_ds_redis(ds['ip'], ds['port'], ds['password'], p_db_name.replace('db', ''))
        keyname = p_key_name.split(' ')[1].replace('"', '').replace("'", '').strip()
        res = redis.keys(keyname)
        return {'code': 0, 'data': res, 'message': ''}
    except:
        traceback.print_exc()
        return {'code': -1, 'data': [], 'message': traceback.format_exc()}
