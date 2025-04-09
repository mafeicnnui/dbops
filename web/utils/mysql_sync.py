#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/10 10:56
# @Author : ma.fei
# @File : mysql_sync.py.py
# @Software: PyCharm

import json

import pymysql

from web.utils.mysql_async import reReplace


def read_json(file):
    with open(file, 'r') as f:
        cfg = json.loads(f.read())
    return cfg


def capital_to_lower(dict_info):
    new_dict = {}
    for i, j in dict_info.items():
        if j is None:
            new_dict[i.lower()] = ''
        else:
            new_dict[i.lower()] = j
    return new_dict


class mysqlManager:
    def __init__(self, db):
        self.conn = pymysql.connect(host=db['db_ip'],
                                    port=int(db['db_port']),
                                    user=db['db_user'],
                                    passwd=db['db_pass'],
                                    db=db['db_service'],
                                    charset=db['db_charset'],
                                    autocommit=False)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exe_type, exe_val, exe_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class mysqlDsManager:
    def __init__(self, db):
        self.conn = pymysql.connect(host=db['ip'],
                                    port=int(db['port']),
                                    user=db['user'],
                                    passwd=db['password'],
                                    db=db['service'],
                                    charset='utf8',
                                    autocommit=False)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exe_type, exe_val, exe_tb):
        if exe_type is None and exe_val is None and exe_tb is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()



class mysqlDictManager:
    def __init__(self, db):
        self.conn = pymysql.connect(host=db['db_ip'],
                                    port=int(db['db_port']),
                                    user=db['db_user'],
                                    passwd=db['db_pass'],
                                    db=db['db_service'],
                                    charset=db['db_charset'],
                                    autocommit=False,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exe_type, exe_val, exe_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


db = read_json('./config/config.json')


class sync_processer:

    def exec_sql(p_sql):
        with mysqlManager(db) as cur:
            cur.execute(p_sql)

    def exec_sql_by_ds(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            cur.execute(p_sql)

    def exec_sql_by_ds_multi(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            for st in reReplace(p_sql):
                cur.execute(st)

    def exec_sql_by_ds_new(p_ds, p_sql):
        print('exec_sql_by_ds_new....')
        with mysqlDsManager(p_ds) as cur:
            cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
            cur.execute('FLUSH TABLES WITH READ LOCK')
            cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ')
            cur.execute('START TRANSACTION /*!40100 WITH CONSISTENT SNAPSHOT */')
            cur.execute('show master status')
            binlog_file, start_position = cur.fetchone()[0:2]
            cur.execute('UNLOCK TABLES')
            cur.execute(p_sql)
            cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
            cur.execute('FLUSH TABLES WITH READ LOCK')
            cur.execute('show master status')
            _, stop_position = cur.fetchone()[0:2]
            cur.execute('UNLOCK TABLES')
        print('exec_sql_by_ds_new....ok')
        return binlog_file, start_position, stop_position

    def exec_sql_by_ds_multi_new(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
            cur.execute('FLUSH TABLES WITH READ LOCK')
            cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ')
            cur.execute('START TRANSACTION /*!40100 WITH CONSISTENT SNAPSHOT */')
            cur.execute('show master status')
            binlog_file, start_position = cur.fetchone()[0:2]
            cur.execute('UNLOCK TABLES')
            for st in reReplace(p_sql):
                cur.execute(st)
            cur.execute('FLUSH /*!40101 LOCAL */ TABLES')
            cur.execute('FLUSH TABLES WITH READ LOCK')
            cur.execute('show master status')
            _, stop_position = cur.fetchone()[0:2]
            cur.execute('UNLOCK TABLES')
        return binlog_file, start_position, stop_position

    def query_one(p_sql):
        with mysqlManager(db) as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return rs

    def query_one_by_ds(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return rs

    def query_list(p_sql):
        with mysqlManager(db) as cur:
            cur.execute(p_sql)
            v_list = []
            rs = cur.fetchall()
            for r in rs:
                v_list.append(list(r))
        return v_list

    def query_list_by_ds(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            cur.execute(p_sql)
            v_list = []
            rs = cur.fetchall()
            for r in rs:
                v_list.append(list(r))
        return v_list

    def query_dict_one(p_sql):
        with mysqlDictManager(db) as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return capital_to_lower(rs)

    def query_dict_list(p_sql):
        with mysqlDictManager(db) as cur:
            cur.execute(p_sql)
            v_list = []
            rs = cur.fetchall()
            for r in rs:
                v_list.append(capital_to_lower(r))
        return v_list
