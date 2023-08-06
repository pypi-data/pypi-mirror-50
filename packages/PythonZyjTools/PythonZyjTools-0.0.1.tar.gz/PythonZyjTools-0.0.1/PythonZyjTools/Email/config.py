# coding=UTF-8
import configparser,os
from PythonZyjTools import Email
from PythonZyjTools.Base.getconfig import getconfig
class config_user:
    def __init__(self):
        self.jiexi()
    def jiexi(self):
        path = os.path.dirname(Email.__file__)+'/config.ini'
        data = getconfig(path).get_data()
        self.configdata = data
        return self
    def __getattr__(self,name):
        if name == 'my_sender':
            return self.configdata['email']['email_address']
        if name == 'my_name':
            return self.configdata['email']['user']
        if name == 'my_pass':
            return self.configdata['email']['password']
        if name == 'service_name':
            return self.configdata['email']['server']
        if name == 'my_port':
            return int(self.configdata['email']['port'])
        if name == 'is_ssl':
            if self.configdata['email']['ssl'] == 'true':
                return True
            else:
                return False