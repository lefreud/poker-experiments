from poker.card import Card
from random import shuffle


class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = [Card(rank + suit) for rank in "23456789TJQKA" for suit in "HDCS"]

    def shuffle(self):
        shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def remove_cards(self, cards):
        self.cards = list(filter(lambda card: card not in cards, self.cards))

    def peek(self, num_cards):
        return self.cards[-num_cards:]
