#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : 马飞
# @File    : t_user.py
# @Software: PyCharm
from web.utils.common import format_sql,aes_encrypt,aes_decrypt
from web.utils.common import exception_info,get_connection,get_connection_ds,get_connection_dict
from web.model.t_db_inst import get_ds_by_instid

def query_db_config(p_inst_env,p_inst_id):
    db = get_connection()
    cr = db.cursor()
    v_where =''
    if p_inst_id != '':
        v_where = v_where + " and  a.inst_id= '{0}'".format(p_inst_id)

    if p_inst_env != '':
        v_where = v_where + " and  b.inst_env= '{0}'".format(p_inst_env)

    sql = """SELECT 
                  a.id as para_id,
                  SUBSTR(a.value,1,INSTR(a.value,'=')-1) AS para_name,
                  SUBSTR(a.VALUE,INSTR(a.value,'=')+1) AS para_val,
                  a.type AS para_type,
                  a.name AS para_desc,
                  DATE_FORMAT(a.create_date,'%Y-%m-%d %h:%i:%s')  AS create_date
            FROM `t_db_inst_parameter` a ,t_db_inst b
              WHERE a.inst_id = b.id 
                 and SUBSTR(a.value,1,INSTR(a.value,'=')-1) 
                    NOT IN('basedir','port','socket','log-error','pid-file','datadir')
              {}
          """.format(v_where)
    print(sql)
    cr.execute(sql)
    v_list = []
    for r in cr.fetchall():
        v_list.append(list(r))
    cr.close()
    db.commit()
    return v_list

def update_db_config(d_db_para):
    result = {}
    val = check_db_para(d_db_para)
    if val['code']=='-1':
        return val
    try:
        db      = get_connection()
        cr      = db.cursor()
        result  = {}

        sql="""update t_db_inst_parameter set value='{}={}',last_update_date=now() where id={}
            """.format(d_db_para['para_name'], d_db_para['para_val'],d_db_para['para_id'])
        print(sql)
        cr.execute(sql)
        cr.close()
        db.commit()
        result['code']='0'
        result['message']='更新成功！'
        return result
    except:
        e_str = exception_info()
        print(e_str)
        result['code'] = '-1'
        result['message'] = '保存失败！'
    return result

def check_db_para(p_db_para):
    result = {}
    if p_db_para["para_val"]=="":
        result['code']='-1'
        result['message']='参数值不能为空!'
        return result

    result['code'] = '0'
    result['message'] = '验证通过'
    return result
