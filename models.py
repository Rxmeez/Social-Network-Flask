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

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
        (Post.user << self.following()) |
        (Post.user == self)
        )

    def following(self):
        """The users that we are following. """
        return(
        User.select().join(
            Relationship, on=Relationship.to_user
        ).where(
            Relationship.from_user == self
            )
        )

    def followers(self):
        return(
        User.select().join(
            Relationship, on=Relationship.from_user
        ).where(
            Relationship.to_user == self
            )
        )


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


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = TextField()
    user = ForeignKeyField(User, related_name = 'posts')

    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name="relationship")
    to_user = ForeignKeyField(User, related_name="related_to")

    class Meta:
        database = DATABASE
        indexes=(
        (('from_user', 'to_user'), True),
        )


def initialize():
    """Initialize the database"""
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship,], safe=True)
    DATABASE.close()
