#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.common import current_rq
from web.utils.common import get_connection

def get_privs_by_userid(p_roleid):
    db = get_connection()
    cr = db.cursor()
    sql="select priv_id from t_user_role where role_id={0}".format(p_roleid)
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    db.commit()
    return rs

def save_role_privs(p_role_id,p_privs):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        print(p_privs)
        for id in p_privs:
          sql="""insert into t_role_privs(role_id,priv_id,creation_date,creator,last_update_date,updator) 
                    values({0},'{1}','{2}','{3}','{4}','{5}')
              """.format(p_role_id,id,current_rq(),'DBA',current_rq(),'DBA')
          print(sql)
          cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def save_role_func_privs(p_role_id,p_privs):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        print(p_privs)
        for id in p_privs:
          sql="""insert into t_role_func_privs(role_id,func_id,creation_date,creator,last_update_date,updator) 
                    values({0},'{1}','{2}','{3}','{4}','{5}')
              """.format(p_role_id,id,current_rq(),'DBA',current_rq(),'DBA')
          print(sql)
          cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result


def upd_role_privs(p_role_id,p_privs_id):
    result={}
    try:
        db = get_connection()
        cr = db.cursor()
        del_role_privs(p_role_id)
        save_role_privs(p_role_id,p_privs_id)
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def upd_role_func_privs(p_role_id,p_privs_id):
    result={}
    try:
        del_role_func_privs(p_role_id)
        save_role_func_privs(p_role_id,p_privs_id)
        result={}
        result['code']='0'
        result['message']='更新成功！'
    except :
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result

def del_role_privs(p_roleid):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = "delete from t_role_privs where role_id={0}".format(p_roleid);
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result = {}
        result['code'] = '0'
        result['message'] = '删除成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def del_role_func_privs(p_roleid):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql = "delete from t_role_func_privs where role_id={0}".format(p_roleid);
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result = {}
        result['code'] = '0'
        result['message'] = '删除成功！'
        return result
    except:
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

