from compiler.HIR.Variable import *

class ArrayVariable(Variable):

    def __init__(self, size: list, init: int, decl: int):
        self.size = size;
