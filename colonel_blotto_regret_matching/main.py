from random import random

def get_possible_deployments(soldiers, battlefields):
    if battlefields == 1:
        return [[soldiers]]
    else:
        deployments = []
        for i in range(0, soldiers + 1):
            for subdeployment in get_possible_deployments(soldiers - i, battlefields - 1):
                deployments += [[i] + subdeployment]
        return deployments

def get_utility(hero_deployment, opponent_deployment):
    hero_wins = 0
    opponent_wins = 0
    for i in range(len(hero_deployment)):
        hero_soldiers = hero_deployment[i]
        opponent_soldiers = opponent_deployment[i]
        if hero_soldiers > opponent_soldiers:
            hero_wins += 1
        elif opponent_soldiers > hero_soldiers:
            opponent_wins += 1
    if hero_wins > opponent_wins:
        return 1
    elif opponent_wins > hero_wins:
        return -1
    else:
        return 0

possible_deployments = get_possible_deployments(5, 3)

class Trainer:
    NUM_ACTIONS = len(possible_deployments)
    NUM_PLAYERS = 2

    def __init__(self, *, iterations):
        self.__cumulative_strategy = [[0 for _ in range(Trainer.NUM_ACTIONS)] for _ in range(Trainer.NUM_PLAYERS)]
        self.__cumulative_regrets = [[0 for _ in range(Trainer.NUM_ACTIONS)] for _ in range(Trainer.NUM_PLAYERS)]
        self.__iterations = iterations
    
    def train(self):
        for _ in range(self.__iterations):
            strategies = [self.get_strategy(0), self.get_strategy(1)]
            for p in range(Trainer.NUM_PLAYERS):
                for a in range(Trainer.NUM_ACTIONS):
                    self.__cumulative_strategy[p][a] = self.__cumulative_strategy[p][a] + strategies[p][a]
            
            simultaneous_actions = [self.sample_action(strategies[0]), self.sample_action(strategies[1])]
            for p in range(Trainer.NUM_PLAYERS):
                hero_deployment = possible_deployments[simultaneous_actions[p]]
                opponent_deployment = possible_deployments[simultaneous_actions[1 - p]]

                actionUtility = []
                for deployment in possible_deployments:
                    actionUtility.append(get_utility(deployment, opponent_deployment))
                
                hero_deployment_utility = get_utility(hero_deployment, opponent_deployment)
                for a in range(Trainer.NUM_ACTIONS):
                    self.__cumulative_regrets[p][a] = self.__cumulative_regrets[p][a] + \
                        get_utility(possible_deployments[a], opponent_deployment) - hero_deployment_utility
    
    
    def sample_action(self, strategy):
        r = random()
        cumulative_probability = 0
        for a in range(Trainer.NUM_ACTIONS):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                return a
        raise RuntimeError("No action chosen")

    def get_strategy(self, player):
        normalizing_sum = sum(filter(lambda x: x > 0, self.__cumulative_regrets[player]))
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum if x > 0 else 0), self.__cumulative_regrets[player]))
        else:
            return  [1 / Trainer.NUM_ACTIONS for _ in range(Trainer.NUM_ACTIONS)]
        
    def get_average_strategy(self, player):
        normalizing_sum = sum(self.__cumulative_strategy[player])
        if normalizing_sum > 0:
            return list(map((lambda x: x / normalizing_sum), self.__cumulative_strategy[player]))
        else:
            return [1 / Trainer.NUM_ACTIONS for _ in range(Trainer.NUM_ACTIONS)]

def get_formatted_strategy(strategy):
    out = ""
    for i, probability in enumerate(strategy):
        out += f"Deployment {possible_deployments[i]}: {(probability*100):.2f} %\n"
    return out

if __name__ == "__main__":
    training_iterations = 100000
    trainer = Trainer(iterations=training_iterations)
    trainer.train()

    print(f"Hero strategy after {training_iterations} iterations:")
    print(get_formatted_strategy(trainer.get_average_strategy(0)))

    print(f"Opponent strategy after {training_iterations} iterations:")
    print(get_formatted_strategy(trainer.get_average_strategy(1)))
