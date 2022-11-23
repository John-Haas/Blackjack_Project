

class Wallet:

    side_bet = False

    def __init__(self, balance):
        self.balance = balance


    def check_balance(self):
        """Check chip amount"""
        print(f"You have ${self.balance}")


    def dub_down(self, bet):
        """Check if enough chips to double down"""
        if self.balance >= bet * 2:
            return True
        else:
            return False


    def bets_please(self, table_min):
        """Take player's bet"""
        self.check_balance()
        placed_bet, bet_valid = False, False

        while not bet_valid:
            placed_bet = int(input("Place your bets please:\t$"))
            # Check for table min
            if placed_bet < table_min:
                print(f"The table minimum is ${table_min}...")
            # Check if bet is too large
            elif placed_bet > self.balance:
                print(f"You only have ${self.balance}...")
            else:
                bet_valid = True

        self.bet = placed_bet
        return placed_bet
