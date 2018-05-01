from compiler.HIR.CodeScope import *
from compiler.HIR.Stmt import *

NL = '\n'
IO_return = dict()

local_variables = []

operators = {
    '*':    ('imul ' + NL),
    '/':    ('idiv ' + NL),
    '<<':   ('ishl ' + NL),
    '>>':   ('ishr ' + NL),
    '>>>':  ('WTF IS THIS???' + NL),
    '&':    ('iand ' + NL),
    '|':    ('ior ' + NL),
    '^':    ('ixor ' + NL),
    '+':    ('iadd ' + NL),
    '-':    ('isub ' + NL),
}

def __getLocalIndex(var_name) -> int:
    for i in range(len(local_variables)):
        if local_variables[i] == var_name:
            return i

    else:
        print("How did semantics not catch this?")
        return len(local_variables)


def __addLocalVar(var_name) -> int:
    index = __getLocalIndex(var_name)
    if index == -1:
        local_variables.append(var_name)

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
            processMethod(module.code[function], out, module)
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
def processMethod(function, out, module):
    del local_variables[:]
    for arg in function.vars[0]:
        local_variables.append(arg.name)

    for i in range(len(function.code)):
        processStmt(function.code[i], out, module.name)

    processReturn(function, out)

    out.write('return' + NL)

def processReturn(function, out):
    if function.ret_var is not None:
        var = function.vars[1][function.ret_var]
        index = __getLocalIndex(var.name)
        if var.type == 'ARR':
            out.write('aload ' + str(index) + NL)
        else:
            out.write('iload ' + str(index) + NL)


def processStmt(stmt, out, mod_name):
    if(isinstance(stmt, Call)):
        __writeCall(stmt, out, mod_name)
    elif isinstance(stmt, Assign):
        __writeRightOP(stmt.right, out, mod_name)
        (final_inst, var_name) = __writeLeftOP(stmt.left, out)
        out.write(final_inst)

def __writeLeftOP(left, out):
    if isinstance(left.access, ArrayAccess):
        access = left.access
        out.write('aload ' + str(access.var) + NL)
        if isinstance(access.index, Variable):
            out.write('iload ' + str(__getLocalIndex(access.index.name)) + NL)
        else:
            out.write('ldc ' + access.index + NL)
        return ('aastore', str(access.var))
    else:
        access = left.access
        return (('istore ' + str(__getLocalIndex(access.var)) + NL), access.var)

def __writeRightOP(right, out, mod_name):
    if right.arr_size:
        __writeArrSize(right.value[0], out)
    elif right.needs_op:
        __writeTerm(right.value[0], out, mod_name)
        __writeTerm(right.value[1], out, mod_name)
        out.write(operators[right.operator])
    else:
        __writeTerm(right.value[0], out, mod_name)

def __writeTerm(term, out, mod_name):
    if isinstance(term.value, Call):
        __writeCall(term.value, out, mod_name)
    elif isinstance(term.value, ArrayAccess):
        __writeArrAccess(term.value, out)
    elif isinstance(term.value, ScalarAccess):
        __writeScalarAccess(term.value, out)
    else:
        out.write('ldc ' + str(self.value) + NL)

def __writeCall(call, out, mod_name):
    processArgsLoading(call, out)
    processFuncCall(call, out, mod_name)

def __writeArrSize(arr_size, out):
    if arr_size.access:
        __writeScalarAccess(arr_size.value, out)
    else:
        out.write('ldc ' + str(arr_size.value) + NL)

def __writeScalarAccess(access, out):
    if access.size:
        out.write('arraylength ' + str(__getLocalIndex(access.var)) + NL)
    else:
        out.write('aload ' + str(__getLocalIndex(access.var)) + NL)

def __writeArrAccess(access, out):
    out.write('aload ' + str(access.var))
    if isinstance(access.index, str):
        out.write('ldc ' + access.index + NL)
    else:
        out.write('iload ' + str(__getLocalIndex(access.index.name)) + NL)

def getArgString(arg):

    if isinstance(arg, str):
        if arg.isdigit():
            return 'I'
        else:
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


def processArgsLoading(call, out):
    for arg in call.args:
        if isinstance(arg, Variable):
            if arg.type == 'ARR':
                out.write('aload ' + str(__getLocalIndex(arg.name)) + NL)
            else:
                out.write('iload ' + str(__getLocalIndex(arg.name)) + NL)
        else:
            out.write('ldc ' + arg + NL)

def processFuncCall(call, out, mod_name):
    out.write('invokestatic ')
    path = ''
    if len(call.calls) is 1:
        path = mod_name + '/' + call.calls[-1]
    else:
        path = call.calls[0] + '/' + call.calls[1]
    out.write(path + '(')

    args = ''
    for arg in call.args:
        args += getArgString(arg)

    out.write(args + ')')
    func = getFunction(call)
    out.write(getReturnString(func) + NL)
