#!/usr/bin/env python
#encoding:utf-8

from flask import current_app
from flask_script import Manager, Server, Shell

from src import create_app
from src.exts import db
from src.models import *
from src.services.qdk import QdkService

manager = Manager(create_app)
server = Server(host='0.0.0.0',port=5001,use_debugger=True)

def make_shell_context():
    return dict(
            app     = current_app,
            db      = db,
            QdkService = QdkService,
            )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', server)

@manager.command
def createdb():
    db.create_all()
    k1 = Keng(floor=11,gender=0, name=u"喜士多",location=u"十二楼男厕左",status=0,is_available=False,device_id="fujun")
    k2 = Keng(floor=12,gender=0, name=u"全家",location=u"十二楼男厕中",status=0,is_available=False,device_id="xunan")
    k3 = Keng(floor=12,gender=1, name=u"711",location=u"十二楼男厕右",status=0,is_available=False,device_id="xukaikai")
    p1 = Pi(device_id=u"fujun", ip="1.1.1.1", mac_id=u"jjrddu", alias=u"富军一号")
    p2 = Pi(device_id=u"xunan", ip="1.1.1.2", mac_id=u"jjrddu1", alias=u"富军二号")
    p3 = Pi(device_id=u"xukaikai", ip="1.1.1.3", mac_id=u"jjrddu2", alias=u"富军三号")
    db.session.add(k1)
    db.session.add(k2)
    db.session.add(k3)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()

@manager.command
def updaterecord():
    QdkService.update_record()



@manager.command
def dropdb():
    db.drop_all()

@manager.command
def initdb():
    dropdb()
    createdb()

if __name__ == "__main__":
    manager.run()