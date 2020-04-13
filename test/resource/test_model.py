from unittest import TestCase
import src.resource.model as model
from flask import Response
from flask_restful import reqparse
from app import app


class TestModel(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_unauthorized(self):
        headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY3NDg2NTgsImlhdCI6MTU4NjczNzg1OCw'
                             'ibmJmIjoxNTg2NzM3ODU4LCJpZGVudGl0eSI6MX0.dHKBCbdzeDyL3S6r5GaUYi2VUx-k6T2FslCXYxq3zrw'
        }

        response = self.app.get('/model', headers=headers)  # type: Response
        self.assertEqual(401, response.status_code)

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
