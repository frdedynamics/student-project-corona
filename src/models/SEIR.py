import logging

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

from src.config import get_config
from .imodel import IModel

config = get_config()
_LOGGER = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel('ERROR')


class SEIR(IModel):
    LOCALS = None

    def __init__(self, total_population=10000, duration_days=100, timestep_days=0.1,
                 alpha=0.2, beta=1.75, gamma=0.5, rho=0.8):
        _LOGGER.debug("Initialize..")

        if self.LOCALS is None:
            self.LOCALS = locals()
            del self.LOCALS['self']

        self.total_population = total_population
        self.S_0 = 1 - 1/total_population
        self.E_0 = 1/total_population
        self.I_0 = 0.0
        self.R_0 = 0.0
        self.duration_days = duration_days
        self.timestep_days = timestep_days

        self.alpha = alpha  # inverse of incubation period
        self.beta = beta  # average contact rate
        self.gamma = gamma  # inverse of the mean infection period
        self.rho = rho  # social distancing (values: 0-1)

        self._t = np.linspace(0, self.duration_days, int(self.duration_days/timestep_days) + 1)
        self._result = [None]*2  # [0] = base model, [1] = social distancing
        self._json = [None]*2

    def solve(self, social_distancing=True):
        _LOGGER.debug("Solve..")
        S, E, I, R = [self.S_0], [self.E_0], [self.I_0], [self.R_0]
        dt = self._t[1] - self._t[0]

        if social_distancing:
            rho = self.rho
            self._json[1] = None
            result_index = 1
        else:
            self._json[0] = None
            rho = 1
            result_index = 0

        for _ in self._t[1:]:
            next_S = S[-1] - (rho*self.beta*S[-1]*I[-1])*dt
            next_E = E[-1] + (rho*self.beta*S[-1]*I[-1] - self.alpha*E[-1])*dt
            next_I = I[-1] + (self.alpha*E[-1] - self.gamma*I[-1])*dt
            next_R = R[-1] + (self.gamma*I[-1])*dt
            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            R.append(next_R)
            self._result[result_index] = np.array([S, E, I, R]).T

    def get_json(self, social_distancing=False):
        _LOGGER.debug("Json..")
        index = 1 if social_distancing else 0
        if self._result[index] is None:
            self.solve(social_distancing)

        if self._json[index] is None:
            df = DataFrame(self._result[index], columns=['S', 'E', 'I', 'R'])
            df['t'] = self._t
            self._json[index] = df.to_json(orient="records", indent=2)
        return self._json[index]

    def plot_base_model(self, draw=True):
        if self._result[0] is None:
            self.solve(social_distancing=False)

        _LOGGER.debug("Plot base model result..")

        plt.clf()
        self.plot_config()
        plt.plot(self._t, self._result[0][:, 2]*self.total_population, label="Without social distancing")

        if draw:
            plt.legend(loc="upper right")
            if config.get("user") == "ci":
                plt.show(block=False)
            elif config.get("show_plots"):
                plt.show(block=True)

    def plot_with_social_distancing(self):
        if self._result[1] is None:
            self.solve()

        _LOGGER.debug("Plot with social distancing result..")
        self.plot_base_model(draw=False)

        plt.plot(self._t, self._result[1][:, 2]*self.total_population, ls="--",
                 label="With social distancing (ρ = %.1f)" % self.rho)

        plt.legend(loc="upper right")
        if config.get("user") == "ci":
            plt.show(block=False)
        elif config.get("show_plots"):
            plt.show(block=True)

    def plot_config(self):
        plt.title("COVID-19 SEIR Model (α = %.1f, β = %.2f, γ = %.1f)\nPopulation: %d" %
                  (self.alpha, self.beta, self.gamma, self.total_population))
        plt.xlabel("Time (Days)")
        plt.ylabel("Infected", rotation="vertical")
