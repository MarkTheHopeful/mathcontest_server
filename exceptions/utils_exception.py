class UnknownUserStateException(Exception):
    def __init__(self, state_code):
        super(UnknownUserStateException, self).__init__(
            f"Attempted to get description of an unknown code: {state_code}")


class WrongArgumentUserStateException(Exception):
    def __init__(self, tried_type):
        super(WrongArgumentUserStateException, self).__init__(
            f"UserState payload should be a dict, got {tried_type} instead")
