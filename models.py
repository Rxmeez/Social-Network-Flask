import datetime

from peewee import *

DATABASE = SqliteDatebase("social.db")

class User(Model):
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_date = DateTimeField(default=datetime.datetime.now)
    bio = TextField(default="")
    is_admin = BooleanField(default=False)

    class Meta():
        database = DATABASE
        order_by = (-joined_date)
