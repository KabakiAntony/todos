"""
this is my application
factory
"""
from config import ProductionConfig
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.api.views.users import users as users_blueprint
from app.api.views.todos import todos as todos_blueprint


migrate = Migrate(compare_type=True)


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_ORIGINS'] = ['*']
    app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
    app.config.from_object(ProductionConfig())

    from app.api.models import db, ma

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(todos_blueprint)
    app.app_context().push()

    return app
