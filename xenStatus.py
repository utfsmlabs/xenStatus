#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Copyright 2009 Javier Aravena Claramunt.
#
# This file is part of XenStatus.
#
# XenStatus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# XenStatus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XenStatus.  If not, see <http://www.gnu.org/licenses/>.


try:
    import json
except ImportError:
    import simplejson as json

from xen.xend.XendClient import server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import signal, os, sys


class XenHTTPRequestHandler(BaseHTTPRequestHandler):
    def prettyprint_json(s):
        return '\n'.join([l.rstrip()
            for l in  json.dumps(
                s, indent=4, sort_keys=True).splitlines()
            ])
        prettyprint_json = staticmethod(prettyprint_json)

    def get_json_list(self):
        vms = server.xend.domains()
        self.send_response(200)
        self.send_header("Content-Type", "text/x-json")
        self.end_headers()
        server_list = map(
                lambda x: filter( lambda x: x[0] == 'name', x)[0][1],
                server.xend.domains())
        self.wfile.write(self.prettyprint_json(server_list))
        self.wfile.close()

    def get_404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("OMG! You broke XenStatus!")
        self.wfile.close()

    def dispatch(self):
        if(self.path=='/list.json'):
            return self.get_json_list
        else:
            return self.get_404
    def do_GET(self):
        self.dispatch()()

def sigHandler(signum, frame):
    os.remove(pidFile)
    print 'SIGTERM received, shutting down server'
    sys.exit(0)

def main():
    f = open(pidFile, 'w')
    f.write(str(os.getpid()))
    f.close()
    signal.signal(signal.SIGTERM, sigHandler)
    try:
        server = HTTPServer(('', 8080), XenHTTPRequestHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
    os.remove(pidFile)
    return 0

pidFile = '/var/run/xen-list.pid'
if __name__ == '__main__':
    sys.exit(main())

