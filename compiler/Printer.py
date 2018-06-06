from antlr4 import FileStream

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

UNDEFINED_VAR = "Undefined variable"
NOT_INITIALIZED = "Variable not initialized"
RET_NOT_INITIALIZED = "Return variable not initialized"
UNDEFINED_FUNC = "Undefined function"
UNKNOWN_COMP = "Unknown comparison"
UNKNOWN_OP = "Unknown operation"
SIZE_ASSIGN = "Size assignment"
DIFF_TYPES = "Types do not match"
NAN_ARR_SIZE = "Unkown array size"
NUMBER_INDEX = "Indexing impossible"
OUT_OF_BOUNDS = "Out of bounds"
NUM_SIZE = "NUM has no size"
NEG_SIZE = "Negative array size"
FUNC_REDECLARED = "Function redeclared"
WRONG_ARGS = "Wrong arguments"
BRANCHING_DIFF = "Variable type unknown"
BRANCH_DECL = "Variable may not be declared"

ALREADY_DEF = "Variable already defined"

def printUsage():
    print("\nUsage:")
    print("    python3 main.py <file_name> [options]\n")
    print("Arguments:")
    print(BOLD + "     file_name" + RESET + "   - Relative or absolute path to the file to compile\n")
    print("Options:")
    print(BOLD + "     --quiet     " + RESET + "(-q)      - Runs the compiler silently. Used mostly for testing the compiler")
    print(BOLD + "     --optimized " + RESET + "(-o)      - Optimizes the code generated")



class ErrorPrinter:
    def __init__(self, source=None):
        if __debug__:
            assert isinstance(source, FileStream), "ErrorPrinter.__init__() 'source' should be 'FileStream'"

        self.source = source
        self.lines = source.strdata.split('\n')
        self.errors = []
        self.warnings = []

    def cropString(string: str) -> (str, int):
        ltrim = string.lstrip()
        left_trimmed = len(string) - len(ltrim)

        alltrim = ltrim.strip()

        return (alltrim, left_trimmed)

    def __addError(self, line, col, simple_msg, detail_msg):
        if __debug__:
            assert isinstance(line, int), "ErrorPrinter.reportError() 'line' should be 'int'"
            assert isinstance(col, tuple), "ErrorPrinter.reportError() 'col' should be '(int, int)'"
            assert isinstance(simple_msg, str), "ErrorPrinter.reportError() 'simple_msg' should be 'str'"
            assert isinstance(detail_msg, str), "ErrorPrinter.reportError() 'detail' should be 'str'"

        error_message = ""

        (err_txt, del_spaces) = ErrorPrinter.cropString(self.lines[line-1])
        line_col =  str(line) + ":" + str(col[0])

        error_message += "\n" + BOLD + simple_msg + "\n" + RESET
        error_message += RED + line_col + RESET + " |  " + err_txt + "\n"

        jump = len(line_col) + 4

        col_start = col[0] - del_spaces
        col_end = col[1] - del_spaces
        for i in range(-jump, len(err_txt)):
            if (i >= col_start and i <= col_end):
                error_message += RED + "^"
            else:
                error_message += " "

        error_message += RESET + "\n - " + detail_msg + RESET

        self.errors.append(error_message)

    def __suggestion(text: str) -> str:
        return "\n " + BOLD + "---> " + RESET + text

    def __addWarning(self, line, col, simple_msg, detail_msg):
        if __debug__:
            assert isinstance(line, int), "ErrorPrinter.reportError() 'line' should be 'int'"
            assert isinstance(col, tuple), "ErrorPrinter.reportError() 'col' should be '(int, int)'"
            assert isinstance(simple_msg, str), "ErrorPrinter.reportError() 'simple_msg' should be 'str'"
            assert isinstance(detail_msg, str), "ErrorPrinter.reportError() 'detail' should be 'str'"

        warn_msg = ""

        (err_txt, del_spaces) = ErrorPrinter.cropString(self.lines[line-1])
        line_col =  str(line) + ":" + str(col[0])

        warn_msg += "\n" + UNDERLINE + simple_msg + "\n" + RESET
        warn_msg += GREEN + line_col + RESET + " | " + err_txt + "\n"
        jump = len(line_col) + 3
        col_start = col[0] - del_spaces
        col_end = col[1] - del_spaces

        for i in range(-jump, len(err_txt)):
            if (i >= col_start and i <= col_end):
                warn_msg += GREEN + "^"
            else:
                warn_msg += " "

        warn_msg += RESET + "\n - " + detail_msg + RESET
        self.warnings.append(warn_msg)

    def __readyArgs(self, func_name, args) -> str:
        args_msg = func_name + "("
        remove = False
        for arg in args:
            remove = True
            args_msg += arg.type + ", "
        if remove:
            args_msg = args_msg[:-2]
        args_msg += ")"

        return args_msg

    #Prints the error messages and clears the error array
    # Returns true if there was a semantic error
    def printMessages(self, verbose) -> bool:
        if not verbose:
            return len(self.errors) > 0
        else:
            error = True
            if len(self.errors) > 0 or len(self.warnings) > 0:
                print("--- BEGIN SEMANTIC ANALYZIS ---")

            for error in self.errors:
                print(error)

            final_msg = ""
            if len(self.errors) is 1:
                final_msg += RED + "--- " + str(len(self.errors))  + " ERROR "
            elif len(self.errors) > 1:
                final_msg += RED + "--- " + str(len(self.errors))  + " ERRORS "
            else:
                error = False
                final_msg += " --- 0 ERRORS "

            for warning in self.warnings:
                print(warning)

            if len(self.warnings) is 1:
                final_msg += GREEN + str(len(self.warnings)) + " WARNING  ---" + RESET
            elif len(self.warnings) > 1:
                final_msg += GREEN + str(len(self.errors))  + " WARNINGS ---" + RESET
            else:
                final_msg += " 0 WARNINGS --- " + RESET

            if len(self.errors) > 0 or len(self.warnings) > 0:
                print("\n" + final_msg)

            self.errors[:] = []
            return error

    # ----- ERROR MESSAGES -------

    def undefVar(self, line, cols, var_name):
        new_cols = (cols[0], cols[1] + len(var_name) - 1)
        self.__addError(line, new_cols, UNDEFINED_VAR, "Variable " + var_name + " is not defined in scope")

    def notInitialized(self, line, cols, var_name):
        new_cols = (cols[0], cols[1] + len(var_name) - 1)
        self.__addError(line, new_cols, NOT_INITIALIZED, "Variable '" + var_name + "' used before initialization")

    def retNotInitialized(self, line, cols, var_name, func_name):
        new_cols = (cols[0], len(self.lines[line+1]))
        self.__addError(line, new_cols, RET_NOT_INITIALIZED, "Return variable '" + var_name + "' of function '" + func_name + "' not inititialized at function end");

    def undefFunc(self, line, cols, func_name):
        self.__addError(line, cols, UNDEFINED_FUNC, "Could not find '" + func_name + "' in current module!" + ErrorPrinter.__suggestion("Maybe it belongs to another module"))

    def unknownComp(self, line, cols, left_var, op, right_var):
        self.__addError(line, cols, UNKNOWN_COMP, "Comparison between two arrays is not possible!" + ErrorPrinter.__suggestion("Maybe you mean '" + left_var + ".size " + op + " " + right_var + ".size'"))

    def unknownOp(self, line, cols, left_var, op, right_var):
        self.__addError(line, cols, UNKNOWN_OP, "Applying '" + op + "' operator to arrays is not possible!" + ErrorPrinter.__suggestion("Maybe you mean '" + left_var + ".size " + op + " " + right_var + ".size'"))

    def sizeAssign(self, line, cols, var, new_size):
        self.__addError(line, cols, SIZE_ASSIGN, "Tried to set '" + var + "' size directly, which is not possible!" + ErrorPrinter.__suggestion("Maybe you mean '" + var + " = [" + str(new_size) + "]'"))

    def diffTypes(self, line, cols, var, var_type, ass_type):
        self.__addError(line, cols, DIFF_TYPES, "Assigning '" + ass_type + "' to '" + var + "' which is of type '" + var_type + "' is not possible")

    def arrSizeNaN(self, line, cols, type, var_name):
        self.__addError(line, cols, NAN_ARR_SIZE, "Tried to use variable of type '" + type + "' as array index!" + ErrorPrinter.__suggestion("Maybe you mean '" + var_name + ".size'"))

    def numberIndexing(self, line, cols, var_name, var_type):
        self.__addError(line, cols, NUMBER_INDEX, "Indexing variable '" + var_name + "' which is of type '" + var_type + "' is not possible!")

    def outOfBounds(self, line, cols, var_name, max_size, accessed):
        self.__addError(line, cols, OUT_OF_BOUNDS, "Indexed position #" + accessed + " when '" + var_name + "' only has #" + max_size + " positions" + ErrorPrinter.__suggestion("(Indexing starts at 0)"))

    def numSize(self, line, cols, var_name, var_type):
        self.__addError(line, cols, NUM_SIZE, "Tried to access property 'size' of variable '" + var_name + "' which is of type '" + var_type + "'" + ErrorPrinter.__suggestion("Property 'size' is only available in ARR"))

    def negSize(self, line, cols, size):
        self.__addError(line, cols, NEG_SIZE, "It is not possible to create an array with " + size + " positions!" + ErrorPrinter.__suggestion("Array size must be a positive number"))

    def funcRedeclaration(self, line, cols, name):
        name_start = self.lines[line-1].find(name)
        self.__addError(line, (name_start, name_start + len(name) - 1), FUNC_REDECLARED, "Function '" + name + "' redeclared")

    def arrSizeFromArr(self, line, cols, name):
        self.__addError(line, cols, UNKNOWN_OP, "Used variable '" + name + "' which is of type 'ARR', as array size!" + ErrorPrinter.__suggestion("Maybe you mean '" + name +  ".size'"))

    def opDiffTypes(self, line, cols, var1_type, op, var2_type):
        self.__addError(line, cols, UNKNOWN_OP, "Applying operator '" + op + "' between '" + var1_type + "' and '" + var2_type + "' is not possible!")

    def wrongArgs(self, line, cols, func_name, expected, got):
        expected_msg = self.__readyArgs(func_name, expected)
        got_msg = self.__readyArgs(func_name, got)

        self.__addError(line, cols, WRONG_ARGS, "Expected: " + expected_msg + "\n - Got: " + got_msg)

    def branchingVars(self, line, cols, var_name, type1, type2):
        new_cols = (cols[0], cols[1] + len(var_name) - 1)
        self.__addError(line, new_cols, BRANCHING_DIFF, "Cannot infer type for '" + var_name + "'!" + ErrorPrinter.__suggestion("First branched declared as '" + type1 + "', second branch declared as '" + type2 + "'"))

    def branchingDecl(self, line, cols, var_name):
        new_cols = (cols[0], cols[1] + len(var_name) - 1)
        self.__addError(line, new_cols, BRANCH_DECL, "Variable '" + var_name + "' only declared on one branch of the code!" + ErrorPrinter.__suggestion("Try declaring it in all possible branching of the code"))
    # ----- WARNING MESSAGES ----

    def alreadyDefined(self, line, cols, name):
        self.__addWarning(line, cols, ALREADY_DEF, "Variable '" + name + "' already defined! Ignoring this line of code")
