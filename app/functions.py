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
from exceptions.GameExceptions import *
from utils import gen_token, full_stack
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
            data = json.dumps({"Error": str(e), "Stack": full_stack()})
            print("DBException:", e)
        except GameException as e:
            code = 410
            data = json.dumps({"Error": str(e), "Stack": full_stack()})
            print("GameException:", e)
        except Exception as e:
            data = json.dumps({"Error": str(e), "Stack": full_stack()})
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
def status():  # TODO: rewrite to add meaningful information
    """
    Get the server's state
    :return: 200, 'State' : 'Ok/Failed', 'API version', 'DB manager' : 'Ok/FAILED', 'Game manager': 'Ok/FAILED',
     'Amount of games', 'Length of queue';
    """
    code = 200
    result = {'State': 'Active', 'API version': 'v1', 'DB manager': 'Ok' if dbm.is_ok() else "FAILED"}
    gm_state, games_amount, queue_len = gm.is_ok()
    result["Game manager"] = "Ok" if gm_state else "FAILED"
    result["Amount of games"] = games_amount
    result["Queue length"] = queue_len
    data = json.dumps(result)
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
def put_user_in_queue(token):
    """
    Add the user with the token to the waiting queue
    :param token: the user's token, string
    :return: 200, {} if success;
    400, {} if the token is invalid or outdated;
    406, {} if the user is already in game;
    411, {} if the user is already in queue;
    """
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data

    try:
        gm.put_user_to_queue(username)
    except GameUserIsAlreadyInException:
        return 406, json.dumps({})
    except GameUserIsAlreadyInQueueException:
        return 411, json.dumps({})
    return 200, json.dumps({})


@function_response
def get_queue_len():
    """
    Get the waiting queue length
    :return: 200, {"Length": <int>}
    """
    return 200, json.dumps({"Length": gm.get_queue_len()})


@function_response
def check_and_create(token):
    """
    Check if a game can be created with somebody in queue, and if possible, create it (The game.state is NOT_STARTED)
    :param token: the user's token
    :return: 200, {"Player": player.username, "Opponent": opponent.username} if game successfully created;
    400, {} if the token is invalid or outdated
    412, {} if the user is not in waiting queue
    413, {} if there is not enough players to create a game
    """
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data

    try:
        game_info = gm.check_and_create_game(username)
    except GameNotInQueueException:
        return 412, json.dumps({})
    except GameNotEnoughtPlayersException:
        return 413, json.dumps({})

    code = 200
    data = json.dumps({"Player": game_info.player, "Opponent": game_info.opponent})
    return code, data


@function_response
def confirm_game_start(token):
    """
    Confirm that you are ready to the game
    :param token: user's token
    :return: 200, {} if confirmed successfully
    201, {} if the user have already confirmed
    400, {} if the token is invalid or outdated
    408, {} if the user is not in any game to confirm
    414, {} if the game is already started and doesn't require a confirmation
    """
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data

    try:
        res = gm.confirm_game_start(username)
    except GameUserHasNoGamesException:
        return 408, json.dumps({})
    except GameIsAlreadyStartedException:
        return 414, json.dumps({})

    if res:
        return 200, json.dumps({})
    else:
        return 201, json.dumps({})


@function_response
def get_game_state(token, is_latex):
    """
    :param is_latex: '0' if should return non-latex functions, otherwise returns latex functions
    :param token: user token
    :return: 200, game_data JSONed if everything is ok;
    400, {} if the token is invalid;
    408, {} if user has no games
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
def make_turn(token, op_ind, fun_indexes, is_latex):
    """
    Make one turn in the user's game
    :param token: user's token
    :param op_ind: index of the operator the user has chosen
    :param fun_indexes: list of indexes the user has chosen
    :param is_latex: boolean (0/1) whether the result should be in latex
    :return: 200, {"Result Function": <fun>} if everything is ok and the turn is done
    400, {} if the token if invalid or outdated
    409, {} if it is not user's turn
    """
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
    except GameNotYourTurnException:
        return 409, json.dumps({})
    except GameIsNotStartedException:
        return 415, json.dumps({})
    except GameException as e:
        print(e)
        raise e


@function_response
def drop_tables(secret_code):
    """
    :param secret_code: admin secret from config
    :return: 403, {} if the secret code is incorrect
    299, {} if everything is dropped and recreated successfully
    """
    if secret_code != Config.ADMIN_SECRET:
        return 403, json.dumps({})
    dbm.clear_all_tables()
    return 299, json.dumps({})
