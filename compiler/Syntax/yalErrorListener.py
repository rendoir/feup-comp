from antlr4.error.ErrorListener import *
from .. import Printer
from pprint import pprint

RED         = "\033[1;31m"
GREEN       = "\033[0;32m"
YELLOW      = "\033[1;33m"
BLUE        = "\033[1;34m"
MAGENTA     = "\033[1;35m"
CYAN        = "\033[1;36m"
RESET       = "\033[0;0m"
BOLD        = "\033[;1m"
REVERSE     = "\033[;7m"
UNDERLINE   = '\033[4m'

SUBST = {
    'REL_OP'      : "['>', '<', '<=', '>=', '==', '!=']",
    'ADDSUB_OP'   : "['+', '-']",
    'ART_OP'      : "['*', '/', '<<', '>>', '>>>']",
    'BTW_OP'      : "['&', '|', '^']",
    'NOT_OP'      : "'!'",
    'ASS_OP'      : "'='",
    'ASPA'        : "'\"'",
    'LPAR'        : "'('",
    'RPAR'        : "')'",
    'COMMA'       : "','",
    'D_COMMA'     : "';'",
    'L_BRACKET'   : "'{'",
    'R_BRACKET'   : "'}'",
    'FUNC'        : "'function'",
    'MODULE'      : "'module'",
    'SIZE'        : "'size'"
}

class yalErrorListener(ErrorListener):
    def __init__(self, verbose):
        super(yalErrorListener, self).__init__()
        self.verbose = verbose

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if self.verbose:
            text_input = recognizer.getInputStream().tokenSource.inputStream.strdata
            code_line = text_input.split('\n')[line-1]
            (trimmed_line, trim_n) = Printer.ErrorPrinter.cropString(code_line)
            line_col = str(line) + ':' + str(column)

            print(BOLD + yalErrorListener.replaceConstants(msg) + RESET)
            print(RED + line_col + RESET + ' |  ' + trimmed_line)
            for i in range(column-trim_n + len(line_col) + 4):
                print(" ", end='')
            for i in range(len(offendingSymbol.text)):
                print(RED + "^", end='')

            print(RESET + "\n")


    def replaceConstants(code_line) -> str:
        for (old, new) in SUBST.items():
            code_line = code_line.replace(old, new)
        return code_line
