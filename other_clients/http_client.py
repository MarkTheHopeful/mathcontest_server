import http.client
import json

from game.game_state import deserialize_game_state

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
    return datum['code'], datum['state'], datum['data']


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
    if code == 400 or code == 404 or code == 406 or code == 407:
        return state
    try:
        return state + ":\n:: " + data["Error"]
    except KeyError:
        return state + ":\n" + "Error information was not received"


def get_game_state():
    code, state, data = send_request(f"/game/get_state/{token}")
    if code == 200:
        return True, data
    elif code == 400 or code == 408:
        return False, state
    try:
        return False, state + ":\n:: " + data["Error"]
    except KeyError:
        return False, state + ":\n" + "Error information was not received"


def get_help_string():
    return """\
To see this help type: 'help'
Too check server's status type: 'status'
To quit type: 'exit' or 'quit'"""


# TODO: catch the "server is offline" situation
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
        elif query == "game state":
            is_ok, info = get_game_state()
            if is_ok:
                game_state = deserialize_game_state(info)
                print(f"You are {game_state.player}, your opponent is {game_state.opponent}")
                print(f"The game state is {game_state.state}, the turn number is {game_state.turn_num}")
                print("Your functions:")
                print(*game_state.players_functions)
                print("Your opponent's functions:")
                print(*game_state.opponents_functions)
                print("Your operators:")
                print(*game_state.players_operators)
                print("Your opponent's operators:")
                print(*game_state.opponents_operators)
            else:
                print(info)
        else:
            print("No such command")
