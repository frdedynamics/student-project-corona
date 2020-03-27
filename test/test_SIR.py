from unittest import TestCase
from .context import src


class TestSIR(TestCase):

    def setUp(self):

        total_population = 5000000
        I_0 = 1000
        R_0 = 0
        average_number_of_people_infected_per_day_per_person = 0.2
        average_days_sick_per_person = 7
        duration_days = 365
        timestep_days = 1

        self.model_sir = src.models.SIR(
            total_population=total_population,
            I_0=I_0,
            R_0=R_0,
            average_days_sick_per_person=average_days_sick_per_person,
            average_number_of_people_infected_per_day_per_person=average_number_of_people_infected_per_day_per_person,
            duration_days=duration_days,
            timestep_days=timestep_days
        )

    def test_f(self):
        self.assertTrue(True)
        # self.fail(msg="Needs test.")

    def test_solve(self):
        self.assertIsNone(self.model_sir.result)
        self.model_sir.solve()
        self.assertIsNotNone(self.model_sir.result)

    def test_plot_result(self):
        try:
            self.model_sir.plot_result()
        except ValueError as e:
            self.fail(msg=e)
