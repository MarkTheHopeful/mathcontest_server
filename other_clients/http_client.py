import http.client

host = "127.0.0.1:5000"


def input_normal(input_line, checker):
    temp = input(input_line)
    while not checker(temp):
        temp = input(input_line)
    return temp


def register():
    username = input_normal("Input your new username:\n", )
    password = input("Input your new password:\n")


def login():
    pass


if __name__ == "__main__":
    host = input("Enter the host address")
    is_registered = input("Are you registered? y/n\n")
    if is_registered.lower() != 'y':
        register()
    login()
