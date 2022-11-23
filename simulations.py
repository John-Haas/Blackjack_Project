from main_blackjack import run_loop
from models.SimShoe import SimShoe
from models.Wallet import Wallet
from models.GameSettings import GameSettings

def run_sim(simulation):
    # Get the game settings
    game_settings = GameSettings()

    # Foundation objects
    print(f"Running {simulation}")
    shoe = SimShoe(simulation)
    wallet = Wallet(game_settings.starting_cash)

    while True:
        # Run the main loop
        run_loop(shoe, wallet, game_settings)

def single_split_lose():
    simulation = "single_split_lose"
    run_sim(simulation)

def multi_split_lose():
    simulation = "multi_split_lose"
    run_sim(simulation)

def even_money_lose():
    simulation = "even_money_lose"
    run_sim(simulation)

def even_money_win():
    simulation = "even_money_win"
    run_sim(simulation)

multi_split_lose()