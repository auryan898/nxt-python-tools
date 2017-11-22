#!/usr/bin/env python

from distutils.core import setup

setup(name='nxt-python-tools',
      version='1.0,0',
      description='Additional tools and utilities that work with the nxt-python package',
      author='Ryan B Au',
      author_email='auryan898@gmail.com',
      # url='',
      packages=['nxttools'],
      scripts=['scripts/nxttools_test'],
     )