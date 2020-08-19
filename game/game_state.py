import json

from sympy import latex

from sympy.parsing.latex import parse_latex
from utils.states import NOT_EXISTS


class GameState:
    state = NOT_EXISTS

    def __init__(self, state, turn_num=-1, player="", opponent="", players_functions=None, opponents_functions=None,
                 players_operators=None, opponents_operators=None):
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
        self.opponents_operators = opponents_operators
        # self.players_functions = list(map(latex, players_functions))
        # self.opponents_function = list(map(latex, opponents_functions))
        # self.players_operators = list(map(str, players_operators))
        # self.opponents_operators = list(map(str, opponents_operators))

    def get_json(self):
        return json.dumps({"GameState": self.state,
                           "Turn Number": self.turn_num,
                           "Player Name": self.player,
                           "Opponent Name": self.opponent,
                           "Players Functions": list(map(latex, self.players_functions)),
                           "Opponents Functions": list(map(latex, self.opponents_functions)),
                           "Players Operators": list(map(str, self.players_operators)),
                           "Opponents Operators": list(map(str, self.opponents_operators))})


def deserialize_game_state(json_dict):
    game_state = json_dict['GameState']
    turn_number = json_dict['Turn Number']
    player_name = json_dict['Player Name']
    opponent_name = json_dict["Opponent Name"]
    players_functions = list(map(parse_latex, json_dict['Players Functions']))
    opponents_functions = list(map(parse_latex, json_dict['Opponents Functions']))
    players_operators = json_dict['Players Operators']
    opponents_operators = json_dict['Opponents Operators']
    return GameState(game_state, turn_number, player_name, opponent_name, players_functions, opponents_functions,
                     players_operators, opponents_operators)
