import time
import logging

import base


class MBRService(base.BaseService):
    def __init__(self, settings):
        super(MBRService, self).__init__([
            (r'/?',              MainHandler),
            (r'/apply/?',        ApplyHandler),
            (r'/status/([^/]+)', StatusHandler),
        ], settings)


class MainHandler(base.BaseHandler):
    def get(self):
        self.response['success'] = 'ok'
        self.write_response()


class ApplyHandler(base.BaseHandler):

    def get(self):
        """ Get all the existing mortgages.
        """
        self.response['mortgages'] = []
        for r in self.db.mbr.apply.find():
            self.response['mortgages'].append(r)
        self.write_response()

    def post(self):
        """ Submit a mortgage application.
        """
        try:
            name, amount, house_id, data = \
                    self.read_request('name', 'amount', 'house_id')
            id = 'MORT' + str(time.time())[:-3]
            self.db.mbr.apply.insert({
                '_id': id,
                'name': name,
                'amount': amount,
                'house_id': house_id,
                'status': '000'})
            self.response['mort_id'] = id
            self.write_response()
        except base.ErrorSentException:
            pass


class StatusHandler(base.BaseHandler):

    def get(self, mort_id):
        """ Get the state code of the given mortgage application.
        """
        app = self.db.mbr.apply.find_one({'_id': mort_id})
        self.response['status'] = app['status'] if app != None else '-1'
        self.write_response()

    def post(self, mort_id):
        """ Update the mortgage application.
        """
        try:
            send, data = self.read_request('from')
            app = self.db.mbr.apply.find_one({'_id': mort_id})
            status = app['status'] if app != None else -1
            if int(status) < 0:
                self.response['update'] = 'fail'
            else:
                bits = list(status)
                if send == 'emp':
                    bits[0] = '1'
                elif send == 'ins':
                    bits[1] = '1'
                elif send == 'mun':
                    bits[2] = '1'
                new_status = ''.join(bits)
                self.db.mbr.apply.update_one({'_id': mort_id}, {
                    "$set": { "status": new_status }
                })
                self.response['update'] = 'success'
            self.write_response()
        except base.ErrorSentException:
            pass
