#!/usr/bin/env python

from setuptools import setup

setup(name='couch',
      version='1.0.0',
      description='Graphical UI for shuffling names in a game of Four on the Couch',
      author='Ralph Embree',
      author_email='ralph.embree@brominator.org',
      url='https://gitlab.com/ralphembree/couch',
      scripts=[],
      keywords="four couch random names",
      classifiers = [
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
      ],
)
