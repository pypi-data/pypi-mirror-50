from flask_login import UserMixin

from flask_app.app import db


class User(UserMixin, db.Document):
    """A user that uses this site."""
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    passwordHash = db.StringField()
