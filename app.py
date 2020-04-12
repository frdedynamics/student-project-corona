import logging
import src
import json
from src.config import get_config

from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from flask_cors import CORS

from src.authorization import authenticate, identity

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'topsecret'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.url_map.strict_slashes = False
api = Api(app)
CORS(app)

jwt = JWT(app, authenticate, identity)  # /auth with {"username": "john", "password": hello}

NOT_IMPLEMENTED = {'message': 'resource not implemented'}, 501


# returns the appropriate sample model with default values
class SampleModel(Resource):
    @jwt_required()  # Authorization: "JWT <access token>"
    def get(self, model_name):
        try:
            model_class = getattr(src.models, model_name)
            model = model_class()
            return {model_name: model.get_json()}
        except AttributeError:
            return {'message': f'No model named {model_name}.'}, 400


# returns data and cache model instances with identical hashes and store in users)
class Model(Resource):
    def get(self, model_name, model_id):
        return NOT_IMPLEMENTED


#  returns a list of available models
class ModelList(Resource):
    def get(self):
        return NOT_IMPLEMENTED


# returns default attributes for a model
class DefaultValues(Resource):
    def get(self, model_name):
        return NOT_IMPLEMENTED


api.add_resource(SampleModel, '/model/<string:model_name>/sample')
api.add_resource(Model, '/model/<string:model_name>/<int:model_id>')
api.add_resource(DefaultValues, '/model/<string:model_name>')
api.add_resource(ModelList, '/model')


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
