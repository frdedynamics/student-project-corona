from unittest import TestCase
from .context import src


class TestSEIR(TestCase):

    def setUp(self):
        total_population = 10000
        duration_days = 100
        timestep_days = 0.1

        self.model_seir = src.models.SEIR(
            total_population=total_population,
            duration_days=duration_days,
            timestep_days=timestep_days
        )

    def test_solve_base_model(self):
        self.assertIsNone(self.model_seir.result)
        self.model_seir.solve_base_model()
        self.assertIsNotNone(self.model_seir.result)

    def test_plot_base_model(self):
        try:
            self.model_seir.plot_base_model()
        except ValueError as e:
            self.fail(msg=e)
