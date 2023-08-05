#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import configparser
import string
import os
import sys

# home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir)
home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0])
#home_dir1 = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.pardir)
#sys.path.append(home_dir + "/lib")
conf_dir = home_dir + '\\conf\\'

#print conf_dir
sys.path.append(conf_dir)

class GetConfigDictClass(configparser.ConfigParser):

    def __init__(self, filename, filepath):
        """
        __init__:初始化该类

        Args:配置文件名字
        Returns:
        Raises:
        Author:work(com@baidu.com)
        """
        configparser.ConfigParser.__init__(self)
        # if os.path.isfile(filename):
        self.filename =  filepath + filename
        print(self.filename)
        configparser.ConfigParser.read(self, self.filename)


if __name__ == '__main__':
    cf = GetConfigDictClass("test.cfg", conf_dir)
    print (cf.sections())
    res = cf.get('Section1', 'foo')
    print (res)
