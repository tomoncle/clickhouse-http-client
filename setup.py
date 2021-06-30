#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 2021/1/30 15:56
# @Author         : tomoncle
# @File           : setup.py
# @Product        : PyCharm
# @Docs           : 
# @Source         : 

from setuptools import setup, find_packages

setup(
    name='clickhouse-http-client',
    version='1.0.0',
    author='liyuanjun',
    author_email='1123431949@qq.com',
    url='https://github.com/tomoncle/clickhouse-http-client',
    description='clickhouse http client, author liyuanjun',
    long_description=open("README.md", "r", encoding="UTF-8").read(),
    license="MIT",
    install_requires=[
        'requests'
    ],
    packages=find_packages()
)
