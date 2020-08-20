import json

from sympy import latex

from sympy.parsing.sympy_parser import parse_expr
from utils.states import NOT_EXISTS
from game.operators import make_smart_rep


class GameState:
    state = NOT_EXISTS

    def __init__(self, state, turn_num=-1, player="", opponent="", players_functions=None, opponents_functions=None,
                 players_operators=None, opponents_operators=None, players_operators_args=None,
                 opponents_operators_args=None):
        if opponents_operators is None:
            opponents_operators = []
        if players_operators is None:
            players_operators = []
        if opponents_functions is None:
            opponents_functions = []
        if players_functions is None:
            players_functions = []

        self.state = state
        self.turn_num = turn_num
        self.player = player
        self.opponent = opponent
        self.players_functions = players_functions
        self.opponents_functions = opponents_functions
        self.players_operators = players_operators
        if players_operators_args is not None:
            self.players_operators_args = players_operators_args
        else:
            self.players_operators_args = [op.ar_cnt for op in players_operators]
        self.opponents_operators = opponents_operators

        if opponents_operators_args is not None:
            self.opponents_operators_args = opponents_operators_args
        else:
            self.opponents_operators_args = [op.ar_cnt for op in opponents_operators]

    def get_json(self, latex_on=False):
        conv_fun = str
        oper_conv = make_smart_rep(latex_on)
        if latex_on:
            conv_fun = latex
        return json.dumps({"GameState": self.state,
                           "Turn Number": self.turn_num,
                           "Player Name": self.player,
                           "Opponent Name": self.opponent,
                           "Players Functions": list(map(conv_fun, self.players_functions)),
                           "Opponents Functions": list(map(conv_fun, self.opponents_functions)),
                           "Players Operators": list(map(oper_conv, self.players_operators)),
                           "Opponents Operators": list(map(oper_conv, self.opponents_operators)),
                           "Players Operators Arguments": list(map(str, self.players_operators_args)),
                           "Opponents Operators Arguments": list(map(str, self.opponents_operators_args))})


def deserialize_game_state(json_dict):  # NON LATEX STRICT
    game_state = json_dict['GameState']
    turn_number = json_dict['Turn Number']
    player_name = json_dict['Player Name']
    opponent_name = json_dict["Opponent Name"]
    players_functions = list(map(parse_expr, json_dict['Players Functions']))
    opponents_functions = list(map(parse_expr, json_dict['Opponents Functions']))
    players_operators = json_dict['Players Operators']
    opponents_operators = json_dict['Opponents Operators']
    players_operators_args = list(map(int, json_dict['Players Operators Arguments']))
    opponents_operators_args = list(map(int, json_dict['Opponents Operators Arguments']))
    return GameState(game_state, turn_number, player_name, opponent_name, players_functions, opponents_functions,
                     players_operators, opponents_operators, players_operators_args, opponents_operators_args)
