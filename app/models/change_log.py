from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Change(UserMixin, db.Model):
    __tablename__ = 'change_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    changer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, nullable=True)
    item_name = db.Column(db.String(50), nullable=True, unique=False)
    changer = db.relationship('User', backref=db.backref('change_log', lazy='dynamic'))
    method = db.Column(db.String(50), nullable=False, unique=False)
    content = db.Column(db.String(100), nullable=True, unique=False)

    def __repr__(self):
        return self.content