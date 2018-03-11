import sys
from antlr4 import *
from antlr4.error.ErrorStrategy import *
from antlr4.error.Errors import *
from pprint import pprint

class yalErrorStrategy(DefaultErrorStrategy):
    def reportInputMismatch(self, recognizer:Parser, e:InputMismatchException):
        msg = "mismatched input " + self.getTokenErrorDisplay(e.offendingToken) \
              + " expecting " + e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)
