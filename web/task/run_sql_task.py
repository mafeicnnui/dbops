#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/6 10:54
# @Author : ma.fei
# @File : schedule.py.py
# @Func : 定时执行工单手动触发
# @Software: PyCharm

import time
from web.model.t_sql_release import exe_sql_sync
from web.utils.mysql_sync import sync_processer
from concurrent.futures import ProcessPoolExecutor,wait,as_completed

host = "ops.zhitbar.cn"

def get_tasks():
    st = """SELECT dbid AS db_id, db AS db_name,
                id AS sql_id,executor AS user_name,run_time,message
                 FROM t_sql_release  WHERE status in('7') """
    return  sync_processer.query_dict_list(st)


def main():
    with ProcessPoolExecutor(max_workers=5) as executor:
        while True:
            tasks = get_tasks()
            if tasks!=[]:
                print('tasks=',tasks)
                all_task = [executor.submit(exe_sql_sync,t['db_id'], t['db_name'], t['sql_id'], t['user_name'],host) for t in tasks]
                for future in as_completed(all_task):
                    res = future.result()
                    print("res=",res)
            else:
               time.sleep(1)
               print('\rSleepping...'.format(),end='')

if __name__=="__main__":
     main()
