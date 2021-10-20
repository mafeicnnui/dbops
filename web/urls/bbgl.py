#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.fei
# @File : logon.py.py
# @Software: PyCharm

from web.services.bbgl  import bbgl_add,bbgl_add_save,bbgl_add_header_save,bbgl_header_query
from web.services.bbgl  import bbgl_add_filter_save,bbgl_filter_query
from web.services.bbgl  import bbgl_add_preprocess_save,bbgl_preprocess_query
from web.services.bbgl  import bbgl_add_statement_save,bbgl_statement_query
from web.services.bbgl  import bbgl_query,bbgl_query_data,bbgl_filter,bbgl_config
from web.services.bbgl  import bbgl_update_header,bbgl_delete_header
from web.services.bbgl  import bbgl_update_filter,bbgl_delete_filter
from web.services.bbgl  import bbgl_query_preprocess,bbgl_update_preprocess,bbgl_delete_preprocess,bbgl_update_statement
from web.services.bbgl  import bbgl_change,bbgl_query_config
from web.services.bbgl  import bbgl_edit,bbgl_delete,bbgl_export,bbgl_query_export,bbgl_export_data,bbgl_download,bbgl_delete_export

bbgl = [
        # 报表定义
        (r"/bbgl/add", bbgl_add),
        (r"/bbgl/add/save", bbgl_add_save),

        (r"/bbgl/add/header/save", bbgl_add_header_save),
        (r"/bbgl/header/query", bbgl_header_query),

        (r"/bbgl/add/filter/save", bbgl_add_filter_save),
        (r"/bbgl/filter/query", bbgl_filter_query),

        (r"/bbgl/add/preprocess/save", bbgl_add_preprocess_save),
        (r"/bbgl/preprocess/query", bbgl_preprocess_query),

        (r"/bbgl/add/statement/save", bbgl_add_statement_save),
        (r"/bbgl/statement/query", bbgl_statement_query),

        (r"/bbgl/update/header", bbgl_update_header),
        (r"/bbgl/delete/header", bbgl_delete_header),

        (r"/bbgl/update/filter", bbgl_update_filter),
        (r"/bbgl/delete/filter", bbgl_delete_filter),

        (r"/bbgl/query/preprocess", bbgl_query_preprocess),
        (r"/bbgl/update/preprocess", bbgl_update_preprocess),
        (r"/bbgl/delete/preprocess", bbgl_delete_preprocess),
        (r"/bbgl/update/statement", bbgl_update_statement),

        # 报表查询
        (r"/bbgl/query", bbgl_query),
        (r"/bbgl/query/data", bbgl_query_data),
        (r"/bbgl/filter", bbgl_filter),
        (r"/bbgl/config", bbgl_config),

        # 报表维护
        (r"/bbgl/change", bbgl_change),
        (r"/bbgl/query/config", bbgl_query_config),
        (r"/bbgl/edit", bbgl_edit),
        (r"/bbgl/delete", bbgl_delete),

        # 报表导出
        (r"/bbgl/export", bbgl_export),
        (r"/bbgl/query/export", bbgl_query_export),
        (r"/bbgl/export/data", bbgl_export_data),
        (r"/bbgl/download", bbgl_download),
        (r"/bbgl/delete/export", bbgl_delete_export),

]
