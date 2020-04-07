from unittest import TestCase
import json
import app


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
