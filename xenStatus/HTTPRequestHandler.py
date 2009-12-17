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
    """
    Request Handler for use with BaseHTTPServer that serves
    Information on the xen domains running in the machine
    using JSON.
    """
    def prettyprint_json(s):
        """
        returns indented json
        """
        return '\n'.join([l.rstrip()
            for l in  json.dumps(
                s, indent=4, sort_keys=True).splitlines()
            ])
    prettyprint_json = staticmethod(prettyprint_json)

    def get_json_list(self):
        """
        Handles a request for the list of hosts
        """
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
        """
        Default case, handles url misses
        """
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("OMG! You broke XenStatus!")
        self.wfile.close()

    def do_GET(self):
        """
        Dispatches the responsability of a request to different methods
        depending on the path the client asked for.
        """
        if(self.path=='/list.json'):
            self.get_json_list()
        else:
            self.get_404()

