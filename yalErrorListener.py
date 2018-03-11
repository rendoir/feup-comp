from antlr4.error.ErrorListener import *
from pprint import pprint

RED = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

class yalErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        text_input = recognizer.getInputStream().tokenSource.inputStream.strdata
        print("\n" + text_input.split('\n')[line-1])
        for i in range(column):
            print(" ", end='')
        for i in range(len(offendingSymbol.text)):
            print(RED + "^", end='')
        print(RESET + "\n")
