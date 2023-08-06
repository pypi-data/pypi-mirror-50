from PythonZyjTools.Email import config
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
class email_send:
    __instance = None
    sourceofsmtplib =None
    shouobj = None
    fajianreng = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    def __init__(self,configs=''):
        if configs == '' :
            self.fajianreng = config.config_user()
        else:
            # 解析ini文件
            self.fajianreng = config.config_user().jiexi(configs)
        # 创建资源
        if self.sourceofsmtplib == None:
            self.create_source()
    def create_source(self):
        try:
            my_sender=self.fajianreng.my_sender    # 发件人邮箱账号
            my_pass =self.fajianreng.my_pass              # 发件人邮箱密码
            self.my_name = self.fajianreng.my_name
            self.my_sender = self.fajianreng.my_sender
            service_name = self.fajianreng.service_name
            my_port = self.fajianreng.my_port
            is_ssl = self.fajianreng.is_ssl
            if is_ssl != False:
                server=smtplib.SMTP_SSL(service_name, my_port)  # 发件人邮箱中的SMTP服务器，端口是25
            else:
                server=smtplib.SMTP(service_name,my_port)
            server.login(my_sender, my_pass)
            self.sourceofsmtplib = server
        except Exception as e:
            print(e)
            self.sourceofsmtplib = None
        return self
    def send_email(self,obj):
        try:
            self.shouobj = obj
            msg=MIMEText(self.shouobj.texts,'plain','utf-8')
            msg['From']=formataddr([self.my_name,self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=self.shouobj.shoujianrengs            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']=self.shouobj.subjects                # 邮件的主题，也可以说是标题
            self.sourceofsmtplib.sendmail(self.my_sender,msg['To'],msg.as_string())
            return True
        except Exception as identifier:
            print(identifier)
    def close(self):
        if self.sourceofsmtplib != None:
            self.sourceofsmtplib.quit()
            self.sourceofsmtplib = None
            print("邮箱资源已销毁")
            