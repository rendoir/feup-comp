import sys
from antlr4 import *
from antlr_yal import *
from compiler import *

from pprint import pprint

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    input = FileStream(argv[1])                         # Open the specified file for input
    lexer = yalLexer(input)                             # Create a lexer parser
    stream = CommonTokenStream(lexer)                   # No clue what this is
    parser = yalRealParser(stream)                          # The actual parser
    parser.addErrorListener(yalErrorListener())
    parser._errHandler = yalErrorStrategy()
    parser.addParseListener(yalParserListener())
    tree = parser.module()                              # Start the parser (error handling should be before this)

    if parser.getNumberOfSyntaxErrors() > 0:
        print(" -> " + RED + str(parser.getNumberOfSyntaxErrors()) + RESET + " Syntax errors detected!")
        return

    module = Module()
    module.parseTree(tree)
    print(module)
    # printTree(tree, 0, recog=parser)

if __name__ == '__main__':
    main(sys.argv)
