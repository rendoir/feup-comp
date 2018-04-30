import sys
from antlr4 import *
from antlr_yal import *
from compiler import *

from pprint import pprint

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    input = FileStream(argv[1])
    printer = Printer.ErrorPrinter(input)
    lexer = yalLexer(input)
    stream = CommonTokenStream(lexer)
    parser = yalRealParser(stream)
    parser.addErrorListener(yalErrorListener())
    parser.addParseListener(yalParserListener())
    tree = parser.module()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(" -> " + RED + str(parser.getNumberOfSyntaxErrors()) + RESET + " Syntax errors detected!")
        return


    module = Module()
    module.parseTree(tree, printer)
    module.semanticCheck(printer)

    if not printer.printMessages():
        generateCode(module,argv[1])

if __name__ == '__main__':
    main(sys.argv)
