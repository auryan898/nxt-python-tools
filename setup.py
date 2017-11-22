#!/usr/bin/env python

from distutils.core import setup

setup(name='nxt-python-tools',
      version='1.0,0',
      description='Additional tools and utilities that work with the nxt-python package',
      author='Ryan B Au',
      author_email='auryan898@gmail.com',
      url='https://github.com/auryan898/nxt-python-tools',
      download_url='https://github.com/auryan898/nxt-python-tools/archive/0.1.tar.gz',
      keywords=['nxt','nxt-python','lego','mindstorms'],
      packages=['nxttools'],
      scripts=['scripts/nxttools_test'],
      classifiers=[],
     )

print "\n***Please Install python-tk (Tk), inputs (inputs), nxt-python (nxt), and their respective dependencies if you haven't already***"