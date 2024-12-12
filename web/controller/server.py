#!/usr/bin/env pythonx
# -*- coding: utf-8 -*-
# @Time    : 2018/6/2 10:48
# @Author  : ma.fei
# @File    : h3bpm_interface.py
# @Software: PyCharm

import asyncio
import os.path
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.options
import tornado.web
from tornado.options import define

from web.utils.urls import urls

from web.webssh import handler
from web.webssh.handler import IndexHandler, WsockHandler, NotFoundHandler
from web.webssh.settings import (
    get_app_settings, get_host_keys_settings, get_policy_setting,
    get_ssl_context, get_server_settings, check_encoding_setting
)

define("port", default=sys.argv[1], help="run on the given port", type=int)


def webssh_handlers():
    loop = tornado.ioloop.IOLoop.current()
    host_keys_settings = get_host_keys_settings(tornado.options.options)
    policy = get_policy_setting(tornado.options.options, host_keys_settings)
    handlers = [
        (r'/ssh', IndexHandler, dict(loop=loop, policy=policy, host_keys_settings=host_keys_settings)),
        (r'/ssh/ws', WsockHandler, dict(loop=loop)),
    ]
    return handlers


class Application(tornado.web.Application):
    def __init__(self):
        ssh = webssh_handlers()
        handlers = urls + ssh
        settings = dict(
            config_file=os.path.join(os.path.dirname(__file__), "../../config/config.json"),
            static_path=os.path.join(os.path.dirname(__file__), "../../static"),
            template_path=os.path.join(os.path.dirname(__file__), "../../templates"),
            cookie_secret="2379874hsdhf0234990sdhsaiuofyasop977djdj",
            xsrf_cookies=False,
            debug=True,
            event_loop=asyncio.get_event_loop(),
            login_url="/login",
            websocket_ping_interval=tornado.options.options.wpintvl,
        )
        ssl_ctx = get_ssl_context(tornado.options.options)
        if ssl_ctx:
            settings.update(ssl_options=ssl_ctx)
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),
                                                max_buffer_size=1073741824,
                                                max_body_size=1073741824)
    http_server.listen(sys.argv[1])
    print('Dbops Server running {0} port ...'.format(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
