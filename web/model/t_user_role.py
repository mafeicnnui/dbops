#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.mysql_async import async_processer

async def get_roles_by_userid(p_userid):
    sql="select cast(role_id as char) as role_id from t_user_role where user_id={0}".format(p_userid)
    return async_processer.query_list(sql)

async def save_user_role(p_userid,p_roles):
    result = {}
    try:
        for role in range(len(p_roles)):
            sql="insert into t_user_role(user_id,role_id) values({0},{1})".format(p_userid,p_roles[role])
            await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_user_role(p_userid,p_roles):
    try:
        await del_user_roles(p_userid);
        await save_user_role(p_userid,p_roles)
        return {'code': '0', 'message': '更新成功!'}
    except :
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_user_roles(p_userid):
    try:
        sql = "delete from t_user_role where user_id='{0}'".format(p_userid)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}