class GameException(Exception):
    pass


class GameUserIsAlreadyInException(GameException):
    pass


class GameNoSuchPlayerException(GameException):
    pass


class GameIsNotStartedException(GameException):
    pass


class GameWaitForAcceptException(GameException):
    pass


class GameIsAlreadyAcceptedException(GameException):
    pass


class GameIsAlreadyStartedException(GameException):
    pass


class GameNotYourTurnException(GameException):
    pass


class GameUserHasNoGamesException(GameException):
    pass


class GameUserIsAlreadyInQueueException(GameException):
    pass


class GameNotInQueueException(GameException):
    pass


class GameNotEnoughPlayersException(GameException):
    pass
