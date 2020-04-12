import json

from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

import src
from src import IModel


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


class ModelData(Resource):
    def get(self, model_name, model_id):
        return NOT_IMPLEMENTED


class DefaultValues(Resource):
    @jwt_required()
    def get(self):
        return {SUCCESS: DEFAULT_VALUES}