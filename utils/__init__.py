import datetime
import uuid
import traceback
import sys

from config import Config


def gen_token():
    return uuid.uuid4().hex, datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.TOKEN_LIFETIME_SEC)


SEPARATOR = '\t'


def convert_array_to_string(array, sep=SEPARATOR, auto_type_caster=str):
    return sep.join(map(auto_type_caster, array))


def convert_string_to_array(string, sep=SEPARATOR, auto_type_caster=str):
    return list(map(auto_type_caster, string.split(sep)))


def full_stack():
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]  # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stack_str = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stack_str += '  ' + traceback.format_exc().lstrip(trc)
    return stack_str
