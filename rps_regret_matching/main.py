from random import random


class RPSTrainer:
    NUM_ACTIONS = 3

    def __init__(self, *, iterations, opponent_strategy):
        self.__cumulative_strategy = [[0, 0,0],[0,0,0]]
        self.__opponent_strategy = opponent_strategy
        self.__iterations = iterations

    def train(self):
        for _ in range(self.__iterations):
            hero_action = self.get_hero_action()
            opponent_action = self.get_opponent_action()
            actionUtility = [0] * RPSTrainer.NUM_ACTIONS
            actionUtility[opponent_action] = 0
            actionUtility[(opponent_action + 1) % RPSTrainer.NUM_ACTIONS] = 1
            actionUtility[(opponent_action + 2) % RPSTrainer.NUM_ACTIONS] = -1
            for a in range(RPSTrainer.NUM_ACTIONS):
                self.__cumulative_regrets[a] += actionUtility[a] - actionUtility[hero_action]
    
    def get_cumulative_regrets(self):
        return self.__cumulative_regrets

    def get_hero_strategy(self):
        normalizing_sum = sum(filter(lambda x: x > 0, self.__cumulative_regrets))
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum if x > 0 else 0), self.__cumulative_regrets))
        else:
            return [1 / RPSTrainer.NUM_ACTIONS] * RPSTrainer.NUM_ACTIONS

    def get_opponent_strategy(self):
        return self.__opponent_strategy

    def get_hero_action(self):
        return RPSTrainer.sample_random_action(self.get_hero_strategy())
            

    def get_opponent_action(self):
        return RPSTrainer.sample_random_action(self.get_opponent_strategy())

    @staticmethod
    def sample_random_action(strategy):
        r = random()
        cumulative_probability = 0
        for a in range(RPSTrainer.NUM_ACTIONS):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                return a
        raise RuntimeError("No action chosen")

def get_formatted_strategy(strategy):
    return f"Rock: {strategy[0]*100} %, Paper: {strategy[1]*100} %, Scissors: {strategy[2]*100} %"

if __name__ == "__main__":
    opponent_strategy = [0.3, 0.3, 0.4]
    print("Opponent's strategy:")
    print(get_formatted_strategy(opponent_strategy))
    training_iterations = 10000
    trainer = RPSTrainer(iterations=training_iterations, opponent_strategy=opponent_strategy)
    trainer.train()
    print(f"Hero strategy after {training_iterations} iterations:")
    print(get_formatted_strategy(trainer.get_hero_strategy()))
