grammar Parser;

vector: '{' primitive (',' primitive)* '}';

primitive: vector | expression | string;

expression: INT
  | sum_
  | difference
  | multiplication
  | division;

sum_: INT '+' expression;
difference: INT '/' expression;
multiplication: INT '*' expression;
division: INT '/' expression;

string: '"' CHAR '"';

CHAR: [a-zA-Z]+;
INT: [0-9]+;
WS : [ \t\r\n]+ -> skip;

PRIMITIVE_TYPE: 'int' | 'char' | 'string';
VISIBILITY: 'public' | 'private' | 'protected';

variable: PRIMITIVE_TYPE string (',' string)* ';';

pyClass: 'class ' ID '{' class_body '};';
class_body:
  ( variable
  | class_access
  | class_method
  )*?;
ID: [a-zA-Z0-9]*;
class_access: VISIBILITY':';
class_method: PRIMITIVE_TYPE string '(' function_args ');'; //Needs to be added the function body later on

function_args: ((PRIMITIVE_TYPE string)? | PRIMITIVE_TYPE string (',' PRIMITIVE_TYPE)*);
