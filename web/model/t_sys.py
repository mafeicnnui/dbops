#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/30 16:30
# @Author : 马飞
# @File : t_sys.py.py
# @Software: PyCharm
import traceback
from web.utils.common import get_connection,format_sql

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
              result['message'] ='字符字段最大长度不是整数!'
              return result
    return result


def check_code(code):
    result = {}
    if code["type_name"]=="":
        result['code']='-1'
        result['message']='类型名称不能为空！'
        return result

    if code["type_code"]=="":
        result['code']='-1'
        result['message']='类型代码不能为空！'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result


def save_audit_rule(rule):
    result = check_rule(rule)
    if result['code']=='-1':
       return result
    try:
        db = get_connection()
        cr = db.cursor()
        for key in rule:
           sql= "update t_sql_audit_rule set rule_value='{}' where rule_code='{}'".format(rule[key],key)
           print('save_audit_rule=',sql)
           cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        print(str(e))
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def save_sys_code_type(code):
    result = check_code(code)
    if result['code']=='-1':
       return result
    try:
        db = get_connection()
        cr = db.cursor()
        sql= "insert into t_dmlx(dm,mc,flag,create_time,update_time) values('{}','{}','{}',now(),now())".\
             format(code['type_code'],code['type_name'],code['type_status'])
        print('save_sys_code_type=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_sys_code_type(code):
    result = check_code(code)
    if result['code']=='-1':
       return result
    try:
        db = get_connection()
        cr = db.cursor()
        sql= """update t_dmlx set  mc ='{}',flag = '{}',update_time=now() where   dm  = '{}'
             """.format(code['type_name'],code['type_status'],code['type_code'])
        print('upd_sys_code_type=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='更新成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_sys_code(code):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        cr.execute("select count(0) from t_dmmx where dm='{}'".format(code))
        rs=cr.fetchone()
        if  rs[0]>0:
            result['code'] = '-1'
            result['message'] = '存在代码明细数据不能删除！'
            return result
        sql= "delete from t_dmlx where dm  = '{}'".format(code)
        print('del_sys_code=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def save_sys_code_detail(code):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql= "insert into t_dmmx(dm,dmm,dmmc,flag,create_time,update_time) values('{}','{}','{}','{}',now(),now())".\
             format(code['type_code'],format_sql(code['detail_code']),code['detail_name'],code['detail_status'])
        print('save_sys_code_detail=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='保存成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def upd_sys_code_detail(code):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql= """update t_dmmx 
                   set dmm ='{}',
                       dmmc ='{}',
                       flag = '{}',
                       update_time=now()
                where   dm  = '{}' and dmm='{}'
             """.format(code['detail_code'],code['detail_name'],code['detail_status'],code['type_code'],format_sql(code['detail_code_old']))
        print('upd_sys_code_detail=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='更新成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '更新失败！'
    return result


def del_sys_code_detail(code,detail):
    result = {}
    try:
        db = get_connection()
        cr = db.cursor()
        sql= "delete from t_dmmx where dm  = '{}' and dmm='{}'".format(code,detail)
        print('del_sys_code_detail=',sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result={}
        result['code']='0'
        result['message']='删除成功！'
        return result
    except Exception as e:
        print(traceback.format_exc())
        result['code'] = '-1'
        result['message'] = '删除失败！'
    return result

def query_dm(p_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if p_code != '':
        v_where = " where  (a.dm like '%{0}%' or a.mc like '%{1}%')".format(p_code,p_code,p_code,p_code)

    sql = """SELECT 
                  a.dm,
                  a.mc,
                  case a.flag when '1' then '启用'  when '0' then '禁用' end  as flag,
                  date_format(a.create_time,'%Y-%m-%d %H:%i:%s')  as  create_time,
                  date_format(a.update_time,'%Y-%m-%d %H:%i:%s')  as  update_time
             FROM t_dmlx a
                {0}
             ORDER BY a.dm,a.create_time
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_dm_detail(p_code):
    db = get_connection()
    cr = db.cursor()
    v_where=' '
    if p_code != '':
        v_where = "  and (b.dm='{0}' or b.dmm='{1}' or a.mc  like '%{2}%')".format(p_code,p_code,p_code)

    sql = """SELECT 
                  a.dm,
                  a.mc,  
                  b.dmm,
                  b.dmmc,                
                  case b.flag when '1' then '启用'  when '0' then '禁用' end  as flag,
                  date_format(b.create_time,'%Y-%m-%d %H:%i:%s')  as  create_time,
                  date_format(b.update_time,'%Y-%m-%d %H:%i:%s')  as  update_time
             FROM t_dmlx a,t_dmmx b
             where  a.dm=b.dm  
               {0}
             ORDER BY b.dm,b.dmm,a.create_time
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def query_rule():
    db = get_connection()
    cr = db.cursor()
    sql = "SELECT rule_code,rule_value FROM t_sql_audit_rule"
    print(sql)
    cr.execute(sql)
    v_dict = {}
    for r in cr.fetchall():
        v_dict[r[0]]=r[1]
    cr.close()
    db.commit()
    print('query_rule=',v_dict)
    return v_dict
