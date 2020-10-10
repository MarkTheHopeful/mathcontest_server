from exceptions.utils_exception import UnknownStateException, WrongArgumentStateException


class State:
    code = 0
    payload = None

    def __init__(self, code, payload=None):
        self.code = code
        if payload is not None:
            if type(payload) is not dict:
                raise WrongArgumentStateException(type(payload))
            self.payload = payload

    def get_description(self):
        try:
            return f"State exception with code {self.code} and payload {self.payload}"
        except KeyError:
            raise UnknownStateException(self.code)

    def __eq__(self, other):
        return type(other) is State and self.code == other.code

    def to_value(self):
        return self.code
