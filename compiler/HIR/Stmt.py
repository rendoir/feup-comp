from antlr4 import ParserRuleContext, tree
from antlr_yal import yalParser
from pprint import pprint
from typing import List
from compiler.HIR.Variable import Variable, ArrayVariable, NumberVariable, UndefinedVariable, BranchedVariable
from compiler.Printer import ErrorPrinter
from .CodeScope import Scope
from ..LIR import Instruction


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
        if isinstance(var_list, dict):
            if var_name in var_list:
                return var_list[var_name]
        else:
            for var in var_list:
                if var_name == var.name:
                    return var

    if not Variable.isLiteral(var_name):
        return None
    else:
        return var_name

def varScope(var_name, vars_list) -> str:
    for i in range(len(vars_list)):
        var_list = vars_list[i]

        if isinstance(var_list, dict):
            if var_name in var_list:
                if (i + 1) >= len(vars_list):
                    return 'F'
                else:
                    return 'L'


        else:
            for var in var_list:
                if var_name == var.name:
                    return 'P'

class Statement:
    def __init__(self, node, parent):
        if __debug__:
            assert isinstance(node, ParserRuleContext), "Statement.__init__() 'node'\n - Expected 'ParserRuleContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "Statement.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(mod_funcs))

        self.parent = parent
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

        self.funcs = Scope.getFuncs(parent)
        self.calls = []
        for child in node.children[0]:
            self.calls.append(str(child))

        self.args = []

        if len(node.children) is 2:
            for arg in node.children[1].children:
                self.args.append(str(arg))


    def __str__(self) -> str:
        ret = ""
        for call in self.calls:
            ret += str(call) + "."
        ret = ret[:-1]
        ret += "("
        remove = False
        for arg in self.args:
            remove = True
            ret += arg + ", "
        if remove:
            ret = ret[:-2]

        ret += ")"
        return ret

    def __checkArguments(self, printer, func_name, func_called, call_vars):
        from . import CodeScope
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Call.__checkArguments() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(func_name, str), "Call.__checkArguments() 'func_name'\n - Expected 'str'\n - Got: " + str(type(func_name))
            assert isinstance(func_called, CodeScope.Function), "Call.__checkArguments() 'func_called'\n - Expected 'CodeScope.Function'\n - Got: " + str(type(func_called))
            assert isinstance(call_vars, list), "Call.__checkArguments() 'call_vars'\n - Expected 'list'\n - Got: " + str(type(call_vars))

        func_args = func_called.vars[0]
        wrong = False

        if len(call_vars) is len(func_called.vars[0]):
            for i in range(len(call_vars)):
                if not Variable.isLiteral(str(call_vars[i])):
                    diff_types = (call_vars[i].diffType(func_args[i]))
                    wrong = wrong or diff_types
                    self.args[i] = call_vars[i]


        if wrong:
            return printer.wrongArgs(self.line, self.cols, func_name, func_args, call_vars)

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Call.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Call.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        func_name = str(self.calls[-1])
        func_called = None
        func_exists = False
        mod_call = len(self.calls) is 2

        #Check if function exists
        if not mod_call:
            if func_name not in self.funcs:
                printer.undefFunc(self.line, self.cols, func_name)
            else:
                func_called = self.funcs[func_name]
                func_exists = True


        call_vars = []
        for arg_name in self.args:
            arg = getVar(arg_name, var_list)
            if arg is not None:
                call_vars.append(arg)
            else:
                if Scope.isBranchVar(self.parent, str(arg_name)):
                    printer.branchingDecl(self.line, self.cols, str(arg_name))
                    self.parent.debranchVar(str(arg_name))
                else:
                    printer.undefVar(self.line, self.cols, str(arg_name))
                    call_vars.append(UndefinedVariable())

        if func_exists:
            self.__checkArguments(printer, func_name, func_called, call_vars)
        elif mod_call:
            self.args = call_vars


    def returnType(self) -> str:
        if len(self.calls) is 1:
            func = self.funcs[str(self.calls[0])]
            return func.ret_str
        else:
            return "???"


class ExprTest(Statement):
    def __init__(self, node, parent):
        super(ExprTest, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.ExprtestContext), "ExprTest.__init__() 'node'\n - Expected 'yalParser.ExprtestContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ExprTest.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))

        self.op = str(node.children[1])
        self.left = LeftOP(node.children[0], parent)
        self.right = RightOP(node.children[2], parent)

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ExprTest.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ExprTest.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.left.checkSemantics(printer, var_list, True)
        self.right.checkSemantics(printer, var_list)

        is_arr = self.left.isArr(var_list)
        right_type = self.right.getType(var_list)
        if right_type is None:
            printer.opDiffTypes(self.line, self.cold, ('ARR' if is_arr else 'NUM'), self.op, '???')
        else:
            if is_arr and right_type == 'ARR':
                printer.unknownComp(self.line, self.cols, self.left.access.var, str(self.op), self.right.value[0].value.var)
            elif (not is_arr and right_type == 'ARR') or (is_arr and right_type == 'NUM'):
                printer.opDiffTypes(self.line, self.cols, ('ARR' if is_arr else 'NUM'), self.op, right_type)


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
            raise StandardError("LeftOP access neither Array nor Scalar!");

    def checkSemantics(self, printer, var_list, report_existance):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "LeftOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "LeftOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))
            assert isinstance(report_existance, bool), "LeftOP.checkSemantics() 'report_existance'\n - Expected 'bool'\n - Got: " + str(type(report_existance))

        self.access.checkSemantics(printer, var_list, report_existance)

    def isArrAccess(self) -> bool:
        return isinstance(self.access, ArrayAccess)

    def isArrSize(self) -> bool:
        return isinstance(self.access, ScalarAccess) and self.access.size

    def isArr(self, var_list) -> bool:
        if isinstance(self.access, ScalarAccess) and not self.access.size:
            var = getVar(self.access.var, var_list)
            return isinstance(var, ArrayVariable)

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
            self.value.append(Term(node.children[2], parent))
            self.needs_op = True
            self.arr_size = False

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "RightOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "RightOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        for term in self.value:
            term.checkSemantics(printer, var_list)

        if self.needs_op:
            type1 = self.value[0].getType(var_list)
            type2 = self.value[1].getType(var_list)
            if type1 == 'ARR' and type2 == 'ARR':
                printer.unknownOp(self.line, self.cols, self.value[0].getVarName(), self.operator, self.value[1].getVarName())

            elif type1 != type2 and type1 != "???" and type2 != '???':
                printer.opDiffTypes(self.line, self.cols, type1, self.operator, type2)

    def isArr(self, var_list) -> bool:
        return len(self.value) is 1 and self.value[0].isArray(var_list)

    def getType(self, var_list) -> str:
        if __debug__:
            assert isinstance(var_list, list), "RightOP.getType() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if self.arr_size:
            return 'ARR'
        elif not self.needs_op:
            return self.value[0].getType(var_list)
        else:
            type1 = self.value[0].getType(var_list)
            type2 = self.value[1].getType(var_list)
            if type1 == 'NUM' and type2 == 'NUM':
                return 'NUM'
            else:
                return '???'

    def getArrSize(self, var_list) -> int:
        if __debug__:
            assert isinstance(var_list, list), "RightOP.getArrSize() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if self.arr_size:
            return self.value[0].getValue(var_list)
        else:
            return -1


    def __str__(self) -> str:
        if self.needs_op:
            return str(self.value[0]) + " " + self.operator + " " + str(self.value[1])
        else:
            return str(self.value[0])



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

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Assign.checkSemantics() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Assign.checkSemantics() 'var_list'\n - Expected: 'list'\n - Got: " + str(type(var_list))

        self.left.checkSemantics(printer, var_list, False)
        self.right.checkSemantics(printer, var_list)
        (var_name, var_info) = self.getVarInfo()
        var = getVar(var_name, var_list)

        if var is not None:
            right_type = self.right.getType(var_list)
            if self.left.isArrSize(): #Check if it is a .size assignment
                printer.sizeAssign(self.line, self.cols, self.left.access.var, str(self.right))
            elif Variable.differentType(right_type, var.type) and var.type != 'ARR': # Check for different types
                print("RIGHT = " + str(right_type) + ", LEFT = " + var.type)
                printer.diffTypes(self.line, self.cols, var.name, var.type, right_type)
            else:
                var.line_init = (self.line, self.cols[0])
        else:
            var_obj = None
            # TODO add array size and number value

            right_type = self.right.getType(var_list)
            if right_type == 'ARR' or right_type is None:
                arr_size = self.right.getArrSize(var_list)
                var_obj = ArrayVariable(var_name, arr_size, (self.line, self.cols[0]), (self.line, self.cols[0]))
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
        self.index = str(node.children[1].children[0])

    def checkSemantics(self, printer, var_list, report_existance=True):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ArrayAccess.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ArrayAccess.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))
            assert isinstance(report_existance, bool), "ArrayAccess.checkSemantics() 'report_existance'\n - Expected 'bool'\n - Got: " + str(type(report_existance))

        if not self.index.isdigit():
            index_var = getVar(self.index, var_list)
            if index_var is not None:
                if not isinstance(index_var, NumberVariable):
                    printer.arrSizeNaN(self.line, self.cols, var.type)
            else:
                if Scope.isBranchVar(self.parent, self.index):
                    printer.branchingDecl(self.line, self.cols, self.index)
                    self.parent.debranchVar(self.index)
                else:
                    printer.undefVar(self.line, self.cols, self.index)

        var = getVar(self.var, var_list)
        if var is not None:
            if not isinstance(var, ArrayVariable):
                printer.numberIndexing(self.line, self.cols, var.name, var.type)
            elif self.index.isdigit() and not var.validAccess(int(self.index)):
                printer.outOfBounds(self.line, self.cols, var.name, var.size, self.index)

        elif report_existance:
            if Scope.isBranchVar(self.parent, self.var):
                printer.branchingDecl(self.line, self.cols, self.var)
                self.parent.debranchVar(self.var)
            else:
                printer.undefVar(self.line, self.cols, self.var)

    def __str__(self) -> str:
        return self.var + "[" + self.index + "]"


class ScalarAccess(Statement):
    def __init__(self, node, parent):
        super(ScalarAccess, self).__init__(node, parent)
        if __debug__:
            assert isinstance(node, yalParser.Scalar_accessContext), "ScalarAccess.__init__() 'node'\n - Expected 'yalParser.Scalar_accessContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "ScalarAccess.__init__() 'parent'\n - Expected 'Scope'\n - Got: " + str(type(parent))


        self.var = str(node.children[0])
        self.size = (len(node.children) is 2)

    def __str__(self) -> str:
        if self.size:
            return self.var + ".size"
        else:
            return self.var

    def indexAccess(self):
        return None

    def checkSemantics(self, printer, var_list, report_existance=True):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "ScalarAccess.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "ScalarAccess.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))
            assert isinstance(report_existance, bool), "ScalarAccess.checkSemantics() 'report_existance'\n - Expected 'bool'\n - Got: " + str(type(report_existance))

        var = getVar(self.var, var_list)

        if var is not None:
            if not var.initialized() and report_existance:
                print("Init = " + str(var))
                if isinstance(var, BranchedVariable):
                    printer.branchingVars(self.line, self.cols, self.var, var.type1, var.type2)
                    var.wasReported()
                else:
                    printer.notInitialized(self.line, self.cols, self.var)

            elif self.size and not isinstance(var, ArrayVariable):
                printer.numSize(self.line, self.cols, var.name, var.type)

        elif report_existance:
            if Scope.isBranchVar(self.parent, self.var):
                printer.branchingDecl(self.line, self.cols, self.var)
                self.parent.debranchVar(self.var)
            else:
                printer.undefVar(self.line, self.cols, self.var)
                self.parent.addVar(self.var, UndefinedVariable())

    def getValue(self, var_list) -> int:
        if __debug__:
            assert isinstance(var_list, list), "ScalarAccess.getValue() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        var = getVar(self.var, var_list)
        if self.size:
            if isinstance(var, ArrayVariable):
                return var.size
            else:
                return -1
        else:
            if isinstance(var, NumberVariable):
                return var.value
            else:
                return -1

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
            self.value = ScalarAccess(node.children[0], parent)
            self.access = True

    def __str__(self) -> str:
        return "[" + str(self.value) + "]"

    def isDigit(node: yalParser.Array_sizeContext):
        return str(node.children[0]).isdigit();

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "RightOP.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "RightOP.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if self.access:
            self.value.checkSemantics(printer, var_list, True)
        elif self.value < 0:
            printer.negSize(self.line, self.cols, self.value)

    def getVarName(self):
        if self.access:
            return self.value.var
        else:
            return self.value

    def getValue(self, var_list) -> int:
        if self.access:
            return self.value.getValue(var_list)
        else:
            return self.value

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

    def __str__(self) -> str:
        if isinstance(self.value, int):
            return str(self.value)
        else:
            return str(self.value)

    def getType(self, var_list) -> str:
        if isinstance(self.value, Call):
            return self.value.returnType()
        elif isinstance(self.value, ArrayAccess):
            return "NUM"
        elif isinstance(self.value, ScalarAccess):
            var = getVar(self.value.var, var_list)
            if self.value.size:
                return "NUM"
            else:
                return var.type
        else:
            return 'NUM'

    def isSize(self) -> bool:
        if isinstance(self.value, ScalarAccess):
            return self.value.size
        return False

    def isArray(self, var_list) -> bool:
        if isinstance(self.value, ScalarAccess) and not self.value.size:
            var = getVar(self.value.var, var_list)
            if var is not None:
                return isinstance(var, ArrayVariable)
            else: # Due to error propagation
                return False

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Term.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "Term.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        if not isinstance(self.value, int):
            self.value.checkSemantics(printer, var_list)

    def getVarName(self) -> str:
        if isinstance(self.value, ArrayAccess) or isinstance(self.value, ScalarAccess):
            return self.value.var
