from __future__ import annotations

from src.database import db


class AdminModel(db.Model):
    __tabelname__ = 'admin'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    access_level = db.Column(db.Integer, nullable=False)

    user = db.relationship('UserModel')

    def __init__(self, user_id, access_level):
        self.user_id = user_id
        self.access_level = access_level

    def json(self):
        return {'admin': self.user.username, 'access_level': self.access_level}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, user_id) -> AdminModel:
        return cls.query.get(user_id)
