import json

from flask import request, abort
from flask_cors import CORS

import src
from app import app, _LOGGER

CORS(app)

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
