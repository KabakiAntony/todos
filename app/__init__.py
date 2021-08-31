"""
this is my application
factory
"""
from flask import Flask


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    # app.app_context().push()

    return app