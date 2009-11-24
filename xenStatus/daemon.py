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

from  xenStatus.HTTPRequestHandler import XenHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import signal, os, sys

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

