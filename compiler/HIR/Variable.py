
class Variable:
    def __init__(self, name: str, type: str, decl: int, init: int):
        self.name = name
        self.type = type
        self.line_init = init
        self.line_decl = decl

    def __str__(self):
        pass

    def setInit(self, value: int, init: int):
        raise NotImplementedError("Implement setInit()!")

    def initialized(self):
        return self.line_init is not None

class NumberVariable (Variable):
    def __init__(self, name: str, value: int, decl: int, init: int):
        super(NumberVariable, self).__init__(name, "NUM", decl, init)
        self.value = value

    def __str__(self):
        print("NUM VAR\n")
        return self.name;

    def setInit(self, init: int):
        if self.init is None:
            self.init = init


class ArrayVariable(Variable):
    def __init__(self, name: str, size: list, decl: int, init: int):
        super(ArrayVariable, self).__init__(name, "ARR", decl, init)
        self.size = size;

    def __str__(self):
        return self.name + "[]"

    def setInit(self, value: int, init: int):
        print("How was this called!?")
