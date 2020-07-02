from constants import *


class Node:
    def __init__(self, information_set: str, *, possible_actions: int):
        self.information_set = information_set
        self.possible_actions = possible_actions
        self.cumulative_strategy = [0 for _ in range(possible_actions)]
        self.cumulative_regrets = [0 for _ in range(possible_actions)]
        self.updates = 0

    def get_strategy(self):
        normalizing_sum = sum(filter(lambda x: x > 0, self.cumulative_regrets))
        if normalizing_sum > 0:
            return list(
                map(
                    (lambda x: x / normalizing_sum if x > 0 else 0),
                    self.cumulative_regrets,
                )
            )
        else:
            return [1 / self.possible_actions for _ in range(self.possible_actions)]

    def get_average_strategy(self):
        normalizing_sum = sum(self.cumulative_strategy)
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum), self.cumulative_strategy))
        else:
            return [1 / self.possible_actions for _ in range(self.possible_actions)]

    def update_average_strategy(self, strategy, realization_weigth: float):
        self.updates += 1
        for a in range(self.possible_actions):
            self.cumulative_strategy[a] += strategy[a] * realization_weigth

    def accumulate_action_regret(self, action_index, regret):
        self.cumulative_regrets[action_index] += regret

    def __str__(self):
        out = f"{self.information_set}:\t"
        average_strategy = self.get_average_strategy()

        for a in range(self.possible_actions):
            out += f"{ACTIONS[a]}: {(average_strategy[a] * 100):.2f} %\t"
        if self.possible_actions == 2:
            out += "\t\t"
        out += f"-> Updated {self.updates} times"
        return out
