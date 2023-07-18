#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/10/18 14:21
# @Author : ma.fei
# @File : t_es.py.py
# @Software: PyCharm

import json
import traceback
from elasticsearch import Elasticsearch
from web.model.t_ds   import get_ds_by_dsid

def get_ds_es(p_ip,p_port):
    conn = Elasticsearch([p_ip],port=p_port)
    return conn

def get_ds_es_auth(p_ip,p_port,p_user,p_pass):
    conn = Elasticsearch(
        ["{}:{}".format(p_ip, p_port)],
        http_auth=(p_user, p_pass),
        sniff_on_start=False,
        sniff_on_connection_fail=False,
        sniffer_timeout=None)
    return conn

def get_ds_es_auth_https(p_ip,p_port,p_user,p_pass):
    conn = Elasticsearch(
        ["https://{}:{}".format(p_ip,p_port)],
        http_auth=(p_user,p_pass),
        sniff_on_start=False,
        sniff_on_connection_fail=False,
        sniffer_timeout=None)
    return conn

async def get_indexes(p_dbid):
    try:
        ds = await get_ds_by_dsid(p_dbid)
        if ds['password']!='':
            es = get_ds_es_auth_https(ds['ip'], ds['port'], ds['user'], ds['password'])
        else:
            es = get_ds_es(ds['ip'], ds['port'])
        #idx = [i for i in es.indices.get_aliases().keys() if i[0] != '.']
        idx = [i for i in es.indices.get_alias("*").keys() if i[0] != '.']
        print('idx=', idx, type(idx))
        return {'code':0,'data':idx,'message':''}
    except:
        traceback.print_exc()
        return {'code':-1,'data':[],'message':traceback.format_exc()}

async def query_es(p_dbid,p_idx_name,p_idx_doc,p_body):
    try:
        ds = await  get_ds_by_dsid(p_dbid)
        if ds['password'] != '':
            es = get_ds_es_auth_https(ds['ip'], ds['port'], ds['user'], ds['password'])
        else:
            es = get_ds_es(ds['ip'], ds['port'])
        #res = es.search(index=p_idx_name,doc_type="_doc",body=json.loads(p_body),size=200)
        res = es.search(index=p_idx_name, doc_type=p_idx_doc, body=json.loads(p_body), size=200)
        return {'code':0,'data':res,'message':''}
    except:
        traceback.print_exc()
        return {'code':-1,'data':[],'message':traceback.format_exc()}

async def query_es_mapping(p_dbid,p_idx_name):
    try:
        ds = await  get_ds_by_dsid(p_dbid)
        if ds['password'] != '':
            es = get_ds_es_auth_https(ds['ip'], ds['port'], ds['user'], ds['password'])
        else:
            es = get_ds_es(ds['ip'], ds['port'])
        res = es.indices.get_mapping(index=p_idx_name)
        return {'code':0,'data':res,'message':''}
    except:
        traceback.print_exc()
        return {'code':-1,'data':[],'message':traceback.format_exc()}