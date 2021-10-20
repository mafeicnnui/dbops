#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : ma.fei
# @File : ds.py
# @Software: PyCharm

import json
from   web.model.t_kpi  import query_kpi_item,query_kpi_item_market,query_kpi,update_kpi,update_item_kpi,\
       generate_item_kpi,update_item_data_kpi,query_kpi_hst,exp_kpi,exp_hst_kpi,query_kpi_task
from   web.model.t_dmmx import get_sync_server
from   web.utils import base_handler

class kpi_item_query(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbtj/kpi_item.html",
                    dm_item_market= await query_kpi_item_market()
                    )

class kpi_create(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbtj/kpi_generate.html",
                    sync_server    = await get_sync_server(),
              )

class _kpi_create(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        task        = self.get_argument("task")
        v_list      = await query_kpi_task(task)
        v_json      = json.dumps(v_list)
        self.write(v_json)


class _kpi_item_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month       = self.get_argument("month")
        market_id   = self.get_argument("market_id")
        v_list      = await query_kpi_item(month,market_id)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class _kpi_item_market(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = await query_kpi_item_market()
        v_json = json.dumps(v_list)
        self.write(v_json)


class kpi_query(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbtj/kpi_query.html",
                    dm_item_market=await query_kpi_item_market()
                    )

class _kpi_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month       = self.get_argument("month")
        market_id   = self.get_argument("market_id")
        v_list      = await query_kpi(month,market_id)
        v_json      = json.dumps(v_list)
        self.write(v_json)

class kpi_hst_query(base_handler.TokenHandler):
    async def get(self):
        self.render("./bbtj/kpi_hst_query.html",
                    dm_item_market=await query_kpi_item_market()
                    )

class _kpi_hst_query(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbrq = self.get_argument("bbrq")
        v_list = await query_kpi_hst(bbrq)
        v_json = json.dumps(v_list)
        self.write(v_json)


class _kpi_hst_export(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        bbrq = self.get_argument("bbrq")
        static_path = self.get_template_path().replace("templates", "static");
        zipfile = await exp_hst_kpi(static_path,bbrq)
        self.write({"code": 0, "message": zipfile})

class _kpi_export(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month = self.get_argument("month")
        market_id = self.get_argument("market_id")
        static_path = self.get_template_path().replace("templates", "static")
        zipfile = await exp_kpi(static_path,month,market_id)
        self.write({"code": 0, "message": zipfile})


class _kpi_update(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month   = self.get_argument("month")
        market_id = self.get_argument("market_id")
        result  = await update_kpi(month,market_id)
        self.write({"code": result['code'], "message": result['message']})


class _kpi_item_update(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month      = self.get_argument("month")
        market_id  = self.get_argument("market_id")
        item_code  = self.get_argument("item_code")
        item_value = self.get_argument("item_value")
        result     = await update_item_kpi(month,market_id,item_code,item_value)
        self.write({"code": result['code'], "message": result['message']})


class _kpi_item_data_update(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month      = self.get_argument("month")
        market_id  = self.get_argument("market_id")
        item_code  = self.get_argument("item_code")
        item_month_value = self.get_argument("item_month_value")
        item_sum_value = self.get_argument("item_sum_value")
        result     = await update_item_data_kpi(month,market_id,item_code,item_month_value,item_sum_value)
        self.write({"code": result['code'], "message": result['message']})


class _kpi_item_generate(base_handler.TokenHandler):
    async def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        month  = self.get_argument("month")
        v_list = await generate_item_kpi(month)
        v_json = json.dumps(v_list)
        self.write(v_json)
