#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import traceback

from web.utils.common import format_sql,aes_encrypt,aes_decrypt
from web.model.t_db_inst import get_ds_by_instid
from web.utils.mysql_async import async_processer

async def query_db_user(p_user_name,p_inst_env,p_inst_id):
    v_where =''
    if p_user_name != '':
       v_where = "  and  b.db_user like '%{0}%'".format(p_user_name)
    if p_inst_env != '':
       v_where = "  and  a.inst_env= '{0}'".format(p_inst_env)
    if p_inst_id != '':
       v_where = "  and  a.id= '{0}'".format(p_inst_id)
    sql = """SELECT  a.id,a.inst_name,
                     (select dmmc from t_dmmx x where x.dm='02' and x.dmm=a.inst_type) as inst_type,
                     (select dmmc from t_dmmx x where x.dm='03' and x.dmm=a.inst_env) as inst_env,
                     b.id,b.db_user,
                     (select dmmc from t_dmmx x where x.dm='25' and x.dmm=b.status) as STATUS,
                     b.description,date_format(b.created_date,'%Y-%m-%d %h:%i:%s')  as created_date
            FROM  t_db_inst a,t_db_user b
            where  a.id=b.inst_id {0}""".format(v_where)
    print(sql)
    return await async_processer.query_list(sql)

async def save_db_user(d_db_user):
    val = check_db_user(d_db_user,'I')
    if val['code']=='-1':
        return val
    try:
        if d_db_user['db_pass'] != '':
            db_pass    = aes_encrypt(d_db_user['db_pass'], d_db_user['db_user'].replace("'","''"))
        else:
            db_pass    = d_db_user['db_pass']
        sql="""insert into t_db_user(inst_id,db_user,db_pass,user_dbs,user_privs,statement,status,description,created_date)
                    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',now())
            """.format(d_db_user['inst_id'],d_db_user['db_user'].replace("'","''"),db_pass,
                       d_db_user['user_dbs'],d_db_user['user_privs'],
                       format_sql(d_db_user['statement']),d_db_user['status'],format_sql(d_db_user['desc']))
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}

async def update_db_user(d_db_user):
    val = check_db_user(d_db_user,'U')
    if val['code']=='-1':
        return val
    try:
        if d_db_user['db_pass'] != '':
            db_pass = aes_encrypt(d_db_user['db_pass'], d_db_user['db_user'].replace("'","''"))
        else:
            db_pass = d_db_user['db_pass']
        sql="""update t_db_user
                  set  inst_id='{}',db_user='{}',db_pass='{}',user_dbs='{}',user_privs='{}',statement='{}',status='{}',description='{}',last_update_date=now() where id={}
                  """.format(d_db_user['inst_id'],d_db_user['db_user'].replace("'","''"),db_pass,
                             d_db_user['user_dbs'],d_db_user['user_privs'],format_sql(d_db_user['statement']),
                             d_db_user['status'],format_sql(d_db_user['desc']),d_db_user['user_id'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def delete_db_user(p_db_user_id):
    try:
        sql     = "delete from t_db_user where id='{}'".format(p_db_user_id)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


def get_user_sql(p_db_user):
    v_priv = ''
    v_user = """create user {} identified by '***';""".format(p_db_user['mysql_db_user'])
    if p_db_user['mysql_privs']=='':
       return v_user
    for db in p_db_user['mysql_dbs'].split(','):
        v_priv=v_priv+'grant {} on `{}`.* to {};\n'.format(p_db_user['mysql_privs'],db,p_db_user['mysql_db_user'])
    return v_user+'\n'+v_priv[0:-1]

async def get_db_name(p_instid):
    try:
        ds   = get_ds_by_instid(p_instid)
        st   = """SELECT schema_name FROM information_schema.`SCHEMATA` 
                   WHERE schema_name NOT IN('information_schema','mysql','performance_schema') ORDER BY schema_name"""
        return {'code':'0','message':await async_processer.query_list_by_ds(ds,st)}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '获取数据库名失败!'}


async def del_db_user(p_db_userid):
    try:
        sql="delete from t_db_user  where id='{0}'".format(p_db_userid)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}

async def check_db_user_rep(p_db_user):
    sql = "select count(0) from t_db_user  where  concat(inst_id,db_user)='{0}{1}'".format(p_db_user["inst_id"],format_sql(p_db_user['db_user']))
    rs  = await async_processer.query_one(sql)
    return rs[0]

def check_db_user(p_db_user,p_flag='I'):
    result = {}
    if p_db_user["inst_id"]=="":
        result['code']='-1'
        result['message']='实例名不能为空!'
        return result
    if p_db_user["db_user"] == "":
        result['code'] = '-1'
        result['message'] = '用户名不能为空!'
        return result
    if p_db_user["db_pass"]=="":
        result['code']='-1'
        result['message']='口令不能为空!'
        return result
    if p_db_user["statement"]=="":
        result['code']='-1'
        result['message'] ='创建语句不能为空!'
        return result
    if p_db_user["status"] == "":
        result['code'] = '-1'
        result['message'] = '用户状态不能为空!'
        return result
    if p_db_user["desc"] == "":
        result['code'] = '-1'
        result['message'] = '用户描述不能为空!'
        return result
    if check_db_user_rep(p_db_user)>0 and p_flag=='I':
        result['code'] = '-1'
        result['message'] = '用户名重复!'
        return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result

async def get_user_privs_zh(p_user_privs):
    st = "SELECT dmmc FROM t_dmmx WHERE dm='31' and instr('{}',dmm)>0".format(p_user_privs)
    v =''
    for p in await async_processer.query_dict_list(st):
       v=v+p['dmmc']+','
    return v[0:-1]

async def query_user_by_id(p_user_id):
    st = """SELECT a.id,
                    a.inst_id,
                    a.description,
                    a.db_user,
                    a.db_pass,
                    a.user_dbs,
                    a.user_privs,
                    a.statement,
                    a.status,
                    date_format(a.created_date,'%Y-%m-%d %H:%i:%s')  as created_date
             FROM t_db_user a  WHERE  a.id='{0}'""".format(p_user_id)
    rs = await async_processer.query_dict_one(st)
    rs['db_pass'] = await aes_decrypt(rs['db_pass'],rs['db_user'].replace("'", "''"))
    rs['user_privs_zh'] = await get_user_privs_zh(rs['user_privs'])
    return rs

async def get_port_by_portid(p_portid):
    st = """select  id,app_name,app_port,app_dev,app_desc,app_ext from t_port where id={0}""".format(p_portid)
    return await async_processer.query_dict_one(st)