import json
from unittest import TestCase
from werkzeug import exceptions
from os import path

from src import deprecated

ABSOLUTE_PATH = path.dirname(path.abspath(__file__))


class TestApp(TestCase):

    def setUp(self):
        with open(ABSOLUTE_PATH + '/test_get_sir_data.json') as json_file:
            self.param_sir = json.load(json_file)

        with open(ABSOLUTE_PATH + '/test_result_get_sir_data.json') as json_file:
            self.expected_result_sir = json.load(json_file)

        with open(ABSOLUTE_PATH + '/test_get_seir_data.json') as json_file:
            self.param_seir = json.load(json_file)

        with open(ABSOLUTE_PATH + '/test_result_get_seir_data.json') as json_file:
            self.expected_result_seir = json.load(json_file)

    def test_get_sir_data(self):
        tmp = deprecated.get_corona_data(param=self.param_sir)
        self.assertTrue(isinstance(tmp, str))
        self.assertEqual(json.loads(tmp), self.expected_result_sir)

    def test_get_seir_data(self):
        tmp = deprecated.get_corona_data(param=self.param_seir)
        self.assertTrue(isinstance(tmp, str))
        self.assertEqual(json.loads(tmp), self.expected_result_seir)

    def test_get_sir_data_pw(self):
        try:
            deprecated.get_corona_data(param={
                "username": "john",
                "password": "yo"
            })
        except Exception as e:
            self.assertTrue(isinstance(e, exceptions.Forbidden))
