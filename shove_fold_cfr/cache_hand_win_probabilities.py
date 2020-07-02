from constants import *
from random import shuffle
from trainer.node import Node
from poker.deck import Deck
from poker.hand import Hand
import json


EXPECTED_VALUE_SIMULATIONS = 200
sorted_deck = Deck()


def get_cards_permutations(current_cards: list, remaining_cards=4):
    if remaining_cards == 0:
        return [current_cards]
    card_permutations = []
    for card in sorted_deck.cards:
        # Only hearts and diamonds
        if not card in current_cards:
            card_permutations += get_cards_permutations(
                current_cards + [card], remaining_cards - 1
            )

    return card_permutations


def compute_hand_win_probability(
    deck: Deck, private_hand_0: Hand, private_hand_1: Hand
):
    """
        Returns a real between 0 and 1 representing the expected win rate
        of Private Hand 0 against Private Hand 1, when randomly sampling
        public cards.
        """
    wins = 0
    for _ in range(EXPECTED_VALUE_SIMULATIONS):
        deck.shuffle()
        public_cards = deck.peek(5)
        full_hand_0 = Hand(private_hand_0.cards + public_cards)
        full_hand_1 = Hand(private_hand_1.cards + public_cards)
        if full_hand_0 > full_hand_1:
            wins += 1
        elif full_hand_0 == full_hand_1:
            wins += 0.5
    return wins / EXPECTED_VALUE_SIMULATIONS


win_probabilities = {}
permutations = get_cards_permutations([])
for i, cards_permutation in enumerate(permutations):
    deck = Deck()
    deck.remove_cards(cards_permutation)
    h1 = Hand(cards_permutation[0:2])
    h2 = Hand(cards_permutation[2:4])
    key = h1.compressed_representation() + "|" + h2.compressed_representation()
    if not win_probabilities.get(key):
        win_probabilities[key] = compute_hand_win_probability(deck, h1, h2)
    if i % 1000 == 0:
        print(f"{i}/{len(permutations)}")

with open(WIN_PROBABILITIES_FILENAME, "w") as f:
    json.dump(win_probabilities, f)
