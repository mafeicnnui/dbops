#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : 马飞
# @File : logon.py.py
# @Software: PyCharm

from web.services.minio        import minioquery,minio_query,minioadd,minioadd_save,miniochange,minioedit,minioedit_save,minioedit_del,minioedit_push,minioclone
from web.services.minio        import miniologquery,minio_log_query,miniologanalyze,minio_log_analyze

# 功能：MinIO图片上传API
minio = [
        (r"/minio/query", minioquery),
        (r"/minio/_query", minio_query),
        (r"/minio/add", minioadd),
        (r"/minio/add/save", minioadd_save),
        (r"/minio/change", miniochange),
        (r"/minio/edit", minioedit),
        (r"/minio/edit/save", minioedit_save),
        (r"/minio/edit/del", minioedit_del),
        (r"/minio/edit/push", minioedit_push),
        (r"/minio/clone", minioclone),
        (r"/minio/log/query", miniologquery),
        (r"/minio/log/_query", minio_log_query),
        (r"/minio/log/analyze", miniologanalyze),
        (r"/minio/log/_analyze", minio_log_analyze),
]