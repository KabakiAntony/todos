from flask import Blueprint

todos = Blueprint("todos", __name__, url_prefix="")
users = Blueprint("users", __name__, url_prefix="")
