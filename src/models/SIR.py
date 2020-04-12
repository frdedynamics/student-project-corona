import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from src.config import get_config
from pandas import DataFrame
from .imodel import IModel

config = get_config()
_LOGGER = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel('ERROR')


class SIR(IModel):
    LOCALS = None

    def __init__(self, total_population=5000000, I_0=1000, R_0=0,
                 average_number_of_people_infected_per_day_per_person=0.2, average_days_sick_per_person=7,
                 duration_days=365, timestep_days=1):
        _LOGGER.debug("Initialize..")

        if self.LOCALS is None:
            self.LOCALS = locals()
            del self.LOCALS['self']

        self.S_0 = total_population - I_0 - R_0
        self.I_0 = I_0
        self.R_0 = R_0
        self.b = average_number_of_people_infected_per_day_per_person
        self.k = 1/average_days_sick_per_person
        self.duration_days = duration_days
        self.timestep_days = timestep_days
        self.total_population = total_population

        self._number_of_timesteps = int(np.floor(duration_days/timestep_days))
        self._t = np.linspace(start=1, stop=self.duration_days, num=self._number_of_timesteps)
        self._result = None
        self._json = None


    # def __sanity_check_inputs(self):
    #     if not False:
    #         _LOGGER.error("Inputs are insane!")
    #         raise ValueError

    def __f(self, y, t):
        s, i, r = y

        f0 = -self.b*s*i
        f1 = self.b*s*i - self.k*i
        f2 = self.k*i

        return [f0, f1, f2]

    def solve(self):
        _LOGGER.debug("Solve ODE..")
        self._json = None
        self._result = odeint(
            self.__f,
            [
                self.S_0/self.total_population,
                self.I_0/self.total_population,
                self.R_0/self.total_population
            ],
            self._t
        )

    def get_json(self):
        _LOGGER.debug("Json..")
        if self._result is None:
            self.solve()

        if self._json is None:
            df = DataFrame(self._result, columns=['S', 'I', 'R'])
            df['t'] = self._t
            self._json = df.to_json(orient="records", indent=2)

        return self._json

    def plot_result(self):
        if self._result is None:
            self.solve()

        _LOGGER.debug("Plot result..")
        plt.clf()
        plt.plot(self._t, self._result[:, 0]*self.total_population)
        plt.plot(self._t, self._result[:, 1]*self.total_population)
        plt.plot(self._t, self._result[:, 2]*self.total_population)
        if config.get("user") == "ci":
            plt.show(block=False)
        elif config.get("show_plots"):
            plt.show(block=True)

