#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/10 10:56
# @Author : ma.fei
# @File : mysql_sync.py.py
# @Software: PyCharm
import os
import pymysql
import json


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
    def __init__(self):
        self.db = read_json(os.path.join(os.path.dirname(__file__)) + '/../../config/config.json')
        self.conn = pymysql.connect(host=self.db['db_ip'],
                                    port=int(self.db['db_port']),
                                    user=self.db['db_user'],
                                    passwd=self.db['db_pass'],
                                    db=self.db['db_service'],
                                    charset=self.db['db_charset'],
                                    autocommit=False)
        print('mysqlManager.__init__ =>self.db:', self.db)
        print('mysqlManager.__init__ =>self.conn:', self.conn)
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
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class mysqlDictManager:
    def __init__(self):
        self.db = read_json(os.path.join(os.path.dirname(__file__)) + '/../../config/config.json')

        self.conn = pymysql.connect(host=self.db['db_ip'],
                                    port=int(self.db['db_port']),
                                    user=self.db['db_user'],
                                    passwd=self.db['db_pass'],
                                    db=self.db['db_service'],
                                    charset=self.db['db_charset'],
                                    autocommit=False,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        print('mysqlDictManager.__init__ =>self.db:', self.db)
        print('mysqlDictManager.__init__ =>self.conn:', self.conn)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exe_type, exe_val, exe_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class mysqlDsDictManager:
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


db = read_json(os.path.join(os.path.dirname(__file__)) + '/../../config/config.json')


class sync_processer:

    def exec_sql(p_sql):
        with mysqlManager() as cur:
            print('cur=', cur)
            cur.execute(p_sql)

    def exec_sql_by_ds(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            print('cur2=', cur)
            cur.execute(p_sql)

    def query_one(p_sql):
        with mysqlManager() as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return rs

    def query_one_by_ds(p_ds, p_sql):
        with mysqlDsManager(p_ds) as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return rs

    def query_list(p_sql):
        with mysqlManager() as cur:
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
        with mysqlDictManager() as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return capital_to_lower(rs)

    def query_dict_list(p_sql):
        with mysqlDictManager() as cur:
            cur.execute(p_sql)
            v_list = []
            rs = cur.fetchall()
            for r in rs:
                v_list.append(capital_to_lower(r))
        return v_list

    def query_dict_one_by_ds(p_ds, p_sql):
        with mysqlDsDictManager(p_ds) as cur:
            cur.execute(p_sql)
            rs = cur.fetchone()
        return capital_to_lower(rs)

    def query_dict_list_by_ds(p_ds, p_sql):
        with mysqlDsDictManager(p_ds) as cur:
            cur.execute(p_sql)
            v_list = []
            rs = cur.fetchall()
            for r in rs:
                v_list.append(capital_to_lower(r))
        return v_list
