# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {code: CODE, data: {JSON}}, where code is the status code
# And the data is the product, which the function returns


import json


def status():
    code = 200
    data = json.dumps({'State': 'OK'})
    return str(Response(code, data))


def login(username, passhash):
    code = 501
    data = json.dumps({'Error': 'Not done yet! Ping me!'})  # TODO: implement
    return str(Response(code, data))


def register(username, passhash):
    code = 501
    data = json.dumps({'Error': 'Not done yet! Ping me!'})  # TODO: implement
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
