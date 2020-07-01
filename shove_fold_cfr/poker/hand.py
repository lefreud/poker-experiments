from poker.card import Card
from poker.hand_value import HandValue
from poker.hand_type import HandType


class Hand:
    def __init__(self, hand):
        self.sorted_cards = self.sort_hand(hand)

    def sort_hand(self, hand):
        cards = [Card(card_string) for card_string in hand.split()]
        card_ranks = []
        for card in cards:
            card_ranks += [card.rank]
        return [card for _, card in sorted(zip(card_ranks, cards), reverse=True)]

    def get_card(self, index):
        return self.sorted_cards[index]

    def get_card_rank(self, index):
        return self.sorted_cards[index].rank

    def get_card_suit(self, index):
        return self.sorted_cards[index].suit

    def get_hand_value(self):
        hand_value = (
            self.get_straight_flush()
            or self.get_four_of_a_kind()
            or self.get_full_house()
            or self.get_flush()
            or self.get_straight()
            or self.get_three_of_a_kind()
            or self.get_two_pairs()
            or self.get_one_pair()
            or self.get_high_card()
        )
        return hand_value

    def get_high_card(self):
        heights = [card.rank for card in self.sorted_cards]
        return HandValue(HandType.HIGH_CARD, heights)

    def get_one_pair(self):
        if self.get_card_rank(0) == self.get_card_rank(1):
            heights = [self.get_card_rank(0)]
            kickers = [
                self.get_card_rank(2),
                self.get_card_rank(3),
                self.get_card_rank(4),
            ]
        elif self.get_card_rank(1) == self.get_card_rank(2):
            heights = [self.get_card_rank(1)]
            kickers = [
                self.get_card_rank(0),
                self.get_card_rank(3),
                self.get_card_rank(4),
            ]
        elif self.get_card_rank(2) == self.get_card_rank(3):
            heights = [self.get_card_rank(2)]
            kickers = [
                self.get_card_rank(0),
                self.get_card_rank(1),
                self.get_card_rank(4),
            ]
        elif self.get_card_rank(3) == self.get_card_rank(4):
            heights = [self.get_card_rank(3)]
            kickers = [
                self.get_card_rank(0),
                self.get_card_rank(1),
                self.get_card_rank(2),
            ]
        else:
            kickers = None
            heights = None

        if kickers:
            return HandValue(HandType.ONE_PAIR, heights, kickers)
        else:
            return None

    def get_two_pairs(self):
        heights = [self.get_card_rank(1), self.get_card_rank(3)]
        if self.get_card_rank(0) == self.get_card_rank(1) and self.get_card_rank(
            2
        ) == self.get_card_rank(3):
            kickers = [self.get_card_rank(4)]
        elif self.get_card_rank(0) == self.get_card_rank(1) and self.get_card_rank(
            3
        ) == self.get_card_rank(4):
            kickers = [self.get_card_rank(2)]
        elif self.get_card_rank(1) == self.get_card_rank(2) and self.get_card_rank(
            3
        ) == self.get_card_rank(4):
            kickers = [self.get_card_rank(0)]
        else:
            kickers = None

        if kickers:
            return HandValue(HandType.TWO_PAIRS, heights, kickers)
        else:
            return None

    def get_three_of_a_kind(self):
        heights = [self.get_card_rank(2)]
        if self.get_card_rank(0) == self.get_card_rank(1) == self.get_card_rank(2):
            kickers = [self.get_card_rank(3), self.get_card_rank(4)]
        elif self.get_card_rank(1) == self.get_card_rank(2) == self.get_card_rank(3):
            kickers = [self.get_card_rank(0), self.get_card_rank(4)]
        elif self.get_card_rank(2) == self.get_card_rank(3) == self.get_card_rank(4):
            kickers = [self.get_card_rank(0), self.get_card_rank(1)]
        else:
            kickers = None

        if kickers:
            return HandValue(HandType.THREE_OF_A_KIND, heights, kickers)
        else:
            return None

    def get_straight(self):
        if self.get_card_rank(1) == 5 and self.get_card_rank(0) == 14:
            heights = [self.get_card_rank(1)]
        else:
            heights = [self.get_card_rank(0)]

        if heights[0] == 5:
            valid_straight = (
                heights[0]
                == self.get_card_rank(1)
                == self.get_card_rank(2) + 1
                == self.get_card_rank(3) + 2
                == self.get_card_rank(4) + 3
            )
        else:
            valid_straight = (
                self.get_card_rank(0)
                == self.get_card_rank(1) + 1
                == self.get_card_rank(2) + 2
                == self.get_card_rank(3) + 3
                == self.get_card_rank(4) + 4
            )

        if valid_straight:
            return HandValue(HandType.STRAIGHT, heights)
        else:
            return None

    def get_flush(self):
        heights = [card.rank for card in self.sorted_cards]
        valid_flush = (
            self.get_card_suit(0)
            == self.get_card_suit(1)
            == self.get_card_suit(2)
            == self.get_card_suit(3)
            == self.get_card_suit(4)
        )

        return HandValue(HandType.FLUSH, heights) if valid_flush else None

    def get_full_house(self):
        if self.get_card_rank(0) == self.get_card_rank(1) == self.get_card_rank(
            2
        ) and self.get_card_rank(3) == self.get_card_rank(4):
            heights = [self.get_card_rank(0)]
            kickers = [self.get_card_rank(3)]
        elif self.get_card_rank(0) == self.get_card_rank(1) and self.get_card_rank(
            2
        ) == self.get_card_rank(3) == self.get_card_rank(4):
            heights = [self.get_card_rank(2)]
            kickers = [self.get_card_rank(0)]
        else:
            heights = kickers = None

        return HandValue(HandType.FULL_HOUSE, heights, kickers) if heights else None

    def get_four_of_a_kind(self):
        if (
            self.get_card_rank(0)
            == self.get_card_rank(1)
            == self.get_card_rank(2)
            == self.get_card_rank(3)
        ):
            heights = [self.get_card_rank(0)]
            kickers = [self.get_card_rank(4)]
        elif (
            self.get_card_rank(1)
            == self.get_card_rank(2)
            == self.get_card_rank(3)
            == self.get_card_rank(4)
        ):
            heights = [self.get_card_rank(1)]
            kickers = [self.get_card_rank(0)]
        else:
            heights = kickers = None

        return HandValue(HandType.FOUR_OF_A_KIND, heights, kickers) if heights else None

    def get_straight_flush(self):
        if not self.get_flush():
            return None

        straight = self.get_straight()
        if straight:
            return HandValue(
                HandType.STRAIGHT_FLUSH, straight.get_heights(), straight.get_kickers()
            )
        else:
            return None

    def __lt__(self, other):
        return self.get_hand_value() < other.get_hand_value()

    def __repr__(self):
        return str(self.sorted_cards)
