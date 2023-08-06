# -*- coding: utf-8 -*-
import sys,os
import configparser
"""
获取配置文件信息
"""
class getconfig:
    config_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/config.ini'
    def __init__(self,path=""):
        if path !='':
            self.config_path = path
    def get_data(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, encoding="utf-8")  # 此处是utf-8-sig，而不是utf-8
        return config