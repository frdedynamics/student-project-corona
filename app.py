import logging
import src
import json
from src.config import get_config
from flask import Flask, request, abort

CONFIG = get_config()
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

USERS = {
    "john": "hello"
}


@app.route("/get_sir_data", methods=["GET"])
def get_sir_data(param=None):
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

    sir = src.SIR(
        total_population=tmp["total_population"],
        I_0=tmp["I_0"],
        R_0=tmp["R_0"],
        average_number_of_people_infected_per_day_per_person=
        tmp["average_number_of_people_infected_per_day_per_person"],
        average_days_sick_per_person=tmp["average_days_sick_per_person"],
        duration_days=tmp["duration_days"],
        timestep_days=tmp["timestep_days"]
    )
    _LOGGER.debug('Solving SIR model..')
    sir.solve()
    _LOGGER.debug('Returning SIR result.')
    return sir.get_json()


if __name__ == '__main__':
    _LOGGER.debug('Starting')
    app.run()
