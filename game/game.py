from utils import full_stack
from utils.states import *
from exceptions.GameExceptions import GameNoSuchPlayerException


class Game:
    players = []
    turn_num = 0
    state = GAME_NOT_CREATED
    game_id = -1
    confirmed_by = 0

    def __init__(self, player_1, player_2, id):
        self.players = [player_1, player_2]
        self.game_id = id
        self.state = GAME_ACCEPTING

    def confirm_start(self, username):
        if username == self.current_player().name:
            self.confirmed_by |= 1
        if username == self.current_opponent().name:
            self.confirmed_by |= 2
        if self.confirmed_by == 3:
            self.state = GAME_STARTED

    def current_player(self):
        return self.players[self.turn_num % len(self.players)]

    def current_opponent(self):
        return self.players[(self.turn_num + 1) % len(self.players)]

    def get_function(self, position):
        player = self.current_player()
        if position >= len(player.functions):
            position -= len(player.functions)
            player = self.current_opponent()
        return player.functions[position]

    def apply_operator(self, op_ind, fun_inds):
        try:
            player = self.current_player()
            print(player.name)
            oper = player.operators[op_ind]
            position = fun_inds[0]
            arguments = [self.get_function(ind) for ind in fun_inds]
            res_function = oper(*arguments)
            if position >= len(player.functions):
                position -= len(player.functions)
                player = self.current_opponent()
            player.functions[position] = res_function
            self.turn_num += 1
            return res_function
        except Exception:  # TODO: This is very dumb
            print(full_stack())
            raise Exception("Function application failed")  # FIXME: And this is dumber

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
