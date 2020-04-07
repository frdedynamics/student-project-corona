import json
import app
from unittest import TestCase
from werkzeug import exceptions


class TestApp(TestCase):

    def setUp(self):
        with open('test/test_get_sir_data.json') as json_file:
            self.param = json.load(json_file)

        with open('test/test_result_get_sir_data.json') as json_file:
            self.expected_result = json.load(json_file)

    def test_get_sir_data(self):
        tmp = app.get_sir_data(param=self.param)
        self.assertTrue(isinstance(tmp, str))
        self.assertEqual(json.loads(tmp), self.expected_result)

    def test_get_sir_data_pw(self):
        try:
            app.get_sir_data(param={
                "username": "john",
                "password": "yo"
            })
        except Exception as e:
            self.assertTrue(isinstance(e, exceptions.Forbidden))
