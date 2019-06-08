from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Message(UserMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store_location_id = db.Column(db.Integer, db.ForeignKey('store_location.id'))
    sender = db.relationship('User', backref=db.backref('messages'))
    store_location = db.relationship('Storage', backref=db.backref('messages'))
    is_recieve = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(50), nullable=True, unique=False)
    content = db.Column(db.String(400), nullable=True, unique=False)

    def __repr__(self):
        return self.id
