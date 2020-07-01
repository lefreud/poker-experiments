RANK_TO_CHAR = {(r + 2): c for (r, c) in enumerate("23456789TJQKA")}
CHAR_TO_RANK = {c: r for (r, c) in RANK_TO_CHAR.items()}


class Card:
    def __init__(self, card):
        self.rank = CHAR_TO_RANK[card[0]]
        self.suit = card[1]

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __lt__(self, other):
        return self.get_rank() < other.get_rank()

    def __gt__(self, other):
        return self.get_rank() > other.get_rank()

    def __repr__(self):
        return RANK_TO_CHAR[self.get_rank()] + self.get_suit()
