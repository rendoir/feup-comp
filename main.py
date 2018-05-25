import sys
from pathlib import Path
from antlr4 import *
from antlr_yal import *
from compiler import *

from pprint import pprint

EXTENSION = '.tmp'

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    if not correctUsage(argv):
        printUsage()
        return

    input = FileStream(argv[1])
    printer = Printer.ErrorPrinter(input)
    lexer = yalLexer(input)
    stream = CommonTokenStream(lexer)
    parser = yalRealParser(stream)
    parser._listeners = [yalErrorListener()]
    parser.addParseListener(yalParserListener())
    tree = parser.module()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(" -> " + RED + str(parser.getNumberOfSyntaxErrors()) + RESET + " Syntax errors detected!")
        return


    module = Module()
    module.parseTree(tree, printer)
    module.semanticCheck(printer)

    sem_errors = printer.printMessages()
    if not sem_errors:
        llir_tree = LowLevelTree(module)
        writeToFile(extractFileName(argv[1]) + EXTENSION, str(llir_tree))
        print("Done!")

    sys.exit(1 if sem_errors else 0)

def extractFileName(file_name) -> str:
    for i in range(len(file_name) - 1, -1, -1):
        if file_name[i] == '.':
            return './' + file_name[:i]

def writeToFile(file_name, content):
    with open(file_name, 'w+') as output:
        output.write(content)

def correctUsage(argv) -> bool:
    if len(argv) is 2:
        if not Path(argv[1]).is_file():
            print("File '" + argv[1] + "' does not exist!")
            return False
    else:
        if len(argv) > 2:
            print("Too many arguments!")
        else:
            print("Not enough arguments!")
        return False

    return True

def printUsage():
    print("Usage:\n    python3 main.py <file_name>\n")

if __name__ == '__main__':
    main(sys.argv)
