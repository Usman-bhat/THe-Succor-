from flaskapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  nullable=False)
    ph_no = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    about_me = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(), nullable=False)
    img_file = db.Column(db.String(), nullable=False, default='default.jpg')
    post = db.relationship('Posts', backref='author', lazy=True)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(150))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ph_no = db.Column(db.Integer)

