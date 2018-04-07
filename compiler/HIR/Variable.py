from typing import Text

class Variable:

    def __init__(self, type: Text, init: int,  decl: int):
        self.type = type;
        self.line_init = init;
        self.line_decl = decl;
