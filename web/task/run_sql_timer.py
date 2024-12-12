#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/6 10:54
# @Author : ma.fei
# @File : schedule.py.py
# @Func : 定时执行工单
# @Software: PyCharm

import asyncio
import datetime
import logging
import time

from web.model.t_sql_release import exe_sql_sync
from web.utils.common import current_time
from web.utils.mysql_sync import sync_processer

host = "ops.zhitbar.cn:59521"


def get_tasks():
    st = """SELECT dbid AS db_id, db AS db_name,id AS sql_id, creator AS user_name,run_time
            FROM t_sql_release  WHERE STATUS in('1','5') AND run_time IS NOT NULL AND run_time !=''"""
    return sync_processer.query_dict_list(st)


async def main():
    logging.basicConfig(filename='./run_sql_timer.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")),
                        format='[%(asctime)s-%(levelname)s:%(message)s]',
                        level=logging.INFO, filemode='a', datefmt='%Y-%m-%d %I:%M:%S')
    while True:
        time.sleep(1)
        tasks = get_tasks()
        logging.info('\rTime:{},Tasks:{}'.format(current_time(), len(tasks)))
        for t in tasks:
            if t['run_time'] == current_time()[0:16]:
                logging.info('Processing Task: db_name={},release_id={},dbid={}...'.
                             format(current_time(), t['db_name'], t['sql_id'], t['db_id']))
                exe_sql_sync(t['db_id'], t['db_name'], t['sql_id'], t['user_name'], host)
                asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
