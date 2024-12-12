#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

from web.model.t_role_privs import save_role_privs, upd_role_privs, del_role_privs, save_role_func_privs, \
    upd_role_func_privs
from web.utils.common import current_rq
from web.utils.mysql_async import async_processer


async def query_role(p_name):
    if p_name == "":
        sql = """select id,name,
                     case status when '1' then '是' when '0' then '否' end  status,
                     creator,date_format(creation_date,'%Y-%m-%d')    creation_date,
                     updator,date_format(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_role
                 order by name""".format(p_name)
    else:
        sql = """select id,name,
                     case status when '1' then '是' when '0' then '否' end  status,
                     creator,date_format(creation_date,'%Y-%m-%d')    creation_date,
                     updator,date_format(last_update_date,'%Y-%m-%d') last_update_date 
                 from t_role 
                where binary name like '%{0}%'              
                 order by name""".format(p_name)
    return await async_processer.query_list(sql)


async def get_roleid():
    sql = "select ifnull(max(id),0)+1 from t_role"
    rs = await async_processer.query_one(sql)
    return rs[0]


async def get_role_by_roleid(p_roleid):
    sql = "select cast(id as char) as roleid,name,status,creation_date,creator,last_update_date,updator from t_role where id={0}".format(
        p_roleid)
    return await async_processer.query_dict_one(sql)


async def get_roles():
    sql = "select cast(id as char) as id,name from t_role where status='1'"
    return await async_processer.query_list(sql)


async def if_exists_role(p_name):
    sql = "select count(0) from t_role where upper(name)='{0}'".format(p_name.upper())
    rs = await async_processer.query_one(sql)
    if rs[0] == 0:
        return False
    else:
        return True


async def is_dba(p_user):
    sql = """SELECT COUNT(0)
              FROM t_role
             WHERE STATUS='1'
               AND id  in (SELECT role_id FROM t_user_role WHERE user_id='{0}')
                AND name='数据库管理员'""".format(p_user['userid'])
    rs = await async_processer.query_one(sql)
    if rs[0] == 0:
        return False;
    else:
        return True


async def save_role(p_role):
    result = {}
    val = await check_role(p_role)
    if val['code'] == '-1':
        return val
    try:
        role_id = await get_roleid()
        role_name = p_role['name']
        status = p_role['status']
        privs = p_role['privs']
        func_privs = p_role['func_privs']
        sql = """insert into t_role(id,name,status,creation_date,creator,last_update_date,updator) 
                values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
            """.format(role_id, role_name, status, current_rq(), 'DBA', current_rq(), 'DBA')
        await async_processer.exec_sql(sql)
        await save_role_privs(role_id, privs)
        await save_role_func_privs(role_id, func_privs)
        result = {}
        result['code'] = '0'
        result['message'] = '保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


async def upd_role(p_role):
    result = {}
    try:
        roleid = p_role['roleid']
        rolename = p_role['name']
        status = p_role['status']
        privs = p_role['privs']
        func_privs = p_role['func_privs']
        sql = """update t_role 
                  set  name    ='{0}',                      
                       status  ='{1}' ,
                       last_update_date ='{2}' ,
                       updator='{3}'
                where id='{4}'""".format(rolename, status, current_rq(), 'DBA', roleid)

        await async_processer.exec_sql(sql)
        await upd_role_privs(roleid, privs)
        await upd_role_func_privs(roleid, func_privs)
        result = {}
        result['code'] = '0'
        result['message'] = '更新成功！'
    except:
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


async def del_role(roleid):
    result = {}
    try:
        sql = "delete from t_role  where id='{0}'".format(roleid)
        print(sql)
        await async_processer.exec_sql(sql)
        await del_role_privs(roleid)
        result = {}
        result['code'] = '0'
        result['message'] = '删除成功！'
    except:
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result


async def check_role(p_role):
    result = {}
    if p_role["name"] == "":
        result['code'] = '-1'
        result['message'] = '角色名不能为空！'
        return result

    if await if_exists_role(p_role["name"]):
        result['code'] = '-1'
        result['message'] = '角色名已存在！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result
