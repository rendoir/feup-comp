
# YAL Compiler G43

This project was developed in the Compilers course of MIEIC at FEUP. It's goal is to compile the yal language into java bytecode, to be executed by a JVM.

## Dependencies
 * [Python3](https://www.python.org/downloads/)
 * [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

It is recommended to add the ANTLR4 jar file as an alias. Dunno how it works in Windows :confused:

The parser code is in the .g4 file.

## Usage
 * Generate the parser using 'antlr4 -Dlanguage=Python3 yal.g4'
 * Run the parser using:
        
       Usage:
         python3 main.py <file_name> [options]
        
       Arguments:
         file_name  - The absolute or relative path to the file to compile.
        
       Options:
         --quiet         (-q)     - Runs the compiler silently, without any print to the console. Used for the testing script
         --register=<n>  (-r=<n>) - Limits the number of registers to the number in '<n>'
         --optimized     (-o)     - Optimizes the code generated

## Compiler Status

### Syntactic Analysis
 Most of the work here is done by the ANTLR tool that we used. It's main limitations are skipping a whole rule in case of failure. This is fine in most cases, however should there be a semantic error on the header of a function, until that error is corrected, no other syntactic error will be reported for that given function.
 
 
 - :white_check_mark: ANTLR handles all syntactic errors
 - :white_check_mark: ANTLR handles reporting more than one syntactic error
 - :white_check_mark: Error message when no input given
 - :white_check_mark: Improve overall readability of error messages.

### Semantic Analysis
 - :white_check_mark: Variables not defined in the current scope
 - :white_check_mark: Variables used before being initialized
 - :white_check_mark: Return variable of function not being initialized before function end
 - :white_check_mark: Undefined function in current module
 - :white_check_mark: Comparison between arrays is impossible.
        
      - In this case the compiler suggests to compare the <i>size</i> of both arrays.
        
 - :white_check_mark: Applying operators to arrays.
        
      - Suggest the use of <i>array.size</i>
    
 - :white_check_mark: Assigning <i>size</i> directly.
        
      - Suggests the use of <array> = [<n>]
        
 - :white_check_mark: Different assignment types.
 - :white_check_mark: Variable NaN as array size.
 - :white_check_mark: Accessing non-array variables by index
 - :white_check_mark: Out of bounds array accesses. (When possible)
 
 - :white_check_mark: Accessing <i>size</i> property of non-array variable
 - :white_check_mark: Positive array size numbers.
        
      - Suggests the number must be positive
 
 - :white_check_mark: Function redeclaration
 - :white_check_mark: <i>arrSizeFromArr</i>
 - :white_check_mark: Applying operator between diferent variable types
 - :white_check_mark: Wrong function argument list.
        
      - Shows what was expected and what it got.
        
 - :white_check_mark: Variable declared in a single <i>if</i> branch, but used after <i>if</i>
        
      - Suggests declaring the variable in all possible code branches
        
 - :white_check_mark: Variable already defined
        
      - This is merely a warning that pop's up on the following case:
        
                module mod {
                a;
                b = 2;
                a; // Variable already defined, ignoring this line
                }
        
 ### Code Generation
 - :white_check_mark: Code for function calls
 - :white_check_mark: Code for arithmetic expressions
 - :white_check_mark: Code for conditional instructions
 - :white_check_mark: Code for loops
 - :white_check_mark: Code to deal with arrays
   - :white_check_mark: Code to handle the following situation:

         a = [10];
         a = 5; //Put the number 5 in all position of the array
         
 - :white_check_mark: Branching variables declaration

### Intermediate Representations
To aid in the development of our compiler, the compiler goes through 2 stages of intermediate representation. 

#### High-Level Intermediate Representation
This representation has the following architecture:

#### Low-Level Intermediate Representation
This representation has the following architecture:

### Code Generation
Using the above mentioned LLIR, code generation becomes a lot easier, as all instructions from the HIR are now translated into simple <i>load</i> and <i>store</i> instructions. 
No third-party libraries were used.

### Optimizations
Our code uses as a default the <i>while</i> templating, even without the <i>-o</i> flag.

The following optimizations are made when that flag is activated:

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
  
### Test Suite
To ensure that at every iteration of the compiler development there were no new bugs inserted, or some regression in functionality we setup multiple test suites to that end.

### Task Distribution
We aimed to keep the task distribution fairly uniform among the group members. At every iteration everyone would help as much as they were able to, however we believe these people stood out in the following areas:

- <b>Daniel Marques</b>

	- Development of the to-be data flow analysis and graph coloring.
	- Refinement of the syntactic analysis results.

- <b>Gonçalo Moreno</b>
	
	- I helped develop the code for the semantic analysis and the associated HIR.
	- Parsing the HIR to a LIR

- <b>João Carvalho</b>

	- Building the HIR and integrating it with the semantic analysis.
	- Continuously testing the project for any errors my colleagues might have missed.
	- Passing the grammar from JavaCC to ANTLR, and starting and keep python's good coding practices. 

- <b>João Almeida</b>

	- Responsible for the generation of the code and the LIR
	- Development of the test suite.


## The Group
 - <b>NAME1:</b> Daniel Filipe Santos Marques, NR1: 201503822, GRADE1: 18.5, CONTRIBUTION1: 25%
 - <b>NAME2:</b> Gonçalo Vasconcelos Cunha Miranda Moreno, NR2: 201503871, GRADE2: 18.5, CONTRIBUTION2: 25%
 - <b>NAME3:</b> João Filipe Lopes de Carvalho, NR3: 201504875, GRADE3: 18.5, CONTRIBUTION3: 25%
 - <b>NAME4:</b> João Francisco Barreiros de Almeida, NR4: 201505866, GRADE4: 18.5, CONTRIBUTION4: 25%
 
        
