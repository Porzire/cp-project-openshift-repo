#!/usr/bin/env python

import logging
import ssl
from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado.options import options as opts

import service


class Service(object):

    def __init__(self):
        self._webapp = service.LoadService({'debug': True})

    def start(self, port, ip):
        print port
        print type(port)
        print ip
        print type(ip)
        self._webapp.listen(port, ip)
        try:
            logging.info('Initialize service.')
            ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            logging.info('Terminate service.')


service = Service()


if __name__ == '__main__':
    service.start(8000, 'localhost')

