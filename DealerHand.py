


class DealerHand:

    def __init__(self):
        self.card_list = []
        self.hand_status = "live"
        self.hole = True


    def hand_sum(self):
        """Find sum of cards in hand"""
        sum_val = 0
        for card in self.card_list:
            sum_val += card.num_value
        return sum_val


    def ace_check(self):
        """Check hand for Aces that should change value from 11 to 1"""
        ace_list = []
        for card in self.card_list:
            if card.num_let == "A":
                ace_list.append(card)
        
        for ace in ace_list:
            if self.hand_sum() > 21:
                ace.ace_switch()


    def bj_check(self):
        """Check hand for blackjack"""
        if self.hand_sum() == 21:
            self.hand_status = "blackjack"
            return True
        else:
            return False


    def overturn_holecard(self):
        """Overturn the first card after the player's hand is dealt"""
        self.hole = False


    def take_card(self, card):
        """Receive card"""
        self.card_list.append(card)
        # Check the sum, if it's an Ace then swap
        self.ace_check()


    def bust_check(self):
        """Check if hand busted"""
        # self.ace_check()
        if self.hand_sum() > 21:
            print(f"Dealer busts at {self.hand_sum()}")
            self.hand_status = "bust"
