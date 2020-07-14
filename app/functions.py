# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, data: {JSON}}, where code is the status code
# And the data is the product, which the function returns


import json
from app import db
from app.models import User, Token
from utils.encrypt import encrypt_string
import uuid
from config import Config
from time import mktime, gmtime
import datetime


def status():
    code = 200
    data = json.dumps({'State': 'OK'})
    return str(Response(code, data))


def login(username, password):
    code = 500
    data = json.dumps({'Error': 'Unknown error! Something is completely wrong! Ping me!'})

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
            tok_exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.TOKEN_LIFETIME_SEC)  # TODO: make separate function for it
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
    return str(Response(code, data))


def register(username, password):
    code = 500
    data = json.dumps({'Error': 'Unknown error! Something is completely wrong! Ping me!'})

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
    return str(Response(code, data))


class Response:
    code = 500
    data = None

    def __init__(self, code=500, data=json.dumps({})):
        self.code = code
        self.data = data

    def __str__(self):
        return str(json.dumps({"code": self.code,
                               "data": self.data}))
