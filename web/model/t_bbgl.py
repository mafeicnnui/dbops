#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/30 15:46
# @Author  : ma.fei
# @File    : t_user.py
# @Software: PyCharm

import traceback
from web.utils.mysql_async import async_processer

async def get_xh(p_bbdm):
    st = "select max(xh)+1 from t_bbgl_header where bbdm='{}'".format(p_bbdm)
    rs = await async_processer.query_one(st)
    print('rs=',rs)
    if rs[0] == None:
       return 1
    else:
      return rs[0]

async def save_bbgl(bbdm,bbmc,dsid,userid):
    try:
        st = "insert into t_bbgl_config(bbdm,bbmc,dsid,creator,create_date,last_update_date) \
                values('{}','{}','{}','{}',now(),now())".format(bbdm,bbmc,dsid,userid)
        await async_processer.exec_sql(st)
        return {'code':0,'message':'保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}


async def save_bbgl_header(bbdm,name,width):
    try:
        st = "insert into t_bbgl_header(bbdm,xh,header_name,header_width) \
                 values('{}',{},'{}','{}')".format(bbdm,(await get_xh(bbdm)),name,width)
        print('st=',st)
        await async_processer.exec_sql(st)
        return {'code':0,'message':'保存成功!'}
    except Exception as e:
        traceback.print_exc()
        return {'code': -1, 'message': '保存失败!'}


async def query_bbgl_header(p_bbdm):
      st = "select xh,header_name,header_width from t_bbgl_header where bbdm='{}'".format(p_bbdm)
      print('query_bbgl_header=',st)
      return await async_processer.query_list(st)
