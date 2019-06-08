from app.extensions import db
from flask_login import UserMixin


class Group(UserMixin, db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, nullable=False, unique=False, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False, unique=False)

    def __repr__(self):
        return self.id

