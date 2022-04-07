#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import re
import traceback
from web.utils.common      import aes_encrypt,aes_decrypt,get_connection_ds_pg
from web.utils.common      import get_connection_ds,get_connection_ds_sqlserver,get_connection_ds_oracle
from web.utils.mysql_async import async_processer

async def query_server(p_name):
    if p_name == "":
        sql ="""SELECT  a.id,
                        c.dmmc as server_type,
                        a.server_desc,
                        a.market_id,
                        b.dmmc as market_name,
                        a.server_ip,
                        a.server_port,
                        a.server_os,
                        CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
                    FROM t_server a,t_dmmx b,t_dmmx c
                    WHERE a.market_id=b.dmm AND b.dm='05'
                      and a.server_type=c.dmm and c.dm='06'
                    ORDER BY a.market_id,a.server_port"""
    else:
        sql = """SELECT a.id,
                        c.dmmc as server_type,
                        a.server_desc,
                        a.market_id,
                        b.dmmc as market_name,
                        a.server_ip,
                        a.server_port,
                        a.server_os,
                        CASE a.STATUS WHEN '1' THEN '启用' WHEN '0' THEN '禁用' END  STATUS
                    FROM t_server a,t_dmmx b,t_dmmx c
                    WHERE a.market_id=b.dmm AND b.dm='05'
                      and a.server_type=c.dmm and c.dm='06'
                      and binary concat(a.market_id,'|',a.server_ip,'|',a.server_port,'|',a.server_desc)  like '%{0}%' 
                    ORDER BY a.market_id,a.server_port""".format(p_name)
    return await async_processer.query_list(sql)

async def get_serverid():
    rs = await async_processer.query_one("select ifnull(max(id),0)+1 from t_server")
    return rs[0]

async def get_server_by_serverid(p_serverid):
    sql = """select cast(id as char) as server_id,
                  market_id,
                  server_type,
                  server_ip,
                  server_port,
                  server_user,
                  server_pass,
                  server_os,
                  server_cpu,
                  server_mem,
                  status,
                  server_desc
           from t_server where id={0}""".format(p_serverid)
    server = await async_processer.query_dict_one(sql)
    server['server_pass'] = await aes_decrypt(server['server_pass'], server['server_user'])
    return server

async def save_server(p_server):
    val = check_server(p_server)
    if val['code']=='-1':
        return val
    try:
        result         = {}
        market_id      = p_server['market_id']
        server_desc    = p_server['server_desc']
        server_type    = p_server['server_type']
        server_ip      = p_server['server_ip']
        server_port    = p_server['server_port']
        server_user    = p_server['server_user']
        server_pass    = await aes_encrypt(p_server['server_pass'],server_user)
        server_os      = p_server['server_os']
        server_cpu     = p_server['server_cpu']
        server_mem     = p_server['server_mem']
        status         = p_server['status']
        sql="""insert into t_server(market_id,server_desc,server_type,server_ip,server_port,server_user,server_pass,server_os,server_cpu,server_mem,status) 
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(market_id,server_desc,server_type,server_ip,server_port,server_user,server_pass,server_os,server_cpu,server_mem,status);
        await async_processer.exec_sql(sql)
        result['code']='0'
        result['message']='保存成功!'
        return result
    except:
        traceback.print_exc()
        result = {}
        result['code'] = '-1'
        result['message'] = '保存失败!'
        return result

async def upd_server(p_server):
    val = check_server(p_server)
    if  val['code'] == '-1':
        return val
    try:
        id              = p_server['server_id']
        market_id       = p_server['market_id']
        server_desc     = p_server['server_desc']
        server_type     = p_server['server_type']
        server_ip       = p_server['server_ip']
        server_port     = p_server['server_port']
        server_user     = p_server['server_user']
        server_pass     = await aes_encrypt(p_server['server_pass'], server_user)
        server_os       = p_server['server_os']
        server_cpu      = p_server['server_cpu']
        server_mem      = p_server['server_mem']
        status          = p_server['status']
        sql="""update t_server 
                  set  market_id     ='{0}', 
                       server_type   ='{1}',
                       server_ip     ='{2}' ,                        
                       server_port   ='{3}',      
                       server_user   ='{4}' ,           
                       server_pass   ='{5}' ,                           
                       server_os     ='{6}' ,           
                       server_cpu    ='{7}' , 
                       server_mem    ='{8}' ,
                       status        ='{9}' ,
                       server_desc   ='{10}'
                where id='{11}'""".format(market_id,server_type,server_ip,server_port,server_user,server_pass,
                                          server_os,server_cpu,server_mem,status,server_desc,id)
        await async_processer.exec_sql(sql)
        result={}
        result['code']='0'
        result['message']='更新成功!'
        return result
    except:
        result = {}
        result['code'] = '-1'
        result['message'] = '更新失败!'
        return result


async def del_server(p_serverid):
    try:
        await async_processer.exec_sql("delete from t_server  where id='{0}'".format(p_serverid))
        result={}
        result['code']='0'
        result['message']='删除成功！'
        return result
    except :
        result = {}
        result['code'] = '-1'
        result['message'] = '删除失败！'
        return result

def check_server(p_server):
    result = {}

    if p_server["server_desc"]=="":
        result['code']='-1'
        result['message']='服务器描述不能为空！'
        return result

    if p_server["market_id"]=="":
        result['code']='-1'
        result['message']='项目编码不能为空！'
        return result

    if p_server["server_type"]=="":
        result['code']='-1'
        result['message']='服务器类型不能为空！'
        return result

    if p_server["server_ip"]=="":
        result['code']='-1'
        result['message']='服务器地址不能为空！'
        return result
    ''' 
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", p_server["server_ip"])==None:
        result['code'] = '-1'
        result['message'] = '服务器地址不正确！'
        return result
    '''
    if p_server["server_port"] == "":
        result['code'] = '-1'
        result['message'] = '服务器口不能为空！'
        return result

    if re.match(r"^([1-9][0-9]{1,5})$",p_server["server_port"])==None:
        result['code'] = '-1'
        result['message'] = '服务器端口为2位连续数字不能以0开头！'
        return result

    if p_server["server_os"] == "":
        result['code'] = '-1'
        result['message'] = '服务器系统不能为空！'
        return result

    if re.match(r"^([a-zA-Z]{2,})",p_server["server_os"]) == None:
        result['code'] = '-1'
        result['message'] = '服务器系统必须以两位字母开头！'
        return result

    if p_server["server_user"] == "":
        result['code'] = '-1'
        result['message'] = '服务器用户不能为空！'
        return result

    if p_server["server_pass"] == "":
        result['code'] = '-1'
        result['message'] = '服务器口令不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result

async def  check_server_valid(p_id):
    result = {}
    try:
        p_ds = await get_server_by_serverid(p_id)
        if p_ds['db_type']=='0':
           get_connection_ds(p_ds)
        elif p_ds['db_type']=='1':
           get_connection_ds_oracle(p_ds)
        elif p_ds['db_type']=='2':
           get_connection_ds_sqlserver(p_ds)
        elif p_ds['db_type']=='3':
           get_connection_ds_pg(p_ds)
        result['code'] = '0'
        result['message'] = '验证通过'
        return result
    except:
        traceback.print_exc()
        result['code'] = '-1'
        result['message'] = '验证失败'
        return result
