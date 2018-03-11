from antlr4.error.ErrorListener import *
from pprint import pprint

class yalErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        text_input = recognizer.getInputStream().tokenSource.inputStream.strdata
        print("\n" + text_input.split('\n')[line-1])
        for i in range(column):
            print(" ", end='')
        print("^")
