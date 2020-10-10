class UnknownStateException(Exception):
    def __init__(self, state_code):
        super(UnknownStateException, self).__init__(
            f"Attempted to get description of an unknown code: {state_code}")


class WrongArgumentStateException(Exception):
    def __init__(self, tried_type):
        super(WrongArgumentStateException, self).__init__(
            f"UserState payload should be a dict, got {tried_type} instead")
