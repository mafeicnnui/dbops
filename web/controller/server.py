#!/usr/bin/env pythonx
# -*- coding: utf-8 -*-
# @Time    : 2018/6/2 10:48
# @Author  : ma.fei
# @File    : h3bpm_interface.py
# @Software: PyCharm

import sys
import asyncio
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.locale
import os.path
from tornado.options  import define
from web.utils.urls   import urls
define("port", default=sys.argv[1], help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls
        settings = dict(static_path = os.path.join(os.path.dirname(__file__), "../../static"),
                        template_path = os.path.join(os.path.dirname(__file__), "../../templates"),
                        cookie_secret = "2379874hsdhf0234990sdhsaiuofyasop977djdj",
                        xsrf_cookies = False,
                        debug = True,
                        event_loop = asyncio.get_event_loop(),
                        login_url = "/login")
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(sys.argv[1])
    print('Dbops Server running {0} port ...'.format(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
