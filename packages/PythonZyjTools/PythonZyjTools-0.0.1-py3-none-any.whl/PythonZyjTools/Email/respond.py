# coding=UTF-8
from email.utils import formataddr
class email_info:
    shoujianrengs = ''
    subjects = ''
    texts = ''
    def __init__(self):
        pass
    # 收件人是字典会自动保存一个属性收件人列表
    def shoujianreng(self,shoujianreng):
        # 类似于这种
        # shoujianreng = {"zhangyongjian":"1158477063@qq.com","frank":"3062617007@qq.com"}
        shoujianrengstr = ''
        if (type(shoujianreng) is dict):
            for key in shoujianreng :
                shoujianrengstr += formataddr([key,shoujianreng[key]])+','
                self.shoujianrengs = shoujianrengstr[:-1]
        elif(type(shoujianreng) is str):
        # 类似于
        # "zhangxinyao <zhangxinyao@sgepri.sgcc.com.cn>"
            self.shoujianrengs = shoujianreng
        return self
    # 主题内容
    def subject(self,str):
        self.subjects = str
        return self
    # 文件的内容
    def text(self,str):
        self.texts = str
        return self