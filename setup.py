#!/usr/bin/env python

from distutils.core import setup

setup(
    name =         'xenStatus',
    version =      '0.1.0',
    description =  'Xen JSON webservice',
    author =       'Javier Aravena Calarmunt',
    author_email = 'javier@aravenas.com',
    license =      'GPLv3',
    packages =     ['xenStatus'],
    scripts =      ['xenStatus.py'],
)

