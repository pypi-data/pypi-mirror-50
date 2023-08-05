# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/18 18:24

import subprocess

##############################
# 初始化环境：第三方依赖包+果芽工具包
##############################
def init_api_env():
    cmd = 'pip3 install --upgrade guoya-api-test'
    subprocess.call(cmd, shell=True)
