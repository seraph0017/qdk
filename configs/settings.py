#!/usr/bin/env python
#encoding:utf-8


from os.path import abspath, dirname, join

PROJECT_NAME                    = "qdk"
DEBUG                           = True
PROJECT_PATH                    = dirname(dirname(abspath(__file__)))
SECRET_KEY                      = '1q2w3e4r'


SQLALCHEMY_DATABASE_URI         = 'mysql://qdk:ZcKrg6xdfKVlI9FY@rm-uf6z6b865h964x5xy.mysql.rds.aliyuncs.com/qdk'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
REDIS_URI                       = 'redis://localhost:6379'

ACCESS_TOKEN_URI                = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}"
CORP_ID                         = "ww2cb3d75879c33965"
CORPSECRET                      = "o09-ai832UfrictpUUJ9X2ziS7LPn7LpZkAjVvdyB2I"


try:
    from configs.local_settings import *
except Exception as e:
    pass