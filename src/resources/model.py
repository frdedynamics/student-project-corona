import json
import logging

from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

import src
from src.models.imodel import IModel
import src.models.imodel

_LOGGER = logging.getLogger(__name__)


def get_default_model_values():
    models = dict()
    for model in IModel.__subclasses__():
        print("test " + model.__name__)
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
print("default values")
MODEL_PARSER = get_parser_arguements()  # type: dict
NOT_IMPLEMENTED = {'message': 'resources not implemented'}, 501


class SampleModel(Resource):
    @jwt_required()  # Authorization: "JWT <access token>"
    def get(self, model_name):
        try:
            model_class = getattr(src.models, model_name)
            print("test " + model_class)
            model = model_class()  # type: IModel
            return {'model': json.loads(model.get_json())}  # TODO change return object
        except AttributeError:
            return {'message': f'No model named {model_name}.'}, 400


class Model(Resource):
    @jwt_required()
    def post(self, model_name):  # return model data
        try:
            model_class = getattr(src.models, model_name)
            data = MODEL_PARSER[model_name].parse_args()

            instance = model_class(**dict(data))  # type: IModel
            return {'model': json.loads(instance.get_json())}
        except AttributeError:
            return {'message': f'No model named {model_name}.'}, 400

    @jwt_required()
    def get(self, model_name):  # return default model values
        return {'default_values': DEFAULT_VALUES[model_name]} if model_name in DEFAULT_VALUES \
                   else ({'message': f'No model named {model_name}.'}, 400)


class ModelData(Resource):
    def get(self, model_name, model_id):
        return NOT_IMPLEMENTED


class DefaultValuesList(Resource):
    @jwt_required()
    def get(self):
        return {'default_values': DEFAULT_VALUES}
