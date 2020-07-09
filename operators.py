from sympy import symbols

class Operator:
    def __init__(self, function, name):
        self.f = function
        self.name = name
        self.ar_cnt = function.__code__.co_argcount

    def __call__(self, *args):
        return self.f(*args)

    def __str__(self):
        return self.name


ADD = Operator((lambda f_1, f_2: f_1 + f_2), "+")
UMN = Operator((lambda f_1: -f_1), "-")
MUL = Operator((lambda f_1, f_2: f_1 * f_2), "*")
DRX = Operator((lambda f_1: f_1.diff(symbols('x'))), "d/dx")

ALL = [ADD, UMN, MUL, DRX]