from  antlr_yal import *

class Function:
    def __init__(self, ret_var: str, args: yalParser.Arg_listContext, stmts: yalParser.Stmt_listContext):
        self.ret_var = ret_var;
        self.arguments = list ();
        self.stmts = list();
        if args is not None:
            self.__addArgs(args)
        if stmts is not None:
            self.__addStmts(stmts)

    def __addArgs(self, args: yalParser.Arg_listContext):
        print("Adding #" + str(args.getChildCount()) + " args!");

    def __addStmts(self, stmts: yalParser.Stmt_listContext):
        print("Adding #" + str(stmts.getChildCount()) + " stmts!");
