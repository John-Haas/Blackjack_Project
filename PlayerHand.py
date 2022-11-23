import time
import sys
from . import constant


def check_exit(val):
    """Exit game"""
    if val and val.lower() == "exit":
        print("Thank you for playing! ")
        print(f"{SNAKE}The Python Casino welcomes you back anytime{SNAKE}\n")
        sys.exit(0)


class PlayerHand:

    def __init__(self):
        self.card_list = []
        self.hand_status = "stage 1"
        self.bet = 0


    def bets_please(self, table_min, W):
        """Take the hand's bet"""
        placed_bet, bet_valid = False, False
        while not bet_valid:
            # Grab the user input
            placed_bet = input("Place your bets please:\t$")

            # Check to see if we should exit
            check_exit(placed_bet)

            # Check to see if digit
            if placed_bet.isdigit():
                placed_bet = int(placed_bet)
                # Check to see if bet if sufficient
                if placed_bet < table_min:
                    print(f"The table minimum is ${table_min}.")
                elif placed_bet > W.balance:
                    print(f"You only have ${W.balance}.")
                else:
                    bet_valid = True
                    self.bet = placed_bet
                    W.balance -= self.bet
            else:
                print("Please enter a valid whole number.")


    def hand_sum(self):
        """Return the sum of the hand"""
        sum_val = 0
        for card in self.card_list:
            sum_val += card.num_value
        return sum_val


    def split_check(self):
        """Check if hand is able to split"""
        if self.card_list[0].num_let == self.card_list[1].num_let:
            return True
        else:
            return False


    def bj_check(self):
        """Check hand for Blackjack"""
        if self.hand_sum() == 21:
            print("Player has BLACKJACK!")
            time.sleep(2)
            self.hand_status = "blackjack"
            return True
        else:
            return False


    def ace_check(self):
        """Check hand for Aces that should change value from 11 to 1"""
        ace_list = []
        for card in self.card_list:
            if card.num_let == "A":
                ace_list.append(card)
        
        for ace in ace_list:
            if self.hand_sum() > 21:
                ace.ace_switch()


    def bust_check(self):
        """Check if hand busted"""
        if self.hand_sum() > 21:
            print("Oh no! Player busts!")
            self.hand_status = "bust"


    def show_hand(self):
        """Print hand"""
        print(self.card_list)


    def stage_2(self):
        """Run stage 2 functions"""
        self.bj_check()
        split_valid = self.split_check()


    def take_card(self, card):
        """Hand receives card"""
        self.card_list.append(card)
        # Check the sum, if it's an Ace then swap
        self.ace_check()


    def dub_down_check(self):
        """Check if hand can double down"""
        if len(self.card_list) == 2:
            return True
        else:
            return False


    def status_change(self, stage):
        """Change hand status"""
        self.hand_status = stage
