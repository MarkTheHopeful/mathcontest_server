from utils.state_dict_constants import user_state_descriptions
from exceptions.utils_exception import UnknownStateException
from utils.state import State


class UserState(State):
    code = 0
    payload = None

    def get_description(self):
        try:
            return user_state_descriptions[self.code]
        except KeyError:
            raise UnknownStateException(self.code)

    def __eq__(self, other):
        return type(other) is UserState and self.code == other.code
