from utils.state_dict_constants import user_state_descriptions
from exceptions.utils_exception import UnknownUserStateException, WrongArgumentUserStateException


class UserState:
    code = 0
    payload = None

    def __init__(self, code, payload=None):
        self.code = code
        if payload is not None:
            if type(payload) is not dict:
                raise WrongArgumentUserStateException(type(payload))
            self.payload = payload

    def get_description(self):
        try:
            return user_state_descriptions[self.code]
        except KeyError:
            raise UnknownUserStateException(self.code)

    def __eq__(self, other):
        return type(other) is UserState and self.code == other.code
