from game.constants import BASE_FUNCTIONS, BASE_OPERATORS
from utils import convert_array_to_string


class User:
    def __init__(self, dbu=None, username="", functions=convert_array_to_string(BASE_FUNCTIONS),
                 operators=convert_array_to_string(BASE_OPERATORS),
                 bio="Hi! I am new here!", history="",
                 rank=""):
        if dbu is None:
            self.username = username
            self.functions = functions
            self.operators = operators
            self.bio = bio
            self.history = history
            self.rank = rank
        else:
            self.username = dbu.username
            self.functions = dbu.functions
            self.operators = dbu.operators
            self.bio = dbu.bio
            self.history = dbu.history
            self.rank = dbu.rank

    def to_base_info_dict(self):
        return {"username": self.username,
                "bio": self.bio,
                "history": self.history,
                "rank": self.rank}
