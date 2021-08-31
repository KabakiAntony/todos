"""
this is my application
factory
"""
from config import DevelopmentConfig
from flask import Flask


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig())
    app.app_context().push()

    return app