class GameException(Exception):
    pass


class GameUserIsAlreadyInException(GameException):
    pass


class GameNoSuchPlayerException(GameException):
    pass
