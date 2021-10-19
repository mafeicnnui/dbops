#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import json
import datetime
import traceback
from web.utils.mysql_async import async_processer
from web.utils.common  import format_sql as fmt_sql,get_seconds
from web.model.t_ds    import get_ds_by_dsid
from web.model.t_sql  import exe_query
from web.utils.mysql_sync import sync_processer


async def get_config(p_bbdm):
    st = "select * from t_bbgl_config where bbdm='{}'".format(p_bbdm)
    if (await async_processer.query_one(st)) is not None:
       return  await async_processer.query_dict_one(st)
    else:
       return  {}

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
         start_time = datetime.datetime.now()
         for s in preprocess:
             print('exec:',s['replace_statement'])
             await async_processer.exec_sql_by_ds(ds,s['replace_statement'])
         preProcessTime = get_seconds(start_time)

         # 调用查询语句返回数据
         result = await exe_query(cfg['dsid'],cfg['statement'],'hopsonone_do')
         result = {"data": result['data'], "column": result['column'], "status": result['status'], "msg": result['msg'],"preTime":str(preProcessTime)}
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

async def query_bbgl_preprocess_detail(p_bbdm,p_xh):
    st = "select * from t_bbgl_preproccess where bbdm='{}' and xh={}".format(p_bbdm,p_xh)
    return await async_processer.query_dict_one(st)

async def update_bbgl_preprocess(p_bbdm,p_xh,p_statement,p_description):
    try:
        st = "update t_bbgl_preproccess " \
             " set statement='{}',`description`='{}' " \
             "  where bbdm='{}' and xh={}".format(p_statement,p_description,p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '更新成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '更新失败!'}

async def delete_bbgl_preprocess(p_bbdm,p_xh):
    try:
        st = "delete from  t_bbgl_preproccess where  bbdm='{}' and xh={}".format(p_bbdm,p_xh)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '删除成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '删除失败!'}


async def update_bbgl_statement(p_bbdm,p_statement):
    try:
        st = "update t_bbgl_config  set statement='{}' where bbdm='{}'".format(fmt_sql(p_statement),p_bbdm)
        await async_processer.exec_sql(st)
        return {'code': 0, 'message': '更新成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '更新失败!'}

async def query_bbgl_config(p_bbdm):
    vv=''
    if p_bbdm!='':
       vv = " and a.bbdm='{}'".format(p_bbdm)
    st = """select 
                 bbdm,
                 bbmc,
                 b.db_desc,
                 u.name,
                 date_format(a.create_date,'%Y-%m-%d')    create_date,
                 date_format(a.last_update_date,'%Y-%m-%d') last_update_date 
           from t_bbgl_config a,t_db_source b,t_user u
           where a.dsid=b.id and a.creator=u.id  {} """.format(vv)
    print('st=',st)
    return  await async_processer.query_list(st)

async def delete_bbgl(p_bbdm):
    try:
        st = "delete from  t_bbgl_header where  bbdm='{}'".format(p_bbdm)
        await async_processer.exec_sql(st)

        st = "delete from  t_bbgl_preproccess where  bbdm='{}'".format(p_bbdm)
        await async_processer.exec_sql(st)

        st = "delete from  t_bbgl_filter where  bbdm='{}'".format(p_bbdm)
        await async_processer.exec_sql(st)

        st = "delete from  t_bbgl_config where  bbdm='{}'".format(p_bbdm)
        await async_processer.exec_sql(st)

        return {'code': 0, 'message': '删除成功!'}

    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '删除失败!'}

async def export_insert(p_bbdm, p_param, p_userid):
    st = """insert into t_bbgl_export(bbdm,filter,status,process,creator,create_time)
                values('{}','{}','1','0%','{}',now())""".format(p_bbdm, json.dumps(p_param), p_userid)
    id = await async_processer.exec_ins_sql(st)
    return id

async def update_export(p_id,p_status,p_process):
    st = "update t_bbgl_export set status='2',process='10%' where id={}".format(p_status,p_process,p_id)
    await async_processer.exec_sql(st)

async def export_bbgl_data(bbdm, param,userid):
    id = await export_insert(bbdm,param,userid)
    print('export_bbgl_data=',id)

    result = await query_bbgl_data(bbdm,param)
    await update_export(id,'2','20%')

    # 3. write excel among write process
    # 4. export complete write status
    # 5. write table header
    # 5. common write excel
    #return result
    return {}

