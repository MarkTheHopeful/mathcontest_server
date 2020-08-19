import http.client
import json

host = "127.0.0.1:5000"     # FIXME: temporal


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
    data = json.loads(stringed_json)
    return data


def register():
    username = input_normal("Input your new username:\n")
    password = input_normal("Input your new password:\n")
    req_res = send_request(f"/register/{username}/{password}")
    code = req_res['code']
    state = req_res['state']
    data = json.loads(req_res['data'])
    return code, state, data


def login():
    username = input_normal("Input your username:\n")
    password = input_normal("Input your password:\n")
    req_res = send_request(f"/login/{username}/{password}")
    code = req_res['code']
    state = req_res['state']
    data = json.loads(req_res['data'])
    return code, state, data


def get_status():
    req_res = send_request("/status")
    code = req_res['code']
    state = req_res['state']
    data = json.loads(req_res['data'])
    return code, state, data


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
            code, state, data = register()
            if code == 200:
                print(state)
                break
            else:
                print("Registration failed with error:")
                print(state)
                print("Try again!")
    token = ""
    while True:
        code, state, data = login()
        if code == 200:
            print(state)
            print(f"Your token is {data['Token']}")
            token = data['Token']
            break
        else:
            print("Login failed with error:")
            print(state)
            print("Try again!")

    while True:
        query = input("What would you like to do next?\n")

        if query == "exit" or query == "quit":
            print("Exiting...")
            break
        elif query == "help":
            print(get_help_string())
        elif query == "status":
            code, state, data = get_status()
            if code == 200:
                print(data['State'])
            else:
                print("Something is totally wrong with server!")
                print(data['Error'])
        else:
            print("No such command")
