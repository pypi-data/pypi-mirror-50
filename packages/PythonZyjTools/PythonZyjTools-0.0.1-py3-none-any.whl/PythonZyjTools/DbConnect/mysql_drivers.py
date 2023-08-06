# -*- coding: utf-8 -*-
import pymysql,datetime,time
from PythonZyjTools.Base.getconfig import getconfig
from PythonZyjTools import DbConnect
import os
class mysql(object):
    __instance  = None
    # mysql资源头
    db = None
    # 影响的行数
    number = None
    def __init__(self):
        self.configdata = getconfig(os.path.dirname(DbConnect.__file__)+"/config.ini").get_data()
        self.ziyuan()
    # 实现单例模式
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    def ziyuan(self):
        try:
            self.db = pymysql.connect(self.configdata['mysql']['host'],self.configdata['mysql']['user'] , self.configdata['mysql']['password'] ,self.configdata['mysql']['db'],int(self.configdata['mysql']['port']))
        except:
            self.db = None
            print("不能连接mysql数据库，请检查mysql数据库情况")
    def run(self,sql=""):
        """
        查询记录
        :param sql:
        :return:
        """
        try:
            cursor = self.db.cursor()
            # 使用 execute()  方法执行 SQL 查询
            print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) + sql)
            self.number = cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchall()
            return data
        except:
            return None
    def run_one(self,sql=""):
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.db.cursor()
            # 使用 execute()  方法执行 SQL 查询
            print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) + sql)
            self.number = cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchone()
            # self.db.close()
            return data
        except:
            return None
    def exec_sql(self,sql=""):
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.db.cursor()
            # 使用 execute()  方法执行 SQL 查询
            print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) + sql)
            self.number = cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            self.db.commit()
            return cursor.rowcount
        except:
            return None
    # 释放资源
    def close(self):
        if self._instance.db != None:
            self._instance.db.close()
            self._instance.db = None











