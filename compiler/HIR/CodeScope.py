from compiler.HIR.Variable import *
from compiler.HIR.Stmt import *
from antlr_yal import *

def checkVar(var_name: str, is_array: bool, defined_vars) -> str:
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
        self.vars = {}
        self.code = []
        self.parent_scope = parent

    def addVar(self, name: str, var: Variable):
        raise NotImplementedError( "Should have implemented this" )


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
            print("VAR = " + str(var))
            if len(var) == 2:
                self.vars[0][var[0]] = ArrayVariable(var[0], None, 0, 0)
            else:
                self.vars[0][var[0]] = NumberVariable(var[0], None, 0, 0)
            #TODO add hinting

    def __addStmts(self, stmts):
        for stmt in stmts:
            self.code.append(parseStmt(stmt, self))

    def __str__(self):
        string = "("
        for name, arg in self.vars[0].items():
            pprint(arg)
            string += str(arg) + " "
        string += ")\n"
        return string

    def checkVariables(self):
        for line in self.code:
            if isinstance(line, yalParser.While_yalContext) or isinstance(line, yalParser.If_yalContext):
                vars = []
                vars.insert(0, self.vars[0])
                vars.insert(0, self.vars[1])
                line.checkVariables(vars)
            elif isinstance(line, Stmt.Assign):
                (name, is_array) = line.getVarInfo()
                # Check if variable type is same as assignment

                if name not in self.vars[0]: # Variable is not an argument
                    if name not in self.vars[1]:
                        if is_array:
                            self.vars[1][name] = ArrayVariable(name, None, 1, 1)
                        else:
                            #TODO check if it has a '.size'
                            self.vars[1][name] = NumberVariable(name, None, 1, 1)
                    else:
                        print("Variable '" + name + "' reaassigned!")
            elif isinstance(line, Stmt.Call):
                func_name = line.calls[0]
                mod_call = len(line.calls) is 2

                if not mod_call:
                    if func_name not in parent.code:
                        return "Function '" + func_name + "' not defined!"


                for arg in line.args:
                    vars_list = []
                    vars_list.insert(0, self.parent.vars)
                    vars_list.insert(0, self.vars[0])
                    vars_list.insert(0, self.vars[1])
                    exists = false
                    for vars in vars_list:
                        exists = exists or (arg in vars)
                        if arg in vars:
                            if not vars[arg].initialized():
                                return "Variable '" + arg + "' used before initialization!"

        return None







class If(Scope):
    def __init__(self, node: yalParser.If_yalContext, parent: Scope):
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
    def __init__(self, node: yalParser.While_yalContext, parent: Scope):
        self.parent_scope = parent
        self.test = ExprTest(node.children[0])
        self.body = []
        self.vars = dict()
        for stmt in node.children[1].children:
            self.body.append(parseStmt(stmt, self))


class Module(Scope):
    def __init__(self):
        self.vars = dict()
        self.code = dict()
        self.parent_scope = None
        self.name = None

    def parseTree(self, tree: ParserRuleContext) -> str:
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
    def __parseDeclaration(self, node: yalParser.DeclarationContext) -> (str,Variable):
        if node is None:
            return;
        child_n = node.getChildCount()
        var_name = node.children[0]

        if child_n is 1: # Only variable name
            return (var_name, NumberVariable(var_name, None, 0, None))
        elif child_n is 2: # Constant declaration?
            return (var_name, NumberVariable(var_name, int(number.getText()), 0, 0))
        elif child_n is 4: # Array declaraction
            size = node.children[2];
            return (var_name, ArrayVariable(var_name, int(size), 0, 0))

    def __parseFunction(self, node: yalParser.FunctionContext) -> (str, Function):
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


    def semanticCheck(self) -> str:
        for name, func in self.code.items():
            func.checkVariables()



    def __str__(self):
        string = "Module '" + self.name + "':\n"
        string += " Members:\n"
        for name, var in self.vars.items():
            string += "  " + str(var) + "\n"

        string += " Functions:\n"
        for name, func in self.code.items():
            string += "  " + name + str(func)

        return string
