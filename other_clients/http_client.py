import os

import requests
import json

from game.game_state import deserialize_game_state

host = os.environ.get("MATHCONTEST_SERVER") or "http://127.0.0.1:5000"
current_game_state = None
token = ""  # initializes later


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


def get_status():
    code, state, data = send_request("/api/v1/service/status")
    if code == 200:
        return f"State: {data['State']}, Api version: {data['API version']}, DB manager: {data['DB manager']},\n " \
               f"Game manager: {data['Game manager']}, Games: {data['Amount of games']}, Queue: {data['Queue length']}"
    try:
        return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
    except KeyError:
        return state + ":\n" + "Error information was not received"


def register():
    username = input_normal("Input your new username:\n")
    password = input_normal("Input your new password:\n")
    code, state, data = send_request(f"/api/v1/user/register/{username}/{password}")
    try_again = False
    if code == 200:
        return try_again, state
    try_again = True
    if code == 200 or code == 405:
        return try_again, state
    try:
        return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
    except KeyError:
        return try_again, state + ":\n" + "Error information was not received"


def login():
    username = input_normal("Input your username:\n")
    password = input_normal("Input your password:\n")
    code, state, data = send_request(f"/api/v1/user/login/{username}/{password}")
    try_again = False
    if code == 200:
        return try_again, data['Token']
    try_again = True
    if code == 402:
        return try_again, state

    try:
        return try_again, state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
    except KeyError:
        return try_again, state + ":\n" + "Error information was not received"


def get_user_info(username):
    code, state, data = send_request(f"/api/v1/user/{username}")
    if code == 200:
        return f"User {data['username']}\n" \
               f"Bio: {data['bio']}\n" \
               f"Rank: {data['rank']}\n" \
               f"Game history: {data['history']}\n"
    elif code == 404:
        return state
    else:
        try:
            return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def set_bio():
    bio = input_normal("Input your new bio:\n")
    code, state, data = send_request(f"/api/v1/user/bio/{token}", {"bio": bio})
    if code == 200:
        return state
    if code == 400:
        return state
    try:
        return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
    except KeyError:
        return state + ":\n" + "Error information was not received"


def get_game_state():
    code, state, data = send_request(f"/api/v1/game/state/{token}/0")
    if code == 200:
        return True, data
    elif code == 400 or code == 408:
        return False, state
    try:
        return False, state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
    except KeyError:
        return False, state + ":\n" + "Error information was not received"


def get_into_queue():
    code, state, data = send_request(f"/api/v1/queue/put/{token}")
    if code == 200:
        return "You are now in the queue. To check amount of users in the queue type 'queue length'.\n" \
               " To try to create a game with somebody type 'try to create'"
    if code == 400 or code == 406 or code == 411:
        return state
    else:
        try:
            return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def del_from_queue():
    code, state, data = send_request(f"/api/v1/queue/del/{token}")
    if code == 200:
        return "You are now removed from the queue"
    if code == 400 or code == 412:
        return state
    else:
        try:
            return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def get_queue_size():
    code, state, data = send_request(f"/api/v1/queue/length")
    if code == 200:
        return data["Length"]
    else:
        try:
            return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def check_if_game_found():
    code, state, data = send_request(f"/api/v1/game/create/{token}")
    if code == 200:
        return False, f"Game created with player {data['Opponent']}. To confirm type 'confirm game'"
    elif code == 412:
        return False, f"You are not in the queue.\n" \
                      f"To check it type 'game state'"
    elif code == 400 or code == 413:
        return False, state
    elif code == 416 or code == 414:
        return True, (state, data)
    else:
        try:
            return False, state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return False, state + ":\n" + "Error information was not received"


def confirm_game_start():
    code, state, data = send_request(f"/api/v1/game/confirm/{token}")
    if code == 200:
        return True, "Game start confirmed successfully"
    elif code == 201:
        return True, state
    elif code == 400 or code == 408 or code == 414:
        return False, state
    else:
        try:
            return False, state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
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

    code, state, data = send_request(f"/api/v1/game/turn/{token}/{operator_ind}/0",
                                     j_payload={"indexes_function": args})
    if code == 200:
        return f"{state}, result functions is {data['Result Function']}"
    elif code == 400 or code == 409 or code == 415:
        return state
    else:
        try:
            return state + ":\n:: " + data["Error"] + "\n" + data["Stack"]
        except KeyError:
            return state + ":\n" + "Error information was not received"


def get_help_string():
    return """\
To see this help type: 'help'
To check server's status type: 'status'
To check some user's information type: 'user <username>'
To set your bio type: 'set bio'
To get in waiting game queue type: 'get in queue'
To get out of waiting queue type: 'del from queue'
To check the amount of users in the queue type: 'queue length'
To try to create game with somebody type: 'try to create'
To confirm that you are ready to start game type 'confirm game'
To get state of your current game type: 'game state'
To make turn type: 'make turn'
To quit type: 'exit' or 'quit'"""


def print_game_state(game_state):
    print(f"You are {game_state.player}, your opponent is {game_state.opponent}")
    print(f"The game state is {game_state.state.get_description()}, the turn number is {game_state.turn_num}")
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
        elif query.split()[0] == "user":
            print(get_user_info(query.split()[1]))
        elif query == "set bio":
            print(set_bio())
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
            # noinspection PyRedeclaration
            current_game_state = deserialize_game_state(info)
            _ = input("Would you like to see new game state? (y/n)")
            if _ == "y":
                print_game_state(current_game_state)
        elif query == "get in queue":
            print(get_into_queue())
        elif query == "del from queue":
            print(del_from_queue())
        elif query == "queue length":
            print(get_queue_size())
        elif query == "try to create":
            is_game_printed, payload = check_if_game_found()
            if not is_game_printed:
                print(payload)
            else:
                state, game_info = payload
                print(state)
                print("The state of your game:")
                current_game_state = deserialize_game_state(game_info)
                print_game_state(current_game_state)
        elif query == "confirm game":
            is_ok, info = confirm_game_start()
            print(info)
            if is_ok:
                is_ok, info = get_game_state()
                if not is_ok:
                    print("Encountered an error while trying to update your game state. Error:")
                    print(info)
                    continue
                current_game_state = deserialize_game_state(info)
                print_game_state(current_game_state)
        else:
            print("No such command")
