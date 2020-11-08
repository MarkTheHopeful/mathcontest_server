from other_clients.Engine import Engine, get_error_message
from other_clients.ServerState import ServerState
from utils import smart_split, full_stack
import validators

CODE_EXIT = -1
CODE_PROCEED = 0

engine = None
token = ""


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


def get_help():
    return """\
List of available commands:
help: print this help
exit: exit client
test_host: test availability of the host
set_host: set new host URL
"""


NAMES_TO_FUNCTIONS = {"test_host": test_host,
                      "set_host": set_host,
                      "get_host_status": get_host_status,
                      "exit": exit_loop,
                      "help": get_help}


def process_command(command_line):
    command, *arguments = smart_split(command_line)
    if command not in NAMES_TO_FUNCTIONS.keys():
        print("No such command")
        return CODE_PROCEED
    try:
        print(NAMES_TO_FUNCTIONS[command](*arguments))
    except ExitException as e:
        if e.payload != "":
            print(e.payload)
        if str(e) != "":
            print(e)
        return CODE_EXIT
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
