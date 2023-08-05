# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/18 20:27
from tools import init_env
from tools import init_project


################################
# 初始化环境：第三方框架+果芽工具包
################################
# 初始化环境(必须最先执行)
def _init_env():
    init_env.init_api_env()

#########################################
# 初始化工程：目录+配置+脚本
#########################################
def _init_project():
    # 初始化工程目录
    init_project.init_dirs()
    # 　初始化配置文件
    init_project.init_config()
    # 初始化allure
    init_project.ini_allure()
    # 初始化演示demo
    init_project.init_test_demo()
    # 初始化excel模板
    init_project.init_data()
    # 初始化conftest模板
    init_project.init_conftest()
    # 初始化run.py
    init_project.ini_run()
    # 初始化git
    init_project.init_git()

def init_api_project():
    _init_env()
    _init_project()

if __name__ == '__main__':
    init_api_project()