from other_clients.Engine import Engine, get_error_message
from other_clients.DataClasses import ServerState, UserInfo
from utils import smart_split, full_stack
import validators

CODE_EXIT = -1
CODE_PROCEED = 0

engine = None


class Current:
    def __init__(self, token):
        self.token = token

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def __str__(self):
        return self.token


current = Current("Missed")


class ExitException(Exception):
    payload = ""

    def __init__(self, payload="", message=""):
        self.payload = payload
        super(ExitException, self).__init__(message)


def test_host():
    test_res = engine.test_host()
    if not test_res & engine.SERVER_REACHABLE:
        return "The server is not reachable"
    if not test_res & engine.SERVER_WORKS:
        return "The server is not working correctly"
    return "The server is working"


def set_host(new_host):
    if not (new_host.startswith("http://") or new_host.startswith("https://")):
        new_host = "http://" + new_host
    if not validators.url(new_host):
        return "New host is not a valid url"
    engine.host = new_host
    return "Successfully changed"


def exit_loop():
    raise ExitException("Exit by request")


def get_host_status():
    code, state, data = engine.send_request("/api/v1/service/status")
    if code == 200:
        server_state = ServerState(data)
        return str(server_state)
    return get_error_message(state, data)


def login(log, pas):
    code, state, data = engine.send_request(f"/api/v1/user/login/{log}/{pas}")
    if code == 200:
        current.set_token(data["Token"])
        return data["Token"]
    if code == 402:
        return state
    return get_error_message(state, data)


def register(log, pas):
    code, state, data = engine.send_request(f"/api/v1/user/register/{log}/{pas}")
    if code == 200 or code == 405:
        return state
    return get_error_message(state, data)


def get_user(username):
    code, state, data = engine.send_request(f"/api/v1/user/{username}")
    if code == 200:
        user_info = UserInfo(data)
        return str(user_info)
    if code == 404:
        return state
    return get_error_message(state, data)


def set_bio(bio, tok=current):
    if tok is Current:
        tok = current.get_token()
    code, state, data = engine.send_request(f"/api/v1/user/bio/{tok}", {"bio": bio})
    if code == 200 or code == 400:
        return state
    return get_error_message(state, data)


def get_help():
    return """\
List of available commands:
help: print this help
exit: exit client
test_host: test availability of the host
set_host <url>: set new host URL
get_host_status: get the host's status
login <log> <pas>: login
register <log> <pas>: register
get_user <username>: get user information
set_bio <bio> [token]: set bio for user with token, if given (else last login token will be used)
"""


NAMES_TO_FUNCTIONS = {"test_host": test_host,
                      "set_host": set_host,
                      "get_host_status": get_host_status,
                      "login": login,
                      "register": register,
                      "get_user": get_user,
                      "set_bio": set_bio,
                      "exit": exit_loop,
                      "help": get_help}


def process_command(command_line):
    try:
        command, *arguments = smart_split(command_line)
        print(NAMES_TO_FUNCTIONS[command](*arguments))
    except ExitException as e:
        if e.payload != "":
            print(e.payload)
        if str(e) != "":
            print(e)
        return CODE_EXIT
    except KeyError:
        print("No such command")
        return CODE_PROCEED
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)
    except Exception as e:
        print(e)
        print(full_stack())
    return CODE_PROCEED


if __name__ == "__main__":
    engine = Engine()

    while True:
        try:
            next_command_line = input("Enter next command:\n")
        except KeyboardInterrupt or EOFError:
            print("An interruption signal caught")
            exit_code = CODE_EXIT
        else:
            exit_code = process_command(next_command_line)
        if exit_code == CODE_EXIT:
            print("Exiting")
            break
