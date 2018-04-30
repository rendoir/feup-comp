grammar yal;

// These symbols need to be here, so that these are matched first.
// It works as a reserved keyword catcher
REL_OP: '>' | '<' | '<=' | '>=' | '==' | '!=';
ADDSUB_OP: '+' | '-';
ART_OP: '*' | '/' | '<<' | '>>' | '>>>';
BTW_OP: '&' | '|' | '^';
NOT_OP: '!';
WHILE: 'while';
IF: 'if';
ELSE: 'else';
ASS_OP: '=';
ASPA: '"';
LPAR: '(';
RPAR: ')';
COMMA: ',';
D_COMMA: ';';
L_BRACKET: '{';
R_BRACKET: '}';
FUNC: 'function';
MODULE: 'module';
SIZE: 'size';

module: MODULE ID L_BRACKET declaration* function* R_BRACKET;

declaration: (array_element | scalar_element)
    (ASS_OP (('[' array_size ']') | ADDSUB_OP? NUMBER))? D_COMMA;

function: ((FUNC (array_element | scalar_element) ASS_OP ID LPAR var_list? RPAR) | (FUNC ID LPAR var_list? RPAR)) L_BRACKET stmt_list R_BRACKET;

var_list: (array_element | scalar_element) (COMMA (array_element | scalar_element))*;
array_element: ID '[' ']';
scalar_element: ID;
stmt_list: stmt*;
stmt: while_yal | if_yal | assign | (call D_COMMA);
assign: left_op ASS_OP right_op D_COMMA;
left_op: array_access | scalar_access;
right_op: (term ((ART_OP | BTW_OP | ADDSUB_OP) term)?) | '[' array_size ']';
array_size: scalar_access | NUMBER;
term: ADDSUB_OP? (NUMBER | call | array_access | scalar_access);
exprtest: LPAR left_op REL_OP right_op RPAR;
while_yal: WHILE exprtest L_BRACKET stmt_list R_BRACKET;
if_yal: IF exprtest L_BRACKET stmt_list R_BRACKET else_yal?;
else_yal:  ELSE L_BRACKET stmt_list R_BRACKET;
call: ID ('.' ID)? LPAR arg_list? RPAR;
arg_list: arg (COMMA arg)*;
arg: (ID | STRING | NUMBER);
array_access: ID '[' index ']';
scalar_access: ID ('.' SIZE)?;
index: (ID | NUMBER);

ID: LETTER (LETTER | DIGIT)*;
LETTER: [_a-zA-Z];
NUMBER: [0-9]+;
DIGIT: [0-9];
STRING: '"' [a-zA-Z0-9:= ]* '"';


// ignore all comments and spaces, newlines and such
SPACES_AND_SUCH: [ \t\n\r] -> skip;
LINE_COMMENT: '//' (~[\n\r])* ('\n' | '\r' | '\r\n') -> skip;
MULTI_COMMENT: '/*' .*? '*/' -> skip;
