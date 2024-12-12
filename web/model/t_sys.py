#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/30 16:30
# @Author : ma.fei
# @File : t_sys.py.py
# @Software: PyCharm

import traceback

from web.utils.common import format_sql
from web.utils.mysql_async import async_processer


def check_rule(rule):
    for key in rule:
        result = {}
        result['code'] = '0'
        result['message'] = '检测成功！'
        if key == 'switch_char_max_len':
            try:
                int(rule[key])
            except:
                result['code'] = '-1'
                result['message'] = '字符字段最大长度不是整数!'
                return result
    return result


def check_code(code):
    result = {}
    if code["type_name"] == "":
        result['code'] = '-1'
        result['message'] = '类型名称不能为空！'
        return result
    if code["type_code"] == "":
        result['code'] = '-1'
        result['message'] = '类型代码不能为空！'
        return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result


def check_setting(code):
    result = {}
    if code["key"] == "":
        result['code'] = '-1'
        result['message'] = '键名不能为空！'
        return result
    if code["value"] == "":
        result['code'] = '-1'
        result['message'] = '键值不能为空！'
        return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result


async def save_audit_rule(rule):
    result = check_rule(rule)
    if result['code'] == '-1':
        return result
    try:
        for key in rule:
            sql = "update t_sql_audit_rule set rule_value='{}' where rule_code='{}'".format(rule[key], key)
            await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def save_sys_code_type(code):
    result = check_code(code)
    if result['code'] == '-1':
        return result
    try:
        sql = "insert into t_dmlx(dm,mc,flag,create_time,update_time) values('{}','{}','{}',now(),now())".format(
            code['type_code'], code['type_name'], code['type_status'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_sys_code_type(code):
    result = check_code(code)
    if result['code'] == '-1':
        return result
    try:
        sql = """update t_dmlx set  mc ='{}',flag = '{}',update_time=now() where   dm  = '{}'""".format(
            code['type_name'], code['type_status'], code['type_code'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_sys_code(code):
    try:
        rs = await async_processer.query_one("select count(0) from t_dmmx where dm='{}'".format(code))
        if rs[0] > 0:
            return {'code': '-1', 'message': '存在代码明细数据不能删除!'}
        sql = "delete from t_dmlx where dm  = '{}'".format(code)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


async def save_sys_code_detail(code):
    try:
        sql = "insert into t_dmmx(dm,dmm,dmmc,dmmc2,flag,create_time,update_time) values('{}','{}','{}','{}','{}',now(),now())" \
            .format(code['type_code'], format_sql(code['detail_code']), code['detail_name'], code['detail_desc'],
                    code['detail_status'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '保存成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_sys_code_detail(code):
    try:
        sql = """update t_dmmx 
                   set dmm ='{}',
                       dmmc ='{}',
                       dmmc2 ='{}',
                       flag = '{}',
                       update_time=now()
                where   dm  = '{}' and dmm='{}'
             """.format(code['detail_code'], code['detail_name'], code['detail_desc'], code['detail_status'],
                        code['type_code'], format_sql(code['detail_code_old']))
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_sys_code_detail(code, detail):
    try:
        sql = "delete from t_dmmx where dm  = '{}' and dmm='{}'".format(code, detail)
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}


async def query_dm(p_code):
    v_where = ' '
    if p_code != '':
        v_where = " where  (a.dm like '%{0}%' or a.mc like '%{1}%')".format(p_code, p_code, p_code, p_code)
    sql = """SELECT a.dm, a.mc,
                  case a.flag when '1' then '启用'  when '0' then '禁用' end  as flag,
                  date_format(a.create_time,'%Y-%m-%d %H:%i:%s')  as  create_time,
                  date_format(a.update_time,'%Y-%m-%d %H:%i:%s')  as  update_time
             FROM t_dmlx a {0} ORDER BY a.dm,a.create_time """.format(v_where)
    return await async_processer.query_list(sql)


async def query_dm_detail(p_code):
    v_where = ' '
    if p_code != '':
        v_where = "  and (b.dm='{0}' or b.dmm='{1}' or a.mc  like '%{2}%')".format(p_code, p_code, p_code)
    sql = """SELECT a.dm,a.mc,
                  substr(b.dmm,1,20) as dmm,
                  substr(b.dmmc,1,50) as dmmc,
                  b.dmmc2,
                  case b.flag when '1' then '启用'  when '0' then '禁用' end  as flag,
                  date_format(b.create_time,'%Y-%m-%d %H:%i:%s')  as  create_time,
                  date_format(b.update_time,'%Y-%m-%d %H:%i:%s')  as  update_time
             FROM t_dmlx a,t_dmmx b
             where  a.dm=b.dm  {0} ORDER BY b.dm,b.dmm,a.create_time
          """.format(v_where)
    return await async_processer.query_list(sql)


async def query_rule():
    sql = "SELECT rule_code,rule_value FROM t_sql_audit_rule"
    v_dict = {}
    for r in await async_processer.query_list(sql):
        v_dict[r[0]] = r[1]
    return v_dict


async def query_settings(p_code):
    v_where = ' '
    if p_code != '':
        v_where = " where  (a.key like '%{0}%' or a.value like '%{1}%')".format(p_code, p_code, p_code, p_code)
    sql = """SELECT a.key, a.value,a.desc,
                  CASE a.status WHEN '1' THEN '启用'  WHEN '0' THEN '禁用' END  AS flag,
                  DATE_FORMAT(a.create_time,'%Y-%m-%d %H:%i:%s')  AS  create_time,
                  DATE_FORMAT(a.update_time,'%Y-%m-%d %H:%i:%s')  AS  update_time
                FROM t_sys_settings a {} ORDER BY a.key,a.create_time""".format(v_where)
    return await async_processer.query_list(sql)


async def save_sys_setting(code):
    result = check_setting(code)
    if result['code'] == '-1':
        return result
    try:
        st = """insert into t_sys_settings(`key`,`value`,`desc`,`status`,create_time,update_time) 
                values('{}','{}','{}','{}',now(),now())""".format(code['key'], code['value'], code['desc'],
                                                                  code['status'])
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': '-1', 'message': '保存失败!'}


async def upd_sys_setting(code):
    result = check_setting(code)
    if result['code'] == '-1':
        return result
    try:
        st = """update t_sys_settings set  
                   `value`='{}',
                   `desc` ='{}',
                   `status` = '{}',
                   update_time=now() 
                where  `key` ='{}'""".format(code['value'], code['desc'], code['status'], code['key'])
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}


async def del_sys_setting(key):
    try:
        rs = await async_processer.query_one("select count(0) from t_sys_settings where `key`='{}'".format(key))
        if rs[0] == 0:
            return {'code': '-1', 'message': '键名:`{}`不存在!'}
        st = "delete from t_sys_settings where `key`  = '{}'".format(key)
        await async_processer.exec_sql(st)
        return {'code': '0', 'message': '删除成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '删除失败!'}
