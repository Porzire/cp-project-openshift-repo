#!/usr/bin/env python

import logging
import ssl
from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado.options import options as opts

import service


class Server(object):

    def __init__(self):
        webapp = service.LoadService({'debug': True})
        self._server = httpserver.HTTPServer(webapp)

    def start(self, port, ip):
        self._server.listen(port, ip)
        try:
            logging.info('Initialize service.')
            ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            logging.info('Terminate service.')


server = Server()


if __name__ == '__main__':
    server.start(8000, 'localhost')
