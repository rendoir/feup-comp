
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

## TODO

### Symbol Table

 - :x: Storing function variables in the same place.

### Semantic Analysis

 - :x: Check if variable has already been declared.
 - :x: Check if variable has been initialized when it is being used.
 - :x: Check if the variable type is correct.
   - Variable type defaults to scalar, unless variable previously declared as array
 - :x: Cannot reassign array size

        var.size = 20; //Error

 - :x: Comparison between arrays is not possible
 - :x: Branching declaration (variables declared/initialized within if/else must be checked)
 
 ### Code Generation
 - :x: Code for function calls
 - :x: Code for arithmetic expressions
