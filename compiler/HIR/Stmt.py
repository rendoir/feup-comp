from typing import List
from antlr4 import *
from antlr_yal import *

class Call:
    def __init__(self, breadcrumbs: List[str], args_node: yalParser.Arg_listContext):
        self.calls = breadcrumbs
        self.args = args_node.children

class Assign:
    class __LeftOP:
        def __init__(self, node: yalParser.Left_opContext):
            if (isinstance(node, yalParser.Array_accessContext):
                self.operator = ArrayAccess(node.child[0])
            elif (isinstance(node, yalParser.Scalar_accessContext):
                self.operator = ScalarAccess(node.child[0])
            else:
                print("WUUUUUUUUUUUTTTTTT??????!!!!!!!");


    class __RightOP:
        def __init__(self, node: yalParser.Right_opContext):
            print("Right childs ")
            if (isinstance(node, str)):
                print(node)
            else:
                for child in node.getChildren():
                    print(child)

    def __init__(self, left_node: ParserRuleContext, right_node: ParserRuleContext):
        self.left = self.__LeftOP(left_node)
        self.right = self.__RightOP(right_node)

class ArrayAccess:
    def __init__(self, node: yalParser.Array_accessContext):
        self.var = node.child[0]
        self.index = int(node.child[1])

class ScalarAccess:
    def __init__(self, node: yalParser.Scalar_accessContext):
        self.var = node.child[0]
        self.size = (len(node.children) is 2)
