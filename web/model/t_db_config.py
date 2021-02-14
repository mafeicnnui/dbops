#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.mysql_async import async_processer

async def query_db_config(p_inst_env,p_inst_id):
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
    return await async_processer.query_list(sql)

async def update_db_config(d_db_para):
    val = check_db_para(d_db_para)
    if val['code']=='-1':
        return val
    try:
        sql="""update t_db_inst_parameter set value='{}={}',last_update_date=now() where id={}""".format(d_db_para['para_name'], d_db_para['para_val'],d_db_para['para_id'])
        await async_processer.exec_sql(sql)
        return {'code': '0', 'message': '更新成功!'}
    except:
        traceback.print_exc()
        return {'code': '-1', 'message': '更新失败!'}

def check_db_para(p_db_para):
    result = {}
    if p_db_para["para_val"]=="":
        result['code']='-1'
        result['message']='参数值不能为空!'
        return result
    result['code'] = '0'
    result['message'] = '验证通过'
    return result
