#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/21 14:19
# @Author : ma.fei
# @File : mysql_rollback.py.py
# @Software: PyCharm

import json
import logging
import traceback

import pymysql
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.row_event import (DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent, )

from web.model.t_sql_check import get_obj_name
from web.utils.common import format_sql
from web.utils.common import get_connection


def get_db(MYSQL_SETTINGS):
    conn = pymysql.connect(host=MYSQL_SETTINGS['host'],
                           port=int(MYSQL_SETTINGS['port']),
                           user=MYSQL_SETTINGS['user'],
                           passwd=MYSQL_SETTINGS['passwd'],
                           db=MYSQL_SETTINGS['db'],
                           charset='utf8', autocommit=True)
    return conn


def format_sql(v_sql):
    return v_sql.replace("\\", "\\\\").replace("'", "\\'")


def get_ins_header(MYSQL_SETTINGS, event):
    v_ddl = 'insert into {0}.{1} ('.format(MYSQL_SETTINGS['db'], event['table'])
    for key in event['data']:
        v_ddl = v_ddl + '`{0}`'.format(key) + ','
    v_ddl = v_ddl[0:-1] + ')'
    return v_ddl


def get_ins_values(event):
    v_tmp = ''
    for key in event['data']:
        if event['data'][key] == None:
            v_tmp = v_tmp + "null,"
        else:
            v_tmp = v_tmp + "'" + format_sql(str(event['data'][key])) + "',"
    return v_tmp[0:-1]


def get_where(MYSQL_SETTINGS, event, p_where):
    db = get_db(MYSQL_SETTINGS)
    cols = get_table_pk_names(db, MYSQL_SETTINGS['db'], event['table'])
    v_where = ' where '
    for key in p_where:
        if check_tab_exists_pk(db, MYSQL_SETTINGS['db'], event['table']) > 0:
            if key in cols:
                v_where = v_where + key + ' = \'' + str(p_where[key]) + '\' and '
        elif p_where[key] is None:
            print('p_key=', key)
            print('p_where[{}]={}', key, p_where[key])
            v_where = v_where + key + ' is NULL and '
        else:
            v_where = v_where + key + ' = \'' + str(p_where[key]) + '\' and '
    return v_where[0:-5]


def set_column(p_data):
    v_set = ' set '
    for key in p_data:
        if p_data[key] is None:
            v_set = v_set + key + '=null,'
        else:
            v_set = v_set + key + '=\'' + str(p_data[key]) + '\','
    return v_set[0:-1]


def gen_sql(MYSQL_SETTINGS, event):
    if event['action'] == 'insert':
        sql = get_ins_header(MYSQL_SETTINGS, event) + ' values (' + get_ins_values(event) + ');'
        rsql = "delete from {0}.{1} {2};".format(MYSQL_SETTINGS['db'], event['table'],
                                                 get_where(MYSQL_SETTINGS, event, event['data']))
    elif event['action'] == 'update':
        sql = 'update {0}.{1} {2} {3};'. \
            format(MYSQL_SETTINGS['db'], event['table'], set_column(event['after_values']),
                   get_where(MYSQL_SETTINGS, event, event['before_values']))
        rsql = 'update {0}.{1} {2} {3};'. \
            format(MYSQL_SETTINGS['db'], event['table'], set_column(event['before_values']),
                   get_where(MYSQL_SETTINGS, event, event['after_values']))
    elif event['action'] == 'delete':
        sql = 'delete from {0}.{1} {2};'.format(MYSQL_SETTINGS['db'], event['table'],
                                                get_where(MYSQL_SETTINGS, event, event['data']))
        rsql = get_ins_header(MYSQL_SETTINGS, event) + ' values (' + get_ins_values(event) + ');'
    else:
        pass
    return sql, rsql


def gen_ddl_sql(p_ddl):
    if p_ddl.find('create table') >= 0:
        tab = get_obj_name(p_ddl)
        rsql = 'drop table {};'.format(tab)
        return rsql
    return p_ddl


def get_wkno(p_id):
    from web.utils.mysql_sync import sync_processer
    sql = "select * from t_sql_release where id={}".format(p_id)
    return sync_processer.query_dict_one(sql)


def get_binlog(p_ds, p_file, p_start_pos, p_end_pos, p_sql_id):
    wk = get_wkno(p_sql_id)
    print('wk=', wk)
    db = get_connection()
    cr = db.cursor()
    if p_start_pos == p_end_pos:
        return

    MYSQL_SETTINGS = {
        "host": p_ds['ip'],
        "port": int(p_ds['port']),
        # "user": "canal2021",
        # "passwd": "canal@Hopson2018",
        "user": p_ds['user'],
        "passwd": p_ds['password'],
        "db": p_ds['service']
    }
    logging.info("MYSQL_SETTINGS=", MYSQL_SETTINGS)

    insEvent = 0
    updEvent = 0
    delEvent = 0
    result = {}
    message = {}
    try:
        stream = BinLogStreamReader(connection_settings=MYSQL_SETTINGS,
                                    only_events=(QueryEvent, DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent),
                                    server_id=9999,
                                    blocking=True,
                                    resume_stream=True,
                                    log_file=p_file,
                                    log_pos=int(p_start_pos))

        schema = MYSQL_SETTINGS['db']
        for binlogevent in stream:
            if binlogevent.event_type in (2,):
                event = {"schema": bytes.decode(binlogevent.schema), "query": binlogevent.query.lower()}
                if ('create' in event['query'] or 'drop' in event['query'] \
                       or 'alter' in event['query'] or 'truncate' in  event['query']):
                    event['table'] = get_obj_name(binlogevent.query.lower())
                    if event['schema'] == wk['db'] and wk['sqltext'].count(event['table']) > 0:
                        if result.get(event['schema'] + '.' + event['table']) is None:
                            result[event['schema'] + '.' + event['table']] = {}

                        if 'create' in event['query']:
                            cr.execute(
                              """insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')"""
                                 .format(p_sql_id, format_sql(gen_ddl_sql(binlogevent.query.lower() + ';'))))
                        # else:
                        #     cr.execute(
                        #         """insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')"""
                        #         .format(p_sql_id, format_sql(binlogevent.query.lower() + ';')))

                            result[event['schema'] + '.' + event['table']]['ddlEvent'] \
                                = result[event['schema'] + '.' + event['table']].get('ddlEvent', 0) + 1


            if isinstance(binlogevent, DeleteRowsEvent) or \
                    isinstance(binlogevent, UpdateRowsEvent) or \
                    isinstance(binlogevent, WriteRowsEvent):
                for row in binlogevent.rows:
                    event = {"schema": binlogevent.schema, "table": binlogevent.table}

                    if event['schema'] == wk['db'] and wk['sqltext'].count(event['table']) > 0:
                        if result.get(event['schema'] + '.' + event['table']) is None:
                            result[event['schema'] + '.' + event['table']] = {}

                        if isinstance(binlogevent, DeleteRowsEvent):
                            event["action"] = "delete"
                            event["data"] = row["values"]
                            sql, rsql = gen_sql(MYSQL_SETTINGS, event)
                            cr.execute(
                                """insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')""".format(
                                    p_sql_id, format_sql(rsql)))
                            result[event['schema'] + '.' + event['table']]['delEvent'] \
                                = result[event['schema'] + '.' + event['table']].get('delEvent', 0) + 1

                        elif isinstance(binlogevent, UpdateRowsEvent):
                            event["action"] = "update"
                            event["after_values"] = row["after_values"]
                            event["before_values"] = row["before_values"]
                            sql, rsql = gen_sql(MYSQL_SETTINGS, event)
                            cr.execute(
                                """insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')""".format(
                                    p_sql_id, format_sql(rsql)))
                            result[event['schema'] + '.' + event['table']]['updEvent'] \
                                = result[event['schema'] + '.' + event['table']].get('updEvent', 0) + 1

                        elif isinstance(binlogevent, WriteRowsEvent):
                            event["action"] = "insert"
                            event["data"] = row["values"]
                            sql, rsql = gen_sql(MYSQL_SETTINGS, event)
                            cr.execute(
                                """insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')""".format(
                                    p_sql_id, format_sql(rsql)))
                            result[event['schema'] + '.' + event['table']]['insEvent'] \
                                = result[event['schema'] + '.' + event['table']].get('insEvent', 0) + 1

                        message[event['schema'] + '.' + event['table']] = {
                            'insert': result[event['schema'] + '.' + event['table']].get('insEvent', 0),
                            'update': result[event['schema'] + '.' + event['table']].get('updEvent', 0),
                            'delete': result[event['schema'] + '.' + event['table']].get('delEvent', 0),
                            'create': result[event['schema'] + '.' + event['table']].get('ddlEvent', 0)
                        }

            if stream.log_pos + 31 == p_end_pos or stream.log_pos >= p_end_pos:
                db.commit()
                stream.close()
                break

        return message

    except Exception as e:
        traceback.print_exc()
    finally:
        stream.close()


def check_tab_exists_pk(db_conn, db_name, tab_name):
    cr = db_conn.cursor()
    st = """select count(0) from information_schema.columns
              where table_schema='{}' and table_name='{}' and column_key='PRI'""".format(db_name, tab_name)
    cr.execute(st)
    rs = cr.fetchone()
    cr.close()
    return rs[0]


def get_table_pk_names(db_conn, db_name, tab_name):
    cr = db_conn.cursor()
    v_col = []
    v_sql = """select column_name 
              from information_schema.columns
              where table_schema='{}'
                and table_name='{}' and column_key='PRI' order by ordinal_position
          """.format(db_name, tab_name)
    cr.execute(v_sql)
    rs = cr.fetchall()
    for i in list(rs):
        v_col.append(i[0])
    cr.close()
    return v_col


def write_rollback_old(p_sql_id, p_ds, p_file, p_start_pos, p_end_pos):
    try:
        db = get_connection()
        rollback = '\n'.join(get_binlog(p_ds, p_file, p_start_pos, p_end_pos))
        logging.info(('rollback statement:', rollback))
        cr = db.cursor()
        cr.execute("delete from t_sql_backup where release_id={}".format(p_sql_id))
        cr.execute("""insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')""".format(p_sql_id,
                                                                                                         format_sql(
                                                                                                             rollback)))
        db.commit()
        return format_sql(rollback)
    except:
        logging.error('write_rollback error:', traceback.format_exc())
        traceback.print_exc()
        return None


def write_rollback_old0215(p_sql_id, p_ds, p_file, p_start_pos, p_end_pos):
    try:
        db = get_connection()
        cr = db.cursor()
        cr.execute("delete from t_sql_backup where release_id={}".format(p_sql_id))
        for r in get_binlog(p_ds, p_file, p_start_pos, p_end_pos):
            print('>>>>>:', r)
            cr.execute("""insert into t_sql_backup(release_id,rollback_statement) values ({},'{}')""".format(p_sql_id,
                                                                                                             format_sql(
                                                                                                                 r)))
        db.commit()
    except:
        logging.error('write_rollback error:', traceback.format_exc())
        traceback.print_exc()


def write_rollback(p_sql_id, p_ds, p_file, p_start_pos, p_end_pos):
    try:
        db = get_connection()
        cr = db.cursor()
        cr.execute("delete from t_sql_backup where release_id={}".format(p_sql_id))
        db.commit()
        print('write rollback log for sqlid:{},please wait!'.format(p_sql_id))
        res = get_binlog(p_ds, p_file, p_start_pos, p_end_pos, p_sql_id)
        print('write rollback log for sqlid:{} end!'.format(p_sql_id))
        cr.execute("update t_sql_release set run_result ='{}' where id={}".format(json.dumps(res), p_sql_id))
        print("update t_sql_release set run_result ='{}' where id={}".format(json.dumps(res), p_sql_id))
        db.commit()
    except:
        logging.error('write_rollback error:', traceback.format_exc())
        traceback.print_exc()


def delete_rollback(p_sql_id):
    try:
        db = get_connection()
        cr = db.cursor()
        cr.execute("delete from t_sql_backup where release_id={}".format(p_sql_id))
        db.commit()
    except:
        print('delete_rollback error!!!')
        traceback.print_exc()
