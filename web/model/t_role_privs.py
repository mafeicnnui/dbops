#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

from web.utils.common import current_rq
from web.utils.mysql_async import async_processer


async def get_privs_by_userid(p_roleid):
    st="select priv_id from t_user_role where role_id={0}".format(p_roleid)
    return await async_processer.query_list(st)

async def save_role_privs(p_role_id,p_privs):
    try:
        for id in p_privs:
          st="""insert into t_role_privs(role_id,priv_id,creation_date,creator,last_update_date,updator) 
                 values({0},'{1}','{2}','{3}','{4}','{5}')""".format(p_role_id,id,current_rq(),'DBA',current_rq(),'DBA')
          await async_processer.exec_sql(st)
        return {'code':'0','message':'保存成功!'}
    except:
        return {'code': '-1', 'message': '保存失败!'}


async def save_role_func_privs(p_role_id,p_privs):
    try:
        for id in p_privs:
          st="""insert into t_role_func_privs(role_id,func_id,creation_date,creator,last_update_date,updator) 
                 values({0},'{1}','{2}','{3}','{4}','{5}')""".format(p_role_id,id,current_rq(),'DBA',current_rq(),'DBA')
          await async_processer.exec_sql(st)
        return {'code': '0', 'message': '保存成功!'}
    except:
        return {'code': '-1', 'message': '保存失败!'}


async def upd_role_privs(p_role_id,p_privs_id):
    try:
        await del_role_privs(p_role_id)
        await save_role_privs(p_role_id,p_privs_id)
        return {'code': '0', 'message': '更新成功!'}
    except :
        return {'code': '-1', 'message': '更新失败!'}


async def upd_role_func_privs(p_role_id,p_privs_id):
    try:
        await del_role_func_privs(p_role_id)
        await save_role_func_privs(p_role_id,p_privs_id)
        return {'code': '0', 'message': '更新成功!'}
    except :
        return {'code': '-1', 'message': '更新失败!'}

async def del_role_privs(p_roleid):
    try:
        st = "delete from t_role_privs where role_id={0}".format(p_roleid)
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '删除成功!'}
    except:
        return {'code': '0', 'message': '删除失败!'}


async def del_role_func_privs(p_roleid):
    try:
        st = "delete from t_role_func_privs where role_id={0}".format(p_roleid);
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '删除成功!'}
    except:
        return {'code': '0', 'message': '删除失败!'}
