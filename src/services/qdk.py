#!/usr/bin/env python
#encoding:utf-8

from src.models import *
from src.decorator import transfer2json


class QdkService(object):

    @classmethod
    @transfer2json("?id|!floor|!name|!comment|!location|$status|!duration|$is_available|!gender")
    def query_all_keng(cls):
        return Keng.query_all()

    @classmethod
    def update_pi_time(cls, device_id):
        Pi.refresh_time(device_id)
        History.add_new_record(device_id, ttype = "hc")
        return 0

    @classmethod
    def update_keng_status(cls, device_id, is_available):
        Keng.refresh_is_available(device_id, is_available)
        History.add_new_record(device_id, ttype = "ultrasonic", is_available=is_available)
        return 0


    @classmethod
    def update_record(cls):
        device_id, is_available = Keng.get_now_is_available()
        mtime = History.query_latast_ultrasonic(device_id, is_available)
        print mtime






