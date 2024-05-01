# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_wtf import CSRFProtect
import ctypes
import os

dll_path = os.getenv("DLL_PATH", default="C:\\msys64\\mingw64\\bin")
ctypes.CDLL(os.path.join(dll_path, 'libgobject-2.0-0.dll'))
ctypes.CDLL(os.path.join(dll_path, 'libpango-1.0-0.dll'))
ctypes.CDLL(os.path.join(dll_path, 'libfontconfig-1.dll'))
ctypes.CDLL(os.path.join(dll_path, 'libpangoft2-1.0-0.dll'))

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app) 

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
     # Initialize database
    #db.init_app(app)
    
    # Initialize CSRF protection
    #CSRFProtect(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

