class GameException(Exception):
    pass


class GameUserIsAlreadyInException(GameException):
    pass


class GameNoSuchPlayerException(GameException):
    pass


class GameIsNotStartedException(GameException):
    pass


class GameNotYourTurnException(GameException):
    pass