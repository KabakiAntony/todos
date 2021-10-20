import os
from app.api import todos
from app.api.models import db
from flask import request, abort
from app.api.models.users import Users
from werkzeug.security import generate_password_hash
from app.api.utils import (
    check_for_whitespace,
    custom_make_response,
    isValidPassword,
    isValidEmail,
    generate_id
)

# get environment variables
KEY = os.getenv("SECRET_KEY")


@todos.route('/users', methods=['POST'])
def create_user():
    """
    given user object (email, password)
    create a system user
    """
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = generate_password_hash(user_data['password'])

        check_for_whitespace(user_data, ["email", "password"])
        isValidEmail(user_data['email'])
        isValidPassword(user_data['password'])

        if Users.query.filter_by(email=user_data["email"]).first():
            abort(409, "User already exists")

        id = generate_id()
        new_user = Users(id=id, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # add token creation and sending emails for account
        # activation
        return custom_make_response(
            "message", "User created successfully", 201)

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)
