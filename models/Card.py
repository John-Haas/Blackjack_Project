

class Card:

    def __init__(self, suit, num_let):

        self.suit = suit
        # numlet is number/letter... 2-10, J, Q, K, A
        self.num_let = num_let
        # this prints out the suit and card *example: ♠10
        self.card_id = f"{suit}{num_let}"

        # this finds the numeric value
        if self.num_let in [str(x) for x in range(1, 11)]:
            self.num_value = int(self.num_let)
        elif self.num_let == "A":
            self.num_value = 11
        else:
            self.num_value = 10

    def ace_switch(self):
        """Change Ace card's value from 11 to 1"""
        self.num_value = 1

    def render(self):
        """print numlet"""
        print(self.card_id)
