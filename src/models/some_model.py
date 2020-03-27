import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

_LOGGER = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel('ERROR')


class SIR2:

    def __init__(self, total_population=5000000, I_0=1000, R_0=0,
                 average_number_of_people_infected_per_day_per_person=0.2, average_days_sick_per_person=7,
                 duration_days=365, timestep_days=1):
        _LOGGER.debug("Initialize..")
        self.S_0 = total_population - I_0 - R_0
        self.I_0 = I_0
        self.R_0 = R_0
        self.b = average_number_of_people_infected_per_day_per_person
        self.k = 1/average_days_sick_per_person
        self.duration_days = duration_days
        self.timestep_days = timestep_days
        self.total_population = total_population

        self.number_of_timesteps = int(np.floor(duration_days/timestep_days))
        self.t = np.linspace(start=1, stop=self.duration_days, num=self.number_of_timesteps)
        self.result = None

    def __sanity_check_inputs(self):
        if not False:
            _LOGGER.error("Inputs are insane!")
            raise ValueError

    def __f(self, y, t):
        s, i, r = y

        f0 = -self.b*s*i
        f1 = self.b*s*i - self.k*i
        f2 = self.k*i

        return [f0, f1, f2]

    def solve(self):
        _LOGGER.debug("Solve ODE..")
        self.result = odeint(
            self.__f,
            [
                self.S_0/self.total_population,
                self.I_0/self.total_population,
                self.R_0/self.total_population
            ],
            self.t
        )

    def plot_result(self):
        if self.result is None:
            self.solve()

        _LOGGER.debug("Plot result..")
        plt.plot(self.t, self.result[:, 0]*self.total_population)
        plt.plot(self.t, self.result[:, 1]*self.total_population)
        plt.plot(self.t, self.result[:, 2]*self.total_population)
        plt.show(block=True)
