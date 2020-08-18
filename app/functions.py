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
from exceptions.GameExceptions import GameException
from utils import gen_token
from game.constants import BASE_FUNCTIONS, BASE_OPERATORS


class Response:
    code = 500
    data = None

    def __init__(self, code=500, data=json.dumps({})):
        self.code = code
        if data is None:
            data = json.dumps({})
        self.data = data

    def __str__(self):
        return str(json.dumps({"code": self.code,
                               "state": CODE[self.code],
                               "data": self.data}))


def function_response(result_function):
    def wrapped(*args, **kwargs):
        code = 500
        try:
            code, data = result_function(*args, **kwargs)
        except DBException as e:
            code = e.code
            data = json.dumps({"Error": str(e)})
            print(e)
        except Exception as e:
            data = json.dumps({"Error": str(e)})
            print(e)
        return str(Response(code, data))

    return wrapped


def token_auth(token):
    try:
        username, exp_time = dbm.get_username_and_exptime_by_token(token)
    except DBTokenNotFoundException:
        return -1
    if exp_time < datetime.datetime.utcnow():
        dbm.delete_token(token)
        return -1
    return username


@function_response
def status():
    code = 200
    data = json.dumps({'State': 'OK'})
    return code, data


@function_response
def debug_verify(token, username):
    p_username = token_auth(token)
    if p_username == username:
        code = 200
    else:
        code = 401

    return code, json.dumps({})


@function_response
def start_game(token, username_other):      # TODO: check if the second name is real
    username_from = token_auth(token)
    if username_from == -1:
        code = 400
        data = json.dumps({})
        return code, data

    game_id = gm.start_game(username_from, username_other)
    code = 200
    data = json.dumps({"Game ID": str(game_id)})
    return code, data


@function_response
def get_game_state(token):
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data

    game_data = gm.get_game_information(username)
    code = 200
    data = game_data.get_json()
    return code, data


@function_response
def make_turn(token, op_ind, fun_indexes):
    username = token_auth(token)
    if username == -1:
        code = 400
        data = json.dumps({})
        return code, data
    try:
        gm.make_turn(username, op_ind, fun_indexes)
    except GameException:
        raise Exception("NOT DONE YET")         # TODO: do.


@function_response
def register(username, password):
    pass_hash = encrypt_password(password)
    try:
        dbm.insert_user(username, pass_hash)
        dbm.insert_functions_to_username(username, BASE_FUNCTIONS)      # TODO: make templates real
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
