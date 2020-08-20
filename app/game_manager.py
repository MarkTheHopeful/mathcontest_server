from sympy import latex

from game.game import Game
from entities.Player import Player
from game.game_state import GameState
from game.operators import ALL
from utils.states import *
from app.db_manager import DBManager
from exceptions.GameExceptions import GameUserIsAlreadyInException, GameNoSuchPlayerException, \
    GameIsNotStartedException, GameNotYourTurnException, GameUserHasNoGamesException


class GameManager:
    current_games = []
    ALARMING_AMOUNT_OF_GAMES = 1000
    users_to_games = dict()
    dbm = None

    def init_dbm(self, db_manager: DBManager):
        self.dbm = db_manager

    def start_game(self, player_1, player_2):
        player_1r = self.make_player(player_1)
        player_2r = self.make_player(player_2)
        game = Game(player_1r, player_2r, len(self.current_games))

        if player_1 in self.users_to_games or player_2 in self.users_to_games:
            raise GameUserIsAlreadyInException()

        self.users_to_games[player_1] = game.game_id
        self.users_to_games[player_2] = game.game_id
        self.current_games.append(game)
        game.state = STARTED
        return game.game_id

    def make_player(self, player_username):
        play = Player(player_username, self.make_functions(player_username), self.make_operators(player_username))
        return play

    def make_functions(self, player_username):
        functions = self.dbm.get_functions_by_username(player_username)
        return functions

    def make_operators(self, player_username):
        index = self.dbm.get_operators_by_username(player_username)
        return [ALL[x] for x in index]

    def get_game_information(self, player_username):
        try:
            game = self.current_games[self.users_to_games[player_username]]
        except KeyError:
            raise GameUserHasNoGamesException()

        opponent_name = game.get_opponent(player_username)
        return GameState(game.state, game.turn_num, player_username, opponent_name,
                         game.get_functions_by_username(player_username), game.get_functions_by_username(opponent_name),
                         game.get_operators_by_username(player_username), game.get_operators_by_username(opponent_name))

    def make_turn(self, player_username, operator_index, functions, is_latex):
        try:
            game = self.current_games[self.users_to_games[player_username]]
        except KeyError:
            raise GameNoSuchPlayerException()

        if game.state != STARTED:
            raise GameIsNotStartedException()

        if game.current_player().name != player_username:
            raise GameNotYourTurnException()

        position = functions[0]
        game.apply_operator(operator_index, functions)
        result = game.get_function(position)
        if is_latex == "0":
            return str(result)
        return latex(result)
