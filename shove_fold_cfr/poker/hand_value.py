class HandValue:
    def __init__(self, hand_type, heights=[], kickers=[]):
        self.hand_type = hand_type
        self.heights = heights
        self.kickers = kickers

    def get_hand_type(self):
        return self.hand_type

    def get_heights(self):
        return self.heights

    def get_kickers(self):
        return self.kickers

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True
        elif self.hand_type.value > other.hand_type.value:
            return False

        if self.heights < other.heights:
            return True
        elif self.heights > other.heights:
            return False

        if self.kickers < other.kickers:
            return True
        else:
            return False

    def __repr__(self):
        return f'Type: {self.hand_type}, Heights: {self.heights}, Kickers: {self.kickers}'