from compiler.HIR.Variable import *

class NumberVariable (Variable):

    def __init__(self, value: int, init: int, decl: int):
        super(NumberVariable, self).__init__("NUM", init, decl)
        self.value = value
