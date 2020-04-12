from src.user import User
from src.config import get_config
import logging

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

users = [  # placeholder for database
    User(1, 'john', 'hello')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    _LOGGER.debug("Authenticate..")
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user


def identity(payload):
    _LOGGER.debug("Identity..")
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)