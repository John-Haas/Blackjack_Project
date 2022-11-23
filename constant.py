# Unicode characters
SPADE = u"\u2660"
DIAMOND = u"\u2666"
CLUB = U"\u2663"
HEART = u"\u2665"
SNAKE = u"\U0001F40D"
FLIPPED_CARD = u"\u25AF"

# For Card construction
NUM_LET_LIST = ['2', '3', '4', '5', '6', '7', '8', '9', '10', "J", "Q", "K", "A"]
SUIT_LIST = [SPADE, DIAMOND, CLUB, HEART]

# Basic commands
AFFIRMATIVE_COMMANDS = ["yes", "y"]
NEGATIVE_COMMANDS = ["no", "n"]
HIT_COMMANDS = ["hit", "h"]
STAND_COMMANDS = ["stand", "s"]
DUB_DOWN_COMMANDS = ["double down", "d", "double", "dd"]
SPLIT_COMMANDS = ["split", "sp"]
END_GAME_COMMANDS = ["exit", "leave table", "good bye"]
CHANGE_SETTINGS_COMMANDS = ["options", "settings", "setting"]

# Stages
# Stage 1: Player hand initial move of Hit, Stand, Split, or Double Down
STAGE_1 = ["stage 1"]
# Stage 2: Player hand move of Hit or Stand
STAGE_2 = ["stage 2"]
# Stage 3: Dealer hand plays
STAGE_3 = ["stand", "stage 3"]
# Stage 4: Directions for payout
STAGE_4 = ["bust", "push", "win", "blackjack"]