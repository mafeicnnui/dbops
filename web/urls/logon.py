#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/5 12:33
# @Author : ma.afei
# @File : logon.py.py
# @Software: PyCharm

from web.services.logon  import index,main,platform,easylife,logon,logout,logon_check,get_tree,get_time,get_verify,error
from web.services.logon  import forget_password,forget_password_check_user,forget_password_check_auth,forget_password_check_pass,update_token,logout_page

# 功能：主页面
logon = [
        (r"/login",                          logon),
        (r"/logout",                         logout),
        (r"/logout_page",                    logout_page),
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
        (r"/refresh_token",                  update_token),


]