
class Variable:
    def __init__(self, name: str, type: str, init: int,  decl: int):
        self.name = name
        self.type = type
        self.line_init = init
        self.line_decl = decl

class NumberVariable (Variable):
    def __init__(self, name: str, value: int, init: int, decl: int):
        super(NumberVariable, self).__init__(name, "NUM", init, decl)
        self.value = value

class ArrayVariable(Variable):
    def __init__(self, name: str, size: list, init: int, decl: int):
        super(ArrayVariable, self).__init__(name, "ARR", init, decl)
        self.size = size;
