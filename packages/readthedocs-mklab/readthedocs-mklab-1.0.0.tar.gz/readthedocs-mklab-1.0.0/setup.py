#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mklab
# Mail: mklabs@163.com
# Created Time:  2019-07-30 10:17:34
#############################################

from setuptools import setup, find_packages           

setup(
    name = "readthedocs-mklab",      
    version = "1.0.0", 
    keywords = ("pip", "readthedocs-mklab","theme"),
    description = "The readthedocs theme for mkdocs,Replacement of Google fonts, etc.",
    long_description = "The readthedocs theme for mkdocs,Replacement of Google fonts, etc.",
    license = "MIT Licence",

    #url = "",     
    author = "mklab",
    author_email = "mklabs@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []       
)
