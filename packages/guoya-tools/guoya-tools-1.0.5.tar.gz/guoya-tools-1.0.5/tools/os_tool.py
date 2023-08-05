# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/11 18:31
import os



def get_root_path():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)).replace('\\', '/')
    print(root_path)
    print(root_path.find('venv'))
    if root_path.find('venv') > 0:
        root_path=root_path[:root_path.find('venv')-1]
    return root_path+'/'

def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)

def remove(path):
    is_exists = os.path.exists(path)
    if is_exists:
        os.remove(path)

def exists(file_or_path):
    is_exists = os.path.exists(file_or_path)
    return is_exists