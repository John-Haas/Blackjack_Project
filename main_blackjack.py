from models.constant import *
from models.Shoe import Shoe
from models.PlayerHand import PlayerHand
from models.DealerHand import DealerHand
from models.Wallet import Wallet
from models.Card import Card
from models.GameSettings import GameSettings
from game_methods import (
    welcome_screen, 
    settings_menu,
    initial_deal, 
    stage_1_ask, 
    insurance_ask, 
    insurance_taken, 
    even_money, 
    stage_1_action, 
    stage_2, 
    payout, 
    dealer_play, 
    split_cards, 
    split_ace_check, 
    render_multihand, 
    stage_1_splithand, 
    split,
    flush_terminal
)
import random
import time
import copy


def run_loop(shoe, wallet, game_settings):
        # Check for table minimum bet
        if wallet.balance < game_settings.table_min:
            print(f"The table minimum is ${game_settings.table_min}, you don't have enough to play...")
            exit()

        # Create the Hands
        base_hand = PlayerHand()
        dealer_hand = DealerHand()

        # Create List of player hands in case of splits
        player_hand_stack = [base_hand]

        # Take first bet
        wallet.check_balance()
        base_hand.bets_please(game_settings.table_min, wallet)

        # Deal the initial hands
        initial_deal(dealer_hand, base_hand, shoe)

        # Display hands and bets
        render_multihand(dealer_hand, player_hand_stack, 0)

        # Check hand for Blackjack
        base_hand.bj_check()

        # Insurance, mutual blackjack, & even money
        if dealer_hand.card_list[1].num_let == "A":
            # Even money, mutual blackjack
            if base_hand.hand_sum() == 21:
                even_money(dealer_hand, base_hand, wallet, game_settings.blackjack_ratio)
            else:
                # `Insurance`
                if insurance_ask(dealer_hand, base_hand, wallet):
                    insurance_taken(dealer_hand, base_hand, wallet)

        #######################################################################################
        # Stage 1 - Split and double down options
        #######################################################################################
        for hand in player_hand_stack:
            while hand.hand_status in STAGE_1:
                # Check if hand is a half dealt split hand
                stage_1_splithand(dealer_hand, player_hand_stack, hand, shoe)
                if hand.hand_status not in STAGE_1:
                    continue

                player_move = stage_1_ask(player_hand_stack, hand, wallet)
                stage_1_action(player_move, dealer_hand, player_hand_stack, hand, wallet, shoe)
            #######################################################################################
            # Stage 2 - Hit or stand
            #######################################################################################
            if hand.hand_status in STAGE_2:
                stage_2(dealer_hand, player_hand_stack, hand, shoe)
        
        #######################################################################################
        # Stage 3 - Dealer plays
        #######################################################################################
        for hand in player_hand_stack:
            if hand.hand_status in STAGE_3:
                dealer_play(dealer_hand, player_hand_stack, shoe)
                break
       
        ###########################################################################################
        # Stage 4 - Payout bets
        #######################################################################################
        payout(dealer_hand, player_hand_stack, wallet, game_settings.blackjack_ratio)

        # Clear table before next hand
        wallet.side_bet = False


if __name__ == "__main__":

    welcome_screen()

    # Get the game settings
    game_settings = GameSettings()
    settings_menu(game_settings)

    # Foundation objects
    flush_terminal()
    print(f"Let's play some Blackjack!")
    shoe = Shoe(game_settings.num_of_decks)
    wallet = Wallet(game_settings.starting_cash)

    while True:
        # Check if Shoe has enough cards
        shoe.shuf_check()

        # Run the main loop
        run_loop(shoe, wallet, game_settings)
