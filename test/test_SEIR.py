from unittest import TestCase
import src


class TestSEIR(TestCase):

    def setUp(self):
        total_population = 10000
        duration_days = 100
        timestep_days = 0.1

        alpha = 0.2  # inverse of incubation period
        beta = 1.75  # average contact rate
        gamma = 0.5
        rho = 0.7

        self.model_seir = src.models.SEIR(
            total_population=total_population,
            duration_days=duration_days,
            timestep_days=timestep_days,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            rho=rho
        )

    def test_solve(self):
        self.assertIsNone(self.model_seir.result_with_social_distancing)
        self.model_seir.solve()
        self.assertIsNotNone(self.model_seir.result_with_social_distancing)

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

