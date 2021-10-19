"""
this is my application
factory
"""
from config import DevelopmentConfig
from flask import Flask
from flask_migrate import Migrate
# blueprint imports here

migrate = Migrate(compare_type=True)


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    # cors configuration here
    app.config.from_object(DevelopmentConfig())

    from app.api.models import db, ma

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    # register blueprints here
    app.app_context().push()

    return app
