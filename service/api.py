import base
from datetime import datetime
import logging
import time
import threading
import os
import ntplib
import random
import string
from Crypto.Hash import MD5


NTP_SERVER_URL = 'pool.ntp.org'
NTP_TIMEOUT = 1
SYNC_INTERVAL = 0.1
ALPHABETA = [c.encode('ascii') for c in string.ascii_lowercase]
CIPHER_TEXT = 'password'

ntp_offset = None
auth_text = None


def gen_hash(text):
    h = MD5.new()
    h.update(text)
    return h.hexdigest()


class LoadService(base.BaseService):

    def __init__(self, settings):
        super(LoadService, self).__init__([
            (r'/?',      MainHandler),
            (r'/test/?', TestHandler),
            (r'/load/?', LoadHandler),
        ], settings)
        global ntp_offset
        ntp_offset = self._sync_ntp_offset()
        hash_func = MD5.new()
        hash_func.update(CIPHER_TEXT)
        global auth_text
        auth_text = hash_func.hexdigest()

    def _sync_ntp_offset(self):
        while True:
            try:
                new_offset = ntplib.NTPClient().request(NTP_SERVER_URL,
                        timeout=NTP_TIMEOUT).offset
                global ntp_offset
                ntp_offset = new_offset
                break
            except ntplib.NTPException:
                pass
        threading.Timer(SYNC_INTERVAL, self._sync_ntp_offset).start()


class MainHandler(base.BaseHandler):
    def get(self):
        self.response['success'] = 'ok'
        self.write_response()

class TestHandler(base.BaseHandler):
    def post(self):
        auth_token = self.request.headers.get('X-Authentication')
        if gen_hash(self.request.body) == auth_token:
            offset = ntp_offset
            self.response['success'] = 'ok'
            self.response['recv_timestamp'] = time.time() + offset
            self.response['send_timestamp'] = time.time() + offset
            self.write_response()
        else:
            self.send_error(401)


class LoadHandler(base.BaseHandler):
    def post(self):
        size, data = self.read_request('size')
        auth_token = self.request.headers.get('X-Authentication')
        if gen_hash(self.request.body) == auth_token:
            offset = ntp_offset
            payload = b''.join([ALPHABETA[int(random.random() * 26)] for _ in range(size)])
            self.response['payload'] = payload
            self.response['success'] = 'ok'
            self.response['recv_timestamp'] = time.time() + offset
            self.response['send_timestamp'] = time.time() + offset
            self.write_response()
        else:
            self.send_error(401)

