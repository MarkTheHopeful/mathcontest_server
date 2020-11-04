from other_clients.Engine import Engine
from utils import smart_split, full_stack

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
    engine.host = new_host
    return "Successfully changed"


def exit_loop():
    raise ExitException("Exit by request")


NAMES_TO_FUNCTIONS = {"test_host": test_host,
                      "set_host": set_host,
                      "exit": exit_loop}


def process_command(command_line):
    command, *arguments = smart_split(command_line)
    if command not in NAMES_TO_FUNCTIONS.keys():
        print("No such command")
        return CODE_PROCEED
    else:
        try:
            print(NAMES_TO_FUNCTIONS[command](*arguments))
        except ExitException as e:
            if e.payload != "":
                print(e.payload)
            if str(e) != "":
                print(e)
            return CODE_EXIT
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
