"""
Imports
"""
import os
from os.path import abspath, dirname, join
from dotenv import load_dotenv

class Config():
    """
    Loads the configuration file
    """
    @staticmethod
    def init_app(app):
        """
        Loads the configuration file
        """
        config_file = join(dirname(abspath(__file__)), '.env-local')
        if not os.path.exists(config_file):
            print(f'{app} - Initializing application...')

    basedir = abspath(dirname(__file__))
    load_dotenv(join(basedir, '.env-local'))

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SWAGGER_URL = os.environ.get('SWAGGER_URL')

class DevelopmentConfig(Config):
    """
    Configuration class for the development database.
    """
    DRIVER = os.environ.get('SQLSERVER.DRIVER')
    USER = os.environ.get('SQLSERVER.USER')
    PASSWD = os.environ.get('SQLSERVER.PASSWD')
    HOST = os.environ.get('SQLSERVER.HOST')
    DB = os.environ.get('SQLSERVER.DB')
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PASSWD}@{HOST}/{DB}"

class TestConfig(Config):
    """
    Configuration class for the test database.
    """
    DRIVER = os.environ.get('TEST.SQLSERVER.DRIVER')
    USER = os.environ.get('TEST.SQLSERVER.USER')
    PASSWD = os.environ.get('TEST.SQLSERVER.PASSWD')
    HOST = os.environ.get('TEST.SQLSERVER.HOST')
    DB = os.environ.get('TEST.SQLSERVER.DB')
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PASSWD}@{HOST}/{DB}"

class ProductionConfig(Config):
    """
    Configuration class for the production database.
    """
    DRIVER = os.environ.get('SQLSERVER.DRIVER')
    USER = os.environ.get('SQLSERVER.USER')
    PASSWD = os.environ.get('SQLSERVER.PASSWD')
    HOST = os.environ.get('SQLSERVER.HOST')
    DB = os.environ.get('SQLSERVER.DB')
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PASSWD}@{HOST}/{DB}"

config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
