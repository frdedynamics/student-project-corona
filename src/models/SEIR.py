import logging
import numpy as np
import matplotlib.pyplot as plt

_LOGGER = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel('ERROR')


class SEIR:

    def __init__(self, total_population=10000, duration_days=100, timestep_days=0.1,
                 alpha=0.2, beta=1.75, gamma=0.5, rho=0.8):
        _LOGGER.debug("Initialize..")

        self.total_population = total_population
        self.S_0 = 1 - 1 / total_population
        self.E_0 = 1 / total_population
        self.I_0 = 0
        self.R_0 = 0
        self.duration_days = duration_days
        self.timestep_days = timestep_days

        self.alpha = alpha  # inverse of incubation period
        self.beta = beta  # average contact rate
        self.gamma = gamma  # inverse of the mean infection period
        self.rho = rho  # social distancing (values: 0-1)

        self.t = np.linspace(0, self.duration_days, int(self.duration_days / timestep_days) + 1)
        self.result_base_model = None
        self.result_with_social_distancing = None
        self.SEIR = plt
        self.plot_config()

    def solve(self, social_distancing=True):
        _LOGGER.debug("Solve..")
        S, E, I, R = [self.S_0], [self.E_0], [self.I_0], [self.R_0]
        dt = self.t[1] - self.t[0]
        rho = self.rho
        if not social_distancing:
            rho = 1

        for _ in self.t[1:]:

            next_S = S[-1] - (rho * self.beta * S[-1] * I[-1]) * dt
            next_E = E[-1] + (rho * self.beta * S[-1] * I[-1] - self.alpha * E[-1]) * dt
            next_I = I[-1] + (self.alpha * E[-1] - self.gamma * I[-1]) * dt
            next_R = R[-1] + (self.gamma * I[-1]) * dt
            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            R.append(next_R)

        if social_distancing:
            self.result_with_social_distancing = np.stack([S, E, I, R]).T
        else:
            self.result_base_model = np.stack([S, E, I, R]).T

    def __sanity_check_inputs(self):
        if not False:
            _LOGGER.error("Inputs are insane!")
            raise ValueError

    def plot_base_model(self, draw=True):
        if self.result_base_model is None:
            self.solve(social_distancing=False)

        _LOGGER.debug("Plot base model result..")

        self.SEIR.plot(self.t, self.result_base_model[:, 2] * self.total_population, label="Without social distancing")

        if draw:
            self.SEIR.legend(loc="upper right")
            self.SEIR.show(block=False)

    def plot_with_social_distancing(self):
        if self.result_with_social_distancing is None:
            self.solve()

        _LOGGER.debug("Plot with social distancing result..")
        self.plot_base_model(draw=False)

        self.SEIR.plot(self.t, self.result_with_social_distancing[:, 2] * self.total_population, ls="--",
                       label="With social distancing (ρ = %.1f)" % self.rho)

        self.SEIR.legend(loc="upper right")
        self.SEIR.show(block=False)

    def plot_config(self):
        self.SEIR.title("COVID-19 SEIR Model (α = %.1f, β = %.2f, γ = %.1f)\nPopulation: %d" %
                        (self.alpha, self.beta, self.gamma, self.total_population))
        self.SEIR.xlabel("Time (Days)")
        self.SEIR.ylabel("Infected", rotation="vertical")

