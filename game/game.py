from utils.states import *
from exceptions.GameExceptions import GameNoSuchPlayerException


class Game:
    players = []
    turn_num = 0
    state = NOT_STARTED
    game_id = -1

    def __init__(self, player_1, player_2, id):
        self.players = [player_1, player_2]
        self.game_id = id
        self.state = STARTED

    def current_player(self):
        return self.players[self.turn_num % len(self.players)]

    def current_opponent(self):
        return self.players[(self.turn_num + 1) % len(self.players)]

    def get_function(self, position):
        player = self.current_player()
        if position >= len(player.functions):
            player = self.current_opponent()
            position -= len(player.functions)
        return player.functions[position]

    def apply_operator(self, op_ind, fun_inds):
        try:
            player = self.current_player()
            oper = player.operators[op_ind]
            position = fun_inds[0]
            arguments = [self.get_function(ind) for ind in fun_inds]
            res_function = oper(*arguments)
            if position >= len(player.functions):
                position -= len(player.functions)
                player = self.current_opponent()
            player.functions[position] = res_function
            return APPLY_SUCCESS
        except Exception:  # TODO: This is very dumb
            return APPLY_FAILED

    def get_functions_by_username(self, username):
        if self.players[0].name == username:
            return self.players[0].functions
        elif self.players[1].name == username:
            return self.players[1].functions
        else:
            raise GameNoSuchPlayerException()

    def get_operators_by_username(self, username):
        if self.players[0].name == username:
            return self.players[0].operators
        elif self.players[1].name == username:
            return self.players[1].operators
        else:
            raise GameNoSuchPlayerException()

    def get_opponent(self, username):
        if self.players[0].name == username:
            return self.players[1].name
        elif self.players[1].name == username:
            return self.players[0].name
        else:
            raise GameNoSuchPlayerException()


if __name__ == "__main__":
    pass
