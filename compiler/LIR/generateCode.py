from compiler.HIR.CodeScope import *

NL = '\n'

def generateCode(module, in_file):
    print('--- BEGIN GENERATING CODE ---')
    out_file = in_file.split('.')[0] + '.tmp' #TODO CHANGE .tmp TO .j
    with open(out_file, 'w') as out:
        #TODO REMOVE PRINTS
        #print(module.vars)
        #print(module.code)

        #Module
        out.write(".class public " + module.name + NL)
        out.write(".super java/lang/Object" + NL + NL)

        #Module Vars
        for var in module.vars:
            out.write(".field static " + module.vars[var].name + " ")
            if(module.vars[var].type == "ARR"):
                out.write("[")
            out.write("I")
            out.write(NL)

        out.close()
    print('--- END GENERATING CODE ---')
