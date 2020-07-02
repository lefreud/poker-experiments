from constants import *
from random import shuffle
from trainer.node import Node
from poker.deck import Deck
from poker.hand import Hand
import json

EXPECTED_VALUE_SIMULATIONS = 1


class Trainer:
    def __init__(self):
        self.node_map = {}
        with open(WIN_PROBABILITIES_FILENAME, "r") as f:
            self.hand_win_probabilities = json.load(f)

    def train(self, *, iterations):
        deck = Deck()
        utility = 0
        for _ in range(iterations):
            deck.reset()
            deck.shuffle()
            p0_hand = Hand([deck.pop(), deck.pop()])
            p1_hand = Hand([deck.pop(), deck.pop()])
            utility += self.cfr(
                deck, [p0_hand, p1_hand], EMPTY_HISTORY, [SMALL_BLIND, BIG_BLIND], 1, 1
            )
        print(f"Average game value: {utility/iterations}")
        for node in map(lambda node: node[1], sorted(self.node_map.items())):
            print(node)

    def cfr(
        self,
        deck: Deck,
        private_hands: list,
        history: str,
        invested_chips: list,
        cf_reach_probability_0: float,
        cf_reach_probability_1: float,
    ):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        if len(history) > 0:
            if history[-1] == "f":
                # Opponent folds, we get its invested chips
                return invested_chips[opponent]

            hand_win_probability = self.get_hand_win_probability(
                private_hands[player], private_hands[opponent]
            )
            player_expected_value = invested_chips[opponent] * (
                hand_win_probability - 0.5
            )
            if history == "cc":
                # We call as small blind, then the big blind checks
                return player_expected_value
            if history[-2:] == "bc":
                # We go all in as, opponent calls
                return player_expected_value

        information_set = (
            private_hands[player].compressed_representation() + "_" + history
        )

        if len(history) > 0 and history[-1] == "b":
            # Opponent went all-in, we can fold or call
            possible_actions = ["f", "c"]
        else:
            possible_actions = ["f", "c", "b"]

        node = self.node_map.get(information_set)
        if node is None:
            node = Node(information_set, possible_actions=len(possible_actions))
            self.node_map[information_set] = node

        strategy = node.get_strategy()
        realization_weigth = (
            cf_reach_probability_0 if player == 0 else cf_reach_probability_1
        )
        node.update_average_strategy(strategy, realization_weigth)

        action_utilities = [0 for _ in range(NUM_ACTIONS)]
        node_utility = 0

        for a, action in enumerate(possible_actions):
            next_history = history + action
            if action == "f":
                player_invested_chips = invested_chips[player]
            elif action == "c":
                player_invested_chips = invested_chips[opponent]
            elif action == "b":
                player_invested_chips = STACK_SIZE

            if player == 0:
                action_utilities[a] = -self.cfr(
                    deck,
                    private_hands,
                    next_history,
                    [player_invested_chips, invested_chips[1]],
                    cf_reach_probability_0 * strategy[a],
                    cf_reach_probability_1,
                )
            else:
                action_utilities[a] = -self.cfr(
                    deck,
                    private_hands,
                    next_history,
                    [invested_chips[0], player_invested_chips],
                    cf_reach_probability_0,
                    cf_reach_probability_1 * strategy[a],
                )
            node_utility += action_utilities[a] * strategy[a]

        for a, _ in enumerate(possible_actions):
            regret = action_utilities[a] - node_utility
            weigthed_regret = (
                regret * cf_reach_probability_1
                if player == 0
                else regret * cf_reach_probability_0
            )
            node.accumulate_action_regret(a, weigthed_regret)

        return node_utility

    def get_hand_win_probability(self, hand1: Hand, hand2: Hand):
        key = (
            hand1.compressed_representation() + "|" + hand2.compressed_representation()
        )
        return self.hand_win_probabilities[key]
