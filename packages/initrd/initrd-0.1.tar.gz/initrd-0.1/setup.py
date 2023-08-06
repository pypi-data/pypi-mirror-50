#!/usr/bin/env python
from setuptools import setup

setup(name='initrd',
      version='0.1',
      description='Linux initrd utilities',
      author='bifferos',
      author_email='bifferos@gmail.com',
      url='https://github.com/bifferos/initrd/',
      license="LGPLv2",
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
      ],
      keywords='inird cpio linux',
      py_modules=['initrd']
     )