#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import traceback
from web.utils.mysql_async import async_processer
from web.utils.common  import format_sql as fmt_sql
from web.model.t_ds    import get_ds_by_dsid
from web.model.t_sql  import exe_query

async def get_config(p_bbdm):
    st = "select * from t_bbgl_config where bbdm='{}'".format(p_bbdm)
    return  await async_processer.query_dict_one(st)

async def get_preprocess(p_bbdm):
    st = "select statement,description from t_bbgl_preproccess where bbdm='{}' ORDER BY xh".format(p_bbdm)
    return  await async_processer.query_dict_list(st)

async def get_filter(p_bbdm):
    st = "select  * from t_bbgl_filter where bbdm='{}' ORDER BY xh".format(p_bbdm)
    return  await async_processer.query_dict_list(st)


async def get_header_xh(p_bbdm):
    st = "select max(xh)+1 from t_bbgl_header where bbdm='{}'".format(p_bbdm)
    rs = await async_processer.query_one(st)
    print('rs=',rs)
    if rs[0] == None:
       return 1
    else:
      return rs[0]

async def get_filter_xh(p_bbdm):
    st = "select max(xh)+1 from t_bbgl_filter where bbdm='{}'".format(p_bbdm)
    rs = await async_processer.query_one(st)
    print('rs=',rs)
    if rs[0] == None:
       return 1
    else:
      return rs[0]

async def get_preprocess_xh(p_bbdm):
    st = "select max(xh)+1 from t_bbgl_preproccess where bbdm='{}'".format(p_bbdm)
    rs = await async_processer.query_one(st)
    print('rs=',rs)
    if rs[0] == None:
       return 1
    else:
      return rs[0]

async def save_bbgl(bbdm,bbmc,dsid,userid):
    try:
        if (await check_bbdm_exists(bbdm)) == 0:
            st = "insert into t_bbgl_config(bbdm,bbmc,dsid,creator,create_date,last_update_date) \
                    values('{}','{}','{}','{}',now(),now())".format(bbdm,bbmc,dsid,userid)
            await async_processer.exec_sql(st)
            return {'code':0,'message':'保存成功!'}
        else:
            st = """update t_bbgl_config set bbmc='{}',dsid='{}',last_update_date=now() where bbdm='{}'""".format(bbmc, dsid,bbdm)
            await async_processer.exec_sql(st)
            return {'code': 0, 'message': '更新成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}


async def save_bbgl_header(bbdm,name,width):
    try:
        st = "insert into t_bbgl_header(bbdm,xh,header_name,header_width) \
                 values('{}',{},'{}','{}')".format(bbdm,(await get_header_xh(bbdm)),name,width)
        await async_processer.exec_sql(st)
        return {'code':0,'message':'保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}


async def save_bbgl_filter(bbdm, filter_name, filter_code,filter_type):
    try:
        st = "insert into t_bbgl_filter(bbdm,xh,filter_name,filter_code,filter_type) \
                 values('{}',{},'{}','{}','{}')".format(bbdm, (await get_filter_xh(bbdm)), filter_name, filter_code,filter_type)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}

async def save_bbgl_preprocess(bbdm, statement, description):
    try:
        st = "insert into t_bbgl_preproccess(bbdm,xh,statement,description) \
                 values('{}',{},'{}','{}')".format(bbdm, (await get_preprocess_xh(bbdm)), fmt_sql(statement), description)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}

async def save_bbgl_statement(bbdm, statement):
    try:
        st = """update t_bbgl_config set statement='{}' where bbdm='{}'""".format(fmt_sql(statement),bbdm)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}

async def query_bbgl_header(p_bbdm):
      st = "select xh,header_name,header_width from t_bbgl_header where bbdm='{}' order by bbdm,xh".format(p_bbdm)
      return await async_processer.query_list(st)

async def query_bbgl_filter(p_bbdm):
    st = "select a.xh,a.filter_name,a.filter_code,a.filter_type,b.dmmc from t_bbgl_filter a,t_dmmx b where a.filter_type=b.dmm and b.dm='42' and a.bbdm='{}' order by a.bbdm,a.xh".format(p_bbdm)
    return await async_processer.query_list(st)

async def query_bbgl_preprocess(p_bbdm):
    st = "select xh,substr(statement,1,50) as statement,description from t_bbgl_preproccess where bbdm='{}' order by bbdm,xh".format(p_bbdm)
    return await async_processer.query_list(st)

async def query_bbgl_statement(p_bbdm):
    st = "select statement from t_bbgl_config where bbdm='{}'".format(p_bbdm)
    return await async_processer.query_dict_one(st)

async def check_bbdm_exists(p_bbdm):
    st = "select count(0) as rec from t_bbgl_config where bbdm='{}'".format(p_bbdm)
    print('rs=',(await async_processer.query_one(st))[0])
    return (await async_processer.query_one(st))[0]

async def get_bbgl_bbdm():
    st = "select bbdm,bbmc from t_bbgl_config order by id"
    return await async_processer.query_list(st)

async def query_bbgl_data(bbdm,param):
     try:
         #1.通过bbdm获取报表定义相关数据
         cfg = await get_config(bbdm)
         preprocess=  await get_preprocess(bbdm)
         ds  = await get_ds_by_dsid(cfg['dsid'])

         #2. 获取预处理脚本，替换变量为实参
         for s in preprocess:
             s['replace_statement'] = s['statement']
             for key,value in param.items():
                 s['replace_statement']= s['replace_statement'].replace('$$'+key+'$$',value)

         #3. 执行预处理代码
         for s in preprocess:
             print('exec:',s['replace_statement'])
             await async_processer.exec_sql_by_ds(ds,s['replace_statement'])

         # 调用查询语句返回数据
         result = await exe_query(cfg['dsid'],cfg['statement'],'hopsonone_do')
         result = {"data": result['data'], "column": result['column'], "status": result['status'], "msg": result['msg']}
         return  result

     except:
         result = {"data": '', "column": '', "status": '1', "msg": traceback.print_exc()}
         return result

async def update_bbgl_header(p_bbdm,p_xh,p_name,p_width):
    try:
        st = "update t_bbgl_header " \
             " set header_name='{}',header_width='{}' " \
             "  where bbdm='{}' and xh={}".format(p_name,p_width,p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '更新成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '更新失败!'}

async def delete_bbgl_header(p_bbdm,p_xh):
    try:
        st = "delete from  t_bbgl_header where  bbdm='{}' and xh={}".format(p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '删除成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '删除失败!'}


async def update_bbgl_filter(p_bbdm,p_xh,p_name,p_code,p_type):
    try:
        st = "update t_bbgl_filter " \
             " set filter_name='{}',filter_code='{}',filter_type='{}' " \
             "  where bbdm='{}' and xh={}".format(p_name,p_code,p_type,p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '更新成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '更新失败!'}

async def delete_bbgl_filter(p_bbdm,p_xh):
    try:
        st = "delete from  t_bbgl_filter where  bbdm='{}' and xh={}".format(p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '删除成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '删除失败!'}