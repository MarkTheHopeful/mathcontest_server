# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, state: STATE, data: {JSON}}, where code is the status code
# State is the description of the code
# And the data is the product, which the function returns


import json
from app import db
from app.models import User, Token
from app import gm
from utils.encrypt import encrypt_password, check_password
from utils.error_messages import CODE
import uuid
from config import Config
import datetime


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
    elif res == 1:
        code = 400
    else:
        code = 401
    return code, json.dumps({})


@function_response
def start_game(token_1, username_1, username_2):
    u1 = User.query.filter_by(username=username_1).first()
    token_verification_result = verify_token(token_1, u1.id)
    if token_verification_result == -1:
        code = 400
        data = json.dumps({})
    elif token_verification_result == 1:
        code = 401
        data = json.dumps({})
    else:
        game_id = gm.start_game(username_1, username_2)
        code = 200
        data = json.dumps({"Game ID": str(game_id)})
    return code, data


@function_response
def login(username, password):
    poss = User.query.filter_by(username=username).first()
    if poss is None:
        code = 402
        data = json.dumps({})
    else:
        u = poss
        u_hash = u.password_hash
        if not check_password(password, u_hash):
            code = 402
            data = json.dumps({})
        else:
            tok_uuid = uuid.uuid4().hex
            tok_exp = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=Config.TOKEN_LIFETIME_SEC)  # TODO: make separate function for it
            tok = Token(id=tok_uuid, expires_in=tok_exp, owner=u)
            try:
                db.session.add(tok)
                db.session.commit()
                code = 200
                data = json.dumps({'Token': tok_uuid})
            except Exception as e:  # FIXME: Too broad!
                print(e)
                code = 502
                data = json.dumps({})
    return code, data


@function_response
def register(username, password):
    poss = User.query.filter_by(username=username).first()
    print(poss, username)
    if poss is not None:
        code = 405
        data = json.dumps({})
    else:
        pass_hash = encrypt_password(password)
        new_user = User(username=username, password_hash=pass_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
            code = 200
            data = json.dumps({})
        except Exception as e:  # FIXME: too broad!
            print(e)
            code = 502
            data = json.dumps({})
    return code, data


@function_response
def drop_tables(secret_code):
    if secret_code != Config.ADMIN_SECRET:
        return 403, json.dumps({})
    try:
        db.drop_all()
        db.create_all()
    except Exception as e:
        print(e)
        code = 599
        data = json.dumps({})
        return code, data
    return 299, json.dumps({})
