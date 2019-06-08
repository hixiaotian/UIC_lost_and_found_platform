from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Category(UserMixin, db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=False)

    def __repr__(self):
        return self.name