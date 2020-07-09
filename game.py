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


if __name__ == "__main__":
    x = sp.symbols("x")

    base_functions = [x + 5, sp.exp(x), sp.sin(x), x ** 2 - 7 * x + 10, sp.asin(x)]

    player_1 = Player(input("Enter the name of the first player:\n"), base_functions.copy(), ops.ALL)
    player_2 = Player(input("Enter the name of the second player:\n"), base_functions.copy(), ops.ALL)

    main_game = Game(player_1, player_2, 0)

    while True:
        player = main_game.current_player()
        print(f"PLayer {player.name}, it's your turn now!")
        print(f"Your functions is:")
        print(*player.functions, sep=", ")
        print(f"Your operators is:")
        print(*player.operators)
        position = int(input("Choose place to the new function! It will also be the first argument\n"))
        args = [player.functions[position]]
        arg_in = int(input("Enter the operator's index!\n"))
        oper = player.operators[arg_in]
        while len(args) < oper.ar_cnt:
            new_pos = int(input(f"Enter the index of argument number {len(args) + 1}!\n"))
            args.append(player.functions[new_pos])
        print(f"The operator is: {oper}")
        print(f"The arguments are:", *args, sep=", ")
        result = oper(*args)
        print(f"The result is: {result}")
        player.functions[position] = result
        turn = 1

