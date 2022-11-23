from .Card import Card
from . import constant

class SimShoe:

    def __init__(self, simulation_name):
        self.shoe_card_list = []
        suit = constant.SUIT_LIST[0]
        cards = []

        if simulation_name == "single_split_lose":
            cards = [2, 2, 2, 2, 2, 2, 8, 8, 7, 7, 10, 10, 10, 10]


        elif simulation_name == "multi_split_lose":
            cards = [2, 2, 2, 2, 2, 2, 8, 8, 7, 7, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

        elif simulation_name == "even_money_lose":
            cards = [2, 2, 2, 2, "A", "A", "10", "10"]

        elif simulation_name == "even_money_win":
            cards = [2, 2, 2, 2, "A", "A", "9", "10"]

        for card in cards:
            self.shoe_card_list.append(Card(suit, str(card)))

    def deal_card(self):
        return self.shoe_card_list.pop()
