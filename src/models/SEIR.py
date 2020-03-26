import logging
import numpy as np
import matplotlib.pyplot as plt

_LOGGER = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel('ERROR')


class SEIR:

    def __init__(self, total_population=10000, duration_days=100, timestep_days=0.1):
        _LOGGER.debug("Initialize..")

        self.total_population = total_population
        self.S_0 = 1 - 1 / total_population
        self.E_0 = 1 / total_population
        self.I_0 = 0
        self.R_0 = 0
        self.duration_days = duration_days
        self.timestep_days = timestep_days

        self.alpha = 0.2
        self.beta = 1.75
        self.gamma = 0.5

        self.t = np.linspace(0, self.duration_days, int(self.duration_days / timestep_days) + 1)
        self.result = None

    def solve_base_model(self):
        _LOGGER.debug("Solve ODE..")
        S, E, I, R = [self.S_0], [self.E_0], [self.I_0], [self.R_0]
        dt = self.t[1] - self.t[0]
        for _ in self.t[1:]:
            next_S = S[-1] - (self.beta * S[-1] * I[-1]) * dt
            next_E = E[-1] + (self.beta * S[-1] * I[-1] - self.alpha * E[-1]) * dt
            next_I = I[-1] + (self.alpha * E[-1] - self.gamma * I[-1]) * dt
            next_R = R[-1] + (self.gamma * I[-1]) * dt
            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            R.append(next_R)
        self.result = np.stack([S, E, I, R]).T

    def solve_with_social_distance(self):
        pass

    def __sanity_check_inputs(self):
        if not False:
            _LOGGER.error("Inputs are insane!")
            raise ValueError

    def plot_base_model(self):
        if self.result is None:
            self.solve_base_model()

        _LOGGER.debug("Plot result..")
        plt.plot(self.t, self.result)
        plt.show()

