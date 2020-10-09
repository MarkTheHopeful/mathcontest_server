from utils.user_state import UserState

USER_PASSIVE = UserState(0)
# TODO: add other states, look to utils.state_dict_constants.py

# Game states:          # FIXME: this is awful as it is. Should be replaced with some dict like thing
ENDED_OK = -3
NOT_EXISTS = -2
NOT_STARTED = -1
STARTED = 1
ENDED = 2

# Function execution results codes:
APPLY_SUCCESS = 0
APPLY_FAILED = -1