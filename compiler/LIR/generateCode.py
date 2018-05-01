from compiler.HIR.CodeScope import *
from compiler.HIR.Stmt import *

NL = '\n'
IO_return = dict()

def generateCode(module, in_file):
    print('--- BEGIN GENERATING CODE ---')
    initIO()
    out_file = in_file.split('.')[0] + '.tmp' #TODO CHANGE .tmp TO .j
    with open(out_file, 'w') as out:
        #Module
        out.write(".class public " + module.name + NL)
        out.write(".super java/lang/Object" + NL + NL)

        #Module Vars
        for var in module.vars:
            out.write(".field static " + var + " ")
            if(module.vars[var].type == "ARR"):
                out.write("[I")
            else:
                out.write("I")
                if module.vars[var].value is not None:
                    out.write(" = " + str(module.vars[var].value))
            out.write(NL)
        out.write(NL)

        #Module Functions
        for function in module.code:
            out.write(".method static " + function + "(" + getArgsString(module.code[function]) + ")" + getReturnString(module.code[function]) + NL)
            out.write(".limit locals " + str(getLocals(module.code[function])) + NL)
            out.write(".limit stack " + str(getStack(module.code)) + NL)
            processMethod(module.code[function].code, out, module)
            out.write(".end method" + NL + NL)
        out.close()
    print('--- END GENERATING CODE ---')


def getArgsString(function):
    args_str = ""
    for i in range(len(function.vars[0])):
        if(function.vars[0][i].type == "ARR"):
            args_str += "[I"
        else:
            args_str += "I"
    return args_str


def getReturnString(function):
    if(not isinstance(function, Function)):
        return IO_return[function]
    if(function.ret_str == "ARR"):
        return "["
    if(function.ret_str == "NUM"):
        return "I"
    if(function.ret_str == '???'):
        return "V"
    return ""


#TODO
def getStack(code):
    return 100


#TODO
def getLocals(function):
    res = 0
    res += len(function.vars[1])
    res += getLocalsList(function.code)
    return res

def getLocalsList(f_list):
    total = 0
    for i in range(len(f_list)):
        total += getLocalsScope(f_list[i])
    return total

def getLocalsScope(scope):
    total = 0
    if not isinstance(scope, Scope):
        return total
    total += len(scope.vars)
    total += getLocalsList(scope.code)
    return total


#TODO
def processMethod(f_list, out, module):
    for i in range(len(f_list)):
        processStmt(f_list[i], out, module)

def processStmt(stmt, out, module):
    if(isinstance(stmt, Call)):
        processArgsLoading(stmt, out, module)
        out.write("invokestatic ")

        path = ""
        if(len(stmt.calls) == 1):
            path = module.name + "/" + stmt.calls[0]
        else:
            for call in stmt.calls:
                path += str(call) + "/"
            path = path[:-1]
        out.write(path + "(")

        args = ""
        for arg in stmt.args:
            args += getArgString(arg)

        out.write(args + ")")
        func = getFunction(stmt)
        out.write(getReturnString(func) + NL)


def getArgString(arg):
    if isinstance(arg, str):
        return 'Ljava/lang/String;'
    if(arg.type == "ARR"):
        return "[I"
    if(arg.type == "NUM"):
        return "I"
    return ""


def getFunction(call):
    func = call.funcs.get(call.calls[-1])
    if(func is not None):
        return func
    return call.calls[-1]


def initIO():
    IO_return["read"] = "I"
    IO_return["print"] = "V"
    IO_return["println"] = "V"


def processArgsLoading(stmt, out, module):
    for arg in stmt.args:
        loadVar(arg, out, module)


def loadVar(var, out, module):
    if(isinstance(var, Variable)):
        print(var.name)
    else:
        out.write("ldc " + var + NL)
