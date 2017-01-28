# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import dtrans
version = dtrans.__version__

setup(
    name='dtrans',
    version=version,
    author='',
    author_email='prad.ads1990@gmail.com',
    packages=[
        'dtrans',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['dtrans/manage.py'],
)