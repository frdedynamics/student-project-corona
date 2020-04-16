
import logging
import datetime
from src.config import get_config

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from src.authorization import authenticate, identity
from src.resources.model import SampleModel, Model, DefaultValuesList
from src.resources.user import UserRegister, UserList
from src.resources.admin import Admin

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)


# auth
app.secret_key = 'topsecret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=3)
app.config['PROPAGATE_EXCEPTIONS'] = True

# database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///src/data.db'


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth with {"username": "john", "password": "hello"}

# resources
api.add_resource(SampleModel, '/model/<string:model_name>/sample')
api.add_resource(Model, '/model/<string:model_name>')
api.add_resource(DefaultValuesList, '/models')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(Admin, '/admin/<string:username>')


if __name__ == '__main__':
    from src.database import db
    _LOGGER.debug('Starting')
    db.init_app(app)
    app.run()
