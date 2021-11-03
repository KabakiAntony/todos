"""
this is my application
factory
"""
from config import TestingConfig
from flask import Flask
from flask_migrate import Migrate
from app.api.views.users import users as users_blueprint
from app.api.views.todos import todos as todos_blueprint

migrate = Migrate(compare_type=True)


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object(TestingConfig())

    from app.api.models import db, ma

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(todos_blueprint)
    app.app_context().push()

    return app
