#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
#############################################
# File Name: setup.py
# Author: Alex_HuA
# Mail: 787001245@qq.com
# Created Time: 2019-8-1 13:10
#############################################
 
 
from setuptools import setup, find_packages

setup(
  name = "xcproxy",
  version = "2.0.1",
  keywords = ["pip", "xcproxy","XCproxy", "XC", "xc"],
  description = "Xi Ci proxy",
  license = "MPL-2.0",
  author = "Alex_HuA",
  author_email = "",
 
  packages = find_packages(),
  include_package_data = True,
  platforms = "any",
  install_requires = ['requests','bs4']
)