import logging

from src.models.user import UserModel
from .config import get_config

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)


def authenticate(username, password):
    _LOGGER.debug("Authenticate..")
    user = UserModel.find_by_username(username)
    if user and password == user.password:
        return user


def identity(payload):
    _LOGGER.debug("Identity..")
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
