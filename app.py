import logging
import datetime
from src.config import get_config

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from src.authorization import authenticate, identity
from src.resource.model import SampleModel, Model, DefaultValues

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'topsecret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=3)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.url_map.strict_slashes = False
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth with {"username": "john", "password": "hello"}

api.add_resource(SampleModel, '/model/<string:model_name>/sample')
api.add_resource(Model, '/model/<string:model_name>')
api.add_resource(DefaultValues, '/model')

if __name__ == '__main__':
    _LOGGER.debug('Starting')
    app.run()
