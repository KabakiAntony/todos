import os
import jwt
import datetime
from app.api import users
from app.api.models import db
from flask import request, abort
from app.api.models.users import Users, user_schema
from werkzeug.security import generate_password_hash
from app.api.utils import (
    check_for_whitespace,
    custom_make_response,
    isValidPassword,
    isValidEmail,
    generate_id,
    token_required
)
from app.api.email_utils import (
    send_mail,
    email_signature,
    verify_email_content,
    button_style,
    password_reset_content
)


# get environment variables
KEY = os.getenv("SECRET_KEY")
VERIFY_EMAIL_URL = os.getenv("VERIFY_EMAIL_URL")
PASSWORD_RESET_URL = os.getenv("PASSWORD_RESET_URL")


@users.route('/users/signup', methods=['POST'])
def create_user():
    """
    given user object (email, password)
    create a system user
    """
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']

        check_for_whitespace(user_data, ["email", "password"])
        isValidEmail(user_data['email'])
        isValidPassword(user_data['password'])

        if Users.query.filter_by(email=user_data["email"]).first():
            abort(409, "User already exists")

        id = generate_id()
        new_user = Users(id=id, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode(
                {
                    "id": id,
                    "exp":
                    datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                },
                KEY,
                algorithm="HS256",
            )

        subject = """Verify your email."""
        content = f"""
        Hey {email.split('.', 1)[0]},
        {verify_email_content()}
        <a href="{VERIFY_EMAIL_URL}?tkn={token.decode('utf-8')}"
        style="{button_style()}">Verify email</a>
        {email_signature()}
        """
        send_mail(email, subject, content)

        return custom_make_response(
            "data", "Your account has been created successfully, Please check\
                your email inbox to verify your email address.", 201)

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@users.route('/users/signin', methods=["POST"])
def user_signin():
    """
    Signin a user into the system.
    """
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']

        check_for_whitespace(user_data, ["email", "password"])
        isValidEmail(email)
        isValidPassword(password)

        user = Users.query.filter_by(email=email).first()
        if not user:
            abort(
                404,
                "User account could not be found,\
                    Please register to use the application.")

        _user = user_schema.dump(user)
        _password = _user["password"]

        if not Users.compare_password(_password, password):
            abort(
                403,
                "Email and or password is incorrect,\
                    please check and try again.")

        token = jwt.encode(
            {
                "id": _user["id"],
                "exp":
                datetime.datetime.utcnow() + datetime.timedelta(minutes=480),
            },
            KEY,
            algorithm="HS256",
        )
        response = custom_make_response(
            "data",
            {
                "message":
                "Signed in successfully preparing your dashboard...",
                "auth_token": token.decode('utf-8'),
            }, 200
        )
        return response

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@users.route('/users/forgot', methods=['POST'])
@token_required
def forgot_password(user):
    """
    Send a password reset link when a user has
    forgotten their password on request.
    """
    try:
        user_data = request.get_json()
        email = user_data['email']

        check_for_whitespace(user_data, ["email"])
        isValidEmail(email)
        user = Users.query.filter_by(email=user_data["email"]).first()
        this_user = user_schema.dump(user)

        if user:
            token = jwt.encode(
                {
                    "id": this_user["id"],
                    # "email": this_user["email"],
                    "exp": datetime.datetime.utcnow() + datetime.
                    timedelta(minutes=30),
                },
                KEY,
                algorithm="HS256",
            )

            subject = """Password Reset Request"""
            content = f"""
            Hey {this_user['email'].split('.', 1)[0]},
            {password_reset_content()}
            <a href="{PASSWORD_RESET_URL}?tkn={token.decode('utf-8')}"
            style="{button_style()}"
            >Reset Password</a>
            {email_signature()}
            """
            send_mail(email, subject, content)

        response = custom_make_response(
            "data", {
                "message": "An email has been sent to the address on record,\
                If you don't receive one shortly, please contact\
                    the site admin.",
            }, 202
        )
        return response

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@users.route('/users/update-password', methods=['PUT'])
@token_required
def update_password(user):
    """
    Update or change the user password
    :param user: a user object will be passed on from
    the decoded token therefore you will be able to access
    various user attributes an id and email uniquely identifying
    the user and therefore updating their password accoringly
    """
    try:
        user_data = request.get_json()
        email = user['email']
        new_password = user_data['password']

        check_for_whitespace(user_data, ["email", "password"])
        isValidEmail(email)
        isValidPassword(new_password)

        Users.query.filter_by(email=user["email"]).update(
            dict(password=f"{generate_password_hash(str(new_password))}")
        )
        db.session.commit()

        # add email sending on successful password change.
        return custom_make_response(
            "data",
            "Your password has been changed successfully.",
            200
        )
    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)
