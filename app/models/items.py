from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
#
# upload = db.Table(
#     "upload",
#     db.Column(db.Integer, db.ForeignKey("user_id")),
#     db.Column(db.Integer, db.ForeignKey("item_id"))
# )


class Item(UserMixin, db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(50), nullable=False, unique=False)
    time = db.Column(db.String(50), nullable=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploader = db.relationship('User', backref=db.backref('items', lazy='dynamic'))
    status = db.Column(db.String(50), nullable=False, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('items'))
    location = db.Column(db.String(50), nullable=True, unique=False)
    description = db.Column(db.String(400), nullable=True, unique=False)
    comment = db.relationship('Comment', backref=db.backref('items'))
    pic = db.Column(db.String(64), default='img/a1.jpg')
    store_location_id = db.Column(db.Integer, db.ForeignKey('store_location.id'), nullable=True)
    store_location = db.relationship('Storage', backref=db.backref('items'))
    # store_location = db.relationship('Storage', backref=db.backref('items',lazy='dynamic'))
    def __repr__(self):
        return self.item_name