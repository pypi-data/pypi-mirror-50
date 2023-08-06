import xlrd
import json
import os
import sys
class xlsx_get_json:
    __file_path = ""
    __resource = None
    def __init__(self,file_path=""):
        if file_path != "":
            self.__file_path = file_path
            self.source()
    # 获取sheets表名
    def get_sheets_title(self):
        return self.__resource.sheet_names()
    # 获取资源头
    def source(self):
        self.__resource = xlrd.open_workbook(self.__file_path)   #打开excel文件
        return self
    # 返回一个数组
    def get_data(self,sheet_names=None,title=1,hulue=[0,1]):
        """
        获取数据
        :param sheet_names: sheet页的名字
        :param hulue:忽略第几行
        :param title:列的字段名
        :return:
        """
        if sheet_names == None:
            sheet2 = self.__resource.sheet_by_index(0)
        else:
            sheet2 = self.__resource.sheet_by_name(sheet_names)
        rows = sheet2.row_values(title)   #表示获取第一行
        cols = sheet2.col_values(0)   #表示获取第一列
        data = []
        for i in range(len(cols)):
            data_hang = []
            if i not in hulue:
                for j in range(len(rows)):
                    data_hang.append({rows[j]:sheet2.row_values(i)[j]})
                data.append(data_hang)
        self.data = data
        return self
    # 直接返回数据数组
    def get_data_str(self,sheet_names=None,title=1,hulue=[0,1]):
        """
        格式化字符串 参数请见get_data
        :param sheet_names:
        :param title:
        :param hulue:
        :return:
        """
        self.data = self.get_data(sheet_names,title,hulue).data
        data = self.data
        data_result = []
        for i in data:
            data_result_one = []
            for j in i:
                key = list(j.keys())
                values = list(j.values())
                for k in key:
                    if type(values[0]) == type(1.0)  or type(values[0]) == type(1):
                        data_result_one.append({str(key[0]):str(int(values[0]))})
                    else:
                        data_result_one.append(j)
            data_result.append(data_result_one)
        return data_result
    def get_title(self,sheet_names=None,hang = 0):
        if sheet_names == None:
            sheet2 = self.__resource.sheet_by_index(0)
        else:
            sheet2 = self.__resource.sheet_by_name(sheet_names)
        rows = sheet2.row_values(hang)   #表示获取第一行
        self.actitle = rows
        return self
    def close(self):
        """
        关闭资源
        :return:
        """
        pass