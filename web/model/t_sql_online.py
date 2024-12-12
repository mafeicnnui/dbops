#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/12/22 9:36
# @Author : ma.fei
# @File : t_sql_online.py.py
# @Software: PyCharm

import re

from web.model.t_ds import get_ds_by_dsid
from web.utils.common import format_sql, format_exception
from web.utils.mysql_async import async_processer, reReplace


def get_obj_type(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("VIEW") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("EVENT") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("DATABASE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("VIEW") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("FUNCTION") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("INDEX") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("EVENT") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TRIGGER") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("DATABASE") > 0:
        obj = re.split(r'\s+', p_sql)[1].replace('`', '')
        if ('(') in obj:
            return obj.split('(')[0].upper()
        else:
            return obj.upper()
    else:
        return ''


def get_obj_op(p_sql):
    if re.split(r'\s+', p_sql)[0].upper() in ('CREATE', 'DROP') and re.split(r'\s+', p_sql)[1].upper() in (
    'TABLE', 'INDEX', 'DATABASE'):
        return re.split(r'\s+', p_sql)[0].upper() + '_' + re.split(r'\s+', p_sql)[1].upper()
    if re.split(r'\s+', p_sql)[0].upper() in ('TRUNCATE'):
        return 'TRUNCATE_TABLE'
    if re.split(r'\s+', p_sql)[0].upper() == 'ALTER' and re.split(r'\s+', p_sql)[1].upper() == 'TABLE' and \
            re.split(r'\s+', p_sql)[3].upper() in ('ADD', 'DROP', 'MODIFY'):
        return re.split(r'\s+', p_sql)[0].upper() + '_' + re.split(r'\s+', p_sql)[1].upper() + '_' + \
            re.split(r'\s+', p_sql)[3].upper()
    if re.split(r'\s+', p_sql)[0].upper() in ('INSERT', 'UPDATE', 'DELETE'):
        return re.split(r'\s+', p_sql)[0].upper()


def get_obj_name(p_sql):
    if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("TRUNCATE") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("ALTER") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("TABLE") > 0 \
            or p_sql.upper().count("DROP") > 0 and p_sql.upper().count("DATABASE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("VIEW") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("FUNCTION") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("PROCEDURE") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("TRIGGER") > 0 \
            or p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("DATABASE") > 0:

        if p_sql.upper().count("CREATE") > 0 and p_sql.upper().count("INDEX") > 0 and p_sql.upper().count("UNIQUE") > 0:
            obj = re.split(r'\s+', p_sql)[3].replace('`', '')
        else:
            obj = re.split(r'\s+', p_sql)[2].replace('`', '')

        if ('(') in obj:
            if obj.find('.') < 0:
                return obj.split('(')[0]
            else:
                return obj.split('(')[0].split('.')[1]
        else:
            return obj

    print('op>>>>>', get_obj_op(p_sql))

    if get_obj_op(p_sql) in ('INSERT', 'DELETE'):
        if re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip().replace('`', '').find('.') < 0:
            return re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()
        else:
            return re.split(r'\s+', p_sql.strip())[2].split('(')[0].strip()

    if get_obj_op(p_sql) in ('UPDATE'):
        if re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip().replace('`', '').find('.') < 0:
            return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip()
        else:
            return re.split(r'\s+', p_sql.strip())[1].split('(')[0].strip()


async def f_get_table_ddl(p_ds, db, tb):
    sql = """show create table {}.{}""".format(db, tb)
    rs = await async_processer.query_one_by_ds(p_ds, sql)
    return rs[1]


async def check_mysql_tab_exists(ds, db, tb):
    sql = """select count(0) from information_schema.tables 
            where table_schema='{}' and table_name='{}'""".format(db, tb)
    rs = await async_processer.query_one_by_ds(ds, sql)
    return rs[0]


def process_result(v):
    if isinstance(v, tuple):
        if len(v) == 1:
            return str(v)
        else:
            return 'code:{0},error:{1}'.format(str(v[0]), str(v[1]))
    else:
        return str(v)


async def get_obj_exists_auto_incr_not_1_multi(p_ds, op, db, tb, cfg):
    res = {'code': 0, 'msg': 'success'}
    try:
        dp = 'drop table {}'
        st = ['''SELECT  count(0)
                 FROM  information_schema.tables   
                WHERE UPPER(table_schema)=upper('{}')
                  AND UPPER(table_name)=upper('{}')
                  and AUTO_INCREMENT IS NULL''',

              '''SELECT  count(0)
                       FROM  information_schema.tables   
                      WHERE UPPER(table_schema)=upper('{}')
                        AND UPPER(table_name)=upper('{}')
                        and AUTO_INCREMENT=1''']
        if op == 'CREATE_TABLE':
            rs = await async_processer.query_one_by_ds(p_ds, st[0].format(db, tb))
            if rs[0] == 1:
                return res
            else:
                rs = await async_processer.query_one_by_ds(p_ds, st[1].format(db, tb))
                cfg[db + '.' + tb] = dp.format(db + '.' + tb)
                if rs[0] == 0:
                    return {'code': -1, 'msg': '表:{}.{}自增ID不为1!'.format(db, tb)}
                else:
                    return res
    except Exception as e:
        return {'code': -1, 'msg': format_sql(format_exception(str(e)))}


async def get_obj_privs_grammar_multi(p_ds, p_sql, op, db, tb, cfg):
    res = {'code': 0, 'msg': 'success'}
    try:
        dp = 'drop table {}'
        if op == 'CREATE_TABLE':
            if await check_mysql_tab_exists(p_ds, db, tb) > 0:
                return {'code': -1, 'msg': '表:{}.{}已存在!'.format(db, tb)}
            else:
                await async_processer.exec_sql_by_ds(p_ds, p_sql)
                cfg[db + '.' + tb] = dp.format(db + '.' + tb)
        elif op in ('ALTER_TABLE_ADD', 'ALTER_TABLE_DROP'):
            td = await f_get_table_ddl(p_ds, db, tb)
            if cfg.get(db + '.' + tb) is None:
                if await check_mysql_tab_exists(p_ds, db, tb) == 0:
                    return {'code': -1, 'msg': '表:{}.{}不存在!'.format(db, tb)}
                else:
                    await async_processer.exec_sql_by_ds(p_ds, td.replace(tb, db + '.' + 'online_' + tb))
                    await async_processer.exec_sql_by_ds(p_ds, p_sql.replace(tb, db + '.' + 'online_' + tb))
                    cfg[db + '.' + 'online_' + tb] = dp.format(db + '.' + tb)
        return res
    except Exception as e:
        return {'code': -1, 'msg': format_sql(format_exception(str(e)))}


async def check_online_ddl(p_dbid, p_sql):
    cfg = {}
    res = []
    ds = await get_ds_by_dsid(p_dbid)
    for s in reReplace(p_sql.replace("\\", "\\\\")):
        ob = get_obj_name(s.strip())
        op = get_obj_op(s.strip())
        tp = get_obj_type(s.strip())
        st = s.strip()

        if st.strip() == '':
            continue

        if ob.find('.') < 0:
            if len(res) > 0:
                for o in res:
                    if o['obj'] != ob:
                        res.append({'obj': ob, 'msg': '对象名`{}`不含库名!'.format(ob)})
                        continue
            else:
                res.append({'obj': ob, 'msg': '对象名`{}`不含库名!'.format(ob)})
                continue
        else:
            db = ob.split('.')[0]
            tb = ob.split('.')[1]

        if tp == 'TABLE':
            print('检测DDL语法及权限...')
            v = await get_obj_privs_grammar_multi(ds, st, op, db, tb, cfg)
            print('v=', v)
            if v['code'] == -1:
                res.append(v)

        if op == 'CREATE_TABLE':
            print('强制自增列初始值为1...')
            if tp == 'TABLE' and (st.upper().count('PRIMARY') > 0 and st.upper().count('KEY') > 0):
                v = await get_obj_exists_auto_incr_not_1_multi(ds, op, db, tb, cfg)
                if v['code'] == -1:
                    res.append(v)

    print('删除临时表...')
    for k, v in cfg.items():
        print('drop table {}'.format(k))
        await async_processer.exec_sql_by_ds(ds, v)

    if len(res) > 0:
        return {'code': False, 'msg': res}
    else:
        return {'code': True, 'msg': 'success'}


async def check_online_dml(p_sql):
    res = []
    for s in reReplace(p_sql.replace("\\", "\\\\")):
        ob = get_obj_name(s.strip())
        print('check_online_dml ob=', ob)
        if s.strip() == '':
            continue

        if ob.find('.') < 0:
            if len(res) > 0:
                for o in res:
                    if o['obj'] != ob:
                        res.append({'obj': ob, 'msg': '对象名`{}`不含库名!'.format(ob)})
            else:
                res.append({'obj': ob, 'msg': '对象名`{}`不含库名!'.format(ob)})

    if len(res) > 0:
        return {'code': False, 'msg': res}
    else:
        return {'code': True, 'msg': 'success'}


async def check_online(p_dbid, p_type, p_sql):
    if p_type == '1':
        return await check_online_ddl(p_dbid, p_sql)

    if p_type == '2':
        return await check_online_dml(p_sql)
