from utils.user_state import UserState
from utils.game_state import GameInnerState

USER_PASSIVE = UserState(0)
USER_QUEUED = UserState(1)
USER_ACCEPTING = UserState(2)
USER_PLAYING = UserState(3)
USER_ENDED = UserState(4)

GAME_NOT_CREATED = GameInnerState(0)
GAME_ACCEPTING = GameInnerState(1)
GAME_STARTED = GameInnerState(2)
GAME_ENDED = GameInnerState(6)
GAME_TO_DELETE = GameInnerState(7)
