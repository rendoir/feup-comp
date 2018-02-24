# Generated from Parser.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ParserParser import ParserParser
else:
    from ParserParser import ParserParser

# This class defines a complete listener for a parse tree produced by ParserParser.
class ParserListener(ParseTreeListener):

    # Enter a parse tree produced by ParserParser#vector.
    def enterVector(self, ctx:ParserParser.VectorContext):
        pass

    # Exit a parse tree produced by ParserParser#vector.
    def exitVector(self, ctx:ParserParser.VectorContext):
        pass


    # Enter a parse tree produced by ParserParser#primitive.
    def enterPrimitive(self, ctx:ParserParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by ParserParser#primitive.
    def exitPrimitive(self, ctx:ParserParser.PrimitiveContext):
        pass


    # Enter a parse tree produced by ParserParser#expression.
    def enterExpression(self, ctx:ParserParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ParserParser#expression.
    def exitExpression(self, ctx:ParserParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ParserParser#sum_.
    def enterSum_(self, ctx:ParserParser.Sum_Context):
        pass

    # Exit a parse tree produced by ParserParser#sum_.
    def exitSum_(self, ctx:ParserParser.Sum_Context):
        pass


    # Enter a parse tree produced by ParserParser#difference.
    def enterDifference(self, ctx:ParserParser.DifferenceContext):
        pass

    # Exit a parse tree produced by ParserParser#difference.
    def exitDifference(self, ctx:ParserParser.DifferenceContext):
        pass


    # Enter a parse tree produced by ParserParser#multiplication.
    def enterMultiplication(self, ctx:ParserParser.MultiplicationContext):
        pass

    # Exit a parse tree produced by ParserParser#multiplication.
    def exitMultiplication(self, ctx:ParserParser.MultiplicationContext):
        pass


    # Enter a parse tree produced by ParserParser#division.
    def enterDivision(self, ctx:ParserParser.DivisionContext):
        pass

    # Exit a parse tree produced by ParserParser#division.
    def exitDivision(self, ctx:ParserParser.DivisionContext):
        pass


    # Enter a parse tree produced by ParserParser#string.
    def enterString(self, ctx:ParserParser.StringContext):
        pass

    # Exit a parse tree produced by ParserParser#string.
    def exitString(self, ctx:ParserParser.StringContext):
        pass


    # Enter a parse tree produced by ParserParser#variable.
    def enterVariable(self, ctx:ParserParser.VariableContext):
        pass

    # Exit a parse tree produced by ParserParser#variable.
    def exitVariable(self, ctx:ParserParser.VariableContext):
        pass


    # Enter a parse tree produced by ParserParser#pyClass.
    def enterPyClass(self, ctx:ParserParser.PyClassContext):
        pass

    # Exit a parse tree produced by ParserParser#pyClass.
    def exitPyClass(self, ctx:ParserParser.PyClassContext):
        pass


    # Enter a parse tree produced by ParserParser#class_body.
    def enterClass_body(self, ctx:ParserParser.Class_bodyContext):
        pass

    # Exit a parse tree produced by ParserParser#class_body.
    def exitClass_body(self, ctx:ParserParser.Class_bodyContext):
        pass


    # Enter a parse tree produced by ParserParser#class_access.
    def enterClass_access(self, ctx:ParserParser.Class_accessContext):
        pass

    # Exit a parse tree produced by ParserParser#class_access.
    def exitClass_access(self, ctx:ParserParser.Class_accessContext):
        pass


    # Enter a parse tree produced by ParserParser#class_method.
    def enterClass_method(self, ctx:ParserParser.Class_methodContext):
        pass

    # Exit a parse tree produced by ParserParser#class_method.
    def exitClass_method(self, ctx:ParserParser.Class_methodContext):
        pass


    # Enter a parse tree produced by ParserParser#function_args.
    def enterFunction_args(self, ctx:ParserParser.Function_argsContext):
        pass

    # Exit a parse tree produced by ParserParser#function_args.
    def exitFunction_args(self, ctx:ParserParser.Function_argsContext):
        pass


