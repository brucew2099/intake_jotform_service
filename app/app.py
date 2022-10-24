"""
Imports
"""
import logging
from logging import FileHandler, Formatter
from flask import Flask
from flask_cors import CORS
from .models import setup_db
from .config import config

def setup_logging(app):
    """
    Sets up logging
    """
    formatter = Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('LOGGING LEVEL: INFO')
    return app

def create_app(config_name):
    """
    :param config_name: Running environment
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    setup_db(app)
    app = setup_logging(app)
    CORS(app, resources={'/': {'origins': '*'}})
    return app
