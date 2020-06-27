from constants import *
from random import shuffle
from node import Node

class Trainer:
    def __init__(self):
        self.node_map = {}

    def train(self, *, iterations):
        cards = [1, 2, 3]
        utility = 0
        for _ in range(iterations):
            shuffle(cards)
            utility += self.cfr(cards, EMPTY_HISTORY, 1, 1)
        print(f"Average game value: {utility/iterations}")
        for node in self.node_map.values():
            print(node)

    def cfr(self, cards: list, history: str, cf_reach_probability_0: float, cf_reach_probability_1: float):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        # Terminal states
        if plays > 1:
            terminal_pass = history[-1] == 'p'
            double_bet = history[-2:] == "bb"
            player_card_higher = cards[player] > cards[opponent]
            if terminal_pass:
                if history == "pp":
                    return 1 if player_card_higher else -1
                else:
                    return 1
            elif double_bet:
                return 2 if player_card_higher else -2

        information_set = str(cards[player]) + history
        node = self.node_map.get(information_set)
        if node is None:
            node = Node(information_set)
            self.node_map[information_set] = node
        
        strategy = node.get_strategy()
        realization_weigth = cf_reach_probability_0 if player == 0 else cf_reach_probability_1
        node.update_average_strategy(strategy, realization_weigth)
        
        action_utilities = [0 for _ in range(NUM_ACTIONS)]
        node_utility = 0
        for a in range(NUM_ACTIONS):
            next_history = history + ACTIONS[a]
            if player == 0:
                action_utilities[a] = -self.cfr(cards, next_history, cf_reach_probability_0 * strategy[a], cf_reach_probability_1)
            else:
                action_utilities[a] = -self.cfr(cards, next_history, cf_reach_probability_0, cf_reach_probability_1 * strategy[a])
            node_utility += action_utilities[a] * strategy[a]
        
        for a in range(NUM_ACTIONS):
            regret = action_utilities[a] - node_utility
            weigthed_regret = regret * cf_reach_probability_1 if player == 0 else regret * cf_reach_probability_0
            node.accumulate_action_regret(a, weigthed_regret)
        
        return node_utility

        
