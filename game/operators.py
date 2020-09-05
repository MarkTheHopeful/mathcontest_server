from sympy import symbols


class Operator:
    def __init__(self, function, basic_rep, latex_rep=""):
        if latex_rep == "":
            latex_rep = basic_rep
        self.f = function
        self.latex_rep = latex_rep
        self.basic_rep = basic_rep
        self.ar_cnt = function.__code__.co_argcount

    def __call__(self, *args):
        return self.f(*args)

    def __str__(self):
        return self.basic_rep


def make_smart_rep(is_latex):
    if is_latex:
        return lambda op: op.latex_rep
    else:
        return lambda op: str(op)


ADD = Operator((lambda f_1, f_2: f_1 + f_2), "+")
UMN = Operator((lambda f_1: -f_1), "-")
MUL = Operator((lambda f_1, f_2: f_1 * f_2), "*")
DRX = Operator((lambda f_1: f_1.diff(symbols('x'))), "d/dx", "\\frac{d}{d x}")
SUP = Operator((lambda f_1, f_2: f_1.subs({symbols('x'): f_2})), "sp()")

ALL = [ADD, UMN, MUL, DRX, SUP]
