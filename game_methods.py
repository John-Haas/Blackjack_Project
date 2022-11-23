from models.constant import *
from models.PlayerHand import *
from models.DealerHand import *
from models.Card import *
from models.Wallet import *
from models.Shoe import *
import time
import os
import sys


def is_float(num):
    """Helper function to parse input values"""
    try:
        float(num)
        return True
    except ValueError:
        return False


def flush_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_exit(val):
    """Exit game"""
    if val and val.lower() == "exit":
        print("Thank you for playing! ")
        print(f"{SNAKE}The Python Casino welcomes you back anytime{SNAKE}\n")
        sys.exit(0)


def ascii_bj():
    """Prints ASCII Blackjack"""
    output = """

              
 _     _            _    _            _    
| |   | |          | |  (_)          | |   
| |__ | | __ _  ___| | ___  __ _  ___| | __
| '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
| |_) | | (_| | (__|   <| | (_| | (__|   < 
|_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\ 
                       _/ |                
                      |__/                 
              
"""
    print(output)
    time.sleep(3)


def welcome_screen():
    """Runs welcome screen with rules and directions to game"""
    flush_terminal()
    ascii_bj()

    # Show rules and commands before game begins
    # else:
    print("""
    Rules:
        To learn the rules of Blackjack, go to:
        wizardofodds.com/games/blackjack/basics/#rules
        
    Commands:   
        (H)it
        (S)tand
        (D)ouble down
        (Sp)lit.""")


def settings_menu(game_settings):
    """Change game settings"""
    continue_or_settings = input("\n\nPress enter to continue, or type \"settings\" to change the game's settings: ")

    if continue_or_settings.lower() == "settings":
        flush_terminal()
        print("Update the default game settings. Press enter to continue.")
        
        # Blackjack Ratio
        blackjack_ratio = input("1. Update Blackjack Ratio (default {}): ".format(game_settings.blackjack_ratio))
        if is_float(blackjack_ratio):
            game_settings.set_blackjack_ratio(float(blackjack_ratio))
        
        # Table minimum
        table_min = input("2. Update Table Minimum (default {}): ".format(game_settings.table_min))
        if table_min.isdigit():
            game_settings.set_table_min(int(table_min))

        # Starting cash
        starting_cash = input("3. Update Starting Cash (default {}): ".format(game_settings.starting_cash))
        if starting_cash.isdigit():
            game_settings.set_starting_cash(int(starting_cash))   
    print(
        ("\nGame Settings:\n" + \
        "\tNumber of Decks: {}\n" + \
        "\tBlackjack Ratio: {}\n" + \
        "\tTable Minimum:   {}\n" + \
        "\tStarting Cash:   {}\n") \
        .format(
            game_settings.num_of_decks,
            game_settings.blackjack_ratio,
            game_settings.table_min,
            game_settings.starting_cash
        ))
    time.sleep(2)


def initial_deal(dealers_hand, players_hand, _shoe):
    """Deal first set of cards"""
    for i in range(2):
        players_hand.take_card(_shoe.deal_card())
        dealers_hand.take_card(_shoe.deal_card())


def card_list_render(hand, hole=False):
    """Building block for render"""
    # The text to display on each row.
    rows = ['', '', '', '', '']

    for i, card in enumerate(hand.card_list):
        rows[0] += ' ___  '  # Print the top line of the card.
        if i == 0 and hole:
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            # rank, suit = card  # The card is a tuple data structure.
            rows[1] += '|{} | '.format(card.num_let.ljust(2))
            rows[2] += '| {} | '.format(card.suit)
            rows[3] += '|_{}| '.format(card.num_let.rjust(2, '_'))

    # Print each row on the screen:
    for row in rows:
        print(row)
    return ""


def hand_stack_render(hand_stack):
    """Render all of player's hands"""
    # The text to display on each row
    rows = ['', '', '', '', '', '', '', '']
    # Comput left adjust

    for j, hand in enumerate(hand_stack):
        card_rows = [[], [], [], []]
        for i, card in enumerate(hand.card_list):
            # Print the top line of the card.
            card_rows[0].append(' ___  ')
            # Print the card's front:
            # rank, suit = card  # The card is a tuple data structure.
            card_rows[1].append('|{} | '.format(card.num_let.ljust(2)))
            card_rows[2].append('| {} | '.format(card.suit))
            card_rows[3].append('|_{}| '.format(card.num_let.rjust(2, '_')))
        
        left_just = (len(hand.card_list)+1) * 6
        rows[0] += ''.join(card_rows[0]).ljust(left_just, ' ')
        rows[1] += ''.join(card_rows[1]).ljust(left_just, ' ')
        rows[2] += ''.join(card_rows[2]).ljust(left_just, ' ')
        rows[3] += ''.join(card_rows[3]).ljust(left_just, ' ')

        # Check if we need to label the hands
        if len(hand_stack) > 1:
            rows[4] += f"[Hand {j}]".ljust(left_just, ' ')

        rows[5] += f"Hand: {hand.hand_sum()}".ljust(left_just, ' ')
        rows[6] += f"Bet: ${hand.bet}".ljust(left_just, ' ')

        # Add to the strings
        if j < (len(hand_stack) - 1):
            for row in rows:
                row += '    '

    # Print each row on the screen:
    for row in rows:
        print(row)


def render_multihand(dealers_hand, hand_stack, active_hand_index):
    """Show Dealer Hand and all player hands, highlights active hand"""
    flush_terminal()
    print("__________________[Dealer Cards]__________________")
    card_list_render(dealers_hand, dealers_hand.hole)
    # print(f"Hand: {dealers_hand.hand_sum()}")

    if len(hand_stack) > 0:
        print("__________________[Player Cards]__________________")
        hand_stack_render(hand_stack)


def stage_1_ask(hand_stack, active_hand, _wallet):
    """This begins stage 1, it asks for the player's move of Hit, Stand, Double Down, and Split"""
    hand_idx = ""
    if len(hand_stack) > 1:
        hand_idx = "(Hand {}) ".format(hand_stack.index(active_hand))

    player_move = ""
    if _wallet.dub_down(active_hand.bet) and active_hand.dub_down_check():

        if active_hand.split_check() and (len(hand_stack) < 4):
            player_move = input("{}Do you want to (H)it, (S)tand, (D)ouble Down, or (Sp)lit? ".format(hand_idx)).lower()
        else:
            player_move = input("{}Do you want to (H)it, (S)tand, or (D)ouble Down? ".format(hand_idx)).lower()
    elif active_hand.split_check() and (len(hand_stack) < 4):
        player_move = input("{}Do you want to (H)it, (S)tand, or (Sp)lit? ".format(hand_idx)).lower()
    else:
        player_move = input("{}Do you want to (H)it or (S)tand? ".format(hand_idx)).lower()

    check_exit(player_move)
    return player_move


def stage_1_splithand(dealers_hand, hand_stack, active_hand, _shoe):
    """This runs a split hand through Stage 1"""
    hand_idx = "(Hand {}) ".format(hand_stack.index(active_hand))

    if len(active_hand.card_list) < 2:
        # time.sleep(3)
        new_card = _shoe.deal_card()
        active_hand.take_card(new_card)
        render_multihand(dealers_hand, hand_stack, hand_stack.index(active_hand))
        print(f"{hand_idx}Player draws a {new_card.card_id}! Player's hand total at {active_hand.hand_sum()}")
        time.sleep(2)
        is_bj = active_hand.bj_check

        if not is_bj:
            split_ace_check(dealers_hand, hand_stack, hand_stack.index(active_hand), active_hand)


def split(dealers_hand, hand_stack, active_hand, _wallet, _shoe):
    """Preform split"""
    # Add new hand
    hand_stack.insert((hand_stack.index(active_hand) + 1), PlayerHand())
    # Move cards
    split_cards(hand_stack, hand_stack.index(active_hand), hand_stack.index(active_hand) + 1, _wallet, _shoe)
    render_multihand(dealers_hand, hand_stack, hand_stack.index(active_hand))
    print("Player splits!")
    time.sleep(2)
    split_ace_check(dealers_hand, hand_stack, hand_stack.index(active_hand), active_hand)


def stage_1_action(player_move, dealers_hand, hand_stack, active_hand, _wallet, _shoe):
    """Preform actions of stage 1"""
    # If player doubled down
    if player_move in DUB_DOWN_COMMANDS:
        # Take doubled bet
        _wallet.balance -= active_hand.bet
        active_hand.bet *= 2
        # Deal double down card
        new_card = _shoe.deal_card()
        active_hand.take_card(new_card)
        render_multihand(dealers_hand, hand_stack, False)
        print(f"Player doubles down and draws a {new_card.card_id}! Player's hand total at {active_hand.hand_sum()}")
        time.sleep(3)
        # Check outcome
        active_hand.status_change("stand")
        active_hand.bust_check()
        return False

    # If player hit
    if player_move in HIT_COMMANDS:
        new_card = _shoe.deal_card()
        active_hand.take_card(new_card)
        render_multihand(dealers_hand, hand_stack, False)
        print(f"Player draws a {new_card.card_id}! Player's hand total at {active_hand.hand_sum()}")
        time.sleep(2)
        active_hand.status_change("stage 2")
        return False

    # If player stands
    if player_move in STAND_COMMANDS:
        active_hand.status_change("stand")
        return False

    # If player split
    if player_move in SPLIT_COMMANDS:
        split(dealers_hand, hand_stack, active_hand, _wallet, _shoe)


def split_cards(player_hand_stack, base_index, split_index, _wallet, _shoe):
    """Splits a hand"""
    # Take second bet
    player_hand_stack[split_index].bet = player_hand_stack[base_index].bet
    _wallet.balance -= player_hand_stack[split_index].bet
    # Move cards
    player_hand_stack[split_index].card_list.append(player_hand_stack[base_index].card_list[1])
    # Delete duplicate card
    del player_hand_stack[base_index].card_list[1]


def split_ace_check(dealers_hand, hand_stack, active_hand_index, active_hand):
    """Preforms single card hit for split hand dealt an Ace"""
    if active_hand.card_list[0].num_let == "A":
        hand_stack[active_hand_index].status_change("stand")
        bj_yn = hand_stack[active_hand_index].bj_check()
        if not bj_yn:
            print(f"Hand stands at {hand_stack[active_hand_index].hand_sum()}")
        # time.sleep(3)


def stage_2(dealers_hand, hand_stack, active_hand, _shoe):
    """Preforms stage 2 actions"""
    render_multihand(dealers_hand, hand_stack, hand_stack.index(active_hand))
    active_hand.bust_check()

    while active_hand.hand_sum() < 21:
        # Get player move
        player_move = input("Do you want to (H)it or (S)tand? ").lower()
        check_exit(player_move)

        # If player stands
        if player_move in STAND_COMMANDS:
            active_hand.status_change("stand")
            break

        # If player hits
        if player_move in HIT_COMMANDS:
            new_card = _shoe.deal_card()
            active_hand.take_card(new_card)
            render_multihand(dealers_hand, hand_stack, False)
            print(f"Player draws a {new_card.card_id}! Player's hand total at {active_hand.hand_sum()}")
            time.sleep(2)

            active_hand.bust_check()

    # Check for 21
    if active_hand.hand_sum() == 21:
        active_hand.status_change("stand")


#  Side bet functions:
def insurance_ask(dealers_hand, players_hand, _wallet):
    """Asks player if they want insurance"""
    print(f"\nDo you want insurance for ${players_hand.bet / 2}?\nInsurance pays 2:1 if the dealer has Blackjack")

    while True:
        want_insurance = input("(Y)es or (N)o:\t")
        if want_insurance.lower() in AFFIRMATIVE_COMMANDS:
            # Take bet
            _wallet.side_bet = players_hand.bet / 2
            return True

        elif want_insurance.lower() in NEGATIVE_COMMANDS:
            if dealers_hand.hand_sum() == 21:
                dealers_hand.overturn_holecard()
                render_multihand(dealers_hand, [players_hand], False)
                print(f"\nDealer has Blackjack\nBet of ${players_hand.bet} lost")
                time.sleep(2)

                players_hand.status_change("bust")
                return False

            else:
                render_multihand(dealers_hand, [players_hand], False)
                print("\nDealer does not have Blackjack")
                time.sleep(2)
                players_hand.status_change("stage 1")
                return False

        else:
            print("Please enter Y/N")


def insurance_taken(dealers_hand, players_hand, _wallet):
    """Preform insurance gameplay"""
    if dealers_hand.hand_sum() == 21:
        dealers_hand.overturn_holecard()

        render_multihand(dealers_hand, [players_hand], 0)
        print(f"Dealer has Blackjack\nInsurance bet pays ${_wallet.side_bet * 2}\nBase bet of ${players_hand.bet} lost.")
        time.sleep(2)
        # take bet
        _wallet.side_bet *= 2
        players_hand.status_change("bust")

    else:
        render_multihand(dealers_hand, [players_hand], 0)
        print(f"Dealer does not have Blackjack\nInsurance bet of ${_wallet.side_bet} lost.")
        time.sleep(2)

        players_hand.status_change("stage 1")
        # take bet
        _wallet.side_bet *= -1


def even_money(dealers_hand, players_hand, _wallet, blackjack_ratio):
    print(f"\nDealer is showing an Ace, would you like to take an even money bet?\n${players_hand.bet / 2} for 2:1 payout")
    yes_no = input("(Y)es or (N)o?:\t").lower()

    if yes_no in AFFIRMATIVE_COMMANDS:
        # Withdraw even money side bet
        _wallet.side_bet += players_hand.bet / 2
        # W.balance -= W.side_bet
        if dealers_hand.hand_sum() == 21:
            dealers_hand.overturn_holecard()

            render_multihand(dealers_hand, [players_hand], 0)
            print(f"Mutual Blackjack\nEven Money bet lost ${_wallet.side_bet}. Blackjack pushes.")
            time.sleep(2)
            # Take bet
            _wallet.side_bet *= -1
            players_hand.status_change("push")
        else:
            dealers_hand.overturn_holecard()

            render_multihand(dealers_hand, [players_hand], 0)
            print(f"Dealer does not have Blackjack\nEven Money bet of ${_wallet.side_bet} won!")
            time.sleep(2)

            players_hand.status_change("blackjack")
            # Take bet
            _wallet.side_bet += players_hand.bet / 2

    elif yes_no in NEGATIVE_COMMANDS:
        if dealers_hand.hand_sum() == 21:
            dealers_hand.overturn_holecard()

            render_multihand(dealers_hand, [players_hand], 0)
            print("Dealer also has Blackjack\nPush")
            time.sleep(2)

            players_hand.status_change("push")
        else:
            print("Dealer does not have Blackjack")
            players_hand.status_change("blackjack")


def dealer_play(dealers_hand, hand_stack, _shoe):
    """Dealer plays their hand"""
    dealers_hand.overturn_holecard()
    render_multihand(dealers_hand, hand_stack, False)
    overturned_card = dealers_hand.card_list[0]
    print(f"Dealer overturns a {overturned_card.card_id}! Dealer's hand total at {dealers_hand.hand_sum()}")
    time.sleep(2)

    while dealers_hand.hand_sum() < 18:
        new_card = _shoe.deal_card()
        dealers_hand.take_card(new_card)
        render_multihand(dealers_hand, hand_stack, False)
        print(f"Dealer draws a {new_card.card_id}! Dealer's hand total at {dealers_hand.hand_sum()}")
        dealers_hand.bust_check()
        time.sleep(2)

    if dealers_hand.hand_status == "live":
        print(f"Dealer stands at {dealers_hand.hand_sum()}")
        time.sleep(2)


def payout(dealers_hand, hand_stack, _wallet, blackjack_ratio):
    """Pay out hand bets and side bets"""
    # Bets are taken from the player's balance upon being placed.
    # This functions payouts with the following rules:
    # A draw is returned x1, a win is returned x2, blackjack is returned at the BJ ratio
    print("__________________________________________________")
    print(f"\n{SNAKE}\t\tComputing Payouts\t\t{SNAKE}")
    print("__________________________________________________")
    time.sleep(2)

    # Payout each hand
    for i, hand in enumerate(hand_stack):
        # Get the hand index
        print("\n\t\t[Hand {} Payout]\t\t".format(i+1))
        hand_idx = "Hand {}".format(i+1)            
            
        # Check for a blackjack
        if hand.hand_status == "blackjack":
            _wallet.balance += hand.bet * blackjack_ratio
            print(f"{hand_idx} has blackjack, you won ${hand.bet * (blackjack_ratio - 1.0)}!!")

        # Check for a push
        elif hand.hand_status == "push" or dealers_hand.hand_sum() == hand.hand_sum():
            _wallet.balance += hand.bet
            print(f"{hand_idx} drew with the dealer and broke even")

        # Check for a bust
        elif hand.hand_status == "bust":
            print(f"{hand_idx} bust, you lost ${hand.bet}.")

        # Assess hand values
        elif hand.hand_status == "stand" and dealers_hand.hand_status == "live":
            # Dealer is closer to 21
            if dealers_hand.hand_sum() > hand.hand_sum():
                print(f"{hand_idx} lost ${hand.bet}.")

            # Player is closer to 21
            elif dealers_hand.hand_sum() < hand.hand_sum():
                _wallet.balance += hand.bet * 2
                print(f"{hand_idx} won ${hand.bet}!")

            # Draw
            elif dealers_hand.hand_sum() == hand.hand_sum():
                _wallet.balance += hand.bet
                print(f"{hand_idx} drew with the dealer, you broke even")

        # Bust
        elif dealers_hand.hand_status == "bust":
            print(f"{hand_idx} won ${hand.bet}!")
            _wallet.balance += hand.bet * 2

    # Payout side bets:
    if _wallet.side_bet:
        _wallet.balance += _wallet.side_bet
        print(f"Side bet pays out ${_wallet.side_bet}")
    print()

