from constants import *

class Node:
    def __init__(self, information_set: str):
        self.information_set = information_set
        self.cumulative_strategy = [0 for _ in range(NUM_ACTIONS)]
        self.cumulative_regrets = [0 for _ in range(NUM_ACTIONS)]
    
    def get_strategy(self):
        normalizing_sum = sum(filter(lambda x: x > 0, self.cumulative_regrets))
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum if x > 0 else 0), self.cumulative_regrets))
        else:
            return  [1 / NUM_ACTIONS for _ in range(NUM_ACTIONS)]

    def get_average_strategy(self):
        normalizing_sum = sum(self.cumulative_strategy)
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum), self.cumulative_strategy))
        else:
            return [1 / NUM_ACTIONS for _ in range(NUM_ACTIONS)]
    
    def update_average_strategy(self, strategy, realization_weigth: float):
        for a in range(NUM_ACTIONS):
            self.cumulative_strategy[a] += strategy[a] * realization_weigth
    
    def accumulate_action_regret(self, action_index, regret):
        self.cumulative_regrets[action_index] += regret

    def __str__(self):
        out = f"{self.information_set}:\t"
        average_strategy = self.get_average_strategy()
        
        for a in range(NUM_ACTIONS):
            out += f"{ACTIONS[a]}: {(average_strategy[a] * 100):.2f} %\t"
        return out