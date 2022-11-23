

class GameSettings:

    def __init__(self):
        self.num_of_decks = 8
        self.table_min = 5
        self.starting_cash = 200
        #   payout ratios
        self.blackjack_ratio = 2.5

    # Functions to change settings

    def set_num_of_decks(self, num_of_decks):
        self.num_of_decks = num_of_decks

    def set_table_min(self, table_min):
        self.table_min = table_min

    def set_starting_cash(self, starting_cash):
        self.starting_cash = starting_cash

    def set_blackjack_ratio(self, blackjack_ratio):
        self.blackjack_ratio = blackjack_ratio
