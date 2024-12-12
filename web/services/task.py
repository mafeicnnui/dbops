#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json

from web.model.t_dmmx import get_dmm_from_dm, get_gather_server
from web.model.t_task import push_task, upd_task, del_task, stop_task, run_task
from web.model.t_task import query_task, save_task, get_task_by_taskid
from web.utils import base_handler


class taskquery(base_handler.TokenHandler):
    def get(self):
        self.render("./task/task_query.html")


class task_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tagname = self.get_argument("tagname")
        v_list = await query_task(tagname)
        v_json = json.dumps(v_list)
        self.write(v_json)


class taskadd(base_handler.TokenHandler):
    async def get(self):
        self.render("./task/task_add.html",
                    dm_task_server=await get_gather_server(),
                    dm_sync_type=await get_dmm_from_dm('34'),
                    dm_sync_time_type=await get_dmm_from_dm('10'))


class taskadd_save(base_handler.TokenHandler):
    async def post(self):
        task = {}
        task['task_tag'] = self.get_argument("task_desc")
        task['task_desc'] = self.get_argument("task_desc")
        task['server_id'] = self.get_argument("task_server")
        task['python3_home'] = self.get_argument("python3_home")
        task['script_base'] = self.get_argument("script_base")
        task['script_name'] = self.get_argument("script_name")
        task['run_time'] = self.get_argument("run_time")
        task['api_server'] = self.get_argument("api_server")
        task['status'] = self.get_argument("status")
        result = await save_task(task)
        self.write({"code": result['code'], "message": result['message']})


class taskchange(base_handler.TokenHandler):
    def get(self):
        self.render("./task/task_change.html")


class taskedit(base_handler.TokenHandler):
    async def get(self):
        task_tag = self.get_argument("task_tag")
        task = await get_task_by_taskid(task_tag)
        self.render("./task/task_edit.html",
                    task_tag=task['task_tag'],
                    task_desc=task['comments'],
                    task_server=task['server_id'],
                    python3_home=task['python3_home'],
                    script_base=task['script_path'],
                    script_name=task['script_file'],
                    run_time=task['run_time'],
                    api_server=task['api_server'],
                    status=task['status'],
                    dm_task_server=await get_gather_server(),
                    )


class taskedit_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        task = {}
        task['task_tag'] = self.get_argument("task_tag")
        task['task_desc'] = self.get_argument("task_desc")
        task['server_id'] = self.get_argument("task_server")
        task['python3_home'] = self.get_argument("python3_home")
        task['script_base'] = self.get_argument("script_base")
        task['script_name'] = self.get_argument("script_name")
        task['run_time'] = self.get_argument("run_time")
        task['api_server'] = self.get_argument("api_server")
        task['status'] = self.get_argument("status")
        result = await upd_task(task)
        self.write({"code": result['code'], "message": result['message']})


class taskedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        sync_tag = self.get_argument("sync_tag")
        result = await del_task(sync_tag)
        self.write({"code": result['code'], "message": result['message']})


class taskedit_push(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = push_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)


class taskedit_run(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = run_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)


class taskedit_stop(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = stop_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)
