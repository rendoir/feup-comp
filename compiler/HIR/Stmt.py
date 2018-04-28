from antlr4 import ParserRuleContext, tree
from antlr_yal import yalParser
from pprint import pprint
from typing import List
from compiler.HIR.Variable import Variable, ArrayVariable, NumberVariable, UndefinedVariable
from compiler.Printer import ErrorPrinter
from .CodeScope import Scope


def parseStmt(stmt, parent) -> ParserRuleContext:
    from . import CodeScope
    if __debug__:
        assert isinstance(stmt, yalParser.StmtContext), "Stmt.parseStmt() 'stmt'\n - Expected 'yalParser.StmtContext'\n - Got: " + str(type(stmt))
        assert isinstance(parent, Scope), "Stmt.parseStmt() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

    child = stmt.children[0]
    if isinstance(child, yalParser.While_yalContext):
        return CodeScope.While(child, parent)
    elif isinstance(child, yalParser.If_yalContext):
        return CodeScope.If(child, parent)
    elif isinstance(child, yalParser.AssignContext):
        return Assign(child, parent)
    elif isinstance(child, yalParser.CallContext):
        return Call(child, parent)
    else:
        print("Oh damn boie")
        return None

def getVar(var_name, vars_list) -> Variable:
    if __debug__:
        assert isinstance(var_name, str), "Stmt.getVar() 'var_name'\n - Expected 'str'\n - Got: " + str(type(var_name))
        assert isinstance(vars_list, list), "Stmt.getVar() 'vars_list'\n - Expected 'list'\n - Got: " + str(type(vars_list))

    for var_list in vars_list:
        if var_name in var_list:
            return var_list[var_name]

    if not Variable.isLiteral(var_name):
        return None
    else:
        return var_name

def expectedGot(func_name, gotten, expected) -> str:
    if __debug__:
        assert isinstance(func_name, str), "Stmt.expectedGot() 'func_name'\n - Expected 'str'\n - Got: " + str(type(func_name))
        assert isinstance(gotten, list), "Stmt.expectedGot() 'gotten'\n - Expected 'list'\n - Got: " + str(type(gotten))
        assert isinstance(expected, list), "Stmt.expectedGot() 'expected'\n - Expected 'list'\n - Got: " + str(type(expected))

    ret = "Expected " + func_name + "("
    remove = False
    for var in expected:
        remove = True
        ret += var.type + ", "
    if remove:
        ret = ret[:-2]
    ret += ") got " + func_name + "("

    remove = False
    for var in gotten:
        remove = True
        ret += var.type + ", "
    if remove:
        ret = ret[:-2]

    ret += ")"
    return ret

class Statement:
    def __init__(self, node, parent):
        if __debug__:
            assert isinstance(node, ParserRuleContext), "Statement.__init__() 'node'\n - Expected 'ParserRuleContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "Statement.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(mod_funcs))

        self.line = node.getLine()
        self.cols = node.getColRange()

    def checkSemantics(self, printer, var_list):
        raise NotImplementedError("Implement checkSemantics()!")

class Call(Statement):
    def __init__(self, node, parent):
        super(Call, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.CallContext), "Call.__init__() 'node'\n - Expected 'yalParser.CallContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "Call.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(mod_funcs))

        self.module_functions = Scope.getFunctions(parent)
        self.calls = node.children[0]
        self.args = []
        for arg in node.children[1].children:
            self.args.append(arg)


    def __checkArguments(self, func_name: str, func_called, call_vars) -> str:
        from . import CodeScope
        if __debug__:
            assert isinstance(func_name, str), "Call.__checkArguments() 'func_name'\n - Expected 'str'\n - Got: " + str(type(func_name))
            assert isinstance(func_called, CodeScope.Function), "Call.__checkArguments() 'func_called'\n - Expected 'CodeScope.Function'\n - Got: " + str(type(func_called))
            assert isinstance(call_vars, list), "Call.__checkArguments() 'call_vars'\n - Expected 'list'\n - Got: " + str(type(call_vars))

        func_args = func_called.vars[0]
        wrong = False

        if len(call_vars) is len(func_called.vars[0]):
            for i in range(len(call_vars)):
                wrong = (wrong or (call_vars[i] != func_called.vars[0][i]))

        if wrong:
            return expectedGot(func_name, call_vars, func_args)
        return None;

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Call.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Call.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        func_name = str(self.calls[0])
        func_called = None
        func_exists = False
        mod_call = len(self.calls) is 2

        #Check if function exists
        if not mod_call:
            if func_name not in self.module_functions:
                printer.addError(self.line, self.col, "Undefined function", "Could not find '" + func_name + "' in current module!\n Maybe it belongs to another module?")
            else:
                func_called = self.module_functions[func_name]
                func_exists = True

        call_vars = []
        for arg_name in self.args:
            arg = getVar(str(arg_name), var_list)
            if arg is not None:
                call_vars.append(arg)
            else:
                printer.addError(self.line, self.col, "Undefined variable", "Variable '" + str(arg_name) + "' is not defined")
                call_vars.append(UndefinedVariable())

        if func_exists:
            msg = self.__checkArguments(func_name, func_called, call_vars)
            if msg is not None:
                errors.append(msg)

class ExprTest(Statement):
    def __init__(self, node, parent):
        super(ExprTest, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.ExprtestContext), "ExprTest.__init__() 'node'\n - Expected 'yalParser.ExprtestContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ExprTest.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

        self.op = node.children[1]
        self.left = LeftOP(node.children[0], parent)
        self.right = RightOP(node.children[2], parent)

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ExprTest.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ExprTest.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.left.checkSemantics(printer, var_list)
        self.right.checkSemantics(printer, var_list)

class LeftOP(Statement):
    def __init__(self, node, parent):
        super(LeftOP, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Left_opContext), "LeftOP.__init__() 'node'\n - Expected 'yalParser.Left_opContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "LeftOP.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

        child = node.children[0]
        if (isinstance(child, yalParser.Array_accessContext)):
            self.access = ArrayAccess(child, parent)
        elif (isinstance(child, yalParser.Scalar_accessContext)):
            self.access = ScalarAccess(child, parent)
        else:
            print("WUUUUUUUUUUUTTTTTT??????!!!!!!!");

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "LeftOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "LeftOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.access.checkSemantics(printer, var_list)


class RightOP(Statement):
    def __init__(self, node, parent):
        super(RightOP, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Right_opContext), "RightOP.__init__() 'node'\n - Expected 'yalParser.Right_opContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "RightOP.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

        self.value = []

        if isinstance(node.children[0], tree.Tree.TerminalNodeImpl):
            self.value.append(ArraySize(node.children[1], parent))
            self.needs_op = False
            self.arr_size = True
        elif node.getChildCount() is 1: #Only term
            self.value.append(Term(node.children[0], parent))
            self.needs_op = False
            self.arr_size = False
        else:
            self.value.append(Term(node.children[0], parent))
            self.operator = str(node.children[1])
            self.value.append(Term(node.children[0], parent))
            self.needs_op = True
            self.arr_size = False

    def resultType(self) -> str:
        if self.arr_size: #TODO need to check function return
            return "ARR"
        else:
            return "NUM"

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "RightOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "RightOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        size_accesses = 0
        for term in self.value:
            term.checkSemantics(printer, var_list)
            if term.isSize():
                size_accesses += 1

        if self.needs_op:
            addsub_op = self.operator is '+' or self.operator is '-'
            if addsub_op and size_accesses >= 2:
                if self.operator is '+':
                    txt = "add"
                else:
                    txt = "subtract"
                    printer.addError(self.line, self.cols, "Forbidden operation", "Tried to " + txt + " two accesses to array size")



class Assign(Statement):
    def __init__(self, node, parent):
        super(Assign, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.AssignContext), "Assign.__init__() 'node'\n - Expected 'yalParser.AssignContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "Assign.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(node))

        self.left = LeftOP(node.children[0], parent)
        self.right = RightOP(node.children[1], parent)
        self.parent = parent

    def getVarInfo(self):
        return (self.left.access.var, self.left.access);

    def isAssignArray(self):
        return self.right.arr_size;

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Assign.checkSemantics() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Assign.checkSemantics() 'var_list'\n - Expected: 'list'\n - Got: " + str(type(var_list))

        (var_name, var_info) = self.getVarInfo()
        index = var_info.indexAccess()
        existing_var = self.__varExists(var_name, var_list)
        if existing_var is not None:
            if self.right.resultType() != existing_var.type:
                printer.addError(self.line, self.cols, "Wrong assignment", "Tried to assign a '" + self.right.resultType() + "' to a '" + existing_var.type + "' variable")
        else:
            var_obj = None
            # TODO add array size and number value
            if self.isAssignArray():
                var_obj = ArrayVariable(var_name, 0, (self.line, self.cols[0]), (self.line, self.cols[0]))
            else:
                var_obj = NumberVariable(var_name, 0, (self.line, self.cols[0]), (self.line, self.cols[0]))
            self.parent.addVar(var_name, var_obj)

    def __varExists(self, var_name, var_lists) -> Variable:
        if __debug__:
            assert isinstance(var_name, str), "Assign.__varExists()\n - Expected: 'str'\n - Got: " + str(type(var_name))
            assert isinstance(var_lists, list), "Assign.__varExists()\n - Expected: 'list'\n - Got: " + str(type(var_lists))

        for var_list in var_lists:
            if var_name in var_list:
                return var_list[var_name]

        return None

class ArrayAccess(Statement):
    def __init__(self, node, parent):
        super(ArrayAccess, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Array_accessContext), "ArrayAccess.__init__() 'node'\n - Expected 'yalParser.Array_accessContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ArrayAccess.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(node))

        self.var = str(node.children[0])
        self.index = str(node.children[1])

    def indexAccess(self):
        return self.index

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ArrayAccess.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ArrayAccess.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        var = getVar(self.var, var_list)

        if var is not None:
            if not isinstance(var, ArrayVariable):
                printer.addError(self.line, self.cols, "Indexing impossible", "Tried to index a variable of type '" + var.type + "', which is only possible with arrays")
            elif not var.validAccess(self.index):
                printer.addError(self.line, self.cols, "Out of bounds", "Tried to index position " + self.index + " when array only has " + var.size + " positions")

        else:
            printer.addError(self.line, self.cols, "Variable undefined", "Could not find '" + self.var + "' in current scope!")

class ScalarAccess(Statement):
    def __init__(self, node, parent):
        super(ScalarAccess, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Scalar_accessContext), "ScalarAccess.__init__() 'node'\n - Expected 'yalParser.Scalar_accessContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ScalarAccess.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))


        self.var = str(node.children[0])
        self.size = (len(node.children) is 2)

    def indexAccess(self):
        return None

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ScalarAccess.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ScalarAccess.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        var = getVar(self.var, var_list)

        if var is not None:
            if self.size and not isinstance(var, ArrayVariable):
                printer.addError(self.line, self.cols, "NUM has no size", "Tried to get 'size' of a '" + var.type + "' variable")

        else:
            printer.addError(self.line, self.cols, "Variable undefined", "Could not find '" + self.var + "' in current scope!")

class ArraySize(Statement):
    def __init__(self, node, parent):
        super(ArraySize, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Array_sizeContext), "ArraySize.__init__() 'node'\n - Expected 'yalParser.Array_sizeContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ArraySize.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(node))

        if ArraySize.isDigit(node):
            self.value = int(str(node.children[0]))
            self.access = False
        else: #Scalar access
            self.value = ScalarAccess(node)
            self.access = True

    def isDigit(node: yalParser.Array_sizeContext):
        return str(node.children[0]).isdigit();

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "RightOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "RightOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if self.access:
            self.value.checkSemantics(printer, var_list)
        elif self.value < 0:
            printer.addError(self.line, self.col, "Negative array size", "Tried to create an array with '" + self.value + "' positions")


class Term(Statement):
    def __init__(self, node, parent):
        super(Term, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.TermContext), "Term.__init__() 'node'\n - Expected 'yalParser.TermContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "Term.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

        base = 0
        if isinstance(node, tree.Tree.TerminalNodeImpl):
            return;

        if str(node.children[0]) == '+' or str(node.children[0]) == '-':
            base = 1

        self.positive = (str(node.children[0]) is not "-")
        child = node.children[base]


        if isinstance(child, yalParser.CallContext):
            self.value = Call(child, parent)
        elif isinstance(child, yalParser.Array_accessContext):
            self.value = ArrayAccess(child, parent)
        elif isinstance(child, yalParser.Scalar_accessContext):
            self.value = ScalarAccess(child, parent)
        elif isinstance(child, tree.Tree.TerminalNodeImpl):
            self.value = int(str(child))
        else:
            print("HMMMMMMMMMMMMM?!!?!")

    def isSize(self) -> bool:
        if isinstance(self.value, ScalarAccess):
            return self.value.size
        return False

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Term.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Term.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if not isinstance(self.value, int):
            self.value.checkSemantics(printer, var_list)
