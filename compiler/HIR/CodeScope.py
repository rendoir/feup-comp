from compiler.HIR.Variable import *
from compiler.HIR.Stmt import *
from antlr_yal import *

class Scope:
    def __init__(self, parent):
        self.vars = {}
        self.code = []
        self.parent_scope = parent


class Function(Scope):
    def __init__(self, ret_var: str, args: yalParser.Arg_listContext, stmts: yalParser.Stmt_listContext, parent: Scope):
        self.ret_var = ret_var
        self.vars = [dict(), dict()]
        self.code = []
        self.parent_scope = parent
        if args is not None:
            self.__addArgs(args)

        if stmts is not None:
            self.__addStmts(stmts.children)

    def __addArgs(self, args: yalParser.Arg_listContext):
        children = args.getChildren()
        for child in children:
            var = child.split('[]')
            if len(var) is 2:
                self.vars[0][var[0]] = ArrayVariable(var[0], None, 0, 0)
            else:
                self.vars[0][var[0]] = NumberVariable(var[0], None, 0, 0)
            #TODO add hinting

    def __addStmts(self, stmts):
        for stmt in stmts:
            self.code.append(parseStmt(stmt, self))

class If(Scope):
    def __init__(self, node: yalParser.If_yalContext, parent: Scope):
        self.parent_scope = parent
        self.test = ExprTest(node.children[0])
        self.code = []
        stmts = node.children[1]
        for stmt in stmts.children:
            self.code.append(parseStmt(stmt, self))

        self.else_code = []
        if node.getChildCount() is 3:
            for stmt in node.children[2].children:
                self.else_code.append(parseStmt(stmt, self))

class While(Scope):
    def __init__(self, node: yalParser.While_yalContext, parent: Scope):
        self.parent_scope = parent
        self.test = ExprTest(node.children[0])
        self.body = []
        for stmt in node.children[1].children:
            self.body.append(parseStmt(stmt, self))


class Module(Scope):
    def __init__(self):
        self.vars = dict()
        self.code = dict()
        self.parent_scope = None
        self.name = None

    def parseTree(self, tree: ParserRuleContext) -> str:
        print("YELLOW")
        children = tree.getChildren()
        i = 0
        for child in children:
            if child is not None:
                ret = None
                if isinstance(child, str):
                    self.name = child
                elif isinstance(child, yalParser.DeclarationContext):
                    (name, info) = self.__parseDeclaration(child, i)
                    i+=1
                    ret = self.__addVariable(name, info)
                elif isinstance(child, yalParser.FunctionContext):
                    (name, info) = self.__parseFunction(child, i)
                    ret = self.__addFunction(name, info)

                if ret is not None:
                    return ret

    # n is in which iteration was this called (used instead of line number and columnnumber)
    # Returns tuple with (<var_name>, <variable_instance>)
    # Need to check if var_name already exists!
    def __parseDeclaration(self, node: yalParser.DeclarationContext, n: int) -> (str,Variable):
        if node is None:
            return;
        child_n = node.getChildCount()
        var_name = node.children[0]

        if child_n is 1: # Only variable name
            return (var_name, NumberVariable(var_name, None, n, None))
        elif child_n is 2: # Constant declaration?
            return (var_name, NumberVariable(var_name, int(number.getText()), n, n))
        elif child_n is 4: # Array declaraction
            size = node.children[2];
            return (var_name, ArrayVariable(var_name, int(size), n, n))

    def __parseFunction(self, node: yalParser.FunctionContext, n: int) -> (str, Function):
        has_ret = isinstance(node.children[1], str)
        if has_ret:
            count = node.getChildCount()
            vars = None
            stmts = node.children[2]
            if count is 4:
                vars = node.children[2]
                stmts = node.children[3]

            return (node.children[1], Function(node.children[0], vars, stmts, self));
        else:
            count = node.getChildCount()
            vars = None
            stmts = node.children[1]
            if count is 3:
                vars = node.children[1]
                stmts = node.children[2]
            return (node.children[0], Function(None, vars, stmts, self))


    def __addVariable(self, var_name: str, var_info: Variable) -> str:
        if var_name in self.vars:
            return "Variable name '" + var_name + "' already declared!"

        self.vars[var_name] = var_info
        return None

    def __addFunction(self, func_name: str, func_info: Function) -> str:
        if func_name in self.code:
            return "Function name '" + func_name + "' already declared!"

        self.code[func_name] = func_info
        return None
