from unittest import TestCase
from src.models.SEIR import SEIR


class TestSEIR(TestCase):

    def setUp(self):
        total_population = 10000
        duration_days = 100
        timestep_days = 0.1

        alpha = 0.2  # inverse of incubation period
        beta = 1.75  # average contact rate
        gamma = 0.5
        rho = 0.7

        self.model_seir = SEIR(
            total_population=total_population,
            duration_days=duration_days,
            timestep_days=timestep_days,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            rho=rho
        )

    def test_solve(self):
        self.assertIsNone(self.model_seir._result[1])
        self.model_seir.solve()
        self.assertIsNotNone(self.model_seir._result[1])

    def test_get_json(self):
        self.assertIsNone(self.model_seir._json[0])
        self.assertIsNone(self.model_seir._json[1])
        json = self.model_seir.get_json(True)
        self.assertIsInstance(json, str)
        json_base_result = self.model_seir.get_json(False)
        self.assertIsInstance(json, str)
        self.assertIsNot(json, json_base_result)
        self.assertIsNotNone(self.model_seir._json[0])
        self.assertIsNotNone(self.model_seir._json[1])

    def test_plot_base_model(self):
        try:
            self.model_seir.plot_base_model()
        except ValueError as e:
            self.fail(msg=e)

    def test_plot_with_social_distancing(self):
        try:
            self.model_seir.plot_with_social_distancing()
        except ValueError as e:
            self.fail(msg=e)
