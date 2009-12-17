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

from  xenStatus.HTTPRequestHandler import XenHTTPRequestHandler
from BaseHTTPServer import HTTPServer

if __name__ == '__main__':
    try:
        server = HTTPServer(('', 8080), XenHTTPRequestHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
