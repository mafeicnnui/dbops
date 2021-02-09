#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.afei
# @File : logon.py.py
# @Software: PyCharm

from web.services.logon  import index,main,platform,easylife,logon,logout,logon_check,get_tree,get_time,get_verify,error,lock,heartbeat
from web.services.logon  import unlock,lock_status,forget_password,forget_password_check_user,forget_password_check_auth,forget_password_check_pass

# 功能：主页面API
logon = [
        (r"/login",                          logon),
        (r"/unlock",                         unlock),
        (r"/lock",                           lock),
        (r"/lock_status",                    lock_status),
        (r"/heartbeat",                      heartbeat),
        (r"/logout",                         logout),
        (r"/error",                          error),
        (r"/",                               index),
        (r"/main",                           main),
        (r"/platform",                       platform),
        (r"/easylife",                       easylife),
        (r"/tree",                           get_tree),
        (r"/get_verify",                     get_verify),
        (r"/logon_check",                    logon_check),
        (r"/time",                           get_time),
        (r"/forget_password",                forget_password),
        (r"/forget_password/check_user",     forget_password_check_user),
        (r"/forget_password/check_auth",     forget_password_check_auth),
        (r"/forget_password/check_pass",     forget_password_check_pass),

]