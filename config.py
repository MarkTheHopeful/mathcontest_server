import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'somebody-once-told-me'
    SERVER_NAME = "0.0.0.0:5660"
