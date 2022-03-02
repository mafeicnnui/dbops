import json
import logging
import tornado.websocket

from tornado.ioloop import IOLoop
from tornado.iostream import _ERRNO_CONNRESET
from tornado.util import errno_from_exception
from webssh.mysql_sync import sync_processer
from webssh import jwt_auth

BUF_SIZE = 32 * 1024
clients = {}  # {ip: {id: worker}}


def clear_worker(worker, clients):
    ip = worker.src_addr[0]
    workers = clients.get(ip)
    assert worker.id in workers
    workers.pop(worker.id)

    if not workers:
        clients.pop(ip)
        if not clients:
            clients.clear()


def recycle_worker(worker):
    if worker.handler:
        return
    logging.warning('Recycling worker {}'.format(worker.id))
    worker.close(reason='worker recycled')


class Worker(object):
    def __init__(self, loop, ssh, chan, dst_addr,token):
        self.loop = loop
        self.ssh = ssh
        self.chan = chan
        self.dst_addr = dst_addr
        self.fd = chan.fileno()
        self.id = str(id(self))
        self.data_to_dst = []
        self.handler = None
        self.mode = IOLoop.READ
        self.closed = False
        self.command = []
        self.commands = []
        self.logs = []
        self.log = {'cmd':'','log':''}
        self.token=token
        print('Worker->->id->token>>>>',self.id,self.token)

    def __call__(self, fd, events):
        if events & IOLoop.READ:
            self.on_read()
        if events & IOLoop.WRITE:
            self.on_write()
        if events & IOLoop.ERROR:
            self.close(reason='error event occurred')

    def set_handler(self, handler):
        if not self.handler:
            self.handler = handler

    def update_handler(self, mode):
        if self.mode != mode:
            self.loop.update_handler(self.fd, mode)
            self.mode = mode
        if mode == IOLoop.WRITE:
            self.loop.call_later(0.1, self, self.fd, IOLoop.WRITE)

    def on_read(self):
        logging.debug('worker {} on read'.format(self.id))
        logging.debug('worker on read token:{}'.format(self.token))
        try:
            data = self.chan.recv(BUF_SIZE)
        except (OSError, IOError) as e:
            logging.error(e)
            if self.chan.closed or errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close(reason='chan error on reading')
        else:
            logging.debug('{!r} from {}:{}'.format(data, *self.dst_addr))
            if not data:
                self.close(reason='chan closed')
                return

            logging.debug('{!r} to {}:{}'.format(data, *self.handler.src_addr))
            try:
                self.handler.write_message(data, binary=True)
                print('on read:>>>>>>>>>>>>>>>>',str(data,encoding='utf-8'),data)
                self.log['log'] = str(data,encoding='utf-8')
                if  data == b'\r\n':
                    self.logs.append(self.log)
                    logging.debug('log>>>:{!r}'.format(self.log))
                    logging.debug('logs>>>:{!r}'.format(self.logs))
                    self.log = {'cmd': '', 'log': ''}
            except tornado.websocket.WebSocketClosedError:
                self.close(reason='websocket closed')

    def on_write(self):
        logging.debug('worker {} on write'.format(self.id))
        logging.debug('worker on write token:{}'.format(self.token))
        if not self.data_to_dst:
            return

        data = ''.join(self.data_to_dst)
        logging.debug('{!r} to {}:{}'.format(data, *self.dst_addr))

        self.command.append(data)
        logging.debug('command1:{}'.format(self.command))
        if data == '\r':
            logging.debug('command2:{}'.format(''.join(self.command[0:-1])))
            self.commands.append(''.join(self.command[0:-1]))
            self.log['cmd'] = ''.join(self.command[0:-1])
            self.command = []
            logging.debug('commands:{}'.format(self.commands))
            #check token
            result = jwt_auth.parse_payload(self.token)
            print('result=',result)
            if not result["status"]:
               self.close(reason='用户认证失败!')

            state = jwt_auth.get_sessoin_state(result['data']['session_id'])
            if state == '3':
               self.close(reason='用户`{}`已离线!'.format(result['data']['username']))

            if (jwt_auth.check_sess_exists(result['data']['session_id'])) == 0:
                self.close(reason='用户`{}`已注销!'.format(result['data']['username']))


        try:
            sent = self.chan.send(data)
        except (OSError, IOError) as e:
            logging.error(e)
            if self.chan.closed or errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close(reason='chan error on writing')
            else:
                self.update_handler(IOLoop.WRITE)
        else:
            self.data_to_dst = []
            data = data[sent:]
            if data:
                self.data_to_dst.append(data)
                self.update_handler(IOLoop.WRITE)
            else:
                self.update_handler(IOLoop.READ)

    def close(self, reason=None):
        if self.closed:
            return
        self.closed = True

        logging.info(
            'Closing worker {} with reason: {}'.format(self.id, reason)
        )
        if self.handler:
            self.loop.remove_handler(self.fd)
            self.handler.close(reason=reason)
        self.chan.close()
        self.ssh.close()
        logging.info('Connection to {}:{} lost'.format(*self.dst_addr))

        clear_worker(self, clients)
        logging.debug(clients)
