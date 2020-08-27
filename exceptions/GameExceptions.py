class GameException(Exception):
    pass


class GameUserIsAlreadyInException(GameException):
    pass


class GameNoSuchPlayerException(GameException):
    pass


class GameIsNotStartedException(GameException):
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


class GameNotEnoughtPlayersException(GameException):
    pass
