#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

try:
    import json
except ImportError:
    import simplejson as json

from xen.xend.XendClient import server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import signal, os, sys


class XenHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        vms = server.xend.domains()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain") #Hacer text/x-jason después
        self.end_headers()
        self.wfile.write('\n'.join(
                         [l.rstrip()
                         for l in  json.dumps(server.xend.domains(),
                                              indent=4,
                                              sort_keys=True).splitlines()
                         ]))
        self.wfile.close

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

