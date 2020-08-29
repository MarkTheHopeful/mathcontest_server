from sympy import latex

from game.game import Game
from entities.player import Player
from game.game_state import GameState
from game.operators import ALL
from utils.states import *
from app.db_manager import DBManager
from exceptions.GameExceptions import GameUserIsAlreadyInException, GameNoSuchPlayerException, \
    GameIsNotStartedException, GameNotYourTurnException, GameUserHasNoGamesException, \
    GameUserIsAlreadyInQueueException, GameNotInQueueException, GameNotEnoughtPlayersException, \
    GameIsAlreadyStartedException, GameException


class GameManager:
    current_games = []
    ALARMING_AMOUNT_OF_GAMES = 1000
    users_to_games = dict()
    waiting_queue = list()
    dbm = None

    def is_ok(self):
        return self.dbm is not None and len(self.users_to_games) < self.ALARMING_AMOUNT_OF_GAMES, len(
            self.current_games), len(self.waiting_queue)

    def init_dbm(self, db_manager: DBManager):
        self.dbm = db_manager

    def put_user_to_queue(self, username):
        if username in self.users_to_games:
            if self.users_to_games[username] == NOT_STARTED:
                raise GameUserIsAlreadyInQueueException()
            elif self.users_to_games[username] == ENDED_OK:
                self.users_to_games[username] = NOT_STARTED
            else:
                raise GameUserIsAlreadyInException

        self.waiting_queue.append(username)
        self.users_to_games[username] = NOT_STARTED

    def get_queue_len(self):
        return len(self.waiting_queue)

    def check_and_create_game(self, player_1):
        if player_1 not in self.waiting_queue:
            raise GameNotInQueueException()

        if len(self.waiting_queue) < 2:
            raise GameNotEnoughtPlayersException()

        opponent = self.waiting_queue.pop(0)
        if opponent == player_1:
            opponent = self.waiting_queue.pop(0)
        else:
            self.waiting_queue.pop(self.waiting_queue.index(player_1))

        player_1r = self.make_player(player_1)
        player_2r = self.make_player(opponent)
        game = Game(player_1r, player_2r, len(self.current_games))
        self.current_games.append(game)
        self.users_to_games[player_1] = game.game_id
        self.users_to_games[opponent] = game.game_id
        return self.get_game_information(player_1)

    def confirm_game_start(self, username):
        try:
            ind = self.users_to_games[username]
            if ind == NOT_STARTED:
                raise KeyError()
            game = self.current_games[ind]
        except KeyError or IndexError:
            raise GameUserHasNoGamesException()
        if game.state != NOT_STARTED:
            raise GameIsAlreadyStartedException()

        _ = game.confirmed_by
        print(game.confirmed_by)
        game.confirm_start(username)
        return _ != game.confirmed_by

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
            ind = self.users_to_games[player_username]
            if ind == NOT_STARTED:
                raise KeyError()
            game = self.current_games[ind]
        except KeyError:
            raise GameUserHasNoGamesException()

        opponent_name = game.get_opponent(player_username)
        return GameState(game.state, game.turn_num, player_username, opponent_name,
                         game.get_functions_by_username(player_username), game.get_functions_by_username(opponent_name),
                         game.get_operators_by_username(player_username), game.get_operators_by_username(opponent_name))

    def make_turn(self, player_username, operator_index, functions, is_latex):
        try:
            ind = self.users_to_games[player_username]
            if ind == NOT_STARTED:
                raise KeyError()
            game = self.current_games[ind]
        except KeyError:
            raise GameNoSuchPlayerException()

        if game.state != STARTED:
            raise GameIsNotStartedException()

        if game.current_player().name != player_username:
            raise GameNotYourTurnException()

        result = game.apply_operator(operator_index, functions)[1]
        if result is None:
            raise GameException()
        if is_latex == "0":
            return str(result)
        return latex(result)
