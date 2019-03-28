from app import app, db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    emails = db.relationship('Email', backref=db.backref('user', lazy='joined'))
    favorites = db.relationship('Favorites', backref=db.backref('user', lazy='joined'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Email(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    time = db.Column(db.DateTime, default=datetime.now().date())

class Favorites(db.Model):
    save_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer)
    title = db.Column(db.String(500))
    artist = db.Column(db.String(500))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
