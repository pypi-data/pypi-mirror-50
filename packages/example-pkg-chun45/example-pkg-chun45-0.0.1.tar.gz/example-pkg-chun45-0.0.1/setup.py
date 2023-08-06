#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         setup
# Description:  
# Author:       codewc
# Date:         2019/8/18
# -------------------------------------------------------------------------------
import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-chun45",
    version="0.0.1",
    author="wangchun",
    author_email="1164004116@qq.com",
    description="测试发布包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
