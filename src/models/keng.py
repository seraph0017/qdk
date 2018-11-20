#!/usr/bin/env python
#encoding:utf-8

from src.models.base import EntityWithNameModel
from src.exts import db
from sqlalchemy import desc




class Keng(EntityWithNameModel):

    __tablename__ = 'keng'

    comment         = db.Column(db.String(120))
    gender          = db.Column(db.Integer)
    location        = db.Column(db.String(120))
    status          = db.Column(db.Boolean())
    duration        = db.Column(db.String(120))
    is_available    = db.Column(db.Boolean())
    device_id       = db.Column(db.String(120))


    @classmethod
    def query_all(cls):
        return cls.query.all()


    @classmethod
    def refresh_is_available(cls, device_id, is_available):
        keng = cls.query.filter(cls.device_id == device_id).first()
        keng.is_available = is_available
        db.session.add(keng)
        db.session.commit()

    @classmethod
    def get_now_is_available(cls):
        ret = cls.query.order_by(desc(cls.modified_time)).first()
        return ret.is_available
