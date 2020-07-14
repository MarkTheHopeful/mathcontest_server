import hashlib


def encrypt_string(string, salt):
    hasher = hashlib.sha256()
    b_salt = salt.encode('utf-8')
    b_string = string.encode('utf-8')
    hasher.update(b_salt)
    hasher.update(b_string)
    return hasher.hexdigest()


if __name__ == "__main__":
    DEFINITELY_NOT_A_SALT = "sugar"
    while True:
        a = input()
        print(encrypt_string(a, DEFINITELY_NOT_A_SALT))
