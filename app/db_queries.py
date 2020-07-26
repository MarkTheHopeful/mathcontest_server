from app import db
from app.models import User, Token
from app.DBExceptions import *
from game.constants import BASE_FUNCTIONS, BASE_OPERATORS
from sqlalchemy.exc import IntegrityError
from utils.converters import convert_array_to_string, convert_string_to_array
from sympy import latex
from sympy.parsing.latex import parse_latex


def database_response(database_fun):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = database_fun(*args, **kwargs)
        except DBException as e:
            print("DB KNOWN::")
            print(e)
            raise e
        except Exception as e:
            print("DB UNKNOWN::")
            print(e)
            raise DBException()
        return result

    return wrapped


@database_response
def get_tokens_by_user_id(user_id):
    return Token.query.filter_by(user_id=user_id).all()


@database_response
def get_user_id_by_username(username):
    return get_user_by_username(username).id


@database_response
def get_user_by_username(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        raise DBUserNotFoundException()
    return u


@database_response
def get_passhash_by_username(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        raise DBUserNotFoundException()
    return u.password_hash


@database_response
def insert_token_to_username(id, expires_in, username):
    u = User.query.filter_by(username=username).first()
    tok = Token(id=id, expires_in=expires_in, owner=u)
    db.session.add(tok)
    db.session.commit()


@database_response
def insert_user(username, pass_hash):
    new_user = User(username=username, password_hash=pass_hash,
                    functions=convert_array_to_string(BASE_FUNCTIONS, auto_type_caster=latex),
                    operators=convert_array_to_string(BASE_OPERATORS))
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        raise DBUserAlreadyExistsException()


@database_response
def clear_all_tables():
    db.drop_all()
    db.create_all()


@database_response
def get_functions_by_username(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        raise DBUserNotFoundException
    return convert_string_to_array(u.functions, auto_type_caster=parse_latex)


@database_response
def get_operators_by_username(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        raise DBUserNotFoundException
    return convert_string_to_array(u.operators, auto_type_caster=int)
