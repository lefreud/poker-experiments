RANK_TO_CHAR = {(r + 2): c for (r, c) in enumerate("23456789TJQKA")}
CHAR_TO_RANK = {c: r for (r, c) in RANK_TO_CHAR.items()}
SUITS = {"H", "C", "D", "S"}


class Card:
    def __init__(self, card):
        self.rank_char = card[0]
        self.rank = CHAR_TO_RANK[card[0]]
        self.suit = card[1]

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __repr__(self):
        return RANK_TO_CHAR[self.rank] + self.suit
