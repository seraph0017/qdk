#!/usr/bin/env python
#encoding:utf-8

from src.models.base import EntityModel
from src.exts import db




class History(EntityModel):

    __tablename__ = 'history'

    ttype           = db.Column(db.String(120))
    device_id       = db.Column(db.String(120))
    is_available    = db.Column(db.Boolean())


    @classmethod
    def add_new_record(cls, device_id, ttype, is_available):
        h = cls(ttype = ttype, device_id = device_id, is_available = is_available)
        db.session.add(h)
        db.session.commit()


    @classmethod
    def query_latast_ultrasonic(cls):
        pass
