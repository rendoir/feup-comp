import sys
from antlr4 import *
from ParserLexer import ParserLexer
from ParserParser import ParserParser

def main(argv):
    input = FileStream(argv[1])
    lexer = ParserLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ParserParser(stream)
    print(parser.pyClass().toStringTree(recog=parser))


if __name__ == '__main__':
    main(sys.argv)
