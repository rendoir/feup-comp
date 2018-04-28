from antlr4 import FileStream

RED = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
UNDERLINE = '\033[4m'

class ErrorPrinter:
    def __init__(self, source=None):
        if __debug__:
            assert isinstance(source, FileStream), "ErrorPrinter.__init__() 'source' should be 'FileStream'"

        self.source = source
        self.lines = source.strdata.split('\n')
        self.errors = []
        self.warnings = []



    def addError(self, line, col, simple_msg, detail_msg):
        if __debug__:
            assert isinstance(line, int), "ErrorPrinter.reportError() 'line' should be 'int'"
            assert isinstance(col, tuple), "ErrorPrinter.reportError() 'col' should be '(int, int)'"
            assert isinstance(simple_msg, str), "ErrorPrinter.reportError() 'simple_msg' should be 'str'"
            assert isinstance(detail_msg, str), "ErrorPrinter.reportError() 'detail' should be 'str'"

        error_message = ""

        err_txt = self.lines[line-1]

        error_message += "\n" + BOLD + simple_msg + RESET + " -> " + UNDERLINE + "(" + str(line) + ":" + str(col[0]) + ")\n" + RESET
        error_message += " " + err_txt + "\n"

        print("LINE = " + str(line) + ", COL[0] = " + str(col[0]) + ", COL[1] = " + str(col[1]) + ", len = " + str(len(err_txt)))

        for i in range(-1, len(err_txt)):
            if (i >= col[0] and i <= col[1]):
                error_message += RED + "^"
            else:
                error_message += " "

        error_message += RESET + "\n - " + detail_msg + RESET

        self.errors.append(error_message)


    def addWarning(self, line, col, simple_msg, detail_msg):
        if __debug__:
            assert isinstance(line, int), "ErrorPrinter.reportError() 'line' should be 'int'"
            assert isinstance(col, tuple), "ErrorPrinter.reportError() 'col' should be '(int, int)'"
            assert isinstance(simple_msg, str), "ErrorPrinter.reportError() 'simple_msg' should be 'str'"
            assert isinstance(detail_msg, str), "ErrorPrinter.reportError() 'detail' should be 'str'"

        error_message = ""

        err_txt = self.lines[line-1]

        error_message += "\n" + UNDERLINE + simple_msg + RESET + " -> (" + str(line) + ":" + str(col[0]) + ")\n" + RESET
        error_message += " " + err_txt + "\n"

        print("LINE = " + str(line) + ", COL[0] = " + str(col[0]) + ", COL[1] = " + str(col[1]) + ", len = " + str(len(err_txt)))

        for i in range(-1, len(err_txt)):
            if (i >= col[0] and i <= col[1]):
                error_message += GREEN + "^"
            else:
                error_message += " "

        error_message += RESET + "\n - " + detail_msg + RESET

    #Prints the error messages and clears the error array
    def printMessages(self):
        print("--- BEGIN SEMANTIC ANALYZIS ---")
        for warning in self.warnings:
            print(warning)

        for error in self.errors:
            print(error)

        final_msg = "--- "
        if len(self.errors) is 1:
            final_msg += RED + str(len(self.errors))  + " ERROR"
        elif len(self.errors) > 1:
            final_msg += RED + str(len(self.errors))  + " ERRORS"
        else:
            final_msg += " 0 ERRORS"

        if len(self.warnings) is 1:
            final_msg += GREEN + str(len(self.warnings)) + " WARNING ---"
        elif len(self.warnings) > 1:
            final_msg += GREEN + str(len(self.errors))  + " WARNINGS ---"
        else:
            final_msg += " 0 WARNINGS --- " + RESET

        print(final_msg)

        self.errors[:] = []
