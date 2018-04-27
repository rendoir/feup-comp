from .Variable import Variable, NumberVariable, ArrayVariable
from compiler.Printer import ErrorPrinter
from antlr_yal import *
from typing import List
from pprint import pprint

def checkVar(var_name, is_array, defined_vars) -> str:
    if __debug__:
        assert isinstance(var_name, str), "CodeSCope.checkVar() 'var_name' should be 'str'"
        assert isinstance(is_array, bool), "CodeScope.checkVar() 'is_array' should be 'bool'"
        assert isinstance(defined_vars, list), "CodeSCope.checkVar() 'defined_vars' should be 'list'"

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
            assert isinstance(parent, Scope), "Scope.__init__() parent should be scope"

        self.vars = {}
        self.code = []
        self.parent_scope = parent

    def addVar(self, name, var):
        raise NotImplementedError( "Should have implemented this" )

# 20 maças, cortar laminadas ++ fino, marshmallows 1 por cada pessoa (+- 100), espeto para por marshmallows (dar para pelos menos 15),

class Function(Scope):
    def __init__(self, ret_var, args , stmts , parent):
        if __debug__:
            assert isinstance(ret_var, str) or ret_var is None, "Function.__init__() 'ret_var' should be 'str'"
            assert isinstance(args, yalParser.Var_listContext) or args is None, "Function.__init__() 'args' should be 'yalParser.Var_listContext'"
            assert isinstance(stmts, yalParser.Stmt_listContext), "Function.__init__() 'stmts' should be 'yalParser.Stmt_listContext'"
            assert isinstance(parent, Scope), "Function.__init__() 'parent' should be 'Scope'"

        self.ret_var = ret_var
        self.ret_is_arr = False
        self.vars = [[], dict()] #[<arguments>, <local_variables>]
        self.code = []
        self.parent_scope = parent
        if args is not None:
            self.__addArgs(args)

        if stmts is not None:
            self.__addStmts(stmts.children)


    def __addArgs(self, args):
        if __debug__:
            assert isinstance(args, yalParser.Var_listContext), "Function.__addArgs() 'args' should be 'yalParser.Var_listContext'"

        children = args.getChildren()
        for child in children:
            var = child.split('[]')
            if len(var) == 2:
                self.vars[0].append(ArrayVariable(var[0], None, 0, 0))
            else:
                self.vars[0].append(NumberVariable(var[0], None, 0, 0))


    def __addStmts(self, stmts: List[yalParser.Stmt_listContext]):
        from . import Stmt
        if __debug__:
            assert isinstance(stmts, list), "Function.__addStmts() 'stmts' should be 'list'"

        for stmt in stmts:
            self.code.append(Stmt.parseStmt(stmt, self))

    def __str__(self) -> str:
        string = "("
        for arg in self.vars[0]:
            print(arg)
            string += arg.name + " "
        string += ")\n"
        return string

    def checkVariables(self, printer) -> List[str]:
        from . import Stmt
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Function.checkVariables() 'printer' should be 'ErrorPrinter'"


        ret_arr = []
        for code_chunk in self.code:
            var_list = [self.vars[1], self.vars[0], self.parent_scope.vars]

            if isinstance(code_chunk, yalParser.While_yalContext) or isinstance(code_chunk, yalParser.If_yalContext):
                ret_arr += code_chunk.checkVariables(printer, var_list)
            elif isinstance(code_chunk, Stmt.Assign):
                ret_arr += self.__checkAssign(printer, code_chunk, var_list)
            elif isinstance(code_chunk, Stmt.Call):
                ret_arr += code_chunk.checkSemantics(printer, var_list, self.parent_scope.code)

        return ret_arr

    def __checkAssign(self, printer, assign, var_lists) -> list:
        from . import Stmt
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Function.__checkAssign() 'printer' should be 'ErrorPrinter'"
            assert isinstance(assign, Stmt.Assign), "Function.__checkAssign() 'assign' should be 'Stmt.Assign'"
            assert isinstance(var_lists, list), "Function.__checkAssign() 'var_lists' should be 'list'"

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
            assert isinstance(node, yalParser.If_yalContext), "If.__init__() 'node' should be 'yalParser.If_yalContext'"
            assert isinstance(parent, Scope), "If.__init__() 'parent' should be 'Scope'"

        self.parent_scope = parent
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

class While(Scope):
    def __init__(self, node, parent):
        from . import Stmt
        if __debug__:
            assert isinstance(node, yalParser.While_yalContext), "While.__init__() 'node' should be 'yalParser.While_yalContext'"
            assert isinstance(parent, Scope), "While.__init__() 'parent' should be 'Scope'"

        self.parent_scope = parent
        self.test = Stmt.ExprTest(node.children[0])
        self.body = []
        self.vars = dict()
        for stmt in node.children[1].children:
            self.body.append(Stmt.parseStmt(stmt, self))

class Module(Scope):
    def __init__(self):
        self.vars = dict()
        self.code = dict()
        self.parent_scope = None
        self.name = None

    def parseTree(self, tree) -> str:
        if __debug__:
            assert isinstance(tree, ParserRuleContext), "Module.parseTree() 'tree' should be 'ParserRuleContext'"

        children = tree.getChildren()
        for child in children:
            if child is not None:
                ret = None
                if isinstance(child, yalParser.DeclarationContext):
                    (name, info) = self.__parseDeclaration(child)
                    ret = self.__addVariable(name, info)
                elif isinstance(child, yalParser.FunctionContext):
                    (name, info) = self.__parseFunction(child)
                    ret = self.__addFunction(name, info)
                else:
                    self.name = str(child);

                if ret is not None:
                    return ret

    # Returns tuple with (<var_name>, <variable_instance>)
    # Need to check if var_name already exists!
    def __parseDeclaration(self, node) -> (str,Variable):
        if __debug__:
            assert isinstance(node, yalParser.DeclarationContext), "Module.__parseDeclaration() 'node' should be 'yalParser.DeclarationContext'"

        if node is None:
            return;
        child_n = node.getChildCount()
        var_name = node.children[0]

        if child_n is 1: # Only variable name
            return (var_name, NumberVariable(var_name, None, 0, 0))
        elif child_n is 2: # Constant declaration?
            return (var_name, NumberVariable(var_name, int(number.getText()), 0, 0))
        elif child_n is 4: # Array declaraction
            size = node.children[2];
            return (var_name, ArrayVariable(var_name, int(size), 0, 0))

    def __parseFunction(self, node) -> (str, Function):
        if __debug__:
            assert isinstance(node, yalParser.FunctionContext), "Module.__parseFunction() 'node' should be 'yalParser.FunctionContext'"

        func_name = node.children[0]
        vars = None
        ret_var = None
        stmts = node.children[-1]

        if not isinstance(node.children[-2], str): # Check if function has arguments
            vars = node.children[-2]

        if isinstance(node.children[1], str): # Check if function has a return variable
            ret_var = node.children[0]
            func_name = node.children[1]

        return (func_name, Function(ret_var, vars, stmts, self))


    def semanticCheck(self, printer):
        if __debug__:
            assert isinstance(printer, ErrorPrinter), "Module.semanticCheck() 'printer' should be 'ErrorPrinter'"

        print("--- Semantic Check ---")
        errors = []
        for name, func in self.code.items():
            errors += func.checkVariables(printer)

        if len(errors):
            print("--- " + str(len(errors)) + " ERROR ---")
            for error in errors:
                print(error)

        print("--- End Semantic Check ---")

    def __addVariable(self, var_name, var_info) -> str:
        if __debug__:
            assert isinstance(var_name, str), "Module.__addVariable() 'var_name' should be 'str'"
            assert isinstance(var_info, Variable), "Module.__addVariable() 'var_info' should be 'Variable'"

        if var_name in self.vars:
            return "Variable name '" + var_name + "' already declared!"

        self.vars[var_name] = var_info
        return None

    def __addFunction(self, func_name: str, func_info: Function) -> str:
        if __debug__:
            assert isinstance(func_name, str), "Module.__addFunction() 'func_name' should be 'str'"
            assert isinstance(func_info, Function), "Module.__addFunction() 'func_info' should be 'Function'"

        if func_name in self.code:
            return "Function name '" + func_name + "' already declared!"

        print("Adding '" + func_name + "', info = " + str(func_info))
        self.code[func_name] = func_info
        return None



    def __str__(self) -> str:
        string = "Module '" + self.name + "':\n"
        string += " Members:\n"
        for name, var in self.vars.items():
            string += "  " + str(var) + "\n"

        string += " Functions:\n"
        for name, func in self.code.items():
            string += "  " + name + str(func)

        return string
