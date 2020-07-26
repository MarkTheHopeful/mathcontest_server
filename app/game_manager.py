from game.game import Game
from entities.Player import Player
from game.operators import ALL
from utils.states import *
from app.db_queries import get_functions_by_username, get_operators_by_username


class GameManager:
    current_games = []
    ALARMING_AMOUNT_OF_GAMES = 1000

    def start_game(self, player_1, player_2):
        player_1r = self.make_player(player_1)
        player_2r = self.make_player(player_2)
        game = Game(player_1r, player_2r, len(self.current_games))
        self.current_games.append(game)
        game.state = STARTED
        return len(self.current_games)

    def make_player(self, player_username):
        play = Player(player_username, self.make_functions(player_username), self.make_operators(player_username))
        return play

    def make_functions(self, player_username):
        functions = get_functions_by_username(player_username)
        return functions

    def make_operators(self, player_username):
        index = get_operators_by_username(player_username)
        return [ALL[x] for x in index]
