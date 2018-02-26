grammar yal;

REL_OP: '>' | '<' | '<=' | '>=' | '==' | '!=';
ADD_OP: '+';
SUB_OP: '-';
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

var_name: LETTER (LETTER | DIGIT)*;
literal: STRING | NUMBER;

expression: var_name '=' literal ';';


LETTER: [_a-zA-Z];
NUMBER: [0-9]+;
DIGIT: [0-9];
STRING: '"' [a-zA-Z0-9:= ]* '"';


// ignore all comments and spaces, newlines and such
SPACES_AND_SUCH: [ \t\n\r] -> skip;
LINE_COMMENT: '//' (~[\n\r])* ('\n' | '\r' | '\r\n') -> skip;
MULTI_COMMENT: '/*' .*? '*/' -> skip;
