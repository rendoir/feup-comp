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

    printTree(tree, 0, recog=parser)


def printTree(tree, indentation, ruleNames:list=None, recog:Parser=None):
    if recog is not None:
        ruleNames = recog.ruleNames

    if isinstance(tree, str):
        return tree
    elif tree is None:
        return "None"
    elif tree.getChildCount() is 0:
        return tree.getText()
    else:
        name = getNodeText(tree, ruleNames, recog)
    print("\n" + spaces(indentation) + "(", end='')

    with StringIO() as buf:
        print(name + " ", end='')

        for i in range(tree.getChildCount()):
            child = tree.children[i]
            print(" " + printTree(child, indentation + 1, ruleNames, recog), end='')

            if i is (tree.getChildCount() - 1):
                print(")\n" + spaces(indentation - 1), end='')

        return buf.getvalue()

def spaces(number):
    space = ""
    for i in range(number):
        space += " "

    return space

def getNodeText(t, rule_names:list=None, recog:Parser=None):
    if recog is not None:
        ruleNames = recog.ruleNames
    if ruleNames is not None:
        if isinstance(t, RuleNode):
            if t.getAltNumber()!=0: # should use ATN.INVALID_ALT_NUMBER but won't compile
                return ruleNames[t.getRuleIndex()]+":"+str(t.getAltNumber())
            return ruleNames[t.getRuleIndex()]
        elif isinstance(t, ErrorNode):
            return str(t)
        elif isinstance(t, TerminalNode):
            if t.symbol is not None:
                return t.symbol.text

#* @description Extracts the function arguments
#* @arg `root` - The root node of the function in the syntax tree
#* @return A dictionary where keys are the argument name
#*       value is a boolean of whether the argument is an array or not
#*
#* @detail It starts by getting the children of the function which are not terminal symbols so it extracts everything but the arguments.
#* After that extractArg is called for every children of the child obtained (the child is the 'var_list' antlr4 rule)
def getFuncArgs(root):
    func_children = root.getChildren(lambda x: not isinstance(x, TerminalNode))
    vars = next(func_children).getChildren()
    arguments = {}

    for var in vars:
        arg = extractArg(var)
        arguments[arg["name"]] = arg["array"]

    return arguments

def extractArg(argument):
    if argument.getChildCount() == 1:
        return {"name": next(argument.getChildren()).getText(), "array": False}
    elif argument.getChildCount() == 3:
        return {"name": next(argument.getChildren()).getText(), "array": True}
    else:
        print("Error! argument has " + argument.getChildCount() + " args")
        return None

if __name__ == '__main__':
    main(sys.argv)
