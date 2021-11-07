import os
from app.api.utils import custom_make_response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(user_email, the_subject, the_content):
    """send email on relevant user action"""
    message = Mail(
        from_email=("kabaki.antony@gmail.com", "Todos Team"),
        to_emails=user_email,
        subject=the_subject,
        html_content=the_content,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_KEY"))
        sg.send(message)
    except Exception as e:
        custom_make_response(
            "error",
            f"An error occured sending email contact administrator\
                     {e}",
            500,
        )


def verify_email_content():
    """
    Email content that goes into the  verification email
    on account creation.
    """
    content = """
    <br/>
    <br/>
    Welcome, you have successfully created a user account,
    to start using the account please click on the verify email,
    button below and that will be it your account will be ready
    for use.
    <br/>
    Note this link will only be active for one hour.
    <br/>
    <br/>
    """
    return content


def password_reset_content():
    """return the message for reset request email"""
    content = """
    <br/>
    <br/>
    You have received this email, because you requested<br/>
    a password reset link, Click on the reset button below to proceed,<br/>
    If you did not please ignore this email.<br/>
    Note this link will only be active for thirty minutes.
    <br/>
    <br/>
    """
    return content


def email_signature():
    """return email signature"""
    signature = """
    <br/>
    <br/>
    All the best,<br/>
    Todos Admin.
    """
    return signature


def button_style():
    """this returns the style for the button"""
    style = """font-weight:bold;
    background-color: #0096D6;
    border-radius:1.5rem;
    text-decoration: none;
    padding: 7px 28px;
    color:rgb(255, 255, 255);
    margin-top:10px;
    margin-bottom: 10px;
    font-size: 120%;"""
    return style
