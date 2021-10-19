"""
reusable functions go in here
"""
import os
import jwt
import random
import string
from functools import wraps
from flask import jsonify, make_response, abort, request
from app.api.models.users import Users, user_schema


KEY = os.getenv("SECRET_KEY")


def custom_make_response(message_or_object, status_code):
    return make_response(jsonify(message_or_object), status_code)


def isValidPassword(my_password):
    """
    :param my_password is one whose length is to
    be checked.
    """
    if len(my_password) < 8:
        abort(
            custom_make_response(
                "Password should be atleast 8 characters",
                400,
            )
        )


def check_for_whitespace(data, items_to_check):
    """
    check if the data supplied has whitespace
    """
    for key, value in data.items():
        if key in items_to_check and not value.strip():
            abort(
                custom_make_response(
                    "One or more of your fields is empty, please\
                        check and try again.",
                    400
                )
            )
    return True


def token_required(f):
    """
    this token is used to allow the user to access
    certain routes
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user_token = None
        if 'auth_token' in request.headers:
            user_token = request.headers['auth_token']
        if not user_token:
            return custom_make_response("Token is missing", 401)
        try:
            if user_token:
                data = jwt.decode(user_token, KEY, algorithm="HS256")
                current_user = Users.query.filter_by(id=data['id']).first()
                _data = user_schema.dump(current_user)
        except Exception as e:
            # exceptions go to site administrator log and email
            # the user gets a friendly error notification
            return custom_make_response(f"Token {e}", 401)
        return f(_data, *args, **kwargs)
    return decorated


def generate_id():
    """
    this function will generate a unique user id
    """
    id = string.ascii_letters + string.digits
    id = "".join(random.choice(id) for i in range(10))
    return id
