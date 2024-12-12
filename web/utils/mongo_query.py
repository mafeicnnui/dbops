#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/10/24 17:06
# @Author : ma.fei
# @File : mongo_query.py
# @Software: PyCharm

import json
import pickle
import re

import pymongo
from bson.objectid import ObjectId

config = {
    'ip': '10.2.39.41',
    'port': '27016',
    'db': 'hopsonone_park'
}


def repl_str1(matched):
    value = matched.group()
    return value.replace('ISODate(', '').replace(')', '')


def repl_str2(matched):
    value = matched.group()
    return """datetime.datetime.strptime({}, "%Y-%m-%d %H:%M:%S")""".format(value)


class mongo_client:

    def __init__(self, ip, port, auth_db=None, db=None, user=None, password=None):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.auth_db = auth_db
        self.db = db
        self.client, self.conn = self.get_db()
        self.where = None
        self.limit = None
        self.columns = None
        self.collection_name = None
        self.find_string = None
        self.find_contents = None

    def __repr__(self):
        return '''
    mongo_query attribute:
    --------------------------------
        ip:{}
        port:{}
        user:{}
        password:{}
        db:{}
        conn:{}
        client:{}
    --------------------------------
    '''.format(self.ip,
               self.port,
               '' if self.user is None else self.user,
               '' if self.password is None else self.password,
               self.db,
               self.conn,
               self.client
               )

    def get_db(self):
        conn = pymongo.MongoClient('mongodb://{0}:{1}/'.format(self.ip, int(self.port)))
        if self.auth_db is not None and self.auth_db != '':
            db = conn[self.auth_db]
            if self.user is not None and self.user != '' and self.password is not None and self.password != '':
                db.authenticate(self.user, self.password)
                return conn, conn[self.db]
            else:
                return conn, [self.db]
        else:
            return conn, conn[self.db]

    def get_databases(self):
        return self.client.list_database_names()

    def get_collections(self, p_db):
        return self.client[p_db].list_collection_names()

    def get_collection_name(self, p_sql):
        pattern1 = re.compile(r'(db\..*\.)', re.I)
        pattern2 = re.compile(r'(db.getCollection\([\',\"].*[\',\"]\))', re.I)
        if pattern1.findall(p_sql) != [] and pattern2.findall(p_sql) == []:
            self.collection_name = pattern1.findall(p_sql)[0].split('.')[1]

        if pattern2.findall(p_sql) != []:
            self.collection_name = pattern2.findall(p_sql)[0].split('(')[1].split(')')[0].replace("'", '').replace('"',
                                                                                                                   '')

    def get_limits(self, p_sql):
        if p_sql.find('.limit') >= 0:
            self.limit = p_sql.split('.limit(')[1].split(')')[0]

    def find_by_where(self, p_query):
        print('p_query=', p_query)
        self.get_collection_name(p_query)
        print('get_collection_name=', self.collection_name)
        self.get_where(p_query)
        print('where=', self.where, type(self.where))
        print('column=', self.columns, type(self.columns))
        self.get_limits(p_query)
        print('limit=', self.limit)

        if self.limit is not None:
            if self.columns is not None:
                print(' limit not & columns not  ')
                rs = self.conn[self.collection_name].find(self.where, self.columns).limit(int(self.limit))
                # rs = self.client[self.db][self.collection_name].find(self.where, self.columns).limit(int(self.limit))
            else:
                print('limit not  & columns null ')
                rs = self.conn[self.collection_name].find(self.where).limit(int(self.limit))
                # rs = self.client[self.db][self.collection_name].find(self.where).limit(int(self.limit))
        else:
            if self.columns is not None:
                print('limit null  & columns not ')
                rs = self.conn[self.collection_name].find(self.where, self.columns)
                # rs = self.client[self.db][self.collection_name].find(self.where, self.columns)
            else:
                print('limit null  & columns null ')
                rs = self.conn[self.collection_name].find(self.where)
                # rs = self.client[self.db][self.collection_name].find(self.where)
        # print('-----------------------------------')
        res = []
        for r in rs:
            r['_id'] = str(r['_id'])
            res.append(r)
            # print(r)
        return res

    def get_where(self, p_sql):
        # resolve find contents
        pattern = re.compile(r'(find\(.*\))', re.I)
        if pattern.findall(p_sql) != []:
            self.find_string = pattern.findall(p_sql)[0].split('.limit')[0].strip()
            print('find_string=', self.find_string)
            t = re.split(r'find\s*\(', self.find_string, flags=re.I)
            self.find_contents = t[1][0:-1]
            print('find_contents=', self.find_contents)
        else:
            raise Exception('`find` keyword not found!')

        # resolve _id,only support $in operator
        if self.find_contents.find('_id') >= 0:
            # pattern = re.compile(r'(\}\s*,\s*\{)', re.I)
            # if pattern.findall(self.find_contents) == []:
            #     id = self.find_contents.split('ObjectId(')[1].split(')')[0].replace('"', '')
            #     self.where = {'_id': ObjectId(id)}
            #     return

            if self.find_contents.count('$in') == 0:
                print('$in = 0 && _id...')
                id = self.find_contents.split('ObjectId(')[1].split(')')[0].replace('"', '')
                pattern = re.compile(r'(\}\s*,\s*\{)', re.I)
                if pattern.findall(self.find_contents) != []:
                    t = re.split(r'(\}\s*,\s*\{)', self.find_contents, flags=re.I)
                    c = '{' + t[2][0:-1]
                    self.where = {'_id': ObjectId(id)}
                    self.columns = json.loads(c)
                    return

            elif self.find_contents.count('$in') == 1:
                print('$in = 1 && _id...')
                t = re.split(r'(\$in\s*:\s*)', self.find_string, flags=re.I)
                objd = t[2].split('[')[1].split(']')[0]
                inid = []
                for o in objd.split(','):
                    id = o.replace('ObjectId', '').replace('(', '').replace(')', '').replace("'", "").replace('"',
                                                                                                              '').strip()
                    inid.append(ObjectId(id))
                self.where = {'_id': {'$in': inid}}

                pattern = re.compile(r'(\}\s*,\s*\{)', re.I)
                if pattern.findall(self.find_contents) != []:
                    print('pattern `},{` be found!')
                    t = re.split(r'(\}\s*,\s*\{)', self.find_contents, flags=re.I)
                    c = '{' + t[2]
                    self.columns = json.loads(c)
                    return
                else:
                    print('not found },{')
                    return

        # resolve where and columns
        print('process where and columns ...')
        pattern = re.compile(r'(\}\s*,\s*\{)', re.I)
        if pattern.findall(self.find_contents) != []:
            print('pattern `},{` be found!')
            if self.find_contents.count('$in') == 0:
                if self.find_contents.count('$and') == 0:
                    print('process $in = 0 ...')
                    t = re.split(r'(\}\s*,\s*\{)', self.find_contents, flags=re.I)
                    c = '{' + t[2]
                    v = t[0] + '}'
                    self.columns = json.loads(c)
                    self.where = json.loads(v)
                    return
                elif self.find_contents.count('ISODate') > 0:
                    print('ISODate found!')
                    print('$and found!')
                    pattern = re.compile(r'([\"\']\$and[\"\']\s+:\s+)', re.I)
                    if pattern.findall(self.find_contents) != []:
                        print('>>`$and` found!')
                        t1 = re.split(r'([\"\']\$and[\"\']\s*:\s*)', self.find_contents, flags=re.I)
                        print('t1=', t1)
                        print('t1[2]=', t1[2])
                        print('t1[2][0:-1]=', t1[2][0:-1])

                    pattern = re.compile(r'(\$and\s*:\s*)', re.I)
                    if pattern.findall(self.find_contents) != []:
                        print('>>>$and found!')
                        t1 = re.split(r'(\$and\s*:\s*)', self.find_contents, flags=re.I)
                        print('t1=', t1)
                        print('t1[2]=', t1[2])
                        print('t1[2][0:-1]=', t1[2][0:-1])

                    pattern = re.compile(r'(ISODate(.*))', re.I)
                    v = pattern.sub(repl_str1, t1[2][0:-1])
                    print('v=', v, type(v))
                    pattern = re.compile(r'([\'\"]\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}[\'\"])', re.I)
                    v2 = pattern.sub(repl_str2, v)
                    print('v2=', v2)
                    self.where = {'$and': list(eval(pickle.loads(pickle.dumps(v2))))}
                    # self.columns=?
                    return
                else:
                    pattern = re.compile(r'([\"\']\$and[\"\']\s+:\s+)', re.I)
                    if pattern.findall(self.find_contents) != []:
                        print('>>`$and` found!')
                        t1 = re.split(r'([\"\']\$and[\"\']\s*:\s*)', self.find_contents, flags=re.I)

                    pattern = re.compile(r'(\$and\s*:\s*)', re.I)
                    if pattern.findall(self.find_contents) != []:
                        print('>>>$and found!')
                        t1 = re.split(r'(\$and\s*:\s*)', self.find_contents, flags=re.I)

                    t2 = re.split(r'(\}\s*,\s*\{)', t1[2], flags=re.I)
                    if t2 != []:
                        if t2[-1].count(']') == 0:
                            w = ''.join(t2[0:-1])
                            self.where = {'$and': json.loads(w[0:w.find(']') + 1])}
                            self.columns = json.loads('{' + t2[-1])
                        else:
                            self.where = {'$and': json.loads(t1[2][0:-1])}
                    else:
                        self.where = {'$and': json.loads(t1[2][0:-1])}

                    return

            if self.find_contents.count('$in') == 1:
                print('process $in = 1 ...')
                t = re.split(r'(\$in\s*:\s*)', self.find_contents, flags=re.I)
                k = t[0].split('{')[1].split(':')[0].replace("'", "").replace('"', '').strip()
                v = t[2].split('[')[1].split(']')[0]
                v2 = json.loads('[' + v + ']')
                self.where = {k: {'$in': v2}}
                t = re.split(r'(\}\s*,\s*\{)', self.find_contents, flags=re.I)
                c = '{' + t[2]
                self.columns = json.loads(c)
                return

        else:
            if self.find_contents.count('$and') > 0:
                pattern = re.compile(r'([\',\"]\$and[\',\"])', re.I)
                if pattern.findall(self.find_contents) != []:
                    self.where = json.loads(self.find_contents)
                else:
                    self.find_contents = self.find_contents.replace('$and', "'$and'")
            else:
                self.where = json.loads(self.find_contents)


'''
  1.一个条件，所有列
  √ db.monitorLog.find({terminalNo:"10000201"}}).limit(10)
  √ db.getCollection('monitorLog').find({terminalNo:"10000201"}).limit(10)
  
  2.一个条件，显示某些列
  √ db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)
  √ db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)
  √ db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)
  √ db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)
  
  3.查询所有数据
  √ db.monitorLog.find({}).limit(10)
  √ db.getCollection('monitorLog').find({}).limit(10) 
  
  4.查询所有数据,显示部分列
  √ db.getCollection('monitorLog').find({},{"terminalNo":1}).limit(5)
  √ db.getCollection('monitorLog').find({},{"terminalNo":1,"ip":1}).limit(5) 
  
  5.支持ObjectID列查询
  √ db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")})
  √ db.monitorLog.find({"_id" : {$in:[ObjectId("5d5e5f338488d5000145b343"),ObjectId("5d5e5fc88488d5000145b344")]}})
  √ db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")},{"terminalNo":1}).limit(5)
  √ db.monitorLog.find({"_id" : {$in:[ObjectId("5d5e5f338488d5000145b343"),ObjectId("5d5e5fc88488d5000145b344")]}},{"terminalNo":1}).limit(5)  
  √ db.getCollection('monitorLog').find({'_id':ObjectId("5d5e5f338488d5000145b343")})
  √ db.monitorLog.find({"_id":{$in:[ObjectId("5d5e5f338488d5000145b343"), ObjectId("5d5e5fc88488d5000145b344")]}}).limit(3)
  √ db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")},{"terminalNo":1}).limit(5)
  √ db.monitorLog.find({"_id" : {$in:[ObjectId("5d5e5f338488d5000145b343"),ObjectId("5d5e5fc88488d5000145b344")]}},{"terminalNo":1}).limit(5)  
  
  √ db.monitorLog.find({ $and : [{"receiveLogDt" : { $gte : ISODate("2019-08-22 00:00:00.000") }}, {"receiveLogDt" : { $lte : ISODate("2019-08-22 23:59:59.000") }}]})
  √ db.monitorLog.find({"logType" : {$in:[1,2]}},{"terminalNo":1,"logType":1}).limit(5)  

  6.支持$and操作

'''


def test():
    mongo = mongo_client(config['ip'], config['port'], config['db'])
    # mongo.conn.list_collection_names()
    print('[打印数据库名列表]....')
    print(mongo.get_databases())
    print('[打印集合列表]....')
    rs = mongo.get_collections('hopson_hft')
    print('rs=', rs)
    rs = mongo.get_collections('hopsonone_park')
    print('rs=', rs)

    # print('[一个条件，所有列.....]')
    # print('\nDEMO1：','''db.monitorLog.find({"terminalNo":"10000201"}).limit(5)''')
    # mongo.find_by_where('''db.monitorLog.find({"terminalNo":"10000201"}).limit(5)''')
    # print('\nDEMO2：','''db.getCollection('monitorLog').find({"terminalNo":"10000201"}).limit(5)''')
    # mongo.find_by_where('''db.getCollection('monitorLog').find({"terminalNo":"10000201"}).limit(5)''')

    # print('一个条件，某些列.....')
    # print('\nDEMO1：','''db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)''')
    # mongo.find_by_where('''db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)''')
    # print('\nDEMO2：','''db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)''')
    # mongo.find_by_where('''db.monitorLog.find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)''')
    # print('\nDEMO3：','''db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)''')
    # mongo.find_by_where('''db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1}).limit(5)''')
    # print('\nDEMO4：','''db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)''')
    # mongo.find_by_where('''db.getCollection('monitorLog').find({"terminalNo":"10000201"},{"terminalNo":1,"ip":1}).limit(5)''')

    # print('所有数据，所有列,部分行.....')
    # print('DEMO1：','''db.monitorLog.find({}).limit(10)''')
    # mongo.find_by_where('''db.monitorLog.find({}).limit(10)''')
    # print('DEMO2：', '''db.getCollection('monitorLog').find({}).limit(5)''')
    # mongo.find_by_where('''db.getCollection('monitorLog').find({}).limit(5)''')

    # print('所有数据，某些列.....')
    # print('DEMO1：','''db.monitorLog.find({},{"terminalNo":1}).limit(10)''')
    # mongo.find_by_where('''db.monitorLog.find({},{"terminalNo":1}).limit(10)''')

    # print('_id查询，一个值，所有列.....')
    # print('DEMO1：','''db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")})''')
    # mongo.find_by_where('''db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")})''')
    # print('DEMO2：','''db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")})''')
    # mongo.find_by_where('''db.getCollection('monitorLog').find({'_id':ObjectId("5d5e5f338488d5000145b343")})''')

    # print('_id查询，一个值$,某些列.....')
    # mongo.find_by_where('''db.monitorLog.find({'_id':ObjectId("5d5e5f338488d5000145b343")},{"terminalNo":1}).limit(5)''')

    # print('_id查询，多值$in,所有列.....')
    # mongo.find_by_where('''db.monitorLog.find({"_id":{$in:[ObjectId("5d5e5f338488d5000145b343"), ObjectId("5d5e5fc88488d5000145b344")]}}).limit(3)''')

    # print('_id查询，多值$in,某些列.....')
    # mongo.find_by_where('''db.monitorLog.find({"_id" : {$in:[ObjectId("5d5e5f338488d5000145b343"),ObjectId("5d5e5fc88488d5000145b344")]}},{"terminalNo":1}).limit(5)''')
    #
    # print('非_id查询，单值,某些列.....')
    # mongo.find_by_where('''db.monitorLog.find({"logType" : 1},{"terminalNo":1,"logType":1}).limit(5)''')
    #
    # print('非_id查询，多值$in,某些列.....')
    # mongo.find_by_where('''db.monitorLog.find({"logType" : {$in:[1,2]}},{"terminalNo":1,"logType":1}).limit(5)''')
    # print('$and操作符测试,所有列...')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ $and : [{"logType" : { "$gte" : 1 }}, {"logType" : { "$lte" : 3 }}] }).limit(10)''')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ $and : [{"logType" : { "$gte" : 1 }}, {"logType" : { "$lte" : 3 }}] },{"terminalNo":1,"ip":1}).limit(10)''')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ "$and" : [{"logType" : { "$gte" : 1 }}] }).limit(10)''')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ $and : [{"logType" : { "$gte" : 1 }}] }).limit(10)''')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ '$and'  :   [{"receiveLogDt" : { "$gte" : ISODate("2019-08-22 00:00:00") }}, {"receiveLogDt" : { "$lte" : ISODate("2019-08-22 23:59:59") }}]}).limit(3)''')
    # mongo.find_by_where('''db.getCollection("monitorLog").find({ $and : [{"receiveLogDt" : { "$gte" : ISODate("2019-08-22 00:00:00") }}, {"receiveLogDt" : { "$lte" : ISODate("2019-08-22 23:59:59") }}]}).limit(3)''')


if __name__ == "__main__":
    test()
