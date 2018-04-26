from antlr4 import *
from antlr_yal import *
from pprint import pprint
from compiler.HIR.Variable import *

def parseStmt(stmt: yalParser.StmtContext, parent) -> ParserRuleContext:
    from compiler.HIR.CodeScope import While, If
    child = stmt.children[0]
    if isinstance(child, yalParser.While_yalContext):
        return While(child, parent)
    elif isinstance(child, yalParser.If_yalContext):
        return If(child, parent)
    elif isinstance(child, yalParser.AssignContext):
        return Assign(child)
    elif isinstance(child, yalParser.CallContext):
        return Call(child.children[0], child.children[1])
    else:
        print("Oh damn boie")
        return None

class Call:
    def __init__(self, calls: str, args_node: yalParser.Arg_listContext):
        self.calls = calls.split('.')
        self.args = []
        for arg in args_node.children:
            self.args.append(str(arg))
class ExprTest:
    def __init__(self, node: yalParser.ExprtestContext):
        self.op = node.children[1]
        self.left = LeftOP(node.children[0])
        self.right = RightOP(node.children[2])

class LeftOP:
    def __init__(self, node: yalParser.Left_opContext):
        child = node.children[0]
        if (isinstance(child, yalParser.Array_accessContext)):
            self.access = ArrayAccess(child)
        elif (isinstance(child, yalParser.Scalar_accessContext)):
            self.access = ScalarAccess(child)
        else:
            print("WUUUUUUUUUUUTTTTTT??????!!!!!!!");

class RightOP:
    def __init__(self, node: yalParser.Right_opContext):
        assert isinstance(node, yalParser.Right_opContext), "Should be a Right_opContext"

        self.value = {}

        if isinstance(node.children[0], tree.Tree.TerminalNodeImpl):
            print(node.children[1])
            print("Is array size!")
            self.value[0] = ArraySize(node.children[1])
            self.needs_op = False
            self.arr_size = True
        elif node.getChildCount() is 1: #Only term
            print("Only term")
            self.value[0] = Term(node.children[0])
            self.needs_op = False
            self.arr_size = False
        else:
            print("3rd option?")
            self.value[0] = Term(node.children[0])
            self.operator = node.children[1]
            self.value[1] = Term(node.children[0])
            self.needs_op = True
            self.arr_size = False

    def resultType(self) -> str:
        if self.arr_size: #TODO need to check function return
            return "ARR"
        else:
            return "NUM"

class Assign:
    def __init__(self, node: yalParser.AssignContext):
        self.left = LeftOP(node.children[0])
        self.right = RightOP(node.children[1])

    def getVarInfo(self):
        return (self.left.access.var, self.left.access);

    def isAssignArray(self):
        return self.right.arr_size;

class ArrayAccess:
    def __init__(self, node: yalParser.Array_accessContext):
        self.var = str(node.children[0])
        self.index = str(node.children[1])

    def indexAccess(self):
        return self.index

class ScalarAccess:
    def __init__(self, node: yalParser.Scalar_accessContext):
        assert isinstance(node, yalParser.Scalar_accessContext), "Should be Scalar_accessContext"
        print("Scalar var = " + str(node))
        self.var = str(node.children[0])
        self.size = (len(node.children) is 2)

    def indexAccess(self):
        return None



class ArraySize:
    def __init__(self, node: yalParser.Array_sizeContext):
        pprint(node)
        assert isinstance(node, yalParser.Array_sizeContext), "node should be Array_sizeContext"

        if ArraySize.isDigit(node):
            self.value = int(str(node.children[0]))
            self.access = False
        else: #Scalar access
            self.value = ScalarAccess(node)
            self.access = True

    def isDigit(node: yalParser.Array_sizeContext):
        return str(node.children[0]).isdigit();

class Term:
    def __init__(self, node: yalParser.TermContext):
        base = 0
        if isinstance(node, tree.Tree.TerminalNodeImpl):
            return;

        if str(node.children[0]) == '+' or str(node.children[0]) == '-':
            base = 1

        self.positive = (str(node.children[0]) is not "-")
        child = node.children[base]


        if isinstance(child, yalParser.CallContext):
            self.value = Call(child.children[0], child.children[1])
        elif isinstance(child, yalParser.Array_accessContext):
            self.value = ArrayAccess(child)
        elif isinstance(child, yalParser.Scalar_accessContext):
            self.value = ScalarAccess(child)
        elif isinstance(child, tree.Tree.TerminalNodeImpl):
            self.value = int(str(child))
        else:
            print("HMMMMMMMMMMMMM?!!?!")
