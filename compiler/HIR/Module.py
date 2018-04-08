from antlr4 import *
from antlr_yal import *
from pprint import pprint
from compiler.HIR.Function import *
from compiler.HIR.Variable import *
from compiler.HIR.NumberVariable import *
from compiler.HIR.ArrayVariable import *


class Module:
    def __init__(self):
        self.vars = dict()
        self.functions = dict()

    def parseTree(self, tree: ParserRuleContext) -> bool:
        children = tree.getChildren()
        i = 0;
        for child in children:
            if child is not None:
                ret = None
                if isinstance(child, str): # Module name
                    self.name = child
                elif isinstance(child, yalParser.DeclarationContext): # A variable declaration
                    (var_name, var_info) = self.__parseDeclaration(child, i)
                    print("Parsed '" + var_name +"'");
                    i+=1
                    ret = self.__addVariable(var_name, var_info)
                elif isinstance(child, yalParser.FunctionContext): # A function declaration
                    (func_name, func_info) = self.__parseFunction(child, i)
                    ret = self.__addFunction(func_name, func_info)

                if ret is not None:
                    print(ret)
                    return False


    # n is in which iteration was this called (used instead of line number and column number)
    # Returns tuple with (<var_name>, <variable_instance>)
    # Need to check if var_name already exists!
    def __parseDeclaration(self, node: yalParser.DeclarationContext, n: int) -> (str, Variable):
        if node is None:
            return;
        child_n = node.getChildCount()
        var_name = node.children[0]

        if child_n is 1: # Only variable name
            return (var_name, NumberVariable(None, n, None))
        elif child_n is 2: # Constant declaration?
            return (var_name, NumberVariable(int(number.getText()), n, n))
        elif child_n is 4: # Array declaraction
            size = node.children[2];
            return (var_name, ArrayVariable(int(size), n, n))

    def __parseFunction(self, node: yalParser.FunctionContext, n: int) -> (str, Function):
        has_ret = isinstance(node.children[1], str)
        if has_ret:
            count = node.getChildCount()
            vars = None
            stmts = node.children[2]
            if count is 4:
                vars = node.children[2]
                stmts = node.children[3]

            return (node.children[1], Function(node.children[0], vars, stmts));
        else:
            count = node.getChildCount()
            vars = None
            stmts = node.children[1]
            if count is 3:
                vars = node.children[1]
                stmts = node.children[2]
            return (node.children[0], Function(None, vars, stmts))

    def __addVariable(self, var_name: str, var_info: Variable) -> str:
        if var_name in self.vars:
            return "Variable name '" + var_name + "' already declared!"

        self.vars[var_name] = var_info
        return None

    def __addFunction(self, func_name: str, func_info: Function) -> str:
        if func_name in self.functions:
            return "Function name '" + func_name + "' already declared!"

        self.functions[func_name] = func_info
        return None
