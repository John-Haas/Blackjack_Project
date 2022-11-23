# from . import Deck
from .Card import Card
# from . import Card
from . import constant
# import constant
import random


class Shoe:

    def __init__(self, num_of_decks):
        self.num_of_decks = num_of_decks
        self.shoe_card_list = []
        self.populate_and_shuf_shoe()
        self.shuf_check()


    def populate_and_shuf_shoe(self):
        """Stock and shuffle Shoe"""
        for decks in range(0, self.num_of_decks):
            for numlet in constant.NUM_LET_LIST:
                for suit in constant.SUIT_LIST:
                    self.shoe_card_list.append(Card(suit, numlet))
        random.shuffle(self.shoe_card_list)


    def shuf_check(self):
        """Check if shoe is past 75% mark"""
        if len(self.shoe_card_list) < (52 * self.num_of_decks * .25):
            self.shoe_card_list = []
            self.populate_and_shuf_shoe()
        return self.shoe_card_list


    def deal_card(self):
        """Deal card from Shoe"""
        return self.shoe_card_list.pop()
