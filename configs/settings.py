#!/usr/bin/env python
#encoding:utf-8


from os.path import abspath, dirname, join

PROJECT_NAME                    = "qdk"
DEBUG                           = True
PROJECT_PATH                    = dirname(dirname(abspath(__file__)))
SECRET_KEY                      = '1q2w3e4r'


SQLALCHEMY_DATABASE_URI         = 'mysql://qdk:ZcKrg6xdfKVlI9FY@rm-uf6z6b865h964x5xyo.mysql.rds.aliyuncs.com/qdk'
SQLALCHEMY_TRACK_MODIFICATIONS  = True


try:
    from configs.local_settings import *
except Exception as e:
    pass