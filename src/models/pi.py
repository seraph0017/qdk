#!/usr/bin/env python
#encoding:utf-8

from src.models.base import EntityModel
from src.exts import db
from functools import wraps
from flask import jsonify, g


def pi_required(func):
    @wraps(func)
    def _(*args, **kwargs):
        ret = func(*args, **kwargs)
        if Pi.validate_device(g.device_id):
            return ret
        return jsonify(dict(code=-1, message=u"device not found"))
    return _



class Pi(EntityModel):

    __tablename__ = 'pi'

    device_id   = db.Column(db.String(120))
    ip          = db.Column(db.String(120))
    mac_id      = db.Column(db.String(120))
    comment     = db.Column(db.String(120))
    alias       = db.Column(db.String(120))



    @classmethod
    def validate_device(cls, device_id):
        return Pi.query.filter(cls.device_id == device_id).first()


    @classmethod
    def refresh_time(cls, device_id):
        pi = Pi.query.filter(cls.device_id == device_id).first()
        pi.modified_time = db.func.current_timestamp()
        db.session.add(pi)
        db.session.commit()
