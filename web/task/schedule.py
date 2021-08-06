#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/6 10:54
# @Author : ma.fei
# @File : schedule.py.py
# @Func : 定时执行工单
# @Software: PyCharm

import time
import asyncio
import logging
from web.model.t_sql_release import exe_sql
from web.utils.mysql_async import async_processer
from web.utils.common import current_time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s', datefmt='%Y-%m-%d')

async def get_tasks():
    st = """SELECT dbid AS db_id,
                   db   AS db_name,
                   id   AS sql_id,
                   'admin' AS user_name,
                   run_time
                FROM t_sql_release 
                 WHERE STATUS in('1','5') AND run_time IS NOT NULL"""
    return await async_processer.query_dict_list(st)

async def main():
      while True:
            time.sleep(1)
            tasks = await get_tasks()
            for t in tasks:
                if t['run_time']  == current_time()[0:16]:
                    print('Time:{} Processing Task: db_name={},sqlid={},dbid={}...'.
                          format(current_time(),t['db_name'],t['sql_id'],t['db_id']))
                    # logging.info('Time:{} Processing Task: db_name={},sqlid={},dbid={}...'.
                    #       format(current_time(), t['db_name'],t['sql_id'], t['db_id']))
                    await exe_sql(t['db_id'], t['db_name'], t['sql_id'], t['user_name'])
                    asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())