#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/6 10:54
# @Author : ma.fei
# @File : schedule.py.py
# @Func : 定时执行工单手动触发
# @Software: PyCharm

import datetime
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from web.model.t_sql_release import exe_sql_sync
from web.utils.common import get_sys_settings_sync
from web.utils.mysql_sync import sync_processer

host = get_sys_settings_sync()['WX_HOST']

def get_tasks():
    st = """SELECT dbid AS db_id, db AS db_name,
                id AS sql_id,executor AS user_name,run_time,message
                 FROM t_sql_release  WHERE status in('7') """
    return sync_processer.query_dict_list(st)


def main():
    logging.basicConfig(filename='./run_sql_task.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")),
                        format='[%(asctime)s-%(levelname)s:%(message)s]',
                        level=logging.INFO, filemode='a', datefmt='%Y-%m-%d %I:%M:%S')

    with ProcessPoolExecutor(max_workers=10) as executor:
        while True:
            tasks = get_tasks()
            if tasks != []:
                logging.info(str(tasks))
                future_to_task  = {
                          executor.submit(exe_sql_sync, t['db_id'], t['db_name'], t['sql_id'], t['user_name'], host): t
                          for t in tasks
                }
                for future in as_completed(future_to_task ):
                    res = future.result()
                    logging.info(str(res))
                    task_params = future_to_task[future]  # 获取任务的参数
                    logging.info(f"Task {task_params} → Result: {res}")
            else:
                time.sleep(1)
                print('\rSleepping...'.format(), end='')


if __name__ == "__main__":
    main()
