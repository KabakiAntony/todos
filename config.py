import os

from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Testing = False
    Debug = False

    database_path = os.environ.get('DATABASE_URL')
    if database_path.startswith("postgres://"):
        database_path = database_path.replace(
            'postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_path


class ProductionConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL').replace(
            'postgres://', 'postgresql://', 1)
