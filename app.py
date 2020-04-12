import logging
import src
import json
import datetime
from src.config import get_config

from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask_cors import CORS

from src.authorization import authenticate, identity
from src import IModel

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'topsecret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=3)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.url_map.strict_slashes = False
api = Api(app)
CORS(app)

jwt = JWT(app, authenticate, identity)  # /auth with {"username": "john", "password": "hello"}


def get_default_model_values():
    models = dict()
    for model in IModel.__subclasses__():
        instance = model()
        models[model.__name__] = instance.LOCALS
    return models


def get_parser_arguements():
    parsers = dict()
    for model in DEFAULT_VALUES:
        parser = reqparse.RequestParser()
        for attribute, value in DEFAULT_VALUES[model].items():
            parser.add_argument(
                attribute,
                default=value,
                type=type(value)
            )
        parsers[model] = parser
    return parsers


DEFAULT_VALUES = get_default_model_values()  # type: dict
MODEL_PARSER = get_parser_arguements() # type: dict
NOT_IMPLEMENTED = {'message': 'resource not implemented'}, 501
SUCCESS = "response"


# returns the appropriate sample model with default values
class SampleModel(Resource):
    @jwt_required()  # Authorization: "JWT <access token>"
    def get(self, model_name):
        try:
            model_class = getattr(src.models, model_name)
            model = model_class()  # type: src.IModel
            return {SUCCESS: json.loads(model.get_json())}  # TODO json.loads for conveience of testing
        except AttributeError:
            return {'message': f'No model named {model_name}.'}, 400


class Model(Resource):
    @jwt_required()
    def post(self, model_name):  # return model data
        try:
            model_class = getattr(src.models, model_name)
            data = MODEL_PARSER[model_name].parse_args()
            instance = model_class(**dict(data))  # type: IModel
            return {SUCCESS: json.loads(instance.get_json())}  # TODO json -> dict -> json
        except AttributeError:
            return {'message': f'No model named {model_name}.'}, 400

    @jwt_required()
    def get(self, model_name):  # return default model values
        return {SUCCESS: DEFAULT_VALUES[model_name]} if model_name in DEFAULT_VALUES \
                   else ({'message': f'No model named {model_name}.'}, 400)


# returns saved models
class ModelData(Resource):
    def get(self, model_name, model_id):
        return NOT_IMPLEMENTED


# returns a list of available models and their values
class DefaultValues(Resource):
    @jwt_required()
    def get(self):
        return {SUCCESS: DEFAULT_VALUES}


api.add_resource(SampleModel, '/model/<string:model_name>/sample')
api.add_resource(Model, '/model/<string:model_name>')
api.add_resource(DefaultValues, '/model')


USERS = {  # deprecated for current branch
    "john": "hello"
}


@app.route("/get_corona_data", methods=["POST"])  # deprecated for current branch
def get_corona_data(param=None):
    if param is not None:
        _LOGGER.debug("Param is not none.")
    else:
        _LOGGER.debug("Param is none.")
        param = request.get_json()

    if param.get('username') in USERS.keys():
        if param.get('password') == USERS[param.get('username')]:
            _LOGGER.debug("User: " + str(param.get('username')))
            pass
        else:
            _LOGGER.debug("Password no good. Username " + str(param.get('username')))
            abort(403)
    else:
        _LOGGER.debug("Username " + str(param.get('username')) + " not in users.")
        abort(403)

    if isinstance(param, str):
        _LOGGER.debug('Received string: ' + param)
        tmp = json.loads(param)
    else:
        _LOGGER.debug('Received: ' + str(param))
        tmp = param

    if tmp["model_type"] == 'SIR':
        mdl = src.SIR(
            total_population=tmp["total_population"],
            I_0=tmp["I_0"],
            R_0=tmp["R_0"],
            average_number_of_people_infected_per_day_per_person=
            tmp["average_number_of_people_infected_per_day_per_person"],
            average_days_sick_per_person=tmp["average_days_sick_per_person"],
            duration_days=tmp["duration_days"],
            timestep_days=tmp["timestep_days"]
        )
        _LOGGER.debug('Solving ' + tmp["model_type"] + ' model..')
        mdl.solve()
        _LOGGER.debug('Returning ' + tmp["model_type"] + ' result.')
        return mdl.get_json()
    elif tmp["model_type"] == 'SEIR':
        mdl = src.models.SEIR(
            total_population=tmp["total_population"],
            duration_days=tmp["duration_days"],
            timestep_days=tmp["timestep_days"],
            alpha=tmp["alpha"],
            beta=tmp["beta"],
            gamma=tmp["gamma"],
            rho=tmp["rho"]
        )
        _LOGGER.debug('Solving ' + tmp["model_type"] + ' model..')
        mdl.solve()
        _LOGGER.debug('Returning ' + tmp["model_type"] + ' result.')
        return mdl.get_json(tmp["social_distancing"])
    else:
        _LOGGER.debug('Model type ' + tmp["model_type"] + ' not supported')
        abort(403)


if __name__ == '__main__':
    _LOGGER.debug('Starting')
    app.run()
