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
      entry_points={
          'console_scripts': ['h5bp-jinja = h5bp_jinja.__main__:run'],
      },
      install_requires=requires,
      extras_require=extras)
