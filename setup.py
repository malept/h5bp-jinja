#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

requires = []
extras = {
    'argcomplete': ['argcomplete'],
}

if sys.version_info < (2, 7):
    requires.append('argparse')

setup(name='h5bp_jinja',
      version='1.0',
      author='Mark Lee',
      packages=['h5bp_jinja'],
      install_requires=requires,
      extras_require=extras)
