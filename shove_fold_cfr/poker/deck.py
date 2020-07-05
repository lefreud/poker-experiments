from poker.card import Card
from random import shuffle
import numpy as np


class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.card_index = 0
        self.cards = np.arange(52)

    def shuffle(self):
        np.random.shuffle(self.cards)

    def pop(self):
        self.card_index += 1
        return self.cards[self.card_index - 1]

    # def remove_cards(self, cards):
    #    self.cards = list(filter(lambda card: card not in cards, self.cards))

    # def peek(self, num_cards):
    #    return self.cards[-num_cards:]
