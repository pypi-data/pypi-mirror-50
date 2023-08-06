#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: mithril
# Created Date: 2019-08-14 14:17:12
# Last Modified: 2019-08-14 14:20:50


# -*- coding: utf-8 -*-
# @Author: mithril



import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='airflow_env_patch',
    version='0.1',

    description='airflow_env_patch',
    long_description=long_description,

    author='Mithril',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='airflow',

    packages=find_packages(),
    
)