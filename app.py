#!/usr/bin/env python

import imp
import os


try:
   zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                           'virtenv', 'bin', 'activate_this.py')
   execfile(zvirtenv, dict(__file__ = zvirtenv) )
except IOError:
   pass


if __name__ == '__main__':
   ip   = os.environ['OPENSHIFT_PYTHON_IP']
   port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
   app = imp.load_source('server', 'server.py')

   app.service.start(port, ip)

