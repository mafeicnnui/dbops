#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/5 16:08
# @Author : 马飞
# @File : ds.py
# @Software: PyCharm
######################################################################################
#                                                                                    #
#                                   数据库备份管理                                        #
#                                                                                    #
######################################################################################

import json
import tornado.web
from   web.model.t_archive import query_archive,save_archive,get_archive_by_archiveid,upd_archive,del_archive
from   web.model.t_archive import query_archive_log,push_archive_task,run_archive_task,stop_archive_task,query_archive_detail
from   web.model.t_dmmx import get_dmm_from_dm,get_sync_server,get_sync_db_server,get_sync_db_server_by_type
from   web.utils.common import current_rq2
from   web.utils.basehandler import basehandler


class dict_gen(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./archive_query.html")


class redis_migrate(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        archive_id  = self.get_argument("archive_id")
        v_list      = query_archive_detail(archive_id)
        v_json      = json.dumps(v_list)
        print('archive_query_detail=',v_json)
        self.write({"code": 0, "message": v_json})
