
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

    def differentType(first_type, second_type) -> bool:
        if __debug__:
            assert isinstance(first_type, str), "Variable.diffType() 'first_type'\n - Expected 'str'\n - Got: " + str(type(first_type))
            assert isinstance(second_type, str), "Variable.diffType() 'second_type'\n - Expected 'str'\n - Got: " + str(type(second_type))

        return first_type != second_type and first_type != '???' and second_type != '???'

    def diffType(self, other) -> bool:
        if __debug__:
            assert isinstance(other, Variable), "Variable.diffType() 'other'\n - Expected 'Variable'\n - Got: " + str(type(other))

        return (self.type != other.type and self.type != "???" and other.type != "???")

    def isLiteral(var: str) -> bool:
        if not isinstance(var, str):
            return True;

        if var[0] == '"' and var[-1] == '"':
            return True;
        if var.isdigit() or (var[0] == '-' and var[1:].isdigit()):
            return True;

        print('Var "' + var + '" not a digit')
        return False

    def toLIR() -> str:
        raise NotImplementedError("Should have implemented Variable::toLIR()")

class NumberVariable (Variable):
    def __init__(self, name: str, value: int, decl: int, init: int):
        super(NumberVariable, self).__init__(name, "NUM", decl, init)
        self.value = value

    def __str__(self):
        return self.name;

    def setInit(self, init: int):
        if self.init is None:
            self.init = init

    def toLIR(self):
        return 'I'

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

    def toLIR(self):
        return '[I'

class UndefinedVariable(Variable):
    def __init__(self, name=None, size=None, decl=None, init=None):
        super(UndefinedVariable, self).__init__(None, "???", 0, 0)

    def __str__(self):
        return 'Undef'

class BranchedVariable(Variable):
    def __init__(self, name, type1, type2, decl=None, init=None):
        super(BranchedVariable, self).__init__(name, "???", None, None)
        self.reported = False
        self.type1 = type1
        self.type2 = type2

    def wasReported(self):
        self.reported = True
        self.init = 0
        self.decl = 0

    def __str__(self):
        return 'Branched'
