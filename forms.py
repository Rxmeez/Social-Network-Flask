from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, Email, ValidationError,
                                Length, EqualTo)

from models import User


def name_exists(form, field):
    """Checks if a username already exists. """
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists.")


def email_exists(form, field):
    """Checks if a email already exists. """
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists.")


class RegisterForm(Form):
    """Building the register form. """
    username = StringField(
                'Username',
                validators=[
                    DataRequired(),
                    Regexp(
                        r'^[a-zA-Z0-9_]+$',
                        message=("Username should be one word, letter, "
                                "numbers, and underscores only")
                    ),
                    name_exists
                ]
    )
    email = StringField(
            'Email',
            validators=[
                DataRequired(),
                Email(),
                email_exists
            ]
    )
    password = PasswordField(
                'Password',
                validators=[
                    DataRequired(),
                    Length(min=2),
                    EqualTo('password2', message="Password must match.")
                ]
    )
    password2 = PasswordField(
                'Confirm Password',
                validators=[
                    DataRequired()
                ]
    )


class LoginForm(Form):
    """Building the login form. """
    email = StringField(
            'Email',
            validators=[
                DataRequired(),
                Email()
            ])
    password = PasswordField(
                'Password',
                validators=[
                    DataRequired()
                ]
    )

class PostForm(Form):
    content = TextAreaField(
        "Hey, whats up?",
        validators=[
        DataRequired()
        ])
