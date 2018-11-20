#!/usr/bin/env python
#encoding:utf-8

import os

from flask import Flask, render_template, redirect, url_for, g, request

from src.exts import db
from src.apis.keng import keng
from configs import settings
from flask_cors import CORS



DEFAULT_APP_NAME = settings.PROJECT_NAME

DEFAULT_MODULES = (
        (keng,'/keng'),
        )



def create_app(app_name=None,modules=None):
    if app_name is None: app_name = DEFAULT_APP_NAME
    if modules is None: modules = DEFAULT_MODULES
    app = Flask(app_name)
    configure_conf(app)
    configure_exts(app)
    configure_modules(app,modules)
    configure_before_handlers(app)
    return app

def configure_exts(app):
    CORS(app, methods=['POST','GET','OPTION'])
    db.init_app(app)



def configure_conf(app):
    app.config.from_pyfile('configs/settings.py')

def configure_modules(app,modules):
    for module, url_prefix in modules:
        app.register_blueprint(module,url_prefix=url_prefix)

def configure_before_handlers(app):

    @app.before_request
    def auth():
        x_device = request.headers.get("X-device")
        g.device_id = x_device



def configure_logging(app):
    import yaml
    import logging
    import logging.config

    yaml_path = os.path.join(app.config['PROJECT_PATH'], 'configs/logging.yaml')
    if os.path.exists(yaml_path):
        with open(yaml_path, 'rt') as f:
            logging_config = yaml.load(f.read())
        logging.config.dictConfig(logging_config)

    # Flask would use DebugHandler as default.


