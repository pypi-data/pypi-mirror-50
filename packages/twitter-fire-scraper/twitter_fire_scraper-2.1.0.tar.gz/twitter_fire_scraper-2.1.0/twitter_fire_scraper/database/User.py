from flask_login import UserMixin

from flask_app.start_webserver import db, login_manager


class User(UserMixin, db.Document):
    """A user that uses this site."""
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    passwordHash = db.StringField()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
