import sympy as sp
from entities.player import Player
from game.game import Game
import game.operators as ops
from utils.states import *

x = sp.symbols("x")

base_functions = [x + 5, sp.exp(x), sp.sin(x), x ** 2 - 7 * x + 10, sp.asin(x)]


if __name__ == "__main__":
    player_1 = Player(input("Enter the name of the first player:\n"), base_functions.copy(), ops.ALL)
    player_2 = Player(input("Enter the name of the second player:\n"), base_functions.copy(), ops.ALL)

    main_game = Game(player_1, player_2, 0)

    while main_game.state == STARTED:
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
