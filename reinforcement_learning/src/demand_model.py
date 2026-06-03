import gymnasium as gym
from gymnasium import spaces
import numpy as np

"""
"""


def calculate_expected_demand(base_demand, price, elasticity):
    """Helper function to calculate expected demand given a price and elasticity and base demand."""
    return base_demand * np.exp(price * elasticity)


class SingleMarket(gym.Env):
    """One article market environment.

    Demand is given as a Poisson distribution with a rate of the attractiveness minus price.
    """

    def __init__(
        self, max_price=100, starting_stock=10, n_periods=3, attractiveness_std=0
    ):
        self.action_space = spaces.Discrete(max_price)
        self.starting_stock = starting_stock
        self.n_periods = n_periods
        self.max_price = max_price
        self.attractiveness_std = attractiveness_std
        self.reset()

    def step(self, action):
        price = action
        demand = np.random.poisson(np.max([self.attractiveness - price, 0]))
        sales = np.minimum(demand, self.stock)
        profit = demand * sales

        if self.t > self.n_periods:
            terminate = True
        else:
            terminate = False

        self.t += 1
        self.stock -= sales

        return (
            (self.t, self.stock),
            profit,
            terminate,
            {"sales": sales},
        )

    def reset(self):
        self.attractiveness = (
            np.random.randn() * self.attractiveness_std + self.max_price
        )
        self.stock = self.starting_stock
        self.t = 0
        return (self.t, self.stock)


# class MultiMarket(gym.Env):
#     def __init__(self, n_articles=7, max_price=100, starting_stock=10, n_periods=3):
#         self.n_articles = n_articles
#         self.action_space = spaces.MultiDiscrete([max_price] * n_articles)
#         self.starting_stock = starting_stock
#         # begin in start state
#         self.reset()

#     def step(self, action):
#         price = action
#         demand = np.random.poisson(np.max(self.attractiveness - price, 0))
#         sales = np.minimum(demand, self.stock)
#         profit = sum(demand * sales)

#         if self.t > self.n_periods:
#             terminate = True
#         else:
#             terminate = False

#         return self.stock, profit, terminate, {"sales": sales}

#     def reset(self):
#         self.attractiveness = np.random.randint(self.starting_stock)
#         self.stock = np.array([10] * self.n_articles)
#         self.t = 0
#         return (self.t, self.stock)


class MultiMarket(gym.Env):
    """WIP"""

    def __init__(self, n_articles=5, starting_stock=500):
        self.n_articles = n_articles
        self.attractiveness_mean = 500
        self.attractiveness_var = 10
        self.elasticity = -2
        self.starting_stock = starting_stock
        self.n_periods = 5
        self.price_range = (10, 50)

    def step(self, action):
        demand = calculate_expected_demand(
            self.base_demand, np.array(action), [self.elasticity] * 5
        )
        sales = np.minimum(demand, self.stock)
        profit = demand * sales

        if self.t > self.n_periods:
            terminate = True
        else:
            terminate = False

        self.t += 1
        self.stock -= sales

        return (
            (self.t, self.stock),
            profit,
            terminate,
            {"sales": sales},
        )

    def reset(self):
        self.base_demand = (
            np.random.randn(self.n_articles) * self.attractiveness_var
            + self.attractiveness_mean
        )

        self.stock = np.ones(self.n_articles) * self.starting_stock

        self.t = 0
        return (self.t, self.stock)
