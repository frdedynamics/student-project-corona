from __future__ import annotations

import src
from src.database import db


class PlotModel(db.Model):
    __tablename__ = 'plot'
    id = db.Column(db.Integer, primary_key=True)
    cpm = db.Column(db.String(30))
    values = db.Column(db.JSON)
    data = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('UserModel')  # type: src.UserModel

    def __init__(self, cpm: str, values, data, user_id):
        self.cpm = cpm
        self.values = values
        self.data = data
        self.user_id = user_id

    def json(self):
        return {'plot': {
            'user': self.user.username,
            'cpm': self.cpm,
            'values': self.values,
            'data': self.data}
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> PlotModel:
        return cls.query.get(_id)
