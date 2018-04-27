from antlr4 import FileStream

RED = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

class ErrorPrinter:
    def __init__(self, source=None):
        if __debug__:
            assert isinstance(source, FileStream), "ErrorPrinter.__init__() 'source' should be 'FileStream'"

        self.source = source
        self.lines = source.strdata.split('\n')



    def reportError(self, line, col, err, msg):
        if __debug__:
            assert isinstance(line, int), "ErrorPrinter.reportError() 'line' should be 'int'"
            assert isinstance(col, (int, int)), "ErrorPrinter.reportError() 'col' should be '(int, int)'"
            assert isinstance(err, (int, int)), "ErrorPrinter.reportError() 'err' should be '(int, int)'"
            assert isinstance(msg, str), "ErrorPrinter.reportError() 'msg' should be 'str'"

        err_txt = self.lines[line-1][start_col, end_col]
        start_err -= start_col
        end_err -= end_col

        print(err_txt)
        for i in range(end_err):
            if i >= start_err:
                print(RED + "^", end='')
            else:
                print(" ", end='')

        print(RESET + "\n - " + msg + "\n")
