from .Variable import Variable, NumberVariable, ArrayVariable
from compiler.Printer import ErrorPrinter
from antlr4 import tree
from antlr_yal import *
from typing import List
from pprint import pprint

def checkVar(var_name, is_array, defined_vars) -> str:
    if __debug__:
        assert isinstance(var_name, str), "CodeSCope.checkVar() 'var_name'\n - Expected: 'str'\n - Got:" + str(type(var_name))
        assert isinstance(is_array, bool), "CodeScope.checkVar() 'is_array'\n - Expected: 'bool'\n - Got:" + str(type(is_array))
        assert isinstance(defined_vars, list), "CodeSCope.checkVar() 'defined_vars'\n - Expected: 'list'\n - Got:" + str(type(defined_vars))

    for vars in defined_vars:
        if var_name in vars:
            also_array = isinstance(vars[var_name], ArrayVariable)
            if is_array != also_array:
                return "Variable '" + var_name + "' defined, but tried using as different type"
            else:
                return None

    return "Variable '" + var_name + "' is not defined!"

class Scope:
    def __init__(self, parent):
        if __debug__:
            assert isinstance(parent, Scope), "Scope.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.vars = {}
        self.code = []
        self.parent = parent

    def addVar(self, name, var):
        raise NotImplementedError( "Should have implemented this" )

    def getFunctions(scope) -> dict:
        if __debug__:
            assert isinstance(scope, Scope) or scope is None, "Scope.getFunctions() 'scope'\n - Expected: 'Scope'\n - Got: " + str(type(ret_var))

        parent = scope.parent
        while parent.parent is not None:
            parent = parent.parent

        return parent.code

    def getVars(self) -> list:
        raise NotImplementedError("Should have implemented Scope::getVars()")

    def getVars(scope) -> list:
        if __debug__:
            assert isinstance(scope, Scope) or scope is None, "Scope.getVars() 'scope'\n - Expected: 'Scope'\n - Got: " + str(type(ret_var))

        ret = []
        temp = scope
        while temp.parent is not None:
            for vars in temp.getVars():
                ret.insert(-1, vars)
            temp = temp.parent

        ret.insert(-1, temp.getVars())
        return ret


# 20 maças, cortar laminadas ++ fino, marshmallows 1 por cada pessoa (+- 100), espeto para por marshmallows (dar para pelos menos 15),

class Function(Scope):
    def __init__(self, ret_var, args , stmts , parent):
        if __debug__:
            assert isinstance(ret_var, str) or ret_var is None, "Function.__init__() 'ret_var'\n - Expected: 'str'\n - Got: " + str(type(ret_var))
            assert isinstance(args, yalParser.Var_listContext) or args is None, "Function.__init__() 'args'\n - Expected: 'yalParser.Var_listContext'\n - Got: " + str(type(args))
            assert isinstance(stmts, yalParser.Stmt_listContext), "Function.__init__() 'stmts'\n - Expected: 'yalParser.Stmt_listContext'\n - Got: " + str(type(stmts))
            assert isinstance(parent, Scope), "Function.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.ret_var = ret_var
        self.ret_is_arr = False
        self.vars = [[], dict()] #[<arguments>, <local_variables>]
        self.code = []
        self.parent = parent
        if args is not None:
            self.__addArgs(args)

        if stmts is not None:
            self.__addStmts(stmts.children)

    def addVar(self, name, var):
        if __debug__:
            assert isinstance(name, str), "Function.addVar() 'name'\n - Expected: 'str'\n - Got: " + str(type(name))
            assert isinstance(var, Variable), "Function.addVar() 'var'\n - Expected: 'Variable'\n - Got: " + str(type(var))

        self.vars[1][name] = var

    def getVars(self) -> list:
        return [self.vars[1], self.vars[0]]

    def __addArgs(self, args):
        if __debug__:
            assert isinstance(args, yalParser.Var_listContext), "Function.__addArgs() 'args'\n - Expected: 'yalParser.Var_listContext'\n - Got: " + str(type(args))

        children = args.getChildren()
        for child in children:
            if isinstance(child, yalParser.Array_elementContext):
                self.vars[0].append(ArrayVariable(str(child.children[0]), None, 0, 0))
            else:
                self.vars[0].append(NumberVariable(str(child.children[0]), None, 0, 0))


    def __addStmts(self, stmts: List[yalParser.Stmt_listContext]):
        from . import Stmt
        if __debug__:
            assert isinstance(stmts, list), "Function.__addStmts() 'stmts'\n - Expected: 'list'\n - Got: " + str(type(stmts))

        for stmt in stmts:
            self.code.append(Stmt.parseStmt(stmt, self))

    def __str__(self) -> str:
        string = "("
        for arg in self.vars[0]:
            string += str(arg) + ", "

        if len(string) > 2:
            string = string[:-2]

        string += ")\n"
        return string

    def checkVariables(self, printer):
        from . import Stmt
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Function.checkVariables() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        for code_chunk in self.code:
            var_list = [self.vars[1], self.vars[0], self.parent.vars]
            code_chunk.checkSemantics(printer, var_list)

    def __checkAssign(self, printer, assign, var_lists) -> list:
        from . import Stmt
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Function.__checkAssign() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(assign, Stmt.Assign), "Function.__checkAssign() 'assign'\n - Expected: 'Stmt.Assign'\n - Got: " + str(type(assign))
            assert isinstance(var_lists, list), "Function.__checkAssign() 'var_lists'\n - Expected: 'list'\n - Got: " + str(type(var_lists))

        (var_name, var_info) = assign.getVarInfo()
        exists = False;
        indexing = var_info.indexAccess();


        for var_list in var_lists:
            if var_name in var_list: #Check var type matches
                exists = True
                var = var_list[var_name]
                assign_type = assign.right.resultType()
                if assign_type != var.type:
                    return ["Assigned wrong type to variable '{}'\n  Expected '{}', got '{}'".format(var_name, var.type, assign_type)]

        if not exists:
            var_obj = None
            is_array = assign.isAssignArray()
            print("Adding var '{}', is_arr '{}'".format(var_name, is_array))
            if is_array:
                var_obj = ArrayVariable(var_name, 0, 0, 0)
            else:
                var_obj = NumberVariable(var_name, 0, 0, 0)
            self.vars[1][var_name] = var_obj

        return []


class If(Scope):
    def __init__(self, node, parent):
        if __debug__:
            assert isinstance(node, yalParser.If_yalContext), "If.__init__() 'node'\n - Expected: 'yalParser.If_yalContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "If.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.parent = parent
        self.test = ExprTest(node.children[0])
        self.vars = dict()
        self.code = []
        stmts = node.children[1]
        for stmt in stmts.children:
            self.code.append(parseStmt(stmt, self))

        self.else_code = []
        if node.getChildCount() is 3:
            for stmt in node.children[2].children:
                self.else_code.append(parseStmt(stmt, self))

    def addVar(self, name, var):
        if __debug__:
            assert isinstance(name, str), "If.addVar() 'name'\n - Expected: 'str'\n - Got: " + str(type(name))
            assert isinstance(var, Variable), "If.addVar() 'var'\n - Expected: 'Variable'\n - Got: " + str(type(var))

        self.vars[name] = var

    def getVars(self) -> list:
        return [self.vars]

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "If.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "If.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.test.checkSemantics(printer, var_list)
        vars = Scope.getVars(self)
        for code_line in self.body:
            code_line.checkSemantics(printer, vars)

class While(Scope):
    def __init__(self, node, parent):
        from . import Stmt
        if __debug__:
            assert isinstance(node, yalParser.While_yalContext), "While.__init__() 'node'\n - Expected: 'yalParser.While_yalContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "While.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.line = node.getLine()
        self.cols = node.getColRange()
        self.parent = parent
        self.test = Stmt.ExprTest(node.children[0], parent)
        self.body = []
        self.vars = dict()
        for stmt in node.children[1].children:
            self.body.append(Stmt.parseStmt(stmt, self))

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "While.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "While.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.test.checkSemantics(printer, var_list)
        vars = Scope.getVars(self)
        for code_line in self.body:
            code_line.checkSemantics(printer, vars)

    def addVar(self, name, var):
        if __debug__:
            assert isinstance(name, str), "While.addVar() 'name'\n - Expected: 'str'\n - Got: " + str(type(name))
            assert isinstance(var, Variable), "While.addVar() 'var'\n - Expected: 'Variable'\n - Got: " + str(type(var))

        self.vars[name] = var

    def getVars(self) -> list:
        return [self.vars]

class Module(Scope):
    def __init__(self):
        self.vars = dict()
        self.code = dict()
        self.parent = None
        self.name = None

    def getVars(self) -> list:
        return [self.vars]

    def parseTree(self, tree, printer) -> str:
        if __debug__:
            assert isinstance(tree, ParserRuleContext), "Module.parseTree() 'tree'\n - Expected: 'ParserRuleContext'\n - Got: " + str(type(tree))
            assert isinstance(printer, ErrorPrinter), "Module.parseTree() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        children = tree.getChildren()
        for child in children:
            if child is not None:
                ret = None
                if isinstance(child, yalParser.DeclarationContext):
                    (name, info) = self.__parseDeclaration(child)
                    if not self.__addVariable(name, info):
                        self.__addVarError(child, printer)
                elif isinstance(child, yalParser.FunctionContext):
                    (name, info) = self.__parseFunction(child)
                    if not self.__addFunction(name, info):
                        self.__addFuncError(child, printer)

                else:
                    self.name = str(child);

                if ret is not None:
                    return ret

    # Returns tuple with (<var_name>, <variable_instance>)
    # Need to check if var_name already exists!
    def __parseDeclaration(self, node) -> (str,Variable):
        if __debug__:
            assert isinstance(node, yalParser.DeclarationContext), "Module.__parseDeclaration() 'node'\n - Expected: 'yalParser.DeclarationContext'\n - Got: " + str(type(node))

        if node is None:
            return;
        only_name = len(node.children) is 1

        # TODO check what happens when node.children[0] is a array_element
        var_name = str(node.children[0].children[0])

        if only_name: # Only variable name
            return (var_name, NumberVariable(var_name, None, 0, 0))
        elif isinstance(node.children[1], int): # Constant declaration?
            return (var_name, NumberVariable(var_name, node.children[1], 0, 0))
        else:
            # If node.children[1] is a scalar access check if it is valid
            # TODO whats up here
            return (var_name, ArrayVariable(var_name, 0, 0, 0))

    def __parseFunction(self, node) -> (str, Function):
        if __debug__:
            assert isinstance(node, yalParser.FunctionContext), "Module.__parseFunction() 'node'\n - Expected: 'yalParser.FunctionContext'\n - Got: " + str(type(node))

        func_name = str(node.children[0])
        vars = None
        ret_var = None
        stmts = node.children[-1]

        if isinstance(node.children[1], tree.Tree.TerminalNodeImpl): # Check if function has a return variable
            ret_var = str(node.children[0])
            func_name = str(node.children[1])

        if not isinstance(node.children[-2], tree.Tree.TerminalNodeImpl): # Check if function has arguments
            vars = node.children[-2]

        return (func_name, Function(ret_var, vars, stmts, self))


    def semanticCheck(self, printer):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Module.semanticCheck() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        for name, func in self.code.items():
            func.checkVariables(printer)

        printer.printMessages()

    def __addVariable(self, var_name, var_info) -> bool:
        if __debug__:
            assert isinstance(var_name, str), "Module.__addVariable() 'var_name'\n - Expected: 'str'\n - Got: " + str(type(var_name))
            assert isinstance(var_info, Variable), "Module.__addVariable() 'var_info'\n - Expected: 'Variable'\n - Got: " + str(type(var_info))

        if var_name in self.vars:
            return False

        self.vars[var_name] = var_info
        return True

    def __addFunction(self, func_name, func_info) -> bool:
        if __debug__:
            assert isinstance(func_name, str), "Module.__addFunction() 'func_name'\n - Expected: 'str'\n - Got: " + str(type(func_name))
            assert isinstance(func_info, Function), "Module.__addFunction() 'func_info'\n - Expected: 'Function'\n - Got: " + str(type(func_info))

        if func_name in self.code:
            return False

        print("Adding '" + func_name + "', info = " + str(func_info))
        self.code[func_name] = func_info
        return True

    def __addVarError(self, var, printer):
        if __debug__:
            assert isinstance(var, yalParser.DeclarationContext), "Module.__addVarError() 'var'\n - Expected: 'yalParser.DeclarationContext'\n - Got: " + str(type(var))
            assert isinstance(printer, ErrorPrinter), "Module.__addVarError() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        printer.addError(var.getLine(), var.getColRange(), "Variable redeclared", "Variable " + str(var.children[0]) + " redeclared!")


    def __addFuncError(self, func, printer):
        if __debug__:
            assert isinstance(func, yalParser.FunctionContext), "Module.__addFuncError() 'func'\n - Expected: 'yalParser.FunctionContext'\n - Got: " + str(type(func))
            assert isinstance(printer, ErrorPrinter), "Module.__addFuncError() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        if isinstance(func.children[0], str) and isinstance(func.children[1], str):
            printer.addError(func.children[1].getLine(), func.children[1].getColRange(), "Function redeclared", "Function " + str(func.children[1]) + " redeclared!")
        else:
            printer.addError(func.children[0].getLine(), func.children[0].getColRange(), "Function redeclared", "Function " + str(func.children[0]) + " redeclared!")

    def __str__(self) -> str:
        string = "Module '" + self.name + "':\n"
        string += " Members:\n"
        for name, var in self.vars.items():
            string += "  " + str(var) + "\n"

        string += " Functions:\n"
        for name, func in self.code.items():
            string += "  " + name + str(func)

        return string
