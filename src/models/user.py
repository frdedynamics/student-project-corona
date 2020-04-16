from __future__ import annotations

from src.database import db
from src.models.admin import AdminModel


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'user': self.username, 'is_admin': (self.is_admin() is not None)}

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return AdminModel.find_by_id(self.id)

    @classmethod
    def find_by_username(cls, username) -> UserModel:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) -> UserModel:
        return cls.query.get(_id)
