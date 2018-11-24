#!/usr/bin/env python

import os
from setuptools import setup

from fastrq import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(name='fastrq',
      version=__version__,
      author='LI Mengxiang',
      author_email='limengxiang876@gmail.com',
      maintainer='LI Mengxiang',
      maintainer_email='limengxiang876@gmail.com',
      url='https://github.com/limen/fastrq',
      description='Queue, Stack and Priority Queue built on Redis',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['fastrq'],
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      install_requires=[
        'redis',
      ],
      tests_require=[
        'pytest',
      ],
      license='MIT',
      platforms=['any'],
     )
