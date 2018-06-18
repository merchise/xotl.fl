#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

from __future__ import (division as _py3_division,
                        print_function as _py3_print)
                        # XXX: Don't put absolute imports in setup.py

import os, sys
from setuptools import setup, find_packages

# Import the version from the release module
project_name = str('xopgi.ql')
_current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_current_dir, 'xopgi', 'ql'))
from release import VERSION as version  # noqa

setup(
    name=project_name,
    version=version,
    description="A xotl.ql translator for Odoo ORM",
    long_description=open(
        os.path.join(_current_dir, 'README.rst')).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='',
    author='Merchise Autrement [~º/~]',
    author_email='',
    url='http://www.merchise.org',
    license='GPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['xopgi', ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6,<3.7',
    install_requires=[
        'xoutil>=1.9.4',
        'xoeuf>=0.40',
        'xotl.ql>=0.6.0',
    ],
    entry_points='''
    [xoeuf.addons]
    test_xopgi_ql_integration = xopgi.ql.tests.test_xopgi_ql_integration
    '''
)
