class Player:
    functions = []
    operators = []

    def __init__(self, name, base_functions, base_operators):
        self.name = name
        self.functions = list(base_functions)
        self.operators = list(base_operators)