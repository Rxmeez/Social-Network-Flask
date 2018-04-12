from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

import datetime


DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_date = DateTimeField(default=datetime.datetime.now)
    bio = TextField(default="")
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ("-joined_date",)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """Create a new user. """
        try:
            with DATABASE.transaction():
                cls.create(username = username,
                           email = email,
                           password = generate_password_hash(password),
                           is_admin = admin)
        except IntegrityError:
            raise ValueError("User already exists!")


def initialize():
    """Initialize the database"""
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
