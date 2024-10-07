import gymnasium as gym
from gymnasium import spaces

"""
Copied from https://github.com/podondra/gym-gridworlds/blob/master/gym_gridworlds/envs/windy_gridworld_env.py

Modified to use gymnasium instead of gym
"""


class WindyGridworldEnv(gym.Env):
    def __init__(self, height=7, width=10, stand_still=False):
        self.height = height
        self.width = width

        if not stand_still:
            self.action_space = spaces.Discrete(4)
            self.moves = {
                0: (-1, 0),  # up
                1: (0, 1),  # right
                2: (1, 0),  # down
                3: (0, -1),  # left
            }
        else:
            self.action_space = spaces.Discrete(5)
            self.moves[4] = (0, 0)

        self.observation_space = spaces.Tuple(
            (spaces.Discrete(self.height), spaces.Discrete(self.width))
        )

        # begin in start state
        self.reset()

    def step(self, action):
        if self.S[1] in (3, 4, 5, 8):
            self.S = self.S[0] - 1, self.S[1]
        elif self.S[1] in (6, 7):
            self.S = self.S[0] - 2, self.S[1]

        x, y = self.moves[action]
        self.S = self.S[0] + x, self.S[1] + y

        self.S = max(0, self.S[0]), max(0, self.S[1])
        self.S = (min(self.S[0], self.height - 1), min(self.S[1], self.width - 1))

        if self.S == (3, 7):
            return self.S, -1, True, {}
        return self.S, -1, False, {}

    def reset(self):
        self.S = (3, 0)
        return self.S
