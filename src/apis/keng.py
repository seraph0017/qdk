#!/usr/bin/env python
#encoding:utf-8

from flask import render_template, redirect, session, flash,\
        request, Blueprint, url_for, current_app, jsonify, g

from src.services.qdk import QdkService
from src.models.pi import pi_required


keng = Blueprint('keng',__name__)


@keng.route('/', methods=['GET'])
def keng_index_handler():
    return jsonify(dict(code=0,message="success",data=QdkService.query_all_keng()))

@keng.route('/hc', methods=['POST'])
@pi_required
def keng_hc_handler():
    ret = QdkService.update_pi_time(g.device_id)
    if ret == 0:
        return jsonify(dict(code=0,message="success"))
    return jsonify(dict(code=2,message=u"service wrong"))


@keng.route('/infrared', methods=['POST'])
def keng_infrared_handler():
    return jsonify(dict(code=0,message="success"))

@keng.route('/ultrasonic', methods=['POST'])
@pi_required
def keng_ultrasonic_handler():
    is_available = request.json.get("is_available")
    print is_available
    ret = QdkService.update_keng_status(g.device_id, is_available)
    if ret == 0:
        return jsonify(dict(code=0,message="success"))
    return jsonify(dict(code=2,message="service wrong"))





    
