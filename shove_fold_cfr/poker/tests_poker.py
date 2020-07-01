import unittest
from poker.hand import Hand
from poker.hand_type import HandType


class TestPokerHands(unittest.TestCase):
    def testHandGetValue(self):
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
        print(f"{high_card.get_hand_value()}")
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


if __name__ == "__main__":
    unittest.main()
