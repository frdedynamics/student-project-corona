from __future__ import annotations

import logging

from src.database import db
from src.models.admin import AdminModel

_LOGGER = logging.getLogger(__name__)


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    plots = db.relationship('PlotModel', lazy='dynamic')  # type: list

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'user': self.username, 'is_admin': (self.is_admin() is not None),
                'plots': [plot.id for plot in self.plots]}

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

    @classmethod
    def set_master_admin(cls, password, access_level) -> bool:
        _LOGGER.debug("Checking master admin..")
        master_admin = UserModel.find_by_username("admin")
        if not master_admin:
            _LOGGER.debug("No master admin set, creating new..")
            user = UserModel("admin", password)
            user.save()
            master_admin = AdminModel(user.id, access_level)
            master_admin.save()
            _LOGGER.debug(f"Admin 'admin' set with password '{password}'.")
            return True

        else:
            _LOGGER.debug("Already set.")
            return False
