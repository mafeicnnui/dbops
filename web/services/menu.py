#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/19 16:03
# @Author : 马飞
# @File : menu.py
# @Software: PyCharm

######################################################################################
#                                                                                    #
#                                   菜单管理                                          #
#                                                                                    #
######################################################################################
import json
import tornado.web
from web.model.t_xtqx  import init_menu,query_menu,get_parent_menus,save_menu,get_menu_by_menuid,upd_menu,del_menu,check_menu
from web.utils.basehandler import basehandler

class menuquery(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./menu_query.html")

class menu_query(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        qname  = self.get_argument("qname")
        v_list = query_menu(qname)
        v_json = json.dumps(v_list)
        self.write(v_json)

class menu_init(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        v_list = init_menu();
        v_dict = {"data": v_list}
        v_json = json.dumps(v_dict)
        self.write(v_json)

class menuadd(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./menu_add.html",
                    menus=get_parent_menus())

class menuadd_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        d_menu={}
        d_menu['name']       = self.get_argument("name")
        d_menu['url']        = self.get_argument("url")
        d_menu['status']     = self.get_argument("status")
        d_menu['parent_id']  = self.get_argument("parent_id")
        result = check_menu(d_menu)
        if result['code']=='0':
           result=save_menu(d_menu)
           self.write({"code": result['code'], "message": result['message']})
        else:
           self.write({"code": result['code'], "message": result['message']})

class menuchange(basehandler):
    @tornado.web.authenticated
    def get(self):
        self.render("./menu_change.html")

class menuedit(basehandler):
    @tornado.web.authenticated
    def get(self):
        menuid=self.get_argument("menuid")
        d_menu=get_menu_by_menuid(menuid)
        self.render("./menu_edit.html",
                     menuid    = d_menu['menuid'],
                     name      = d_menu['name'],
                     status    = d_menu['status'],
                     url       = d_menu['url'],
                     parent_id = d_menu['parent_id'],
                     menus     = get_parent_menus()
                    )

class menuedit_save(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        d_menu={}
        d_menu['menuid']    = self.get_argument("menuid")
        d_menu['name']      = self.get_argument("name")
        d_menu['url']       = self.get_argument("url")
        d_menu['status']    = self.get_argument("status")
        d_menu['parent_id'] = self.get_argument("parent_id")
        result=upd_menu(d_menu)
        self.write({"code": result['code'], "message": result['message']})

class menuedit_del(basehandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        menuid  = self.get_argument("menuid")
        result=del_menu(menuid)
        self.write({"code": result['code'], "message": result['message']})
