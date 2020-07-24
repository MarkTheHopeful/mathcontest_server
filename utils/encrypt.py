import bcrypt


def check_password(password, hashed):
    password = password.encode('utf-8')
    hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password, hashed)


def encrypt_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")


def encrypt_string(string):
    return encrypt_password(string)


if __name__ == "__main__":
    while True:
        a = input()
        enc = encrypt_string(a)
        print(enc)
        print(f"Check password: {check_password(a, enc)}")