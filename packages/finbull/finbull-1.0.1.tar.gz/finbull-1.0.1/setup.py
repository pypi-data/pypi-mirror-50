#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
File: setup.py.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2019-08-01 11:20
"""
import sys

from setuptools import setup

if sys.version_info < (3, 7):
    print('finbull must run in python3.7.+')
    sys.exit(1)

setup(
    name="finbull",
    version="1.0.1",
    packages=["finbull", "finbull.lib"],
    include_package_data=True,
    author="Liqiang Dong",
    author_email="dongliqiang@baidu.com",
    url="https://code.aliyun.com/finsight/FinBull",
    license="The MIT LICENSE (MIT)",
    description="the finbull framework.",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    install_requires=[
        "requests>=2.21.0",
        "pandas>=0.23.4",
        "numpy>=1.15.4",
        "tornado>=4.4.2",
        "tornadis>=0.8.0",
        "configobj>=5.0.6",
        "six>=1.10.0"
    ]
)
