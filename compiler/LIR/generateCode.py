from compiler.HIR.CodeScope import *

def generateCode(module, in_file):
    print('--- BEGIN GENERATING CODE ---')
    out_file = in_file.split('.')[0] + '._j' #TODO REMOVE UNDERSCORE
    with open(out_file, 'w') as out:
        
        out.close()
    print('--- END GENERATING CODE ---')
