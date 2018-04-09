from  antlr_yal import *
from compiler.HIR.ArrayVariable import ArrayVariable
from compiler.HIR.NumberVariable import NumberVariable

class Function:
    def __init__(self, ret_var: str, args: yalParser.Arg_listContext, stmts: yalParser.Stmt_listContext):
        self.ret_var = ret_var;
        self.arguments = {};
        self.stmts = list();
        if args is not None:
            self.__addArgs(args)
        for key, item in self.arguments.items():
            print("args = " + key);

        if stmts is not None:
            self.__addStmts(stmts.getChildren())

    def __addArgs(self, args: yalParser.Arg_listContext):
        children = args.getChildren()
        for child in children:
            var = child.split('[]')
            if len(var) is 2:
                self.arguments[var[0]] = ArrayVariable(None, 0, 0)
            else:
                self.arguments[var[0]] = NumberVariable(None, 0, 0)

                #TODO add hinting
    def __addStmts(self, stmts):
        for stmt_node in stmts:
            for stmt in stmt_node.getChildren():
                if isinstance(stmt, yalParser.While_yalContext):
                    print("WHILE");
                elif isinstance(stmt, yalParser.If_yalContext):
                    print("IF");
                elif isinstance(stmt, yalParser.AssignContext):
                    print("ASSIGN");
                elif isinstance(stmt, yalParser.CallContext):
                    print("CALL");
