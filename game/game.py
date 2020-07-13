from utils.states import *


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


if __name__ == "__main__":
    pass
