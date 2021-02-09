#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.db_inst      import dbinstquery,db_inst_query,db_inst_save,db_inst_update,db_inst_query_by_id,dbinstmgr,get_tree_by_inst,db_inst_sql_query,db_inst_delete,get_inst_tab_ddl,get_inst_idx_ddl,drop_inst_tab
from web.services.db_inst      import dbinstcrtquery,db_inst_crt_query,db_inst_create,db_inst_destroy,db_inst_log,db_inst_manager
from web.services.db_inst      import dbinstparaquery,dbinstpara_query,dbinstparaadd_save,dbinstparaedit_save,dbinstparaedit_del,dbinstoptlogquery,dbinstoptlog_query
from web.services.db_user      import dbuserquery,db_user_query,db_user_save,db_user_update,db_user_delete,db_user_sql,db_user_dbs,db_user_info,db_user_query_by_id
from web.services.db_config    import dbinstcfgquery,db_inst_cfg_query,db_inst_cfg_update

# 功能： 功能：数据库管理
inst = [
        # 功能：数据库管理-新增实例API
        (r"/db/inst/crt/query", dbinstcrtquery),
        (r"/db/inst/crt/_query", db_inst_crt_query),
        (r"/db/inst/save", db_inst_save),
        (r"/db/inst/update", db_inst_update),
        (r"/db/inst/del", db_inst_delete),
        (r"/db/inst/create", db_inst_create),
        (r"/db/inst/destroy", db_inst_destroy),
        (r"/db/inst/log", db_inst_log),
        (r"/db/inst/manager", db_inst_manager),

        # 功能：数据库管理-实例管理API
        (r"/db/inst/query", dbinstquery),
        (r"/db/inst/_query", db_inst_query),
        (r"/db/inst/query/id", db_inst_query_by_id),
        (r"/db/inst/mgr", dbinstmgr),
        (r"/db/inst/sql/_query", db_inst_sql_query),
        (r"/get/inst/tree", get_tree_by_inst),
        (r"/get/inst/tab/ddl", get_inst_tab_ddl),
        (r"/get/inst/idx/ddl", get_inst_idx_ddl),
        (r"/drop/inst/tab", drop_inst_tab),

        # 功能：数据库管理-用户管理API
        (r"/db/user/query", dbuserquery),
        (r"/db/user/query/id", db_user_query_by_id),
        (r"/db/user/_query", db_user_query),
        (r"/db/user/save", db_user_save),
        (r"/db/user/update", db_user_update),
        (r"/db/user/del", db_user_delete),
        (r"/db/user/sql", db_user_sql),
        (r"/db/user/dbs", db_user_dbs),
        (r"/db/user/info", db_user_info),

        # 功能：数据库管理-参数管理API
        (r"/db/inst/para/query", dbinstparaquery),
        (r"/db/inst/para/_query", dbinstpara_query),
        (r"/db/inst/para/add/save", dbinstparaadd_save),
        (r"/db/inst/para/edit/save", dbinstparaedit_save),
        (r"/db/inst/para/edit/del", dbinstparaedit_del),

        # 功能：数据库管理-操作日志API
        (r"/db/inst/opt/log/query", dbinstoptlogquery),
        (r"/db/inst/opt/log/_query", dbinstoptlog_query),

        # 功能：数据库管理-配置管理API
        (r"/db/inst/cfg/query", dbinstcfgquery),
        (r"/db/inst/cfg/_query", db_inst_cfg_query),
        (r"/db/inst/cfg/update", db_inst_cfg_update),
]