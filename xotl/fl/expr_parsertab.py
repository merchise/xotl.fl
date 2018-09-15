
# expr_parsertab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftKEYWORD_WHEREleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW ATTR_ACCESS BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON DATE DATETIME DATETIME_INTERVAL DATE_INTERVAL DOT_OPERATOR DOUBLESLASH EQ FLOAT KEYWORD_CLASS KEYWORD_DATA KEYWORD_IN KEYWORD_INSTANCE KEYWORD_LET KEYWORD_WHERE LBRACKET LOWER_IDENTIFIER LPAREN MINUS NEWLINE OPERATOR PADDING PERCENT PIPE PLUS RBRACKET RPAREN SLASH SPACE STAR STRING TICK_OPERATOR UNDER_IDENTIFIER UPPER_IDENTIFIERexpr_factor : expr_factor SPACE expr_factorexpr_factor : ATTR_ACCESS\n    expr_term9 : expr_factor infixr_operator_9 expr_term9\n               | expr_factor\n\n    expr_term7 : expr_term7 infixl_operator_7 expr_term9\n               | expr_term9\n\n    expr_term6 : expr_term6 infixl_operator_6 expr_term7\n               | expr_term7\n\n    expr_term2 : expr_term2 infixl_operator_2 expr_term6\n               | expr_term6\n\n    expr_term1 : expr_term2 infixr_operator_2 expr_term1\n               | expr_term2\n\n    expr_term0 : expr infixl_operator_0 expr_term0\n               | expr_term1\n\n    \n    st_expr : expr\n\n    expr : expr_term0\n\n    expr_factor : literal\n                | identifier\n                | enclosed_expr\n                | unit_value\n                | letexpr\n                | where_expr\n                | lambda_expr\n\n    st_type_expr : type_expr\n\n    literal : number\n             | concrete_number\n             | string\n             | char\n             | date\n             | datetime\n             | date_interval\n             | datetime_interval\n    date : DATE\n    datetime : DATETIME\n    date_interval : DATE_INTERVAL\n    datetime_interval : DATETIME_INTERVAL\n    unit_value : LPAREN RPAREN\n    char : CHARstring : STRINGidentifier : _identifier\n\n    _identifier : UNDER_IDENTIFIER\n                   | UPPER_IDENTIFIER\n                   | LOWER_IDENTIFIER\n\n    enclosed_expr : LPAREN expr RPARENexpr_factor : enclosed_expr expr_factor\n                   | expr_factor enclosed_expr\n    enclosed_expr : LPAREN DOT_OPERATOR RPAREN\n                     | LPAREN operator RPAREN\n    \n    infixr_operator_9 : DOT_OPERATOR\n\n    infixl_operator_7 : STAR\n                     | SLASH\n                     | DOUBLESLASH\n                     | PERCENT\n\n    infixl_operator_6 : PLUS\n                     | MINUS\n\n    infixr_operator_2 : COLON\n\n    infixl_operator_2 : OPERATOR\n                     | ARROW\n\n    infixl_operator_0 : TICK_OPERATOR\n\n    operator : infixl_operator_0\n             | infixl_operator_2\n             | infixr_operator_2\n             | infixl_operator_6\n             | infixl_operator_7\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : lambda_expr : BACKSLASH parameters ARROW expr\n    parameters : _identifier _parameters\n       _parameters : SPACE _identifier _parameters\n    _parameters : empty\n    pattern : parametersequation : pattern EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    \n    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr\n\n    \n    where_expr : expr KEYWORD_WHERE SPACE equations\n    where_expr : expr KEYWORD_WHERE PADDING equations\n    type_expr : type_function_expr\n                 | type_termtype_function_expr : type_term ARROW _maybe_padding type_function_expr\n                          | type_term\n    type_term : type_app_expression\n                 | type_factortype_app_expression : type_factor _app_args_non_empty_app_args : SPACE type_factor _app_args\n       _app_args_non_empty : SPACE type_factor _app_args\n    _app_args : emptytype_variable : LOWER_IDENTIFIERtype_cons : UPPER_IDENTIFIERtype_factor : type_variable\n                   | type_cons\n\n    type_factor : LPAREN _maybe_padding type_expr _maybe_padding RPARENtype_factor : LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET_maybe_padding : PADDING\n                      | empty\n    program : definitions\n    definitions : definition _definition_set\n    _definition_set : NEWLINE definition _definition_set\n    _definition_set : empty\n    definition : nametype_decl\n                  | valuedef\n                  | datatype_definition\n    valuedef : equation\n    nametype_decl : _identifier COLON COLON st_type_expr\n    datatype_definition : _datatype_lhs EQ _data_rhs\n    _datatype_lhs : KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params\n    _cons_params : SPACE LOWER_IDENTIFIER _cons_params\n    _cons_params : empty\n    _data_rhs : data_cons _data_conses\n       _data_conses : _maybe_padding PIPE data_cons _data_conses\n    _data_conses : emptydata_cons : _data_cons_data_cons : UPPER_IDENTIFIER _cons_args_cons_args : SPACE cons_arg _cons_args\n    _cons_args : empty\n    cons_arg : type_variable\n       cons_arg : type_cons\n       cons_arg : _cons_arg_factor\n    _cons_arg_factor : LPAREN type_expr RPAREN\n    _cons_arg_factor : LBRACKET type_expr RBRACKET\n    '
    
_lr_action_items = {'ATTR_ACCESS':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[10,10,10,10,-59,10,10,-56,-57,-58,10,-54,-55,10,-50,-51,-52,-53,10,10,-49,10,-44,-47,-48,10,10,10,]),'LPAREN':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,100,104,105,107,109,110,111,113,114,115,117,118,],[27,-15,-16,-14,-12,-10,-8,-6,64,-2,-17,-18,27,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,27,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,27,-59,27,27,-56,-57,-58,27,-54,-55,27,-50,-51,-52,-53,27,27,-46,-49,27,64,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,27,-84,-85,-80,-82,27,-74,27,-73,-79,-83,-81,]),'KEYWORD_LET':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[28,28,28,28,-59,28,28,-56,-57,-58,28,-54,-55,28,-50,-51,-52,-53,28,28,-49,28,-44,-47,-48,28,28,28,]),'BACKSLASH':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[29,29,29,29,-59,29,29,-56,-57,-58,29,-54,-55,29,-50,-51,-52,-53,29,29,-49,29,-44,-47,-48,29,29,29,]),'BASE10_INTEGER':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[30,30,30,30,-59,30,30,-56,-57,-58,30,-54,-55,30,-50,-51,-52,-53,30,30,-49,30,-44,-47,-48,30,30,30,]),'BASE16_INTEGER':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[31,31,31,31,-59,31,31,-56,-57,-58,31,-54,-55,31,-50,-51,-52,-53,31,31,-49,31,-44,-47,-48,31,31,31,]),'BASE8_INTEGER':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[32,32,32,32,-59,32,32,-56,-57,-58,32,-54,-55,32,-50,-51,-52,-53,32,32,-49,32,-44,-47,-48,32,32,32,]),'BASE2_INTEGER':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[33,33,33,33,-59,33,33,-56,-57,-58,33,-54,-55,33,-50,-51,-52,-53,33,33,-49,33,-44,-47,-48,33,33,33,]),'FLOAT':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[34,34,34,34,-59,34,34,-56,-57,-58,34,-54,-55,34,-50,-51,-52,-53,34,34,-49,34,-44,-47,-48,34,34,34,]),'STRING':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,67,93,94,95,100,110,113,],[35,35,35,35,-59,35,35,-56,-57,-58,35,-54,-55,35,-50,-51,-52,-53,35,35,-49,35,35,-44,-47,-48,35,35,35,]),'CHAR':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,67,93,94,95,100,110,113,],[36,36,36,36,-59,36,36,-56,-57,-58,36,-54,-55,36,-50,-51,-52,-53,36,36,-49,36,36,-44,-47,-48,36,36,36,]),'DATE':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[37,37,37,37,-59,37,37,-56,-57,-58,37,-54,-55,37,-50,-51,-52,-53,37,37,-49,37,-44,-47,-48,37,37,37,]),'DATETIME':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[38,38,38,38,-59,38,38,-56,-57,-58,38,-54,-55,38,-50,-51,-52,-53,38,38,-49,38,-44,-47,-48,38,38,38,]),'DATE_INTERVAL':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[39,39,39,39,-59,39,39,-56,-57,-58,39,-54,-55,39,-50,-51,-52,-53,39,39,-49,39,-44,-47,-48,39,39,39,]),'DATETIME_INTERVAL':([0,13,27,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,93,94,95,100,110,113,],[40,40,40,40,-59,40,40,-56,-57,-58,40,-54,-55,40,-50,-51,-52,-53,40,40,-49,40,-44,-47,-48,40,40,40,]),'UNDER_IDENTIFIER':([0,13,27,29,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,67,77,82,83,93,94,95,100,102,108,110,113,],[41,41,41,41,41,-59,41,41,-56,-57,-58,41,-54,-55,41,-50,-51,-52,-53,41,41,-49,41,41,41,41,41,-44,-47,-48,41,41,41,41,41,]),'UPPER_IDENTIFIER':([0,13,27,29,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,67,77,82,83,93,94,95,100,102,108,110,113,],[42,42,42,42,42,-59,42,42,-56,-57,-58,42,-54,-55,42,-50,-51,-52,-53,42,42,-49,42,42,42,42,42,-44,-47,-48,42,42,42,42,42,]),'LOWER_IDENTIFIER':([0,13,27,29,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,67,77,82,83,93,94,95,100,102,108,110,113,],[43,43,43,43,43,-59,43,43,-56,-57,-58,43,-54,-55,43,-50,-51,-52,-53,43,43,-49,43,43,43,43,43,-44,-47,-48,43,43,43,43,43,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[0,-15,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,-45,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'SPACE':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,62,65,69,79,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,106,107,109,111,112,114,115,117,118,],[-15,-16,-14,-12,-10,-8,-6,61,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,77,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,82,-46,61,-37,102,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,113,-80,-82,-74,102,-73,-79,-83,-81,]),'DOT_OPERATOR':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,-8,-6,63,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,70,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,70,63,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'STAR':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,56,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,56,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,56,-4,-37,-13,-11,-9,56,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'SLASH':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,57,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,57,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,57,-4,-37,-13,-11,-9,57,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'DOUBLESLASH':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,58,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,58,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,58,-4,-37,-13,-11,-9,58,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'PERCENT':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,59,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,59,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,59,-4,-37,-13,-11,-9,59,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'PLUS':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,53,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,53,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,53,-4,-37,-13,-11,53,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'MINUS':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,54,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,54,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,54,-4,-37,-13,-11,54,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'COLON':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,49,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,49,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,49,-4,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'OPERATOR':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,50,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,50,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,50,-4,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'ARROW':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,69,78,79,81,84,85,86,87,88,89,90,91,92,93,94,95,97,101,103,104,105,107,109,111,112,114,115,116,117,118,],[-15,-16,-14,51,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,51,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,51,-4,-37,100,-73,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-75,-77,-84,-85,-80,-82,-74,-73,-73,-79,-76,-83,-81,]),'KEYWORD_WHERE':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,65,66,68,69,80,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[45,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,-4,45,45,-37,45,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,45,-73,45,-83,-81,]),'TICK_OPERATOR':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,64,65,66,68,69,80,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[46,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,46,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,46,-4,46,46,-37,46,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,46,-73,46,-83,-81,]),'RPAREN':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,46,49,50,51,53,54,56,57,58,59,62,65,68,69,70,71,72,73,74,75,76,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,69,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-59,-56,-57,-58,-54,-55,-50,-51,-52,-53,-46,-45,93,-37,94,95,-60,-61,-62,-63,-64,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'PADDING':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,62,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,83,-46,-45,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,108,-84,-85,-80,-82,-74,108,-79,-83,-81,]),'KEYWORD_IN':([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,30,31,32,33,34,35,36,37,38,39,40,41,42,43,62,65,69,81,84,85,86,87,88,89,90,91,92,93,94,95,96,97,104,105,107,109,111,114,115,117,118,],[-15,-16,-14,-12,-10,-8,-6,-4,-2,-17,-18,-19,-20,-21,-22,-23,-25,-26,-27,-28,-29,-30,-31,-32,-40,-65,-66,-67,-68,-69,-39,-38,-33,-34,-35,-36,-41,-42,-43,-46,-45,-37,-13,-11,-9,-7,-5,-3,-1,-70,-71,-72,-44,-47,-48,106,-73,-84,-85,-80,-82,-74,-73,-79,-83,-81,]),'ANNOTATION':([18,30,31,32,33,34,],[67,-65,-66,-67,-68,-69,]),'EQ':([41,42,43,79,98,99,101,103,112,116,],[-41,-42,-43,-73,110,-78,-75,-77,-73,-76,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'st_expr':([0,113,],[1,117,]),'expr':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[2,66,68,80,66,66,66,66,66,66,68,111,115,2,]),'expr_term0':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[3,3,3,81,3,3,3,3,3,3,3,3,3,3,]),'expr_term1':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[4,4,4,4,84,4,4,4,4,4,4,4,4,4,]),'expr_term2':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,]),'expr_term6':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[6,6,6,6,6,85,6,6,6,6,6,6,6,6,]),'expr_term7':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[7,7,7,7,7,7,86,7,7,7,7,7,7,7,]),'expr_term9':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[8,8,8,8,8,8,8,87,88,8,8,8,8,8,]),'expr_factor':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[9,65,9,9,9,9,9,9,9,89,9,9,9,9,]),'literal':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'identifier':([0,13,27,44,47,48,52,55,60,61,64,67,100,110,113,],[12,12,12,12,12,12,12,12,12,12,12,92,12,12,12,]),'enclosed_expr':([0,9,13,27,44,47,48,52,55,60,61,64,65,89,100,110,113,],[13,62,13,13,13,13,13,13,13,13,13,13,62,62,13,13,13,]),'unit_value':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'letexpr':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[15,15,15,15,15,15,15,15,15,15,15,15,15,15,]),'where_expr':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[16,16,16,16,16,16,16,16,16,16,16,16,16,16,]),'lambda_expr':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'number':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'concrete_number':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'string':([0,13,27,44,47,48,52,55,60,61,64,67,100,110,113,],[20,20,20,20,20,20,20,20,20,20,20,90,20,20,20,]),'char':([0,13,27,44,47,48,52,55,60,61,64,67,100,110,113,],[21,21,21,21,21,21,21,21,21,21,21,91,21,21,21,]),'date':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'datetime':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'date_interval':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'datetime_interval':([0,13,27,44,47,48,52,55,60,61,64,100,110,113,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'_identifier':([0,13,27,29,44,47,48,52,55,60,61,64,67,77,82,83,100,102,108,110,113,],[26,26,26,79,26,26,26,26,26,26,26,26,26,79,79,79,26,112,79,26,26,]),'infixl_operator_0':([2,27,64,66,68,80,111,115,],[44,72,72,44,44,44,44,44,]),'infixr_operator_2':([5,27,64,],[47,74,74,]),'infixl_operator_2':([5,27,64,],[48,73,73,]),'infixl_operator_6':([6,27,64,85,],[52,75,75,52,]),'infixl_operator_7':([7,27,64,86,],[55,76,76,55,]),'infixr_operator_9':([9,65,89,],[60,60,60,]),'operator':([27,64,],[71,71,]),'parameters':([29,77,82,83,108,],[78,99,99,99,99,]),'equations':([77,82,83,],[96,104,105,]),'equation':([77,82,83,108,],[97,97,97,114,]),'pattern':([77,82,83,108,],[98,98,98,98,]),'_parameters':([79,112,],[101,116,]),'empty':([79,97,112,114,],[103,109,103,109,]),'_equation_set':([97,114,],[107,118,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> st_expr","S'",1,None,None,None),
  ('expr_factor -> expr_factor SPACE expr_factor','expr_factor',3,'p_application','parsers.py',481),
  ('expr_factor -> ATTR_ACCESS','expr_factor',1,'p_attr_access','parsers.py',486),
  ('expr_term9 -> expr_factor infixr_operator_9 expr_term9','expr_term9',3,'p_expressions_precedence_rules','parsers.py',498),
  ('expr_term9 -> expr_factor','expr_term9',1,'p_expressions_precedence_rules','parsers.py',499),
  ('expr_term7 -> expr_term7 infixl_operator_7 expr_term9','expr_term7',3,'p_expressions_precedence_rules','parsers.py',501),
  ('expr_term7 -> expr_term9','expr_term7',1,'p_expressions_precedence_rules','parsers.py',502),
  ('expr_term6 -> expr_term6 infixl_operator_6 expr_term7','expr_term6',3,'p_expressions_precedence_rules','parsers.py',504),
  ('expr_term6 -> expr_term7','expr_term6',1,'p_expressions_precedence_rules','parsers.py',505),
  ('expr_term2 -> expr_term2 infixl_operator_2 expr_term6','expr_term2',3,'p_expressions_precedence_rules','parsers.py',507),
  ('expr_term2 -> expr_term6','expr_term2',1,'p_expressions_precedence_rules','parsers.py',508),
  ('expr_term1 -> expr_term2 infixr_operator_2 expr_term1','expr_term1',3,'p_expressions_precedence_rules','parsers.py',510),
  ('expr_term1 -> expr_term2','expr_term1',1,'p_expressions_precedence_rules','parsers.py',511),
  ('expr_term0 -> expr infixl_operator_0 expr_term0','expr_term0',3,'p_expressions_precedence_rules','parsers.py',513),
  ('expr_term0 -> expr_term1','expr_term0',1,'p_expressions_precedence_rules','parsers.py',514),
  ('st_expr -> expr','st_expr',1,'p_standalone_definitions','parsers.py',527),
  ('expr -> expr_term0','expr',1,'p_standalone_definitions','parsers.py',529),
  ('expr_factor -> literal','expr_factor',1,'p_standalone_definitions','parsers.py',531),
  ('expr_factor -> identifier','expr_factor',1,'p_standalone_definitions','parsers.py',532),
  ('expr_factor -> enclosed_expr','expr_factor',1,'p_standalone_definitions','parsers.py',533),
  ('expr_factor -> unit_value','expr_factor',1,'p_standalone_definitions','parsers.py',534),
  ('expr_factor -> letexpr','expr_factor',1,'p_standalone_definitions','parsers.py',535),
  ('expr_factor -> where_expr','expr_factor',1,'p_standalone_definitions','parsers.py',536),
  ('expr_factor -> lambda_expr','expr_factor',1,'p_standalone_definitions','parsers.py',537),
  ('st_type_expr -> type_expr','st_type_expr',1,'p_standalone_definitions','parsers.py',539),
  ('literal -> number','literal',1,'p_literals','parsers.py',547),
  ('literal -> concrete_number','literal',1,'p_literals','parsers.py',548),
  ('literal -> string','literal',1,'p_literals','parsers.py',549),
  ('literal -> char','literal',1,'p_literals','parsers.py',550),
  ('literal -> date','literal',1,'p_literals','parsers.py',551),
  ('literal -> datetime','literal',1,'p_literals','parsers.py',552),
  ('literal -> date_interval','literal',1,'p_literals','parsers.py',553),
  ('literal -> datetime_interval','literal',1,'p_literals','parsers.py',554),
  ('date -> DATE','date',1,'p_date','parsers.py',560),
  ('datetime -> DATETIME','datetime',1,'p_datetime','parsers.py',566),
  ('date_interval -> DATE_INTERVAL','date_interval',1,'p_date_interval','parsers.py',572),
  ('datetime_interval -> DATETIME_INTERVAL','datetime_interval',1,'p_datetime_interval','parsers.py',578),
  ('unit_value -> LPAREN RPAREN','unit_value',2,'p_unit_value','parsers.py',584),
  ('char -> CHAR','char',1,'p_char','parsers.py',590),
  ('string -> STRING','string',1,'p_string','parsers.py',595),
  ('identifier -> _identifier','identifier',1,'p_variable','parsers.py',600),
  ('_identifier -> UNDER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',607),
  ('_identifier -> UPPER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',608),
  ('_identifier -> LOWER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',609),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','parsers.py',616),
  ('expr_factor -> enclosed_expr expr_factor','expr_factor',2,'p_application_after_paren','parsers.py',621),
  ('expr_factor -> expr_factor enclosed_expr','expr_factor',2,'p_application_after_paren','parsers.py',622),
  ('enclosed_expr -> LPAREN DOT_OPERATOR RPAREN','enclosed_expr',3,'p_operators_as_expressios','parsers.py',628),
  ('enclosed_expr -> LPAREN operator RPAREN','enclosed_expr',3,'p_operators_as_expressios','parsers.py',629),
  ('infixr_operator_9 -> DOT_OPERATOR','infixr_operator_9',1,'p_operator','parsers.py',639),
  ('infixl_operator_7 -> STAR','infixl_operator_7',1,'p_operator','parsers.py',641),
  ('infixl_operator_7 -> SLASH','infixl_operator_7',1,'p_operator','parsers.py',642),
  ('infixl_operator_7 -> DOUBLESLASH','infixl_operator_7',1,'p_operator','parsers.py',643),
  ('infixl_operator_7 -> PERCENT','infixl_operator_7',1,'p_operator','parsers.py',644),
  ('infixl_operator_6 -> PLUS','infixl_operator_6',1,'p_operator','parsers.py',646),
  ('infixl_operator_6 -> MINUS','infixl_operator_6',1,'p_operator','parsers.py',647),
  ('infixr_operator_2 -> COLON','infixr_operator_2',1,'p_operator','parsers.py',649),
  ('infixl_operator_2 -> OPERATOR','infixl_operator_2',1,'p_operator','parsers.py',651),
  ('infixl_operator_2 -> ARROW','infixl_operator_2',1,'p_operator','parsers.py',652),
  ('infixl_operator_0 -> TICK_OPERATOR','infixl_operator_0',1,'p_operator','parsers.py',654),
  ('operator -> infixl_operator_0','operator',1,'p_operator','parsers.py',656),
  ('operator -> infixl_operator_2','operator',1,'p_operator','parsers.py',657),
  ('operator -> infixr_operator_2','operator',1,'p_operator','parsers.py',658),
  ('operator -> infixl_operator_6','operator',1,'p_operator','parsers.py',659),
  ('operator -> infixl_operator_7','operator',1,'p_operator','parsers.py',660),
  ('number -> BASE10_INTEGER','number',1,'p_integer','parsers.py',667),
  ('number -> BASE16_INTEGER','number',1,'p_integer','parsers.py',668),
  ('number -> BASE8_INTEGER','number',1,'p_integer','parsers.py',669),
  ('number -> BASE2_INTEGER','number',1,'p_integer','parsers.py',670),
  ('number -> FLOAT','number',1,'p_float','parsers.py',699),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','parsers.py',704),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','parsers.py',705),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','parsers.py',706),
  ('empty -> <empty>','empty',0,'p_empty','parsers.py',715),
  ('lambda_expr -> BACKSLASH parameters ARROW expr','lambda_expr',4,'p_lambda_definition','parsers.py',720),
  ('parameters -> _identifier _parameters','parameters',2,'p_parameters','parsers.py',728),
  ('_parameters -> SPACE _identifier _parameters','_parameters',3,'p_parameters','parsers.py',729),
  ('_parameters -> empty','_parameters',1,'p_empty__parameters','parsers.py',738),
  ('pattern -> parameters','pattern',1,'p_pattern','parsers.py',744),
  ('equation -> pattern EQ expr','equation',3,'p_equation','parsers.py',750),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','parsers.py',760),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','parsers.py',769),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','parsers.py',778),
  ('letexpr -> KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','parsers.py',788),
  ('where_expr -> expr KEYWORD_WHERE SPACE equations','where_expr',4,'p_where_expr','parsers.py',796),
  ('where_expr -> expr KEYWORD_WHERE PADDING equations','where_expr',4,'p_where_expr','parsers.py',797),
  ('type_expr -> type_function_expr','type_expr',1,'p_type_expr','parsers.py',807),
  ('type_expr -> type_term','type_expr',1,'p_type_expr','parsers.py',808),
  ('type_function_expr -> type_term ARROW _maybe_padding type_function_expr','type_function_expr',4,'p_type_function_expr','parsers.py',813),
  ('type_function_expr -> type_term','type_function_expr',1,'p_type_function_expr','parsers.py',814),
  ('type_term -> type_app_expression','type_term',1,'p_type_term','parsers.py',824),
  ('type_term -> type_factor','type_term',1,'p_type_term','parsers.py',825),
  ('type_app_expression -> type_factor _app_args_non_empty','type_app_expression',2,'p_type_application_expr','parsers.py',830),
  ('_app_args -> SPACE type_factor _app_args','_app_args',3,'p_type_application_args','parsers.py',842),
  ('_app_args_non_empty -> SPACE type_factor _app_args','_app_args_non_empty',3,'p_type_application_args','parsers.py',843),
  ('_app_args -> empty','_app_args',1,'p_type_application_args_empty','parsers.py',851),
  ('type_variable -> LOWER_IDENTIFIER','type_variable',1,'p_type_variable','parsers.py',856),
  ('type_cons -> UPPER_IDENTIFIER','type_cons',1,'p_type_cons','parsers.py',861),
  ('type_factor -> type_variable','type_factor',1,'p_type_factor_identifier','parsers.py',866),
  ('type_factor -> type_cons','type_factor',1,'p_type_factor_identifier','parsers.py',867),
  ('type_factor -> LPAREN _maybe_padding type_expr _maybe_padding RPAREN','type_factor',5,'p_type_factor_paren','parsers.py',874),
  ('type_factor -> LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET','type_factor',5,'p_type_factor_bracket','parsers.py',879),
  ('_maybe_padding -> PADDING','_maybe_padding',1,'p_maybe_padding','parsers.py',884),
  ('_maybe_padding -> empty','_maybe_padding',1,'p_maybe_padding','parsers.py',885),
  ('program -> definitions','program',1,'p_program','parsers.py',891),
  ('definitions -> definition _definition_set','definitions',2,'p_definitions','parsers.py',907),
  ('_definition_set -> NEWLINE definition _definition_set','_definition_set',3,'p_definition_set','parsers.py',915),
  ('_definition_set -> empty','_definition_set',1,'p_definition_set2','parsers.py',923),
  ('definition -> nametype_decl','definition',1,'p_definition','parsers.py',929),
  ('definition -> valuedef','definition',1,'p_definition','parsers.py',930),
  ('definition -> datatype_definition','definition',1,'p_definition','parsers.py',931),
  ('valuedef -> equation','valuedef',1,'p_valuedef','parsers.py',937),
  ('nametype_decl -> _identifier COLON COLON st_type_expr','nametype_decl',4,'p_nametype_decl','parsers.py',943),
  ('datatype_definition -> _datatype_lhs EQ _data_rhs','datatype_definition',3,'p_datatype_definition','parsers.py',952),
  ('_datatype_lhs -> KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params','_datatype_lhs',4,'p_datatype_lhs','parsers.py',960),
  ('_cons_params -> SPACE LOWER_IDENTIFIER _cons_params','_cons_params',3,'p_datatype_cons_params','parsers.py',969),
  ('_cons_params -> empty','_cons_params',1,'p_datatype_cons_params_empty','parsers.py',978),
  ('_data_rhs -> data_cons _data_conses','_data_rhs',2,'p_datatype_body','parsers.py',984),
  ('_data_conses -> _maybe_padding PIPE data_cons _data_conses','_data_conses',4,'p_datatype_body','parsers.py',985),
  ('_data_conses -> empty','_data_conses',1,'p_datatype_conses_empty','parsers.py',994),
  ('data_cons -> _data_cons','data_cons',1,'p_data_cons','parsers.py',999),
  ('_data_cons -> UPPER_IDENTIFIER _cons_args','_data_cons',2,'p_bare_data_cons','parsers.py',1005),
  ('_cons_args -> SPACE cons_arg _cons_args','_cons_args',3,'p_data_cons_args','parsers.py',1010),
  ('_cons_args -> empty','_cons_args',1,'p_data_cons_args_empty','parsers.py',1019),
  ('cons_arg -> type_variable','cons_arg',1,'p_cons_arg','parsers.py',1025),
  ('cons_arg -> type_cons','cons_arg',1,'p_cons_arg','parsers.py',1026),
  ('cons_arg -> _cons_arg_factor','cons_arg',1,'p_cons_arg','parsers.py',1027),
  ('_cons_arg_factor -> LPAREN type_expr RPAREN','_cons_arg_factor',3,'p_cons_arg_factor','parsers.py',1033),
  ('_cons_arg_factor -> LBRACKET type_expr RBRACKET','_cons_arg_factor',3,'p_cons_arg_factor_list','parsers.py',1039),
]
