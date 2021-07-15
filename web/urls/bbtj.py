#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.kpi  import kpi_item_query,_kpi_item_query,_kpi_item_market,\
        kpi_query,_kpi_query,_kpi_update,_kpi_item_update,_kpi_item_generate,\
        _kpi_item_data_update,kpi_hst_query,_kpi_hst_query,_kpi_hst_export,_kpi_export,kpi_create,_kpi_create

bbtj = [
        (r"/bbtj/kpi/item/query", kpi_item_query),
        (r"/bbtj/kpi/item/_query", _kpi_item_query),
        (r"/bbtj/kpi/market", _kpi_item_market),
        (r"/bbtj/kpi/query", kpi_query),
        (r"/bbtj/kpi/_query", _kpi_query),
        (r"/bbtj/kpi/_update", _kpi_update),
        (r"/bbtj/kpi/item/_update", _kpi_item_update),
        (r"/bbtj/kpi/item/_generate", _kpi_item_generate),
        (r"/bbtj/kpi/item/data/_update", _kpi_item_data_update),

        (r"/bbtj/kpi/hst/query", kpi_hst_query),
        (r"/bbtj/kpi/hst/_query", _kpi_hst_query),
        (r"/bbtj/kpi/hst/_export", _kpi_hst_export),
        (r"/bbtj/kpi/_export", _kpi_export),
        (r"/bbtj/kpi/create", kpi_create),
        (r"/bbtj/kpi/_create", _kpi_create),


 ]
