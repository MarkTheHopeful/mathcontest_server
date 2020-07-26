import sympy as sp

x = sp.symbols("x")

BASE_FUNCTIONS = [x + 5, sp.exp(x), sp.sin(x), x ** 2 - 7 * x + 10, sp.asin(x)]
BASE_OPERATORS = [0, 1, 2, 3]