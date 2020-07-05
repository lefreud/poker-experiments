from poker.card import Card, SUITS, RANK_TO_CHAR
from poker.hand_value import HandValue
from poker.hand_type import HandType

MAX_HAND_SIZE = 7


class Hand:
    def __init__(self, hand):
        if type(hand) == str:
            self.cards = [Card(card_string) for card_string in hand.split()]
        else:
            self.cards = hand
        self.sorted_cards = Hand.sort_cards(self.cards)
        self.sorted_ranks = [card // 4 for card in self.sorted_cards]
        self.sorted_suits = [card % 4 for card in self.sorted_cards]

    @staticmethod
    def sort_cards(cards):
        card_ranks = [card // 4 for card in cards]
        return [card for _, card in sorted(zip(card_ranks, cards), reverse=True)]

    def get_card(self, index):
        return self.sorted_cards[index]

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
        for i in range(len(self.sorted_cards) - 1):
            if self.sorted_ranks[i] == self.sorted_ranks[i + 1]:
                heights = [self.sorted_ranks[i]]
                kickers = self.sorted_cards[:i] + self.sorted_cards[(i + 2) :]
                break
        else:
            kickers = None
            heights = None

        if kickers:
            return HandValue(HandType.ONE_PAIR, heights, kickers)
        else:
            return None

    def get_two_pairs(self):
        first_pair_index = None
        second_pair_index = None
        for i in range(len(self.sorted_cards) - 3):
            if self.sorted_ranks[i] == self.sorted_ranks[i + 1]:
                heights = [self.sorted_ranks[i]]
                first_pair_index = i
                break
        else:
            return None

        for i in range(first_pair_index + 2, len(self.sorted_cards) - 1):
            if self.sorted_ranks[i] == self.sorted_ranks[i + 1]:
                heights += [self.sorted_ranks[i]]
                second_pair_index = i
                break
        else:
            return None

        kickers = (
            self.sorted_cards[:first_pair_index]
            + self.sorted_cards[(first_pair_index + 2) : second_pair_index]
            + self.sorted_cards[(second_pair_index + 2) :]
        )
        return HandValue(HandType.TWO_PAIRS, heights, kickers)

    def get_three_of_a_kind(self):
        for i in range(len(self.sorted_cards) - 2):
            if (
                self.sorted_ranks[i]
                == self.sorted_ranks[i + 1]
                == self.sorted_ranks[i + 2]
            ):
                heights = [self.sorted_ranks[i]]
                kickers = self.sorted_ranks[:i] + self.sorted_ranks[(i + 2) :]
                break
        else:
            return None

        return HandValue(HandType.THREE_OF_A_KIND, heights, kickers)

    def get_straight(self):
        unique_ranks = list(set(self.sorted_ranks))

        if len(unique_ranks) >= 5:
            for i in range(len(unique_ranks) - 4):
                if unique_ranks[i : i + 4] == [2, 3, 4, 5] and unique_ranks[-1] == 14:
                    # Ace 2 3 4 5
                    heights = [5]
                    break
                elif (
                    unique_ranks[i + 4]
                    == unique_ranks[i + 3] + 1
                    == unique_ranks[i + 2] + 2
                    == unique_ranks[i + 1] + 3
                    == unique_ranks[i] + 4
                ):
                    heights = [unique_ranks[i + 4]]
                    break
            else:
                return None
            return HandValue(HandType.STRAIGHT, heights)
        else:
            return None

    def get_flush(self):
        suits = {
            suit: len(list(filter(lambda s: s == suit, self.sorted_suits)))
            for suit in SUITS
        }
        flush_suit = list(filter(lambda suit: suit[1] >= 5, suits.items()))
        if len(flush_suit) == 1:
            heights = list(
                map(
                    lambda card: card.rank,
                    filter(
                        lambda card: card.suit == flush_suit[0][0], self.sorted_cards
                    ),
                )
            )
        else:
            return None

        return HandValue(HandType.FLUSH, heights)

    def get_full_house(self):
        if (
            self.sorted_ranks[0] == self.sorted_ranks[1] == self.sorted_ranks[2]
            and self.sorted_ranks[3] == self.sorted_ranks[4]
        ):
            heights = [self.sorted_ranks[0]]
            kickers = [self.sorted_ranks[3]]
        elif (
            self.sorted_ranks[0] == self.sorted_ranks[1]
            and self.sorted_ranks[2] == self.sorted_ranks[3] == self.sorted_ranks[4]
        ):
            heights = [self.sorted_ranks[2]]
            kickers = [self.sorted_ranks[0]]
        else:
            heights = kickers = None

        return HandValue(HandType.FULL_HOUSE, heights, kickers) if heights else None

    def get_four_of_a_kind(self):
        if (
            self.sorted_ranks[0]
            == self.sorted_ranks[1]
            == self.sorted_ranks[2]
            == self.sorted_ranks[3]
        ):
            heights = [self.sorted_ranks[0]]
            kickers = [self.sorted_ranks[4]]
        elif (
            self.sorted_ranks[1]
            == self.sorted_ranks[2]
            == self.sorted_ranks[3]
            == self.sorted_ranks[4]
        ):
            heights = [self.sorted_ranks[1]]
            kickers = [self.sorted_ranks[0]]
        else:
            return None

        return HandValue(HandType.FOUR_OF_A_KIND, heights, kickers)

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

    def __eq__(self, other):
        return self.get_hand_value() == other.get_hand_value()

    def __repr__(self):
        return str(self.sorted_cards)

    def compressed_representation(self):
        heights = (
            RANK_TO_CHAR[self.sorted_ranks[0] + 2]
            + RANK_TO_CHAR[self.sorted_ranks[1] + 2]
        )
        suited = self.sorted_suits[0] % 4 == self.sorted_suits[1] % 4
        if suited:
            return heights + "s"
        else:
            return heights + "o"
