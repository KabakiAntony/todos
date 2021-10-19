"""
reusable functions go in here
"""
import os
import re
import jwt
import random
import string
from functools import wraps
from flask import jsonify, make_response, abort, request
from app.api.models.users import Users, user_schema


KEY = os.getenv("SECRET_KEY")


def custom_make_response(message_or_object, status_code):
    return make_response(jsonify(message_or_object), status_code)


def isValidPassword(password):
    """
    Check if a password meets the requirements for a password
    :param password: is the password that is being checked
    """
    if len(password) < 8:
        abort(
            custom_make_response(
                "Password should be atleast 8 characters",
                400,
            )
        )


def isValidEmail(email):
    """
    Check if an email is a valid email string,
    :param email: is the email string to be checked for validity
    """
    if not re.match(
            r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        # abort("Please enter a valid email addres", 400)
        abort(
            custom_make_response("Please enter a valid email address", 400)
            )
    return True


def check_for_whitespace(data, items_to_check):
    """
    Check if the data supplied has whitespace and
    if the fields are empty, if the  fields are not
    empty strip the whitespace.

    :param data: this is a list holding key value pairs
    that are to be stripped for whitespace
    :param items_to_check: this are singular elements in the data
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
    Get a token from certain routes decode it
    for validity and correctness to acertain that
    the user who possesses it is who they are or is allowed to
    carryout the action that they want to carryout.
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
    Generate a unique user id for the user primary key.
    """
    id = string.ascii_letters + string.digits
    id = "".join(random.choice(id) for i in range(10))
    return id
