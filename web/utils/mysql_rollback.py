#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/21 14:19
# @Author : ma.fei
# @File : mysql_rollback.py.py
# @Software: PyCharm

from web.utils.common import get_connection_dict
from web.utils.common import format_sql

import traceback
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.row_event import (
     DeleteRowsEvent,
     UpdateRowsEvent,
     WriteRowsEvent,
)


def format_sql(v_sql):
    return v_sql.replace("\\","\\\\").replace("'","\\'")

def get_ins_header(MYSQL_SETTINGS,event):
    v_ddl = 'insert into {0}.{1} ('.format(MYSQL_SETTINGS['db'],event['table'])
    for key in event['data']:
        v_ddl = v_ddl + '`{0}`'.format(key) + ','
    v_ddl = v_ddl[0:-1] + ')'
    return v_ddl

def get_ins_values(event):
    v_tmp=''
    for key in event['data']:
        if event['data'][key]==None:
           v_tmp=v_tmp+"null,"
        else:
           v_tmp = v_tmp + "'" + format_sql(str(event['data'][key])) + "',"
    return v_tmp[0:-1]

def get_where(p_where):
    v_where = ' where '
    for key in p_where:
        v_where = v_where+ key+' = \''+str(p_where[key]) + '\' and '
    return v_where[0:-5]

def set_column(p_data):
    v_set = ' set '
    for key in p_data:
        v_set = v_set + key + '=\''+ str(p_data[key]) + '\','
    return v_set[0:-1]

def gen_sql(MYSQL_SETTINGS,event):
    if event['action']=='insert':
        sql  = get_ins_header(MYSQL_SETTINGS,event)+ ' values ('+get_ins_values(event)+');'
        rsql = "delete from {0}.{1} {2};".format(MYSQL_SETTINGS['db'],event['table'],get_where(event['data']))
    elif event['action']=='update':
        sql  = 'update {0}.{1} {2} {3};'.\
               format(MYSQL_SETTINGS['db'],event['table'],set_column(event['after_values']),get_where(event['before_values']))
        rsql = 'update {0}.{1} {2} {3};'.\
               format(MYSQL_SETTINGS['db'],event['table'],set_column(event['before_values']),get_where(event['after_values']))
    elif event['action']=='delete':
        sql  = 'delete from {0}.{1} {2};'.format(MYSQL_SETTINGS['db'],event['table'],get_where(event['data']))
        rsql = get_ins_header(event)+ ' values ('+get_ins_values(event)+');'
    else:
       pass
    return sql,rsql

def get_binlog(p_ds,p_file,p_start_pos,p_end_pos):

    MYSQL_SETTINGS = {
        "host": p_ds['ip'],
        "port": int(p_ds['port']),
        "user": "canal2021",
        "passwd": "canal@Hopson2018",
        "db": p_ds['service']
    }

    print(MYSQL_SETTINGS)

    rollback_statments = []
    try:
        stream = BinLogStreamReader(connection_settings=MYSQL_SETTINGS,
                                    only_events=(QueryEvent, DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent),
                                    server_id=9999,
                                    blocking=True,
                                    resume_stream=True,
                                    log_file=p_file,
                                    log_pos=int(p_start_pos)
                                    )

        schema = MYSQL_SETTINGS['db']
        for binlogevent in stream:
            print('binlogeven=', binlogevent.event_type,binlogevent.packet.log_pos,binlogevent.schema)
            if binlogevent.event_type in (2,):
                event = {"schema": bytes.decode(binlogevent.schema), "query": binlogevent.query.lower()}
                if 'create' in event['query'] or 'drop' in event['query']  or 'alter' in event['query'] or 'truncate' in event['query']:
                    if event['schema'] == schema:
                        print(binlogevent.query.lower())

            if binlogevent.event_type in (30, 31, 32):
                for row in binlogevent.rows:
                    event = {"schema": binlogevent.schema, "table": binlogevent.table}

                    if event['schema'] == schema:
                        if isinstance(binlogevent, DeleteRowsEvent):
                            event["action"] = "delete"
                            event["data"] = row["values"]
                            sql,rsql = gen_sql(MYSQL_SETTINGS,event)

                        elif isinstance(binlogevent, UpdateRowsEvent):
                            event["action"] = "update"
                            event["after_values"] = row["after_values"]
                            event["before_values"] = row["before_values"]
                            sql, rsql = gen_sql(MYSQL_SETTINGS,event)

                        elif isinstance(binlogevent, WriteRowsEvent):
                            event["action"] = "insert"
                            event["data"] = row["values"]
                            sql,rsql = gen_sql(MYSQL_SETTINGS,event)

                        print('Execute :',sql)
                        print('Rollback :',rsql)
                        rollback_statments.append(rsql)

            if stream.log_pos + 31 == p_end_pos or stream.log_pos >=p_end_pos:
                #print('rollback_statements:', rollback_statments[::-1])
                stream.close()
                break

        return rollback_statments[::-1]

    except Exception as e:
        traceback.print_exc()
    finally:
        stream.close()

def write_rollback(p_sql_id,p_ds,p_file,p_start_pos,p_end_pos):
    try:
        db = get_connection_dict()
        rollback= '\n'.join(get_binlog(p_ds,p_file,p_start_pos,p_end_pos))
        print('rollback=',rollback)
        cr=db.cursor()
        cr.execute("""insert into t_sql_backup(release_id,rollback_statement) 
                        values ({},'{}')""".format(p_sql_id,format_sql(rollback)))
        db.commit()
    except:
      print('write_rollback error!!!')
      traceback.print_exc()