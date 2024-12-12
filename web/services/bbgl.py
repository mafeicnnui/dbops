#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
import traceback

import pandas as pd

from web.model.t_bbgl import query_bbgl_data, get_bbgl_bbdm, get_filter, get_config
from web.model.t_bbgl import query_bbgl_preprocess_detail, update_bbgl_preprocess, delete_bbgl_preprocess
from web.model.t_bbgl import save_bbgl, save_bbgl_header, query_bbgl_header, save_bbgl_task, query_bbgl_task, \
    upd_bbgl_task, push_bbgl_task, run_bbgl_task, stop_bbgl_task, del_bbgl_task, get_bbgl_task_by_tag, get_bbgl_id, \
    get_bbgl_tjrq_type, get_bbgl_tjrq_value, get_imp_data_type
from web.model.t_bbgl import save_bbgl_filter, query_bbgl_filter
from web.model.t_bbgl import save_bbgl_preprocess, query_bbgl_preprocess
from web.model.t_bbgl import save_bbgl_statement, query_bbgl_statement
from web.model.t_bbgl import update_bbgl_filter, delete_bbgl_filter
from web.model.t_bbgl import update_bbgl_header, delete_bbgl_header
from web.model.t_bbgl import update_bbgl_statement, query_bbgl_config, delete_bbgl, export_bbgl_data, get_download, \
    query_bbgl_export, del_export
from web.model.t_dmmx import get_bbtj_db_server
from web.model.t_dmmx import get_dmm_from_dm, get_dmlx_from_dm_bbgl, get_dmm_from_dm_bbgl, get_gather_server, \
    get_bbtj_db_imp_server
from web.model.t_ds import get_ds_by_dsid_by_cdb
from web.utils import base_handler
from web.utils.common import DateEncoder, get_file_size
from web.utils.common import format_sql, fmt_val
from web.utils.mysql_async import async_processer


class bbgl_query(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_query.html",
                    dm_bbdm=await get_bbgl_bbdm())


class bbgl_query_data(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        param = self.get_argument("param")
        param = json.loads(param)
        print('param=', param)
        v_list = await query_bbgl_data(bbdm, param)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_query_dm(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        dm = self.get_argument("dm")
        print('dm=', dm)
        v_list = await get_dmm_from_dm_bbgl(dm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_filter(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await get_filter(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_config(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await get_config(bbdm)
        print('v_list=', v_list, type(v_list))
        v_json = json.dumps(v_list, cls=DateEncoder)
        self.write(v_json)


class bbgl_add(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_add.html",
                    db_server=await get_bbtj_db_server(),
                    dm_filter=await get_dmm_from_dm('42'),
                    dm_select_cfg=await get_dmlx_from_dm_bbgl(),
                    )


class bbgl_add_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        bbmc = self.get_argument("bbmc")
        dsid = self.get_argument("dsid")
        db = self.get_argument("db")
        v_list = await save_bbgl(bbdm, bbmc, dsid, db, self.userid)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_add_header_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        name = self.get_argument("name")
        width = self.get_argument("width")
        v_list = await save_bbgl_header(bbdm, name, width)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_add_filter_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        item = self.get_argument("item")
        cfg = self.get_argument("cfg")
        notnull = self.get_argument("notnull")
        is_range = self.get_argument("is_range")
        rq_range = self.get_argument("rq_range")
        is_like = self.get_argument("is_like")
        v_list = await save_bbgl_filter(bbdm, filter_name, filter_code, filter_type, item, cfg, notnull, is_range,
                                        rq_range, is_like)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_add_preprocess_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        statement = self.get_argument("statement")
        description = self.get_argument("description")

        print('bbgl_add_preprocess_save=', bbdm, statement, description)
        print('bbgl_add_preprocess_save2=', bbdm)
        print('bbgl_add_preprocess_save3=', statement)
        print('bbgl_add_preprocess_save=4', description)
        v_list = await save_bbgl_preprocess(bbdm, statement, description)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_add_statement_save(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        statement = self.get_argument("statement")
        v_list = await save_bbgl_statement(bbdm, statement)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_header_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_header(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_filter_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_filter(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_preprocess_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_preprocess(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_statement_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_statement(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_header(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        name = self.get_argument("name")
        width = self.get_argument("width")
        v_list = await update_bbgl_header(bbdm, xh, name, width)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_delete_header(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        v_list = await delete_bbgl_header(bbdm, xh)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_filter(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        filter_name = self.get_argument("name")
        filter_code = self.get_argument("code")
        filter_type = self.get_argument("type")
        item = self.get_argument("item")
        cfg = self.get_argument("cfg")
        notnull = self.get_argument("notnull")
        is_range = self.get_argument("is_range")
        rq_range = self.get_argument("rq_range")
        is_like = self.get_argument("is_like")
        v_list = await update_bbgl_filter(bbdm, xh, filter_name, filter_code, filter_type, item, cfg, notnull, is_range,
                                          rq_range, is_like)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_delete_filter(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        v_list = await delete_bbgl_filter(bbdm, xh)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_query_preprocess(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        v_list = await query_bbgl_preprocess_detail(bbdm, xh)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_preprocess(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        statement = self.get_argument("statement")
        description = self.get_argument("description")
        v_list = await update_bbgl_preprocess(bbdm, xh, statement, description)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_delete_preprocess(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        xh = self.get_argument("xh")
        v_list = await delete_bbgl_preprocess(bbdm, xh)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_update_statement(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        statement = self.get_argument("statement")
        v_list = await update_bbgl_statement(bbdm, statement)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_change(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_change.html",
                    dm_bbdm=await get_bbgl_bbdm())


class bbgl_query_config(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_config(bbdm)
        v_json = json.dumps(v_list, cls=DateEncoder)
        print('v_json=', v_json)
        self.write(v_json)


class bbgl_query_export(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await query_bbgl_export(bbdm)
        v_json = json.dumps(v_list, cls=DateEncoder)
        print('v_json=', v_json)
        self.write(v_json)


class bbgl_edit(base_handler.TokenHandler):
    async def get(self):
        bbdm = self.get_argument("bbdm")
        dsid = self.get_argument("dsid")
        db = self.get_argument("db")
        print('bbgl_edit=', bbdm)
        self.render("./bbgl/bbgl_edit.html",
                    bbdm=bbdm,
                    dsid=int(dsid),
                    db=db,
                    db_server=await get_bbtj_db_server(),
                    dm_filter=await get_dmm_from_dm('42'),
                    dm_select_cfg=await get_dmlx_from_dm_bbgl(),
                    )


class bbgl_delete(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        v_list = await delete_bbgl(bbdm)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgl_export(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_export.html",
                    dm_bbdm=await get_bbgl_bbdm())


class bbgl_export_data(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbdm = self.get_argument("bbdm")
        param = self.get_argument("param")
        param = json.loads(param)
        path = self.get_template_path().replace("templates", "static")
        res = await export_bbgl_data(bbdm, param, self.userid, path)
        self.write(json.dumps(res))


class bbgl_download(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        res = await get_download(id)
        v_json = json.dumps(res, cls=DateEncoder)
        print(v_json)
        self.write(v_json)


class bbgl_delete_export(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        id = self.get_argument("id")
        res = await del_export(id)
        v_json = json.dumps(res, cls=DateEncoder)
        print(v_json)
        self.write(v_json)


'''任务管理'''


class bbgltaskquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_task.html",
                    gather_servers=await get_gather_server(),
                    gather_bbgl_ids=await get_bbgl_id(),
                    bbgl_tjrq_type=await get_bbgl_tjrq_type(),
                    )


class bbgltask_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        task_tag = self.get_argument("task_tag")
        v_list = await query_bbgl_task(task_tag, self.userid, self.username)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgltaskadd_save(base_handler.TokenHandler):
    async def post(self):
        d_task = {}
        d_task['add_bbgl_task_tag'] = self.get_argument("add_bbgl_task_tag")
        d_task['add_bbgl_task_desc'] = self.get_argument("add_bbgl_task_desc")
        d_task['add_bbgl_server'] = self.get_argument("add_bbgl_server")
        d_task['add_bbgl_id'] = self.get_argument("add_bbgl_id")
        d_task['add_bbgl_tjrq_begin_value'] = self.get_argument("add_bbgl_tjrq_begin_value")
        d_task['add_bbgl_tjrq_end_value'] = self.get_argument("add_bbgl_tjrq_end_value")
        d_task['add_bbgl_tjrq_begin_type'] = self.get_argument("add_bbgl_tjrq_begin_type")
        d_task['add_bbgl_tjrq_end_type'] = self.get_argument("add_bbgl_tjrq_end_type")
        d_task['add_bbgl_task_run_time'] = self.get_argument("add_bbgl_task_run_time")
        d_task['add_bbgl_task_python3_home'] = self.get_argument("add_bbgl_task_python3_home")
        d_task['add_bbgl_task_script_base'] = self.get_argument("add_bbgl_task_script_base")
        d_task['add_bbgl_task_script_name'] = self.get_argument("add_bbgl_task_script_name")
        d_task['add_bbgl_task_api_server'] = self.get_argument("add_bbgl_task_api_server")
        d_task['add_bbgl_task_status'] = self.get_argument("add_bbgl_task_status")
        d_task['add_bbgl_receiver'] = self.get_argument("add_bbgl_receiver")
        d_task['add_bbgl_cc'] = self.get_argument("add_bbgl_cc")
        result = await save_bbgl_task(d_task)
        self.write({"code": result['code'], "message": result['message']})


class bbgltaskupd_save(base_handler.TokenHandler):
    async def post(self):
        d_task = {}
        d_task['upd_bbgl_task_tag'] = self.get_argument("upd_bbgl_task_tag")
        d_task['upd_bbgl_task_desc'] = self.get_argument("upd_bbgl_task_desc")
        d_task['upd_bbgl_server'] = self.get_argument("upd_bbgl_server")
        d_task['upd_bbgl_id'] = self.get_argument("upd_bbgl_id")
        d_task['upd_bbgl_tjrq_begin_value'] = self.get_argument("upd_bbgl_tjrq_begin_value")
        d_task['upd_bbgl_tjrq_end_value'] = self.get_argument("upd_bbgl_tjrq_end_value")
        d_task['upd_bbgl_tjrq_begin_type'] = self.get_argument("upd_bbgl_tjrq_begin_type")
        d_task['upd_bbgl_tjrq_end_type'] = self.get_argument("upd_bbgl_tjrq_end_type")
        d_task['upd_bbgl_task_run_time'] = self.get_argument("upd_bbgl_task_run_time")
        d_task['upd_bbgl_task_python3_home'] = self.get_argument("upd_bbgl_task_python3_home")
        d_task['upd_bbgl_task_script_base'] = self.get_argument("upd_bbgl_task_script_base")
        d_task['upd_bbgl_task_script_name'] = self.get_argument("upd_bbgl_task_script_name")
        d_task['upd_bbgl_task_api_server'] = self.get_argument("upd_bbgl_task_api_server")
        d_task['upd_bbgl_task_status'] = self.get_argument("upd_bbgl_task_status")
        d_task['upd_bbgl_receiver'] = self.get_argument("upd_bbgl_receiver")
        d_task['upd_bbgl_cc'] = self.get_argument("upd_bbgl_cc")
        d_task['upd_bbgl_task_tag_old'] = self.get_argument("upd_bbgl_task_tag_old")
        result = await upd_bbgl_task(d_task)
        self.write({"code": result['code'], "message": result['message']})


class bbgltaskedit_del(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        task_tag = self.get_argument("task_tag")
        result = await del_bbgl_task(task_tag)
        self.write({"code": result['code'], "message": result['message']})


class bbgltask_push(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = push_bbgl_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgltask_run(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = run_bbgl_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgltask_stop(base_handler.TokenHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        tag = self.get_argument("tag")
        api = self.get_argument("api")
        v_list = stop_bbgl_task(tag, api)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgltask_data(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_tag = self.get_argument("task_tag")
        v_list = await get_bbgl_task_by_tag(v_tag)
        v_json = json.dumps(v_list)
        self.write(v_json)


class bbgltask_tjrq_value(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_tjlx = self.get_argument("tjlx")
        v_list = await get_bbgl_tjrq_value(v_tjlx)
        v_json = json.dumps(v_list)
        self.write(v_json)


'''数据导入'''


class bbglimportquery(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbgl/bbgl_import.html",
                    db_server=await get_bbtj_db_imp_server(),
                    imp_data_type=await get_imp_data_type()
                    )


class bbglimport2(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas = self.request.files["file"]
        type = self.get_argument("type")
        dsid = self.get_argument("dsid")
        try:
            ds = await get_ds_by_dsid_by_cdb(dsid, 'hopsonone_analysis')
            await async_processer.exec_sql_by_ds(ds, "delete from hopsonone_analysis.t_bbgl_imp where type='{}'".format(
                type))
            for meta in file_metas:
                file_path = static_path + '/' + 'assets/images/bbgl'
                file_name = file_path + '/' + meta['filename']
                with open(file_name, 'wb') as up:
                    up.write(meta['body'])
                df = pd.read_excel(file_name)
                cols = df.columns.values.tolist()
                tmp = ','.join(['`v{}`'.format(str(i + 1)) for i in range(len(cols))])
                header = "insert into hopsonone_analysis.t_bbgl_imp(`type`,{}) values ('{}',".format(tmp, type)
                for _, item in df.iterrows():
                    values = ''
                    for col in df.columns.values.tolist():
                        values = values + "'" + format_sql(str(item[col])) + "',"
                    sql = header + values[0:-1] + ')'
                    try:
                        await async_processer.exec_sql_by_ds(ds, sql)
                    except:
                        traceback.print_exc()
                        print(sql)
                        raise
                print('{} import sucess'.format(meta['filename']))
            self.write({"code": 0, "file_path": '/static/assets/images/bbgl', "file_name": file_name})
        except Exception as e:
            traceback.print_exc()
            self.write({"code": -1, "message": '导入失败' + str(e)})


class bbglimport(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        static_path = self.get_template_path().replace("templates", "static")
        file_metas = self.request.files["file"]
        type = self.get_argument("type")
        dsid = self.get_argument("dsid")
        try:
            ds = await get_ds_by_dsid_by_cdb(dsid, 'hopsonone_analysis')
            await async_processer.exec_sql_by_ds(ds, "delete from hopsonone_analysis.t_bbgl_imp where type='{}'".format(
                type))
            res = []
            for meta in file_metas:
                file_path = static_path + '/' + 'assets/images/bbgl'
                file_name = file_path + '/' + meta['filename']
                with open(file_name, 'wb') as up:
                    up.write(meta['body'])
                df = pd.read_excel(file_name)
                rows, columns = df.shape
                cols = df.columns.values.tolist()
                vals = ','.join(['%s' for i in range(len(cols) + 1)])
                tmp = ','.join(['`v{}`'.format(str(i + 1)) for i in range(len(cols))])
                sql = "insert into hopsonone_analysis.t_bbgl_imp(`type`,{}) values ({})".format(tmp, vals)
                data = []
                for _, item in df.iterrows():
                    row = [type]
                    for col in df.columns.values.tolist():
                        row.append('' if str(item[col]) == 'nan' else fmt_val(item[col]))
                    data.append(tuple(row))
                await async_processer.exec_sql_by_ds_batch(ds, sql, data)
                print('{} import sucess'.format(meta['filename']))
                res.append((
                    meta['filename'],
                    get_file_size(file_name),
                    rows
                ))
            self.write({"code": 0, "message": res})
        except Exception as e:
            traceback.print_exc()
            self.write({"code": -1, "message": '导入失败' + str(e)})
