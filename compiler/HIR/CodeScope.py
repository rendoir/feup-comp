from .Variable import Variable, NumberVariable, ArrayVariable, UndefinedVariable
from compiler.Printer import ErrorPrinter
from antlr4 import tree
from antlr_yal import *
from typing import List
from pprint import pprint

class Scope:
    def __init__(self, parent):
        if __debug__:
            assert isinstance(parent, Scope), "Scope.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.vars = {}
        self.code = []
        self.branched_vars = {}
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

    def getFuncs(scope) -> dict:
        if __debug__:
            assert isinstance(scope, Scope) or scope is None, "Scope.getVars() 'scope'\n - Expected: 'Scope'\n - Got: " + str(type(ret_var))

        temp = scope
        while temp.parent is not None:
            temp = temp.parent

        return temp.code


# 20 maças, cortar laminadas ++ fino, marshmallows 1 por cada pessoa (+- 100), espeto para por marshmallows (dar para pelos menos 15),

class Function(Scope):
    def __init__(self, ret_var, args , stmts , parent):
        super(Function, self).__init__(parent)
        if __debug__:
            assert isinstance(ret_var, ParserRuleContext) or ret_var is None, "Function.__init__() 'ret_var'\n - Expected: 'ParserRuleContext'\n - Got: " + str(type(ret_var))
            assert isinstance(args, yalParser.Var_listContext) or args is None, "Function.__init__() 'args'\n - Expected: 'yalParser.Var_listContext'\n - Got: " + str(type(args))
            assert isinstance(stmts, yalParser.Stmt_listContext), "Function.__init__() 'stmts'\n - Expected: 'yalParser.Stmt_listContext'\n - Got: " + str(type(stmts))
            assert isinstance(parent, Scope), "Function.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.vars = [[], dict()] #[<arguments>, <local_variables>]
        if ret_var is not None:
            self.ret_var = ret_var.children[0]
            self.ret_is_arr = isinstance(ret_var, yalParser.Array_elementContext)
            self.vars[1][self.ret_var] = (ArrayVariable(self.ret_var, None, 0, None) if self.ret_is_arr else NumberVariable(self.ret_var, None, 0, None))
        else:
            self.ret_var = None

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

    def checkSemantics(self, printer):
        from . import Stmt
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Function.checkSemantics() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        for code_chunk in self.code:
            var_list = [self.vars[1], self.vars[0], self.parent.vars]
            code_chunk.checkSemantics(printer, var_list)

class If(Scope):
    def __init__(self, node, parent):
        from . import Stmt
        super(If, self).__init__(parent)
        if __debug__:
            assert isinstance(node, yalParser.If_yalContext), "If.__init__() 'node'\n - Expected: 'yalParser.If_yalContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "If.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.line = node.getLine()
        self.cols = node.getColRange()
        self.checking_else = False
        self.test = Stmt.ExprTest(node.children[0], self)
        self.else_code = []

        for stmt in node.children[1].children:
            self.code.append(Stmt.parseStmt(stmt, self))

        if node.getChildCount() is 3:
            for stmt in node.children[2].children[0].children:
                self.else_code.append(Stmt.parseStmt(stmt, self))

    def addVar(self, name, var):
        if __debug__:
            assert isinstance(name, str), "If.addVar() 'name'\n - Expected: 'str'\n - Got: " + str(type(name))
            assert isinstance(var, Variable), "If.addVar() 'var'\n - Expected: 'Variable'\n - Got: " + str(type(var))

        if name in self.vars:
            existing_var = self.vars[name]
            print("Checking else = " + str(self.checking_else))
            if self.checking_else:
                if not existing_var.type != var.type:
                    if existing_var.type == 'ARR':
                        var_obj = ArrayVariable(name, (-1 if existing_var.size != var.size else var.size), (self.line, self.cols[0]), (self.line, self.cols[0]))
                    else:
                        var_obj = NumberVariable(name, (-1 if existing_var.value != var.value else var.value), (self.line, self.cols[0]), (self.line, self.cols[0]))

                    self.parent.addVar(name, var_obj)
                else:
                    self.parent.branched_vars[name] = UndefinedVariable(name, None, None, None)
                    print("'" + name + "' in both branches but different types :-(")

        else:
            self.vars[name] = var

    def getVars(self) -> list:
        return [self.vars]

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "If.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "If.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.test.checkSemantics(printer, var_list)

        for code_line in self.code:
            code_line.checkSemantics(printer, var_list + [self.vars])

        self.checking_else = True
        for code_line in self.else_code:
            code_line.checkSemantics(printer, var_list + [{}])

class While(Scope):
    def __init__(self, node, parent):
        from . import Stmt
        super(While, self).__init__(parent)
        if __debug__:
            assert isinstance(node, yalParser.While_yalContext), "While.__init__() 'node'\n - Expected: 'yalParser.While_yalContext'\n - Got: " + str(type(node))
            assert isinstance(parent, Scope), "While.__init__() 'parent'\n - Expected: 'Scope'\n - Got: " + str(type(parent))

        self.line = node.getLine()
        self.cols = node.getColRange()
        self.test = Stmt.ExprTest(node.children[0], parent)
        for stmt in node.children[1].children:
            self.code.append(Stmt.parseStmt(stmt, self))

    def checkSemantics(self, printer, var_list):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "While.checkSemantics() 'printer'\n - Expected 'ErrorPrinter'\n - Got: " + str(type(printer))
            assert isinstance(var_list, list), "While.checkSemantics() 'var_list'\n - Expected 'list'\n - Got: " + str(type(var_list))

        self.test.checkSemantics(printer, var_list)
        vars = Scope.getVars(self)
        for code_line in self.code:
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
        return self.vars

    def parseTree(self, tree, printer) -> str:
        if __debug__:
            assert isinstance(tree, ParserRuleContext), "Module.parseTree() 'tree'\n - Expected: 'ParserRuleContext'\n - Got: " + str(type(tree))
            assert isinstance(printer, ErrorPrinter), "Module.parseTree() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        children = tree.getChildren()
        for child in children:
            if child is not None:
                ret = None
                if isinstance(child, yalParser.DeclarationContext):
                    (name, info) = self.__parseDeclaration(child, printer)
                    self.__addVariable(name, info)
                elif isinstance(child, yalParser.FunctionContext):
                    (name, info) = self.__parseFunction(child)
                    if not self.__addFunction(name, info):
                        self.__addFuncError(child, printer)

                else:
                    self.name = str(child);

                if ret is not None:
                    return ret

    # TODO omg this function smells soooo baaaddd
    def __parseDeclaration(self, node, printer) -> (str,Variable):
        from .Stmt import ScalarAccess
        if __debug__:
            assert isinstance(node, yalParser.DeclarationContext), "Module.__parseDeclaration() 'node'\n - Expected: 'yalParser.DeclarationContext'\n - Got: " + str(type(node))

        var_name = str(node.children[0].children[0])
        only_name = len(node.children) is 1
        line = node.getLine()
        cols = node.getColRange()
        var = None

        if var_name in self.vars:
            var = self.vars[var_name]

        if only_name: # Only variable name
            if var is not None:
                printer.alreadyDefined(line, cols, var_name)

            return (var_name, NumberVariable(var_name, None, (line, cols[0]), None))

        elif str(node.children[1]).isdigit(): # Constant declaration?
            if var is not None and not isinstance(var, NumberVariable):
                printer.diffTypes(line, cols, var.name, var.type, "NUM")

            value = int(str(node.children[1]))
            return (var_name, NumberVariable(var_name, value, (line, cols[0]), (line, cols[0])))

        else:
            arr_size = node.children[1].children[0]
            if not isinstance(var, ArrayVariable) and var is not None:
                printer.diffTypes(line, cols, var.name, var.type, 'ARR')
                return (var_name, None)
            else:
                if isinstance(arr_size, yalParser.Scalar_accessContext):
                    size_var_info = ScalarAccess(arr_size, self)
                    size_var_info.checkSemantics(printer, [self.vars])

                    if size_var_info.var in self.vars:
                        size_var = self.vars[size_var_info.var]
                        if size_var_info.size:
                            if isinstance(size_var, ArrayVariable):
                                if var is not None:
                                    var.size = size_var.size
                                else:
                                    return (var_name, ArrayVariable(var_name, size_var.size, (line, cols[0]), (line, cols[0])))
                            else:
                                printer.numSize(line, cols, size_var_name, size_var.type)
                        else:
                            if isinstance(size_var, NumberVariable):
                                if var is not None:
                                    var.size = size_var.value
                                else:
                                    return (var_name, ArrayVariable(var_name, size_var.value, (line, cols[0]), (line, cols[0])))
                            else:
                                printer.arrSizeFromArr(line, cols, size_var_info.var)
                                return (var_name, ArrayVariable(var_name, -1, (line, cols[0]), (line, cols[0])))

                    else:
                        printer.undefVar(line, cols, size_var_name)
                    return (var_name, ArrayVariable(var_name, -1, (line, cols[0]), (line, cols[0])))

                else:
                    if var is not None:
                        if isinstance(var, ArrayVariable):
                            var.size = int(str(arr_size))
                        else:
                            printer.diffTypes(line, cols, var.name, var.type, 'ARR')
                    else:
                        return (var_name, ArrayVariable(var_name, int(str(arr_size)), (line, cols[0]), (line, cols[0])))

        return (var_name, None)

    def __parseFunction(self, node) -> (str, Function):
        if __debug__:
            assert isinstance(node, yalParser.FunctionContext), "Module.__parseFunction() 'node'\n - Expected: 'yalParser.FunctionContext'\n - Got: " + str(type(node))

        func_name = str(node.children[0])
        vars = None
        ret_var = None
        stmts = node.children[-1]

        if isinstance(node.children[1], tree.Tree.TerminalNodeImpl): # Check if function has a return variable
            ret_var = node.children[0]
            func_name = str(node.children[1])

        if not isinstance(node.children[-2], tree.Tree.TerminalNodeImpl): # Check if function has arguments
            vars = node.children[-2]

        return (func_name, Function(ret_var, vars, stmts, self))


    def semanticCheck(self, printer):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Module.semanticCheck() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        for name, func in self.code.items():
            func.checkSemantics(printer)

    def __addVariable(self, var_name, var_info):
        if __debug__:
            assert isinstance(var_name, str), "Module.__addVariable() 'var_name'\n - Expected: 'str'\n - Got: " + str(type(var_name))
            assert (isinstance(var_info, Variable) or var_info is None), "Module.__addVariable() 'var_info'\n - Expected: 'Variable'\n - Got: " + str(type(var_info))

        if var_name in self.vars:
            return

        self.vars[var_name] = var_info

    def __addFunction(self, func_name, func_info) -> bool:
        if __debug__:
            assert isinstance(func_name, str), "Module.__addFunction() 'func_name'\n - Expected: 'str'\n - Got: " + str(type(func_name))
            assert isinstance(func_info, Function), "Module.__addFunction() 'func_info'\n - Expected: 'Function'\n - Got: " + str(type(func_info))

        if func_name in self.code:
            return False

        self.code[func_name] = func_info
        return True

    def __addFuncError(self, func, printer):
        if __debug__:
            assert isinstance(func, yalParser.FunctionContext), "Module.__addFuncError() 'func'\n - Expected: 'yalParser.FunctionContext'\n - Got: " + str(type(func))
            assert isinstance(printer, ErrorPrinter), "Module.__addFuncError() 'printer'\n - Expected: 'ErrorPrinter'\n - Got: " + str(type(printer))

        if isinstance(func.children[0], str) and isinstance(func.children[1], str):
            printer.funcRedeclaration(func.children[1].getLine(), func.children[1].getColRange(), str(func.children[1]))
        else:
            printer.funcRedeclaration(func.children[0].getLine(), func.children[0].getColRange(), str(func.children[0]))

    def __str__(self) -> str:
        string = "Module '" + self.name + "':\n"
        string += " Members:\n"
        for name, var in self.vars.items():
            string += "  " + str(var) + "\n"

        string += " Functions:\n"
        for name, func in self.code.items():
            string += "  " + name + str(func)

        return string
