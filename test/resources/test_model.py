from unittest import TestCase
import src.resources.model as model
from flask_restful import reqparse
from app import app


class TestModel(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_default_model_values(self):
        values = model.get_parser_arguements()
        self.assertIsInstance(values, dict)
        parser = next(iter(values.values()))
        self.assertIsInstance(parser, reqparse.RequestParser)

    def test_get_parser_arguements(self):
        values = model.get_default_model_values()
        self.assertIsInstance(values, dict)
        arguements = next(iter(values.values()))
        self.assertIsInstance(arguements, dict)
