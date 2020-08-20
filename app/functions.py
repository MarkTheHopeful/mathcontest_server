# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, state: STATE, data: {JSON}}, where code is the status code
# State is the description of the code
# And the data is the product, which the function returns


import json
import datetime
from app.extensions import gm, dbm
from utils.encrypt import encrypt_password, check_password
from exceptions.error_messages import CODE
from config import Config
from exceptions.DBExceptions import DBException, DBUserAlreadyExistsException, DBUserNotFoundException, \
    DBTokenNotFoundException
from exceptions.GameExceptions import GameException, GameUserIsAlreadyInException, GameUserHasNoGamesException
from utils import gen_token
from game.constants import BASE_FUNCTIONS, BASE_OPERATORS


class Response:
    code = 500
    data = None

    def __init__(self, code=500, data=json.dumps({})):
        self.code = code
        if data is None:
            data = json.dumps({})
        self.data = json.loads(data)

    def __str__(self):
        return str(json.dumps({"code": self.code,
                               "state": CODE[self.code],
                               "data": self.data}))


def function_response(result_function):
    """
    :param result_function: function to wrap, have to return code (Int) and data (JSON)
    :return: wrapped function, input stays same, exceptions handled, output converted to str(Response)
    Wrapper for all functions in routes
    Gets code and data from the wrapped function and returns a [[app.functions.Response]] object, casted to string
    If an exception occurs, its string goes to the data["Error"] and logs (to stdout)

    Catches DBExceptions with error codes 6xx (699 for unknown db error)
    Catches all other exceptions with error code 500
    """

    def wrapped(*args, **kwargs):
        code = 500
        try:
            code, data = result_function(*args, **kwargs)
        except DBException as e:
            code = e.code
            data = json.dumps({"Error": str(e)})
            print("DBException:", e)
        except Exception as e:
            data = json.dumps({"Error": str(e)})
            print(e)
        return str(Response(code, data))

    return wrapped


def token_auth(token):
    """
    :param token: user token, string
    :return: -1, if no such token exists or if the token is outdated, username otherwise
    """
    try:
        username, exp_time = dbm.get_username_and_exptime_by_token(token)
    except DBTokenNotFoundException:
        return -1
    if exp_time < datetime.datetime.utcnow():
        dbm.delete_token(token)
        return -1
    return username


@function_response
def status():  # TODO: rewrite to see correct status
    code = 200
    data = json.dumps({'State': 'OK'})
    return code, data


@function_response
def start_game(token, username_other):
    """
    :param token: token of the invitor, used to get theirs username
    :param username_other: username of the invited, should be real user's username
    :return: 200, {"Game ID": <game_id>} if everything is ok and game created;
    400, {} if the token is invalid or outdated;
    404, {} if there is no user with "username_other"
    406, {} if one of the users is already in game;
    407, {} if invited user is the invitor itself
    """
    username_from = token_auth(token)
    if username_from == -1:
        code = 400
        data = json.dumps({})
        return code, data

    if not dbm.is_user_exists(username_other):
        code = 404
        data = json.dumps({})
        return code, data

    if username_other == username_from:
        code = 407
        data = json.dumps({})
        return code, data

    try:
        game_id = gm.start_game(username_from, username_other)
    except GameUserIsAlreadyInException:
        code = 406
        data = json.dumps({})
        return code, data

    code = 200
    data = json.dumps({"Game ID": str(game_id)})
    return code, data


@function_response
def get_game_state(token, is_latex):
    """
    :param is_latex: '0' if should return non-latex functions, otherwise returns latex functions
    :param token: user token
    :return: 200, game_data JSONed if everything is ok; 400, {} if the token is invalid, 408, {} if user has no games
    """
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data

    try:
        game_data = gm.get_game_information(username)
    except GameUserHasNoGamesException:
        code = 408
        data = json.dumps({})
        return code, data
    code = 200
    data = game_data.get_json(is_latex != "0")
    return code, data


@function_response
def make_turn(token, op_ind, fun_indexes, is_latex):  # FIXME: some strange errors appear
    op_ind = int(op_ind)
    fun_indexes = list(map(int, fun_indexes))
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data
    try:
        lat_result = gm.make_turn(username, op_ind, fun_indexes, is_latex)
        return 200, json.dumps({"Result Function": lat_result})
    except GameException as e:
        raise e


@function_response
def register(username, password):
    """
    :param username: new username, should be unique and consist only of allowed characters
    TODO: add allowed characters list and verification
    :param password: password, should be strong
    TODO: add password check
    :return: 200, {} if success; 405, {} if username is already in use
    Can throw DBException, but shouldn't
    """
    pass_hash = encrypt_password(password)
    try:
        dbm.insert_user(username, pass_hash)
        dbm.insert_functions_to_username(username, BASE_FUNCTIONS)  # TODO: make templates real
        dbm.insert_operators_to_username(username, BASE_OPERATORS)
    except DBUserAlreadyExistsException:
        code = 405
        data = json.dumps({})
        return code, data
    finally:
        code = 200
        data = json.dumps({})
    return code, data


@function_response
def login(username, password):
    """
    :param username: not empty, should be real username
    :param password: not empty, should be user's password
    :return: 402, {} if there is no user with such credentials; 200, {'Token': <token>} if there is
    Can throw DBException, but shouldn't
    """
    try:
        u_hash = dbm.get_passhash_by_username(username)
    except DBUserNotFoundException:
        code = 402
        data = json.dumps({})
        return code, data

    if not check_password(password, u_hash):
        code = 402
        data = json.dumps({})
        return code, data

    tok_uuid, tok_exp = gen_token()
    dbm.insert_token_to_username(tok_uuid, tok_exp, username)
    code = 200
    data = json.dumps({'Token': tok_uuid})
    return code, data


@function_response
def drop_tables(secret_code):
    if secret_code != Config.ADMIN_SECRET:
        return 403, json.dumps({})
    dbm.clear_all_tables()
    return 299, json.dumps({})
