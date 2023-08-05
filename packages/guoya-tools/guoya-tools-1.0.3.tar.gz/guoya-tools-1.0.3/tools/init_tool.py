# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/18 20:27
from tools import init_env
from tools import init_project
from tools import os_tool
from tools import request_tool
from tools import yaml_tool
from tools import zip_tool
root_path = os_tool.get_root_path()
################################
# 初始化环境：第三方框架+果芽工具包
################################
# 初始化环境(必须最先执行)
def _init_env():
    init_env.init_api_env()

#########################################
# 初始化工程：目录+配置+脚本
#########################################
def _init_api_project():
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
    _init_api_project()

def init_ui_project():
    yaml_path = root_path+'tools/init_project.yaml'
    content =yaml_tool.get_yaml(yaml_path)

    driver_info = content['init_ui']['chromedriver']
    url = driver_info['url']
    save_path=root_path+driver_info['save_path']
    os_tool.mkdir(save_path)
    save_name=driver_info['save_name']
    unzip_name=driver_info['unzip_name']
    zip_path = save_path+save_name
    unzip_path = save_path+unzip_name
    os_tool.remove(unzip_path)
    request_tool.down_big_file(url, zip_path)
    zip_tool.unzip_file(zip_path, save_path)
    os_tool.remove(zip_path)

    files = content['init_ui']['files']
    for file in files:
        url = file['url']
        save_path = root_path+file['save_path']
        save_name = save_path+file['save_name']
        os_tool.mkdir(save_path)
        request_tool.copy_github_file(url,save_name)

    dirs = content['init_ui']['dirs']
    for dir in dirs:
        os_tool.mkdir(root_path+dir)

if __name__ == '__main__':
    init_ui_project()