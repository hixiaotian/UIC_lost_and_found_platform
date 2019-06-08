from flask import current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    student_id = db.Column(db.Integer, nullable=False)
    true_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=False)
    password_hash = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), default=2)
    group = db.relationship('Group', backref=db.backref('users', lazy='dynamic'))
    storage_id = db.Column(db.Integer, db.ForeignKey('store_location.id'), nullable=True)
    storage = db.relationship('Storage', backref=db.backref('users', lazy='dynamic'))
    last_login = db.Column(db.DateTime, default=datetime.now)
    icon = db.Column(db.String(64), default='img/a3.jpg')
    # Add a backreference to another model
    # Parameter 1: the associated model name
    # backref：Dynamically added fields in the associated model
    # Load mode: dynamic, no load, but provide record query
    # if use one to one，add uselist=Flase
    # posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return self.username

    # Password field protection
    @property
    def password(self):
        raise AttributeError('keyword is Unreadable attribute')

    # Set the password and encrypt the storage
    @password.setter
    def password(self, password):
        #Equivalent to execution  user.password_hash=password
        self.password_hash = generate_password_hash(password)

    # Password check
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# A callback to login authentication, written in the user model
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

