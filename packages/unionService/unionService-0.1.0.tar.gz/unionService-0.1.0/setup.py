#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: harrett
# Mail: harrett@163.com
# Created Time:  2019-08-05 17:25:34 PM
#############################################


from setuptools import setup, find_packages

setup(
    name = "unionService",
    version = "0.1.0",
    keywords = ("union", "taobao", "jd", "jingdong"),
    description = "alibaba taobao & jd union service",
    long_description = "alibaba taobao & jd union service, a part of haoyouhui project",
    license = "MIT Licence",

    url = "https://github.com/harrett/unionService.git",
    author = "harrett",
    author_email = "harrett@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['scrapy', 'furl']
)
