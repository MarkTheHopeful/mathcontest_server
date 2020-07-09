from utils.states import *
import sympy as sp
import operators as ops
from entities.Player import Player


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
    x = sp.symbols("x")

    base_functions = [x + 5, sp.exp(x), sp.sin(x), x ** 2 - 7 * x + 10, sp.asin(x)]

    player_1 = Player(input("Enter the name of the first player:\n"), base_functions.copy(), ops.ALL)
    player_2 = Player(input("Enter the name of the second player:\n"), base_functions.copy(), ops.ALL)

    main_game = Game(player_1, player_2, 0)

    while True:
        player = main_game.current_player()
        opponent = main_game.current_opponent()
        print(f"PLayer {player.name}, it's your turn now!")
        print(f"Your functions are:")
        print(*player.functions, sep=", ")
        print("Your opponent's function are:")
        print(*opponent.functions, sep=", ")
        print(f"Your operators is:")
        print(*player.operators)
        position = int(input("Choose place to the new function! It will also be the first argument\n"))
        args = [position]
        op_ind = int(input("Enter the operator's index!\n"))
        ar_cnt = player.operators[op_ind].ar_cnt
        while len(args) < ar_cnt:
            new_pos = int(input(f"Enter the index of argument number {len(args) + 1}!\n"))
            args.append(new_pos)
        print(f"The operator is: {player.operators[op_ind]}")
        print(f"The arguments are:", *[main_game.get_function(pos) for pos in args], sep=", ")
        apply_state = main_game.apply_operator(op_ind, args)
        if apply_state == APPLY_SUCCESS:
            print(f"The result is: {main_game.get_function(position)}")
            main_game.turn_num += 1
        else:
            print("FATAL ERROR, idk why, please, try again, lol")
