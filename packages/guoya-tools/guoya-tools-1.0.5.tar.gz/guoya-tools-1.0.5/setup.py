# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/15 10:46
# !/usr/bin/python

from distutils.core import setup

setup(
    name="guoya-tools",  # 这里是pip项目发布的名称
    version="1.0.5",  # 版本号，数值大的会优先被pip
    keywords=["tools", "auto-test"],
    description="to simplify auto test",
    long_description="A tools package,to simplify develope auto test",
    license="MIT Licence",

    url="https://github.com/LudvikWoo/guoya-tools",  # 项目相关文件地址，一般是github
    author="wuling",
    author_email="wuling@guoyasoft.com",

    packages=['tools'],
    platforms="python",
    install_requires=[
        'pinyin==0.4.0',
        'PyMySQL==0.9.3',
        'requests==2.22.0',
        'xlrd==1.2.0',
        'xlwt==1.3.0',
        'selenium==3.141.0',
        'pyyaml==5.1.1',
        'allure-pytest==2.7.0',
        'pytest==5.0.1'
    ]
)