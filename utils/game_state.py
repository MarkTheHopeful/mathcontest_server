from utils.state_dict_constants import game_state_descriptions
from utils.state import State
from exceptions.utils_exception import UnknownStateException


class GameInnerState(State):
    code = 0
    payload = None

    def get_description(self):
        try:
            return game_state_descriptions[self.code]
        except KeyError:
            raise UnknownStateException(self.code)

    def __eq__(self, other):
        return type(other) is GameInnerState and self.code == other.code
