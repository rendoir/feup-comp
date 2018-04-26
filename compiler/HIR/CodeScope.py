from compiler.HIR.Variable import *
from compiler.HIR.Stmt import *
from antlr_yal import *

from pprint import pprint

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

# 20 maças, cortar laminadas ++ fino, marshmallows 1 por cada pessoa (+- 100), espeto para por marshmallows (dar para pelos menos 15),

class Function(Scope):
    def __init__(self, ret_var: str, args: yalParser.Arg_listContext, stmts: yalParser.Stmt_listContext, parent: Scope):
        self.ret_var = ret_var
        self.vars = [[], dict()] #[<arguments>, <local_variables>]
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
            if len(var) == 2:
                self.vars[0].append(ArrayVariable(var[0], None, 0, 0))
            else:
                self.vars[0].append(NumberVariable(var[0], None, 0, 0))
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
        for code_chunk in self.code:
            var_list = [self.vars[1], self.vars[0], self.parent_scope.vars]
            ret = None

            if isinstance(code_chunk, yalParser.While_yalContext) or isinstance(code_chunk, yalParser.If_yalContext):
                ret = code_chunk.checkVariables(var_list)
            elif isinstance(code_chunk, Assign):
                ret = self.__checkAssign(code_chunk, var_list)
            elif isinstance(code_chunk, Call):
                ret = self.__checkCallSemantic(code_chunk, var_list)

            if ret is not None:
                print(ret)

        return None


    def __checkCallSemantic(self, line: Call, var_list) -> str:
        func_name = line.calls[0]
        func_called = None
        mod_call = len(line.calls) is 2

        # Check if function exists
        if not mod_call:
            if func_name not in self.parent_scope.code:
                return "Function '" + func_name + "' not defined!"
            else:
                func_called = self.parent_scope.code[func_name]

        call_vars = []
        #Check if arguments exists
        for arg_name in line.args:
            exists = False
            for vars in var_list:
                exists = exists or (arg_name in vars)
                if arg_name in vars:
                    if not vars[arg_name].initialized():
                        return "Variable '" + arg_name + "' used before initialization!"
                    call_vars.append(vars[arg_name])

            if not exists:
                if not Variable.isLiteral(arg_name):
                    return "Variable '" + arg_name + "' not defined!"


        #Check correct type of parameters
        func_args = func_called.vars[0]
        wrong = False

        if len(call_vars) is len(func_called.vars[0]):
            for i in range(len(call_vars)):
                if call_vars[i].type != func_called.vars[0][i].type:
                    wrong = True
        else:
            wrong = True

        if wrong:
            ret = "Expected " + func_name + "("
            remove = False
            for var in func_called.vars[0]:
                remove = True
                ret += var.type + ", "
            if remove:
                ret = ret[:-2]
            ret += "), got " + func_name + "("

            for var in call_vars:
                ret += var.type + ", "
            ret = ret[:-2]
            ret += ")"
            return ret

        return None

    def __checkAssign(self, assign: Assign, var_lists) -> str:
        (var_name, var_info) = assign.getVarInfo()
        exists = False;
        indexing = var_info.indexAccess();


        for var_list in var_lists:
            if var_name in var_list: #Check var type matches
                exists = True
                var = var_list[var_name]
                assign_type = assign.right.resultType()
                if assign_type != var.type:
                    return "Assigned wrong type to variable '{}'\n  Expected '{}', got '{}'".format(var_name, var.type, assign_type)

        if not exists:
            var_obj = None
            is_array = assign.isAssignArray()
            print("Adding var '{}', is_arr '{}'".format(var_name, is_array))
            if is_array:
                var_obj = ArrayVariable(var_name, 0, 0, 0)
            else:
                var_obj = NumberVariable(var_name, 0, 0, 0)
            self.vars[1][var_name] = var_obj


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


    def semanticCheck(self):
        print("--- Semantic Check ---")
        err_n = 0
        for name, func in self.code.items():
            ret = func.checkVariables()
            if ret is not None:
                err_n += 1
                print(ret)

        if err_n > 0:
            print(str(err_n) + " semantic errors!")
        print("--- End Semantic Check ---")


    def __str__(self):
        string = "Module '" + self.name + "':\n"
        string += " Members:\n"
        for name, var in self.vars.items():
            string += "  " + str(var) + "\n"

        string += " Functions:\n"
        for name, func in self.code.items():
            string += "  " + name + str(func)

        return string
