# There the functions are being implemented.
# Then the routes.py will use them
# The functions always produce output as JSON
# The format is: {response: CODE, data: {JSON}}, where response is the status code
# And the data is the product, which the function returns


import json


def status():
    response = 200
    data = json.dumps({'State': 'OK'})
    return str(json.dumps({"response": response, "data": data}))
