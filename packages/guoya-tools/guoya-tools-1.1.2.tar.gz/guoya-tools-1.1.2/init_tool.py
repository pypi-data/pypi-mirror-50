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
    # -*- coding:utf-8 -*-
    # Author : 小吴老师
    # Data ：2019/8/1 11:41
    from tools import shell_tool, yaml_tool
    from tools import os_tool

    ## 先删除，再下载tools和ui工程
    tools_prj = 'c:/guoya/auto_test_init/guoya-tools'
    ui_prj = 'c:/guoya/auto_test_init/guoya-ui-test'
    os_tool.deldir(tools_prj)
    os_tool.deldir(ui_prj)
    os_tool.mkdir(tools_prj)
    os_tool.mkdir(ui_prj)
    cmd = 'git clone https://github.com/LudvikWoo/guoya-tools.git ' + tools_prj
    shell_tool.invoke(cmd)
    cmd = 'git clone https://github.com/LudvikWoo/guoya-ui-test.git ' + ui_prj
    shell_tool.invoke(cmd)

    ## 读取ui初始化配置文件
    y = yaml_tool.get_yaml(ui_prj + '/init_ui_project.yaml')
    ## 复制文件夹
    dirs = y['dirs']
    root_path = os_tool.get_root_path()
    for dir in dirs:
        os_tool.copy_dir(ui_prj + '/' + dir, root_path + '/' + dir)
    ## 复制文件
    files = y['files']
    for file in files:
        os_tool.copy_file(ui_prj + '/' + file, root_path)

if __name__ == '__main__':
    init_ui_project()