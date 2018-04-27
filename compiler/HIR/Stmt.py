from antlr4 import ParserRuleContext, tree
from antlr_yal import yalParser
from pprint import pprint
from typing import List
from compiler.HIR.Variable import Variable, UndefinedVariable
from compiler.Printer import ErrorPrinter


def parseStmt(stmt, parent) -> ParserRuleContext:
    from . import CodeScope
    if __debug__:
        assert isinstance(stmt, yalParser.StmtContext), "Stmt.parseStmt() 'stmt' should be 'yalParser.StmtContext'"
        assert isinstance(parent, CodeScope.Scope), "Stmt.parseStmt() 'parent' should be 'CodeScope.Scope'"

    child = stmt.children[0]
    if isinstance(child, yalParser.While_yalContext):
        return CodeScope.While(child, parent)
    elif isinstance(child, yalParser.If_yalContext):
        return CodeScope.If(child, parent)
    elif isinstance(child, yalParser.AssignContext):
        return Assign(child)
    elif isinstance(child, yalParser.CallContext):
        return Call(child.children[0], child.children[1])
    else:
        print("Oh damn boie")
        return None

def getVar(var_name, vars_list) -> Variable:
    if __debug__:
        assert isinstance(var_name, str), "Stmt.getVar() 'var_name' should be 'str'"
        assert isinstance(vars_list, list), "Stmt.getVar() 'vars_list' should be 'list'"

    for var_list in vars_list:
        if var_name in var_list:
            return var_list[var_name]

    if not Variable.isLiteral(var_name):
        return None
    else:
        return var_name

def expectedGot(func_name, gotten, expected) -> str:
    if __debug__:
        assert isinstance(func_name, str), "Stmt.expectedGot() 'func_name' should be 'str'"
        assert isinstance(gotten, list), "Stmt.expectedGot() 'gotten' should be 'list'"
        assert isinstance(expected, list), "Stmt.expectedGot() 'expected' should be 'list'"

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

class Call:
    def __init__(self, calls, args_node):
        if __debug__:
            assert isinstance(calls, str), "Call.__init__() 'calls' should be 'str'"
            assert isinstance(args_node, yalParser.Arg_listContext), "Call.__init__() 'args_node' should be 'yalParser.Arg_listContext'"

        self.calls = calls.split('.')
        self.args = []
        for arg in args_node.children:
            self.args.append(str(arg))


    def __checkArguments(self, func_name: str, func_called, call_vars) -> str:
        from . import CodeScope
        if __debug__:
            assert isinstance(func_name, str), "Call.__checkArguments() 'func_name' should be 'str'"
            assert isinstance(func_called, CodeScope.Function), "Call.__checkArguments() 'func_called' should be 'CodeScope.Function'"
            assert isinstance(call_vars, list), "Call.__checkArguments() 'call_vars' should be 'list'"

        func_args = func_called.vars[0]
        wrong = False

        if len(call_vars) is len(func_called.vars[0]):
            for i in range(len(call_vars)):
                wrong = (wrong or (call_vars[i] != func_called.vars[0][i]))
                print("WRONG = " + str(wrong))

        if wrong:
            return expectedGot(func_name, call_vars, func_args)
        return None;

    def checkSemantics(self, printer, var_list, mod_funcs) -> List[str]:
        from . import CodeScope
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Call.checkSemantics() 'printer' should be 'ErrorPrinter'"
            assert isinstance(var_list, list), "Call.checkSemantics() 'var_list' should be 'list'"
            assert isinstance(mod_funcs, dict), "Call.checkSemantics() 'mod_funcs' should be 'dict'"

        errors = []

        func_name = self.calls[0]
        func_called = None
        func_exists = False
        mod_call = len(self.calls) is 2

        #Check if function exists
        if not mod_call:
            if func_name not in mod_funcs:
                errors.append("Function '" + func_name + "' not defined!")
            else:
                func_called = mod_funcs[func_name]
                func_exists = True
                print("Found function = " + str(func_called))

        call_vars = []
        for arg_name in self.args:
            arg = getVar(arg_name, var_list)
            if arg is not None:
                call_vars.append(arg)
            else:
                errors.append("Variable '" + arg_name + "' not defined!")
                call_vars.append(UndefinedVariable())

        if func_exists:
            msg = self.__checkArguments(func_name, func_called, call_vars)
            if msg is not None:
                errors.append(msg)

        return errors

class ExprTest:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.ExprtestContext), "ExprTest.__init__() 'node' should be 'yalParser.ExprtestContext'"

        self.op = node.children[1]
        self.left = LeftOP(node.children[0])
        self.right = RightOP(node.children[2])

class LeftOP:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.Left_opContext), "LeftOP.__init__() 'node' should be 'yalParser.Left_opContext'"

        child = node.children[0]
        if (isinstance(child, yalParser.Array_accessContext)):
            self.access = ArrayAccess(child)
        elif (isinstance(child, yalParser.Scalar_accessContext)):
            self.access = ScalarAccess(child)
        else:
            print("WUUUUUUUUUUUTTTTTT??????!!!!!!!");

class RightOP:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.Right_opContext), "RightOP.__init__() 'node' should be 'yalParser.Right_opContext'"

        self.value = {}

        if isinstance(node.children[0], tree.Tree.TerminalNodeImpl):
            self.value[0] = ArraySize(node.children[1])
            self.needs_op = False
            self.arr_size = True
        elif node.getChildCount() is 1: #Only term
            self.value[0] = Term(node.children[0])
            self.needs_op = False
            self.arr_size = False
        else:
            self.value[0] = Term(node.children[0])
            self.operator = node.children[1]
            self.value[1] = Term(node.children[0])
            self.needs_op = True
            self.arr_size = False

    def resultType(self) -> str:
        if self.arr_size: #TODO need to check function return
            return "ARR"
        else:
            return "NUM"

class Assign:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.AssignContext), "Assign.__init__() 'node' should be 'yalParser.AssignContext'"

        self.left = LeftOP(node.children[0])
        self.right = RightOP(node.children[1])

    def getVarInfo(self):
        return (self.left.access.var, self.left.access);

    def isAssignArray(self):
        return self.right.arr_size;

    def checkSemantics(self, printer, var_list: list) -> list:
        pass

class ArrayAccess:
    def __init__(self, node: yalParser.Array_accessContext):
        if __debug__:
            assert isinstance(node, yalParser.Array_accessContext), "ArrayAccess.__init__() 'node' should be 'yalParser.Array_accessContext'"

        self.var = str(node.children[0])
        self.index = str(node.children[1])

    def indexAccess(self):
        return self.index

class ScalarAccess:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.Scalar_accessContext), "ScalarAccess.__init__() 'node' should be 'yalParser.Scalar_accessContext'"

        self.var = str(node.children[0])
        self.size = (len(node.children) is 2)

    def indexAccess(self):
        return None



class ArraySize:
    def __init__(self, node):
        if __debug__:
            assert isinstance(node, yalParser.Array_sizeContext), "ArraySize.__init__() 'node' should be 'yalParser.Array_sizeContext'"

        if ArraySize.isDigit(node):
            self.value = int(str(node.children[0]))
            self.access = False
        else: #Scalar access
            self.value = ScalarAccess(node)
            self.access = True

    def isDigit(node: yalParser.Array_sizeContext):
        return str(node.children[0]).isdigit();

class Term:
    def __init__(self, node: yalParser.TermContext):
        if __debug__:
            assert isinstance(node, yalParser.TermContext), "Term.__init__() 'node' should be 'yalParser.TermContext'"

        base = 0
        if isinstance(node, tree.Tree.TerminalNodeImpl):
            return;

        if str(node.children[0]) == '+' or str(node.children[0]) == '-':
            base = 1

        self.positive = (str(node.children[0]) is not "-")
        child = node.children[base]


        if isinstance(child, yalParser.CallContext):
            self.value = Call(child.children[0], child.children[1])
        elif isinstance(child, yalParser.Array_accessContext):
            self.value = ArrayAccess(child)
        elif isinstance(child, yalParser.Scalar_accessContext):
            self.value = ScalarAccess(child)
        elif isinstance(child, tree.Tree.TerminalNodeImpl):
            self.value = int(str(child))
        else:
            print("HMMMMMMMMMMMMM?!!?!")
