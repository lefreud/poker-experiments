import unittest
from poker.hand import Hand
from poker.hand_type import HandType
from poker.deck import Deck


class TestPokerHands(unittest.TestCase):
    def test_hand_value_five_cards(self):
        high_card = Hand("TH 2C 3C 4C 5C")
        one_pair = Hand("6H 6D TC JS 8C")
        two_pairs = Hand("9C 9D 8C 7C 8S")
        three_of_a_kind = Hand("3C 3S 3D AS KS")
        straight_1 = Hand("AC 2D 3D 4S 5H")
        straight_2 = Hand("6C 2D 3D 4S 5H")
        straight_3 = Hand("AH KH QS JS TS")
        flush_1 = Hand("AC TC 3C 4C 5C")
        flush_2 = Hand("JS TS AS KS 2S")
        full_house_1 = Hand("AS AD AC TD TS")
        full_house_2 = Hand("AS AD TH TD TS")
        four_of_a_kind = Hand("3C 3S 3C 3D 4C")
        straight_flush_1 = Hand("AC 2C 3C 4C 5C")
        straight_flush_2 = Hand("AC KC QC JC TC")
        self.assertEqual(HandType.HIGH_CARD, high_card.get_hand_value().get_hand_type())
        self.assertEqual(HandType.ONE_PAIR, one_pair.get_hand_value().get_hand_type())
        self.assertEqual(HandType.TWO_PAIRS, two_pairs.get_hand_value().get_hand_type())
        self.assertEqual(
            HandType.THREE_OF_A_KIND, three_of_a_kind.get_hand_value().get_hand_type()
        )
        self.assertEqual(HandType.STRAIGHT, straight_1.get_hand_value().get_hand_type())
        self.assertEqual(HandType.STRAIGHT, straight_2.get_hand_value().get_hand_type())
        self.assertEqual(HandType.STRAIGHT, straight_3.get_hand_value().get_hand_type())
        self.assertEqual(HandType.FLUSH, flush_1.get_hand_value().get_hand_type())
        self.assertEqual(HandType.FLUSH, flush_2.get_hand_value().get_hand_type())
        self.assertEqual(
            HandType.FULL_HOUSE, full_house_1.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.FULL_HOUSE, full_house_2.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.FOUR_OF_A_KIND, four_of_a_kind.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.STRAIGHT_FLUSH, straight_flush_1.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.STRAIGHT_FLUSH, straight_flush_2.get_hand_value().get_hand_type()
        )

    def test_hand_value_seven_cards(self):
        high_card = Hand("TH 2C 3C 4C 5C 8H 9D")
        one_pair = Hand("4C 9C 6H 6D TC JS 8C")
        two_pairs = Hand("6D 9C AC 9D 8C 7C 8S")
        three_of_a_kind = Hand("3C 3S 3D AS KS 2H 7D")
        straight_1 = Hand("AC QC 2D 3D TD 4S 5H")
        straight_2 = Hand("6C 2D 3D 8D 4S 5H 9D")
        straight_3 = Hand("AH KH QS JS TS 2D 3D")
        flush_1 = Hand("AC TC 3C 4C 5C 9D 8D")
        flush_2 = Hand("JS TS AS KS 2S 3C 4C")
        full_house_1 = Hand("AS AD AC TD TS 9C 9H")
        full_house_2 = Hand("AS AD TH TD TS 2C 3C")
        four_of_a_kind = Hand("3C 3S 3C 3D 4C 5D 6H")
        straight_flush_1 = Hand("AC 2C 3C 4C 5C 8D 9D")
        straight_flush_2 = Hand("AC KC QC JC TC 2H 3H")
        self.assertEqual(HandType.HIGH_CARD, high_card.get_hand_value().get_hand_type())
        self.assertEqual(HandType.ONE_PAIR, one_pair.get_hand_value().get_hand_type())
        self.assertEqual(HandType.TWO_PAIRS, two_pairs.get_hand_value().get_hand_type())
        self.assertEqual(
            HandType.THREE_OF_A_KIND, three_of_a_kind.get_hand_value().get_hand_type()
        )
        self.assertEqual(HandType.STRAIGHT, straight_1.get_hand_value().get_hand_type())
        self.assertEqual(HandType.STRAIGHT, straight_2.get_hand_value().get_hand_type())
        self.assertEqual(HandType.STRAIGHT, straight_3.get_hand_value().get_hand_type())
        self.assertEqual(HandType.FLUSH, flush_1.get_hand_value().get_hand_type())
        self.assertEqual(HandType.FLUSH, flush_2.get_hand_value().get_hand_type())
        self.assertEqual(
            HandType.FULL_HOUSE, full_house_1.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.FULL_HOUSE, full_house_2.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.FOUR_OF_A_KIND, four_of_a_kind.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.STRAIGHT_FLUSH, straight_flush_1.get_hand_value().get_hand_type()
        )
        self.assertEqual(
            HandType.STRAIGHT_FLUSH, straight_flush_2.get_hand_value().get_hand_type()
        )


class TestDeck(unittest.TestCase):
    def test_shuffle(self):
        deck1 = Deck()
        deck2 = Deck()
        deck2.shuffle()
        assert deck1.cards != deck2.cards
        assert len(deck2.cards) == 52


if __name__ == "__main__":
    unittest.main()
