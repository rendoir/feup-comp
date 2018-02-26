import sys
from antlr4 import *
from yalLexer import yalLexer
from yalParser import yalParser

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    input = FileStream(argv[1])                         # Open the specified file for input
    lexer = yalLexer(input)                          # Create a lexer parser
    stream = CommonTokenStream(lexer)                   # No clue what this is
    parser = yalParser(stream)                       # The actual parser
    print(parser.module().toStringTree(recog=parser))  # Prints the matches, if there are multiple matches, need to call parse.pyClass() multiple times


if __name__ == '__main__':
    main(sys.argv)
