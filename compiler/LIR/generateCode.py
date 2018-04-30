from compiler.HIR.CodeScope import *
from compiler.HIR.Stmt import *

NL = '\n'

def generateCode(module, in_file):
    print('--- BEGIN GENERATING CODE ---')
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
            processMethod(module.code[function].code, out)
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
def processMethod(f_list, out):
    for i in range(len(f_list)):
        processStmt(f_list[i], out)

def processStmt(stmt, out):
    if(isinstance(stmt, Call)):
        out.write("invokestatic ")

        path = ""
        for call in stmt.calls:
            path += str(call) + "/"
        if(len(stmt.calls) > 0):
            path = path[:-1]
        out.write(path + NL)


        args = ""
        remove = False
        for arg in stmt.args:
            remove = True
            args += getArgString(arg) + ";"

        if remove:
            args = args[:-1]
        out.write(args + NL)


def getArgString(arg):
    if __debug__:
        assert isinstance(arg, Variable) or isinstance(arg, str), "getArgString() 'arg'\n - Expected: 'Variable'\n - Got: " + str(type(arg))

    if isinstance(arg, str):
        return 'Ljava/lang/String'
    if(arg.type == "ARR"):
        return "[I"
    if(arg.type == "NUM"):
        return "I"
    return ""
