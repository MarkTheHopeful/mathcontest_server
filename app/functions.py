# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, state: STATE, data: {JSON}}, where code is the status code
# State is the description of the code
# And the data is the product, which the function returns


import json
import datetime
from app import gm
from utils.encrypt import encrypt_password, check_password
from utils.error_messages import CODE
from config import Config
from app.db_queries import get_tokens_by_user_id, get_user_id_by_username, get_passhash_by_username, \
    insert_token_to_username, insert_user, clear_all_tables
from app.DBExceptions import DBException, DBUserAlreadyExistsException, DBUserNotFoundException
from utils.server_specials import gen_token


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
        data = json.dumps({})
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


def verify_token(token, user_id):
    poss_tokens = get_tokens_by_user_id(user_id)
    for poss_tok in poss_tokens:
        if poss_tok.id == token:
            tok_exp = poss_tok.expires_in
            if tok_exp > datetime.datetime.utcnow():
                return 0
    return -1


def verify_token_by_username(token, username):
    uid = get_user_id_by_username(username)
    return verify_token(token, uid)


@function_response
def status():
    code = 200
    data = json.dumps({'State': 'OK'})
    return code, data


@function_response
def debug_verify(token, username):
    try:
        res = verify_token_by_username(token, username)
        if res == 0:
            code = 200
        else:
            code = 401
    except DBUserNotFoundException:
        code = 404
    return code, json.dumps({})


@function_response
def start_game(token_1, username_1, username_2):
    try:
        token_verification_result = verify_token_by_username(token_1, username_1)
        if token_verification_result == -1:
            code = 400
            data = json.dumps({})
            return code, data
    except DBUserNotFoundException:
        code = 404
        data = json.dumps({})
        return code, data

    game_id = gm.start_game(username_1, username_2)
    code = 200
    data = json.dumps({"Game ID": str(game_id)})
    return code, data


@function_response
def login(username, password):
    try:
        u_hash = get_passhash_by_username(username)
    except DBUserNotFoundException:
        code = 402
        data = json.dumps({})
        return code, data

    if not check_password(password, u_hash):
        code = 402
        data = json.dumps({})
        return code, data

    tok_uuid, tok_exp = gen_token()
    insert_token_to_username(tok_uuid, tok_exp, username)
    code = 200
    data = json.dumps({'Token': tok_uuid})
    return code, data


@function_response
def register(username, password):
    pass_hash = encrypt_password(password)
    try:
        insert_user(username, pass_hash)
    except DBUserAlreadyExistsException:
        code = 405
        data = json.dumps({})
        return code, data
    finally:
        code = 200
        data = json.dumps({})
    return code, data


@function_response
def drop_tables(secret_code):
    if secret_code != Config.ADMIN_SECRET:
        return 403, json.dumps({})
    clear_all_tables()
    return 299, json.dumps({})
