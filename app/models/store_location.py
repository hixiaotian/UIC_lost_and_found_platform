from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Storage(UserMixin, db.Model):
    __tablename__ = 'store_location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(50), nullable=False, unique=False)
    available_time = db.Column(db.String(50), nullable=True, unique=False)
    phone_number = db.Column(db.String(50), nullable=True, unique=False)
    # admin = db.relationship('User', backref=db.backref('store_location'))
    # store_item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # items = db.relationship('Item', backref=db.backref('store_location', lazy='dynamic'))
    pic = db.Column(db.String(64), default='img/a1.jpg')

    def __repr__(self):
        return self.id