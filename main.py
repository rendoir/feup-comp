import sys
from antlr4 import *
from antlr4.error import *
from yalLexer import yalLexer
from yalParser import yalParser
from yalListener import yalListener


class Listener(yalListener):
    def enterModule(self, ctx:yalParser.ModuleContext):
        print("Module = " + ctx.getText())

    def enterArray_element(self, ctx:yalParser.Array_elementContext):
        print("Elem = " + ctx.getText())

    def enterScalar_element(self, ctx:yalParser.Scalar_elementContext):
        print("Scalar = " + ctx.getText())

# ParserParser class will have a method for each 'rule' in the parser.
# So since the parser has rules such as 'vector', 'expression' and 'pyClass'
# It generates a method to parse each one of these
def main(argv):
    input = FileStream(argv[1])                         # Open the specified file for input
    lexer = yalLexer(input)                             # Create a lexer parser
    stream = CommonTokenStream(lexer)                   # No clue what this is
    parser = yalParser(stream)                          # The actual parser




    # parser._errHandler = BailErrorStrategy()
    tree = parser.module()                              # Start the parser (error handling should be before this)

    walker = ParseTreeWalker()
    listener = Listener()
    walker.walk(listener, tree)                         # Walks the tree calling the listener when it enters a rule

    # print(tree.toStringTree(recog=parser))   # Prints the matches, if there are multiple matches, need to call parse.pyClass() multiple times


if __name__ == '__main__':
    main(sys.argv)
