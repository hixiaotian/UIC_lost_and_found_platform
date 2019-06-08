from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Broadcast(UserMixin, db.Model):
    __tablename__ = 'broadcast'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploader = db.relationship('User', backref=db.backref('broadcast'))
    title = db.Column(db.String(50), nullable=True, unique=False)
    content = db.Column(db.String(400), nullable=True, unique=False)

    def __repr__(self):
        return self.content