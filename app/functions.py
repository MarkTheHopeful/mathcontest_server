# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, data: {JSON}}, where code is the status code
# And the data is the product, which the function returns


import json
from app import db
from app.models import User, Token
from app import gm
from utils.encrypt import encrypt_string
import uuid
from config import Config
from time import mktime, gmtime
import datetime


class Response:
    code = 500
    data = None

    def __init__(self, code=500, data=json.dumps({})):
        self.code = code
        self.data = data

    def __str__(self):
        return str(json.dumps({"code": self.code,
                               "data": self.data}))


def function_response(result_function):
    def wrapped(*args, **kwargs):
        code = 500
        data = json.dumps({'Error': 'Unknown error! Something is completely wrong! Ping me!'})
        try:
            code, data = result_function(*args, **kwargs)
        except Exception as e:
            print(e)
        return str(Response(code, data))

    return wrapped


def verify_token(token, user_id):
    poss_tokens = Token.query.filter_by(user_id=user_id).all()
    for poss_tok in poss_tokens:
        if poss_tok.id == token:
            tok_exp = poss_tok.expires_in
            if tok_exp < datetime.datetime.utcnow():
                return 1
            return 0
    return -1


@function_response
def status():
    code = 200
    data = json.dumps({'State': 'OK'})
    return code, data


@function_response
def debug_verify(token, username):
    u = User.query.filter_by(username=username).first()
    res = verify_token(token, u.id)
    if res == 0:
        code = 200
        data = json.dumps({'Result': "OK, token is okay"})
    elif res == 1:
        code = 300
        data = json.dumps({'Error': "The token is outdated"})
    else:
        code = 400
        data = json.dumps({'Error': "No such token"})
    return code, data


@function_response
def start_game(token_1, username_1, username_2):
    u1 = User.query.filter_by(username=username_1).first()
    token_verification_result = verify_token(token_1, u1.id)
    if token_verification_result == -1:
        code = 400
        data = json.dumps({'Error': "No such token"})
    elif token_verification_result == 1:
        code = 300
        data = json.dumps({'Error': "The token is outdated"})
    else:
        game_id = gm.start_game(username_1, username_2)
        code = 200
        data = json.dumps({"Result": "OK, game started", "Game ID": str(game_id)})
    return code, data


@function_response
def login(username, password):
    poss = User.query.filter_by(username=username).first()
    if poss is None:
        code = 400
        data = json.dumps({'Error': 'There are no user with this username!'})
    else:
        u = poss
        p_hash = encrypt_string(password, Config.SECRET_KEY)
        if u.password_hash != p_hash:
            code = 403
            data = json.dumps({'Error': 'There are no user with these username and password!'})
        else:
            tok_uuid = uuid.uuid4().hex
            tok_exp = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=Config.TOKEN_LIFETIME_SEC)  # TODO: make separate function for it
            tok = Token(id=tok_uuid, expires_in=tok_exp, owner=u)
            try:
                db.session.add(tok)
                db.session.commit()
                code = 200
                data = json.dumps({'Result': "Login successfully!", 'Token': tok_uuid})
            except Exception as e:  # FIXME: Too broad!
                print(e)
                code = 502
                data = json.dumps({'Error': 'Something wrong happened during adding token into db!'})
    return code, data


@function_response
def register(username, password):
    poss = User.query.filter_by(username=username).first()
    print(poss, username)
    if poss is not None:
        code = 400
        data = json.dumps({'Error': 'User with this username already exists!'})
    else:
        pass_hash = encrypt_string(password, Config.SECRET_KEY)  # TODO: is this ok?
        new_user = User(username=username, password_hash=pass_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
            code = 200
            data = json.dumps({'Result': 'User created successfully!'})
        except Exception as e:  # FIXME: too broad!
            print(e)
            code = 502
            data = json.dumps(
                {'Error': 'Something wrong happened during adding user into db! Ping me and|or try again!'})
    return code, data
