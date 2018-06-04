import sys
from pathlib import Path
from antlr4 import *
from antlr_yal import *
from compiler import *

from pprint import pprint
RED         = "\033[1;31m"
RESET       = "\033[0;0m"

EXTENSION = '.tmp'

verbose = True
optimized = False
register = 0

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    global verbose
    if not correctUsage(argv) or not parseOptions(argv[2:]):
        Printer.printUsage()
        return

    input = FileStream(argv[1])
    printer = Printer.ErrorPrinter(input)
    lexer = yalLexer(input)
    stream = CommonTokenStream(lexer)
    parser = yalRealParser(stream)
    parser._listeners = [yalErrorListener(verbose)]
    parser.addParseListener(yalParserListener())
    tree = parser.module()

    if parser.getNumberOfSyntaxErrors() > 0:
        if verbose:
            print(" -> " + RED + str(parser.getNumberOfSyntaxErrors()) + RESET + " Syntax errors detected!")

        sys.exit(10)


    module = CodeScope.Module()
    module.parseTree(tree, printer)
    module.semanticCheck(printer)

    sem_errors = printer.printMessages(verbose)
    if not sem_errors:
        llir_tree = Tree.LowLevelTree(module)
        file_name = extractFileName(argv[1]) + EXTENSION
        writeToFile(file_name, str(llir_tree))
        if verbose:
            print(GREEN + "\n ---> SUCCESS <---" + RESET + "\nOutput written to '" + file_name + "'")

    sys.exit(10 if sem_errors else 0)

def extractFileName(file_name) -> str:
    for i in range(len(file_name) - 1, -1, -1):
        if file_name[i] == '.':
            return './' + file_name[:i]

def writeToFile(file_name, content):
    with open(file_name, 'w+') as output:
        output.write(content)

def correctUsage(argv) -> bool:
    arg_n = len(argv)
    if 2 <= arg_n <= 5:
        if not Path(argv[1]).is_file():
            print("File '" + argv[1] + "' does not exist!")
            return False
    else:
        if arg_n > 5:
            print("Too many arguments!")
        else:
            print("Not enough arguments!")
        return False

    return True

def parseOptions(argv) -> bool:
    global verbose
    for arg in argv:
        if '--quiet' == arg or '-q' == arg:
            verbose = False
        elif '--optimized' == arg or '-o' == arg:
            optimized = True
            Variable.Variable.optimized = True
            Instruction.Operator.optimized = True
        elif arg.startswith('--register=') or arg.startswith('-r='):
            args = arg.split('=')
            if len(args) == 2:
                register = int(args[1])
            else:
                print("Register wrong format! '" + arg + "'")
                return False
        else:
            print("Unknown option! '" + arg + "'")
            return False

    return True

if __name__ == '__main__':
    main(sys.argv)
