#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from xen.xend.XendClient import server
try:
    import json
except ImportError:
    import simplejson as json

def xen_host_to_dict(xendata):
    """
    Converts an xen style key-value pair into a dictionary
    Doesn't walk the tree but instead just considers all values strings
    """
    host={}
    for i in xendata[1:]:
            host[i[0]] = str(i[1])
    return host

def xen_list_to_dict_list(xendata):
    hosts = []
    for i in xendata:
        hosts.append(xen_host_to_dict(i))
    return hosts

def main():
    hosts = xen_list_to_dict_list(server.xend.domains())
    print json.dumps(hosts)
    return 0

if __name__ == '__main__':
   main()

