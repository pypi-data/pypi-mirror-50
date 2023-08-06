from PythonZyjTools.DbConnect import mysql_drivers
from PythonZyjTools.Base.getconfig import getconfig
from PythonZyjTools import DbConnect
import os
import time,random,hashlib
class data_mode:
    def __init__(self):
        # 调用父类的构造方法
        data = getconfig(os.path.dirname(DbConnect.__file__)+'/config.ini').get_data()
        self.db = data['mysql']['db']
        self.class_name = self.__class__.__name__
    __data = []
    __listkey = []
    # 获得所有的键
    def get_key(self):
        sql = "select COLUMN_NAME,DATA_TYPE from information_schema.columns where table_schema='%s' and table_name = '%s'"%(self.db,self.class_name )
        data = mysql_drivers.mysql().run(sql)
        data_key=[]
        if data != None:
            for i in data:
                data_key.append([i[0],i[1]])
                self.__listkey.append(i[0])
        self.__data = data_key
        return self.__data
    # 获得所有的值
    def get_data_active(self,where=""):
        self.get_key()
        key_string = ''
        for i in self.__data:
            key_string += self.class_name+'.'+i[0]+','
        if where != "":
            sql = "select "+key_string[0:-1]+" from %s %s"%(self.class_name,where)
        else:
            sql = "select "+key_string[0:-1]+" from %s "%(self.class_name)
        data = mysql_drivers.mysql().run(sql)
        result_data = []
        for i in data:
            result_data_temp={}
            for j in range(len(self.__data)):
                result_data_temp[self.__data[j][0]] = i[j]
            result_data.append(result_data_temp)
        return result_data
    def update(self,ziduan,value,where=""):
        resource = mysql_drivers.mysql()
        if type(value) == type(" "):
            sql = "update "+self.class_name+" set "+ziduan+" = "+"'"+value+"'"+" "+where
            resource.exec_sql(sql)
        elif type(value) == type(1):
            sql = "update "+self.class_name+" set "+ziduan+" = "+str(value)+" "+where
            resource.exec_sql(sql)
        return resource.number
    def insert(self,data):
        self.get_key()
        lie = []
        value=[]
        for i in data:
            if i in self.__listkey:
                if type(data[i]) == type(' '):
                    value.append("'"+data[i]+"'")
                    lie.append(i)
                elif type(data[i]) == type(1):
                    lie.append(i)
                    value.append(data[i])
        sql = "insert into %s ( %s)  value ( %s )"%(self.class_name,",".join(lie),",".join(value))
        resource = mysql_drivers.mysql()
        resource.exec_sql(sql)
        return resource.number
    def close(self):
        # 关闭资源，销毁对象
        pass