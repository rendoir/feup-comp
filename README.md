
# feup-comp

## Dependencies
 * [Python3](https://www.python.org/downloads/)
 * [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

It is recommended to add the ANTLR4 jar file as an alias. Dunno how it works in Windows :confused:

The parser code is in the .g4 file.

## Usage
 * Generate the parser using 'antlr4 -Dlanguage=Python3 yal.g4'
 * Run the parser using 'python3 main.py <file_name>'


## ANTLR Syntax Highlighters
 * [Atom :heart_eyes: ](https://atom.io/packages/language-antlr)
 * [Sublime Text :neutral_face:](https://github.com/iuliux/SublimeText2-Antlr-syntax)
 * [VS Code :rage: ](https://marketplace.visualstudio.com/items?itemName=mike-lischke.vscode-antlr4)
 * [IDE :scream: ](http://www.antlr.org/tools.html)

## Status

### Syntactic Analysis
 - :white_check_mark: ANTLR handles all syntactic errors
 - :white_check_mark: ANTLR handles reporting more than one syntactic error
 - :white_check_mark: Error message when no input given
 - :white_check_mark: Improve overall readability of error messages.

### Semantic Analysis

 - :white_check_mark: Check if variable has already been declared.
 - :white_check_mark: Check if variable has been initialized when it is being used.
 - :white_check_mark: Check if the variable type is correct.
   - :white_check_mark: Variable type defaults to scalar, unless variable previously declared as array
 - :white_check_mark: Cannot reassign array size

        var.size = 20; //Error

 - :white_check_mark: Comparison between arrays is not possible
 - :white_check_mark: Check if type of arguments passed on function call is valid
 - :white_check_mark: Branching declaration (variables declared/initialized within if/else must be checked)

 ### Code Generation
 - :white_check_mark: Code for function calls
 - :white_check_mark: Code for arithmetic expressions
 - :white_check_mark: Code for conditional instructions
 - :white_check_mark: Code for loops
 - :white_check_mark: Code to deal with arrays
   - :white_check_mark: Code to handle the following situation:

         a = [10];
         a = 5; //Put the number 5 in all position of the array

 #### Additional Notes
 - limit locals assumes that the first argument of main function is constantly used

### Optimizations
 - :white_check_mark: Constant propagation
   - Works for both local variables and module variables
 
 - :white_check_mark: Constant folding
 - :white_check_mark: While and If templating (saves 1 goto)
 - :white_check_mark: Lower cost instruction selection
   
   - Checks the size of the constants to use and uses the lowest available instruction from bipush, sipush and ldc.
   - Uses iload_#, istore_# when available
   - Uses iinc when possible, even for subtraction, in which case the compiler changes the constant signal
   
- :white_check_mark: Algebraic Simplification
   
   - Sums/Subtractions by 0
   - Multiplications by 1 or 0
   - Divisions by self or 1
   - Bitwise-Shifts by 0
  
