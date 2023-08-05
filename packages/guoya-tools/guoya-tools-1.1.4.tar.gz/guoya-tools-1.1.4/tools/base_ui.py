# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/31 14:56

class BaseUI:
    def __init__(self,driver):
        self.driver = driver

    def get(self,url):
        self.driver.get(url)