from random import random


class RPSTrainer:
    NUM_ACTIONS = 3
    NUM_PLAYERS = 2

    def __init__(self, *, iterations):
        self.__cumulative_strategy = [[0,0,0],[0,0,0]]
        self.__cumulative_regrets = [[0,0,0],[0,0,0]]
        self.__iterations = iterations

    def train(self):
        for _ in range(self.__iterations):
            strategies = [self.get_strategy(0), self.get_strategy(1)]
            for p in range(RPSTrainer.NUM_PLAYERS):
                for a in range(RPSTrainer.NUM_ACTIONS):
                    self.__cumulative_strategy[p][a] = self.__cumulative_strategy[p][a] + strategies[p][a]
            
            simultaneous_actions = [self.sample_action(strategies[0]), self.sample_action(strategies[1])]
            for p in range(RPSTrainer.NUM_PLAYERS):
                hero_action = simultaneous_actions[p]
                opponent_action = simultaneous_actions[1 - p]
                actionUtility = [0, 0, 0]
                actionUtility[opponent_action] = 0
                actionUtility[(opponent_action + 1) % RPSTrainer.NUM_ACTIONS] = 1
                actionUtility[(opponent_action + 2) % RPSTrainer.NUM_ACTIONS] = -1
                for a in range(RPSTrainer.NUM_ACTIONS):
                    self.__cumulative_regrets[p][a] = self.__cumulative_regrets[p][a] + actionUtility[a] - actionUtility[hero_action]
    
    def get_cumulative_regrets(self):
        return self.__cumulative_regrets

    def sample_action(self, strategy):
        r = random()
        cumulative_probability = 0
        for a in range(RPSTrainer.NUM_ACTIONS):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                return a
        raise RuntimeError("No action chosen")

    def get_strategy(self, player):
        normalizing_sum = sum(filter(lambda x: x > 0, self.__cumulative_regrets[player]))
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum if x > 0 else 0), self.__cumulative_regrets[player]))
        else:
            return [1 / RPSTrainer.NUM_ACTIONS, 1 / RPSTrainer.NUM_ACTIONS, 1 / RPSTrainer.NUM_ACTIONS]
    
    def get_average_strategy(self, player):
        normalizing_sum = sum(self.__cumulative_strategy[player])
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum), self.__cumulative_strategy[player]))
        else:
            return [1 / RPSTrainer.NUM_ACTIONS, 1 / RPSTrainer.NUM_ACTIONS, 1 / RPSTrainer.NUM_ACTIONS]


def get_formatted_strategy(strategy):
    return f"Rock: {strategy[0]*100} %, Paper: {strategy[1]*100} %, Scissors: {strategy[2]*100} %"

if __name__ == "__main__":
    training_iterations = 10000
    trainer = RPSTrainer(iterations=training_iterations)
    trainer.train()

    print(f"Hero strategy after {training_iterations} iterations:")
    print(get_formatted_strategy(trainer.get_average_strategy(0)))

    print(f"Opponent strategy after {training_iterations} iterations:")
    print(get_formatted_strategy(trainer.get_average_strategy(1)))
