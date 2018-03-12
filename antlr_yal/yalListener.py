# Generated from yal.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .yalParser import yalParser
else:
    from yalParser import yalParser

# This class defines a complete listener for a parse tree produced by yalParser.
class yalListener(ParseTreeListener):

    # Enter a parse tree produced by yalParser#module.
    def enterModule(self, ctx:yalParser.ModuleContext):
        pass

    # Exit a parse tree produced by yalParser#module.
    def exitModule(self, ctx:yalParser.ModuleContext):
        pass


    # Enter a parse tree produced by yalParser#declaration.
    def enterDeclaration(self, ctx:yalParser.DeclarationContext):
        pass

    # Exit a parse tree produced by yalParser#declaration.
    def exitDeclaration(self, ctx:yalParser.DeclarationContext):
        pass


    # Enter a parse tree produced by yalParser#function.
    def enterFunction(self, ctx:yalParser.FunctionContext):
        pass

    # Exit a parse tree produced by yalParser#function.
    def exitFunction(self, ctx:yalParser.FunctionContext):
        pass


    # Enter a parse tree produced by yalParser#var_list.
    def enterVar_list(self, ctx:yalParser.Var_listContext):
        pass

    # Exit a parse tree produced by yalParser#var_list.
    def exitVar_list(self, ctx:yalParser.Var_listContext):
        pass


    # Enter a parse tree produced by yalParser#array_element.
    def enterArray_element(self, ctx:yalParser.Array_elementContext):
        pass

    # Exit a parse tree produced by yalParser#array_element.
    def exitArray_element(self, ctx:yalParser.Array_elementContext):
        pass


    # Enter a parse tree produced by yalParser#scalar_element.
    def enterScalar_element(self, ctx:yalParser.Scalar_elementContext):
        pass

    # Exit a parse tree produced by yalParser#scalar_element.
    def exitScalar_element(self, ctx:yalParser.Scalar_elementContext):
        pass


    # Enter a parse tree produced by yalParser#stmt_list.
    def enterStmt_list(self, ctx:yalParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by yalParser#stmt_list.
    def exitStmt_list(self, ctx:yalParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by yalParser#stmt.
    def enterStmt(self, ctx:yalParser.StmtContext):
        pass

    # Exit a parse tree produced by yalParser#stmt.
    def exitStmt(self, ctx:yalParser.StmtContext):
        pass


    # Enter a parse tree produced by yalParser#assign.
    def enterAssign(self, ctx:yalParser.AssignContext):
        pass

    # Exit a parse tree produced by yalParser#assign.
    def exitAssign(self, ctx:yalParser.AssignContext):
        pass


    # Enter a parse tree produced by yalParser#left_op.
    def enterLeft_op(self, ctx:yalParser.Left_opContext):
        pass

    # Exit a parse tree produced by yalParser#left_op.
    def exitLeft_op(self, ctx:yalParser.Left_opContext):
        pass


    # Enter a parse tree produced by yalParser#right_op.
    def enterRight_op(self, ctx:yalParser.Right_opContext):
        pass

    # Exit a parse tree produced by yalParser#right_op.
    def exitRight_op(self, ctx:yalParser.Right_opContext):
        pass


    # Enter a parse tree produced by yalParser#array_size.
    def enterArray_size(self, ctx:yalParser.Array_sizeContext):
        pass

    # Exit a parse tree produced by yalParser#array_size.
    def exitArray_size(self, ctx:yalParser.Array_sizeContext):
        pass


    # Enter a parse tree produced by yalParser#term.
    def enterTerm(self, ctx:yalParser.TermContext):
        pass

    # Exit a parse tree produced by yalParser#term.
    def exitTerm(self, ctx:yalParser.TermContext):
        pass


    # Enter a parse tree produced by yalParser#exprtest.
    def enterExprtest(self, ctx:yalParser.ExprtestContext):
        pass

    # Exit a parse tree produced by yalParser#exprtest.
    def exitExprtest(self, ctx:yalParser.ExprtestContext):
        pass


    # Enter a parse tree produced by yalParser#while_yal.
    def enterWhile_yal(self, ctx:yalParser.While_yalContext):
        pass

    # Exit a parse tree produced by yalParser#while_yal.
    def exitWhile_yal(self, ctx:yalParser.While_yalContext):
        pass


    # Enter a parse tree produced by yalParser#if_yal.
    def enterIf_yal(self, ctx:yalParser.If_yalContext):
        pass

    # Exit a parse tree produced by yalParser#if_yal.
    def exitIf_yal(self, ctx:yalParser.If_yalContext):
        pass


    # Enter a parse tree produced by yalParser#else_yal.
    def enterElse_yal(self, ctx:yalParser.Else_yalContext):
        pass

    # Exit a parse tree produced by yalParser#else_yal.
    def exitElse_yal(self, ctx:yalParser.Else_yalContext):
        pass


    # Enter a parse tree produced by yalParser#call.
    def enterCall(self, ctx:yalParser.CallContext):
        pass

    # Exit a parse tree produced by yalParser#call.
    def exitCall(self, ctx:yalParser.CallContext):
        pass


    # Enter a parse tree produced by yalParser#arg_list.
    def enterArg_list(self, ctx:yalParser.Arg_listContext):
        pass

    # Exit a parse tree produced by yalParser#arg_list.
    def exitArg_list(self, ctx:yalParser.Arg_listContext):
        pass


    # Enter a parse tree produced by yalParser#arg.
    def enterArg(self, ctx:yalParser.ArgContext):
        pass

    # Exit a parse tree produced by yalParser#arg.
    def exitArg(self, ctx:yalParser.ArgContext):
        pass


    # Enter a parse tree produced by yalParser#array_access.
    def enterArray_access(self, ctx:yalParser.Array_accessContext):
        pass

    # Exit a parse tree produced by yalParser#array_access.
    def exitArray_access(self, ctx:yalParser.Array_accessContext):
        pass


    # Enter a parse tree produced by yalParser#scalar_access.
    def enterScalar_access(self, ctx:yalParser.Scalar_accessContext):
        pass

    # Exit a parse tree produced by yalParser#scalar_access.
    def exitScalar_access(self, ctx:yalParser.Scalar_accessContext):
        pass


    # Enter a parse tree produced by yalParser#index.
    def enterIndex(self, ctx:yalParser.IndexContext):
        pass

    # Exit a parse tree produced by yalParser#index.
    def exitIndex(self, ctx:yalParser.IndexContext):
        pass


