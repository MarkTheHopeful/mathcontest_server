import http.client
import json

host = "127.0.0.1:5000"  # FIXME: temporal
token = ""  # initialises later


def input_normal(input_line, checker=lambda x: x):
    temp = input(input_line)
    while not checker(temp):
        temp = input(input_line)
    return temp


def send_request(request_line):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", request_line)
    resp = conn.getresponse().read()
    stringed_json = resp.decode('utf8').replace("'", '"')
    datum = json.loads(stringed_json)
    return datum['code'], datum['state'], json.loads(datum['data'])


def register():
    username = input_normal("Input your new username:\n")
    password = input_normal("Input your new password:\n")
    code, state, data = send_request(f"/register/{username}/{password}")
    try_again = False
    if code == 200:
        return try_again, state
    try_again = True
    if code == 200 or code == 405:
        return try_again, state
    try:
        return try_again, state + ":\n:: " + data["Error"]
    except KeyError:
        return try_again, state + ":\n" + "Error information was not received"


def login():
    username = input_normal("Input your username:\n")
    password = input_normal("Input your password:\n")
    code, state, data = send_request(f"/login/{username}/{password}")
    try_again = False
    if code == 200:
        return try_again, data['Token']
    try_again = True
    if code == 402:
        return try_again, state

    try:
        return try_again, state + ":\n:: " + data["Error"]
    except KeyError:
        return try_again, state + ":\n" + "Error information was not received"


def get_status():
    code, state, data = send_request("/status")
    if code == 200:
        return state
    try:
        return state + ":\n:: " + data["Error"]
    except KeyError:
        return state + ":\n" + "Error information was not received"


def start_game_with(opponent_name):
    code, state, data = send_request(f"/start_game/{token}/{opponent_name}")
    if code == 200:
        return state + f"\n Game ID: {data['Game ID']}"
    if code == 400:
        return state
    try:
        return state + ":\n:: " + data["Error"]
    except KeyError:
        return state + ":\n" + "Error information was not received"


def get_help_string():
    return """\
To see this help type: 'help'
Too check server's status type: 'status'
To quit type: 'exit' or 'quit'"""


if __name__ == "__main__":
    # host = input("Enter the host address\n")
    is_registered = input("Are you registered? y/n\n")
    if is_registered.lower() != 'y':
        while True:
            fail, result = register()
            print(result)
            if not fail:
                break
            print("Registration failed with error:")
            print(result)
            print("Try again!")
    while True:
        fail, result = login()
        if not fail:
            token = result
            print("Login successful")
            # print(token)  TODO: add special debug mode
            break
        print("Login failed with error:")
        print(result)
        print("Try again!")

    while True:
        query = input("What would you like to do next?\n")

        if query == "exit" or query == "quit":
            print("Exiting...")
            break
        elif query == "help":
            print(get_help_string())
        elif query == "status":
            result = get_status()
            print(result)
        elif query.startswith("start_game_with"):
            query = query.split()
            if len(query) != 2:
                print("Illegal amount of arguments. Required: 1, opponent username, given", len(query))
                continue
            opponent_username = query[1]
            result = start_game_with(opponent_username)
            print(result)
        else:
            print("No such command")
