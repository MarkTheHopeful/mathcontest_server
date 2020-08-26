import os

import requests
import json

from game.game_state import deserialize_game_state

host = os.environ.get("MATHCONTEST_SERVER") or "http://127.0.0.1:5000"
current_game_state = None
token = ""  # initialises later


def input_normal(input_line, checker=lambda x: x):
    temp = input(input_line)
    while not checker(temp):
        temp = input(input_line)
    return temp


def send_request(request_line, j_payload=None):
    if j_payload is None:
        conn = requests.get(host + request_line)
    else:
        conn = requests.post(host + request_line, json=j_payload)

    resp = conn.text
    stringed_json = resp.replace("'", '"')
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
    code, state, data = send_request(f"/game/get_state/{token}/0")
    if code == 200:
        return True, data
    elif code == 400 or code == 408:
        return False, state
    try:
        return False, state + ":\n:: " + data["Error"]
    except KeyError:
        return False, state + ":\n" + "Error information was not received"


def make_turn():
    print("Choose place to the new function! It will also be the first argument")
    pos = int(input_normal("Enter correct position:\n",
                           lambda ind:
                           0 <= int(ind) < len(current_game_state.players_functions) + len(
                               current_game_state.opponents_functions)))
    operator_ind = int(input_normal("Enter the operator's index:\n",
                                    lambda ind: 0 <= int(ind) <= len(current_game_state.players_operators)))
    args = [pos]
    while len(args) < current_game_state.players_operators_args[operator_ind]:
        args.append(int(input_normal("Enter another argument's index:\n",
                                     lambda ind:
                                     0 <= int(ind) < len(current_game_state.players_functions) + len(
                                         current_game_state.opponents_functions))))

    code, state, data = send_request(f"/game/make_turn/{token}/{operator_ind}/0", j_payload={"fun_indexes": args})
    if code == 200:
        return f"{state}, result functions is {data['Result Function']}"
    elif code == 400 or code == 409:
        return state
    else:
        try:
            return state + ":\n:: " + data["Error"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def get_help_string():
    return """\
To see this help type: 'help'
To check server's status type: 'status'
To start game with somebody type: 'start_game_with <opponent's username>'
To get state of your current game type: 'game state'
To make turn type: 'make turn'
To quit type: 'exit' or 'quit'"""


def print_game_state(game_state):
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


# TODO: catch the "server is offline" situation
if __name__ == "__main__":
    # print(os.environ.get('PYTHONPATH'))
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

    is_ok, info = get_game_state()
    if is_ok:
        current_game_state = deserialize_game_state(info)
        print("Found a game, where you are already in! Would you like to see its state? (y/n)")
        _ = input()
        if _.lower() == "y":
            print_game_state(current_game_state)
        else:
            print("Okay, you can always access it via 'game state' command.")
    else:
        current_game_state = None

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
            is_ok, info = get_game_state()
            if is_ok:
                current_game_state = deserialize_game_state(info)
                print(result)
            else:
                print("The game started successfully, but by some reasons you can't get game information")  # FIXME
                print(info)

        elif query == "game state":
            is_ok, info = get_game_state()
            if is_ok:
                current_game_state = deserialize_game_state(info)
                print_game_state(current_game_state)
            else:
                print(info)
        elif query == "make turn":
            is_ok, info = get_game_state()
            if not is_ok:
                print("Encountered an error while trying to update your game state. Error:")
                print(info)
                continue
            current_game_state = deserialize_game_state(info)
            print(make_turn())
            is_ok, info = get_game_state()
            if not is_ok:
                print("Encountered an error while trying to update your game state. Error:")
                print(info)
                continue
            current_game_state = deserialize_game_state(info)
            _ = input("Would you like to see new game state? (y/n)")
            if _ == "y":
                print_game_state(current_game_state)

        else:
            print("No such command")
