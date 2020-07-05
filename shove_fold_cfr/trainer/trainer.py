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
        self.iteration = 1
        self.cumulative_stack_utilities = [
            0 for stack_size in range(TOTAL_STACKS + 1)  # (stack_size) / TOTAL_STACKS
        ]
        for self.iteration in range(1, iterations):
            for p0_stack in range(1, TOTAL_STACKS):
                p1_stack = TOTAL_STACKS - p0_stack
                deck.reset()
                deck.shuffle()
                p0_hand = Hand([deck.pop(), deck.pop()])
                p1_hand = Hand([deck.pop(), deck.pop()])
                big_blind = min(BIG_BLIND, p0_stack, p1_stack)
                self.cumulative_stack_utilities[p0_stack] += self.cfr(
                    deck,
                    (p0_hand, p1_hand),
                    EMPTY_HISTORY,
                    (p0_stack, p1_stack),
                    (SMALL_BLIND, big_blind),
                    (1, 1),
                )
        # print(f"Average game value: {utility/iterations}")
        print(f"Iterations: {iterations}")
        print("Stack size,Utility")
        for stack_size, utility in enumerate(self.cumulative_stack_utilities):
            print(f"{stack_size},{self.get_average_stack_utility(stack_size)}")
        for node in map(lambda node: node[1], sorted(self.node_map.items())):
            print(node)

    def get_average_stack_utility(self, stack_size):
        if stack_size == TOTAL_STACKS:
            return 1  # 100% sure of winning
        elif stack_size == 0:
            return -1  # 100% sure of losing
        return self.cumulative_stack_utilities[stack_size] / self.iteration

    def cfr(
        self,
        deck: Deck,
        private_hands: tuple,
        history: str,
        stack_sizes: tuple,
        invested_chips: tuple,
        cf_reach_probabilities: tuple,
    ):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        if len(history) > 0:
            if history[-1] == "f":
                # Opponent folds, we get its invested chips
                return self.get_average_stack_utility(
                    stack_sizes[player] + invested_chips[opponent]
                )

            hand_win_probability = self.get_hand_win_probability(
                private_hands[player], private_hands[opponent]
            )
            # player_expected_value = invested_chips[opponent] * (
            #    hand_win_probability - 0.5
            # )
            win_expected_utility = (
                self.get_average_stack_utility(
                    stack_sizes[player] + invested_chips[opponent]
                )
                * hand_win_probability
            )
            lose_expected_utility = self.get_average_stack_utility(
                stack_sizes[player] - invested_chips[player]
            ) * (1 - hand_win_probability)
            if history == "cc":
                # We call as small blind, then the big blind checks
                return win_expected_utility + lose_expected_utility
            if history[-2:] == "bc":
                # We go all in, opponent calls
                return win_expected_utility + lose_expected_utility

        information_set = (
            private_hands[player].compressed_representation()
            + "_"
            + str(stack_sizes[player])
            + "_"
            + str(stack_sizes[opponent])
            + "_"
            + history
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
        node.update_average_strategy(strategy, cf_reach_probabilities[player])

        action_utilities = [0 for _ in range(NUM_ACTIONS)]
        node_utility = 0

        for a, action in enumerate(possible_actions):
            next_history = history + action
            if action == "f":
                player_invested_chips = invested_chips[player]
            elif action == "c":
                player_invested_chips = invested_chips[opponent]
            elif action == "b":
                player_invested_chips = min(stack_sizes)

            if player == 0:
                new_invested_chips = (player_invested_chips, invested_chips[1])
                new_cf_reach_probabilities = (
                    cf_reach_probabilities[0] * strategy[a],
                    cf_reach_probabilities[1],
                )
            else:
                new_invested_chips = (invested_chips[0], player_invested_chips)
                new_cf_reach_probabilities = (
                    cf_reach_probabilities[0],
                    cf_reach_probabilities[1] * strategy[a],
                )

            action_utilities[a] = -self.cfr(
                deck,
                private_hands,
                next_history,
                stack_sizes,
                new_invested_chips,
                new_cf_reach_probabilities,
            )
            node_utility += action_utilities[a] * strategy[a]

        for a, _ in enumerate(possible_actions):
            regret = action_utilities[a] - node_utility
            weigthed_regret = regret * cf_reach_probabilities[opponent]
            node.accumulate_action_regret(a, weigthed_regret)

        return node_utility

    def get_hand_win_probability(self, hand1: Hand, hand2: Hand):
        key = (
            hand1.compressed_representation() + "|" + hand2.compressed_representation()
        )
        return self.hand_win_probabilities[key]
