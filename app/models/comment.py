from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Comment(UserMixin, db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploader = db.relationship('User', backref=db.backref('comment'))
    comment_item = db.Column(db.Integer, db.ForeignKey('items.id'))
    content = db.Column(db.String(400), nullable=True, unique=False)

    def __repr__(self):
        return self.content
