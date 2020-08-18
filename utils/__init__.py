import uuid
import datetime
from config import Config


def gen_token():
    return uuid.uuid4().hex, datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.TOKEN_LIFETIME_SEC)


SEPARATOR = '\t'


def convert_array_to_string(array, sep=SEPARATOR, auto_type_caster=str):
    return sep.join(map(auto_type_caster, array))


def convert_string_to_array(string, sep=SEPARATOR, auto_type_caster=str):
    return list(map(auto_type_caster, string.split(sep)))
