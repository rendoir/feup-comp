
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

    def __ne__(self, other) -> bool:
        if __debug__:
            assert isinstance(other, Variable), "Variable.__ne__() 'other' should be 'Variable'"

        return (self.type != other.type and (self.type != "???" and other.type != "???"))


    def isLiteral(var: str) -> bool:
        if not isinstance(var, str):
            return True;

        if var[0] == '"' and var[-1] == '"':
            return True;
        if var[0].isdigit():
            return True;

        return False

class NumberVariable (Variable):
    def __init__(self, name: str, value: int, decl: int, init: int):
        super(NumberVariable, self).__init__(name, "NUM", decl, init)
        self.value = value

    def __str__(self):
        return self.name;

    def setInit(self, init: int):
        if self.init is None:
            self.init = init

class ArrayVariable(Variable):
    def __init__(self, name: str, size: int, decl: int, init: int):
        super(ArrayVariable, self).__init__(name, "ARR", decl, init)
        self.size = size;

    def __str__(self):
        return self.name + "[]"

    def validAccess(self, access) -> bool:
        if __debug__:
            assert isinstance(access, int), "ArrayVariable.validAccess() 'access'\n - Expected 'int'\n - Got: " + str(type(access))

        # When size is -1, it means its impossible to know size
        return (self.size > access or self.size is -1)

    def setInit(self, value: int, init: int):
        print("How was this called!?")

class UndefinedVariable(Variable):
    def __init__(self, name=None, size=None, decl=None, init=None):
        super(UndefinedVariable, self).__init__(None, "???", None, None)
