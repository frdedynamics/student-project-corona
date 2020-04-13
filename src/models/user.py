from __future__ import annotations
from src.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username) -> UserModel:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) -> UserModel:
        return cls.query.filter_by(id=_id).first()
