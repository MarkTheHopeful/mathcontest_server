from exceptions.DBExceptions import *
from utils import convert_array_to_string, convert_string_to_array
from sympy.parsing.sympy_parser import parse_expr
import entities.user


def database_response(database_fun):
    def wrapped(*args, **kwargs):
        try:
            result = database_fun(*args, **kwargs)
        except DBException as e:
            # print("DB KNOWN::")
            # print(e)
            raise e
        except Exception as e:
            print("DB UNKNOWN::")
            print(e)
            raise DBException()
        return result

    return wrapped


class DBManager:
    db = None
    models = None

    def init_db(self, db, models):
        self.db = db
        self.models = models

    def is_ok(self):
        return self.db is not None and self.models is not None

    @database_response
    def get_tokens_by_user_id(self, user_id):
        return self.models.Token.query.filter_by(user_id=user_id).all()

    # @database_response
    # def get_user_id_by_username(self, username):
    #     return self.get_user_by_username(username).id

    @database_response
    def get_username_and_exptime_by_token(self, token):
        # print(token)
        tok = self.models.Token.query.filter_by(id=token).first()
        # print(tok)
        if tok is None:
            raise DBTokenNotFoundException()
        print(tok.owner.username, tok.expires_in)
        return tok.owner.username, tok.expires_in

    @database_response
    def delete_token(self, token):
        tok = self.models.Token.query.filter_by(id=token).first()
        if tok is not None:
            self.db.session.delete(tok)
            self.db.session.commit()

    # @database_response
    # def get_user_by_username(self, username):
    #     u = self.models.User.query.filter_by(username=username).first()
    #     if u is None:
    #         raise DBUserNotFoundException()
    #     return u

    @database_response
    def get_passhash_by_username(self, username):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        return u.password_hash

    @database_response
    def insert_token_to_username(self, token_id, expires_in, username):
        u = self.models.User.query.filter_by(username=username).first()
        tok = self.models.Token(id=token_id, expires_in=expires_in, owner=u)
        self.db.session.add(tok)
        self.db.session.commit()

    @database_response
    def insert_user(self, user_obj, pass_hash):
        new_user = self.models.User(username=user_obj.username, password_hash=pass_hash,
                                    functions=user_obj.functions,
                                    operators=user_obj.operators,
                                    bio=user_obj.bio,
                                    history=user_obj.history,
                                    rank=user_obj.rank)
        try:
            self.db.session.add(new_user)
            self.db.session.commit()
        except IntegrityError as e:
            raise DBUserAlreadyExistsException(message=e)

    @database_response
    def get_base_user_info(self, username):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        return entities.user.User(dbu=u).to_base_info_dict()

    @database_response
    def update_user_bio(self, username, new_bio):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        u.bio = new_bio
        self.db.session.commit()

    @database_response
    def clear_all_tables(self):
        self.db.drop_all()
        self.db.create_all()

    @database_response
    def get_functions_by_username(self, username):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        print(u.functions)
        return convert_string_to_array(u.functions, auto_type_caster=parse_expr)

    @database_response
    def get_operators_by_username(self, username):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        return convert_string_to_array(u.operators, auto_type_caster=int)

    @database_response
    def insert_functions_to_username(self, username, functions):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        old_funs = u.functions
        new_funs = convert_array_to_string(functions, auto_type_caster=str)
        res = convert_array_to_string([old_funs, new_funs]).strip()
        u.functions = res
        self.db.session.commit()

    @database_response
    def insert_operators_to_username(self, username, operators):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            raise DBUserNotFoundException()
        old_ops = u.operators
        new_ops = convert_array_to_string(operators)
        res = convert_array_to_string([old_ops, new_ops]).strip()
        u.operators = res
        self.db.session.commit()

    def is_user_exists(self, username):
        u = self.models.User.query.filter_by(username=username).first()
        if u is None:
            return False
        return True
