class Card:
    def __init__(self, card):
        self.rank = self.get_rank_from_char(card[0])
        self.suit = card[1]

    def get_rank(self):
        return self.rank

    def get_rank_string(self):
        if self.get_rank() == 10:
            rank = 'T'
        elif self.get_rank() == 11:
            rank = 'J'
        elif self.get_rank() == 12:
            rank = 'Q'
        elif self.get_rank() == 13:
            rank = 'K'
        elif self.get_rank() == 14:
            rank = 'A'
        else:
            rank = str(self.get_rank())
        return rank

    def get_suit(self):
        return self.suit

    def get_rank_from_char(self, char_rank):
        if char_rank == 'T':
            rank = 10
        elif char_rank == 'J':
            rank = 11
        elif char_rank == 'Q':
            rank = 12
        elif char_rank == 'K':
            rank = 13
        elif char_rank == 'A':
            rank = 14
        else:
            rank = int(char_rank)
        return rank

    def __lt__(self, other):
        return self.get_rank() < other.get_rank()

    def __gt__(self, other):
        return self.get_rank() > other.get_rank()

    def __repr__(self):
        return self.get_rank_string() + self.get_suit()
