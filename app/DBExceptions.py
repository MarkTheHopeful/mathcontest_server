from utils.error_messages import CODE


class DBException(Exception):
    code = 699

    def __init__(self, code=699, message=CODE[699]):
        self.code = code
        super(DBException, self).__init__(message)


class DBUserNotFoundException(DBException):
    def __init__(self, message=""):
        super(DBUserNotFoundException, self).__init__(601, message)


class DBUserAlreadyExistsException(DBException):
    def __init__(self, message=""):
        super(DBUserAlreadyExistsException, self).__init__(602, message)