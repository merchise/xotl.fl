
# type_parsertab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_type_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftKEYWORD_WHEREleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW ATTR_ACCESS BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON DATE DATETIME DATETIME_INTERVAL DATE_INTERVAL DOT_OPERATOR DOUBLESLASH EQ FLOAT KEYWORD_CLASS KEYWORD_DATA KEYWORD_IN KEYWORD_INSTANCE KEYWORD_LET KEYWORD_WHERE LBRACKET LOWER_IDENTIFIER LPAREN MINUS NEWLINE OPERATOR PADDING PERCENT PIPE PLUS RBRACKET RPAREN SLASH SPACE STAR STRING TICK_OPERATOR UNDER_IDENTIFIER UPPER_IDENTIFIERexpr_factor : expr_factor SPACE expr_factorexpr_factor : ATTR_ACCESS\n    expr_term9 : expr_factor infix_operator_9 expr_term9\n               | expr_factor\n\n    expr_term7 : expr_term7 infix_operator_7 expr_term9\n               | expr_term9\n\n    expr_term6 : expr_term6 infix_operator_6 expr_term7\n               | expr_term7\n\n    expr_term2 : expr_term2 infix_operator_2 expr_term6\n               | expr_term6\n\n    expr_term0 : expr infix_operator_0 expr_term0\n               | expr_term2\n\n    \n    st_expr : expr\n\n    expr : expr_term0\n\n    expr_factor : literal\n                | identifier\n                | enclosed_expr\n                | unit_value\n                | letexpr\n                | where_expr\n                | lambda_expr\n\n    st_type_expr : type_expr\n\n    literal : number\n             | concrete_number\n             | string\n             | char\n             | date\n             | datetime\n             | date_interval\n             | datetime_interval\n    date : DATE\n    datetime : DATETIME\n    date_interval : DATE_INTERVAL\n    datetime_interval : DATETIME_INTERVAL\n    unit_value : LPAREN RPAREN\n    char : CHARstring : STRINGidentifier : _identifier\n\n    _identifier : UNDER_IDENTIFIER\n                   | UPPER_IDENTIFIER\n                   | LOWER_IDENTIFIER\n\n    enclosed_expr : LPAREN expr RPARENexpr_factor : enclosed_expr expr_factor\n                   | expr_factor enclosed_expr\n    enclosed_expr : LPAREN DOT_OPERATOR RPAREN\n                     | LPAREN operator RPAREN\n    \n    infix_operator_9 : DOT_OPERATOR\n\n    infix_operator_7 : STAR\n                     | SLASH\n                     | DOUBLESLASH\n                     | PERCENT\n\n    infix_operator_6 : PLUS\n                     | MINUS\n\n    infix_operator_2 : OPERATOR\n                     | ARROW\n\n    infix_operator_0 : TICK_OPERATOR\n\n    operator : infix_operator_0\n             | infix_operator_2\n             | infix_operator_6\n             | infix_operator_7\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : lambda_expr : BACKSLASH parameters ARROW expr\n    parameters : _identifier _parameters\n       _parameters : SPACE _identifier _parameters\n    _parameters : empty\n    pattern : parametersequation : pattern EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    \n    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr\n\n    \n    where_expr : expr KEYWORD_WHERE SPACE equations\n    where_expr : expr KEYWORD_WHERE PADDING equations\n    type_expr : type_function_expr\n                 | type_termtype_function_expr : type_term ARROW _maybe_padding type_function_expr\n                          | type_term\n    type_term : type_app_expression\n                 | type_factortype_app_expression : type_factor _app_args_non_empty_app_args : SPACE type_factor _app_args\n       _app_args_non_empty : SPACE type_factor _app_args\n    _app_args : emptytype_variable : LOWER_IDENTIFIERtype_cons : UPPER_IDENTIFIERtype_factor : type_variable\n                   | type_cons\n\n    type_factor : LPAREN _maybe_padding type_expr _maybe_padding RPARENtype_factor : LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET_maybe_padding : PADDING\n                      | empty\n    program : definitions\n    definitions : definition _definition_set\n    _definition_set : NEWLINE definition _definition_set\n    _definition_set : empty\n    definition : nametype_decl\n                  | valuedef\n                  | datatype_definition\n    valuedef : equation\n    nametype_decl : _identifier COLON COLON st_type_expr\n    datatype_definition : _datatype_lhs EQ _data_rhs\n    _datatype_lhs : KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params\n    _cons_params : SPACE LOWER_IDENTIFIER _cons_params\n    _cons_params : empty\n    _data_rhs : data_cons _data_conses\n       _data_conses : _maybe_padding PIPE data_cons _data_conses\n    _data_conses : emptydata_cons : _data_cons_data_cons : UPPER_IDENTIFIER _cons_args_cons_args : SPACE cons_arg _cons_args\n    _cons_args : empty\n    cons_arg : type_variable\n       cons_arg : type_cons\n       cons_arg : _cons_arg_factor\n    _cons_arg_factor : LPAREN type_expr RPAREN\n    _cons_arg_factor : LBRACKET type_expr RBRACKET\n    '
    
_lr_action_items = {'LPAREN':([0,9,10,13,15,16,17,18,19,20,26,],[9,-69,-69,-69,9,9,-98,-99,9,9,9,]),'LBRACKET':([0,9,10,13,15,16,17,18,19,20,26,],[10,-69,-69,-69,10,10,-98,-99,10,10,10,]),'LOWER_IDENTIFIER':([0,9,10,13,15,16,17,18,19,20,26,],[11,-69,-69,-69,11,11,-98,-99,11,11,11,]),'UPPER_IDENTIFIER':([0,9,10,13,15,16,17,18,19,20,26,],[12,-69,-69,-69,12,12,-98,-99,12,12,12,]),'$end':([1,2,3,4,5,6,7,8,11,12,14,21,24,25,27,28,31,32,33,34,],[0,-22,-82,-83,-86,-87,-94,-95,-92,-93,-88,-69,-85,-84,-90,-91,-69,-96,-97,-89,]),'PADDING':([3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,27,28,31,32,33,34,],[-82,-83,-86,-87,-94,-95,17,17,-92,-93,17,-88,-69,17,17,-85,-84,-90,-91,-69,-96,-97,-89,]),'RPAREN':([3,4,5,6,7,8,11,12,14,17,18,21,22,24,25,27,28,29,31,32,33,34,],[-82,-83,-86,-87,-94,-95,-92,-93,-88,-98,-99,-69,-69,-85,-84,-90,-91,32,-69,-96,-97,-89,]),'RBRACKET':([3,4,5,6,7,8,11,12,14,17,18,21,23,24,25,27,28,30,31,32,33,34,],[-82,-83,-86,-87,-94,-95,-92,-93,-88,-98,-99,-69,-69,-85,-84,-90,-91,33,-69,-96,-97,-89,]),'ARROW':([4,5,6,7,8,11,12,14,21,24,27,28,31,32,33,34,],[13,-86,-87,-94,-95,-92,-93,-88,-69,13,-90,-91,-69,-96,-97,-89,]),'SPACE':([6,7,8,11,12,21,31,32,33,],[15,-94,-95,-92,-93,26,26,-96,-97,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'st_type_expr':([0,],[1,]),'type_expr':([0,16,19,],[2,22,23,]),'type_function_expr':([0,16,19,20,],[3,3,3,25,]),'type_term':([0,16,19,20,],[4,4,4,24,]),'type_app_expression':([0,16,19,20,],[5,5,5,5,]),'type_factor':([0,15,16,19,20,26,],[6,21,6,6,6,31,]),'type_variable':([0,15,16,19,20,26,],[7,7,7,7,7,7,]),'type_cons':([0,15,16,19,20,26,],[8,8,8,8,8,8,]),'_app_args_non_empty':([6,],[14,]),'_maybe_padding':([9,10,13,22,23,],[16,19,20,29,30,]),'empty':([9,10,13,21,22,23,31,],[18,18,18,28,18,18,28,]),'_app_args':([21,31,],[27,34,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> st_type_expr","S'",1,None,None,None),
  ('expr_factor -> expr_factor SPACE expr_factor','expr_factor',3,'p_application','parsers.py',481),
  ('expr_factor -> ATTR_ACCESS','expr_factor',1,'p_attr_access','parsers.py',486),
  ('expr_term9 -> expr_factor infix_operator_9 expr_term9','expr_term9',3,'p_expressions_precedence_rules','parsers.py',498),
  ('expr_term9 -> expr_factor','expr_term9',1,'p_expressions_precedence_rules','parsers.py',499),
  ('expr_term7 -> expr_term7 infix_operator_7 expr_term9','expr_term7',3,'p_expressions_precedence_rules','parsers.py',501),
  ('expr_term7 -> expr_term9','expr_term7',1,'p_expressions_precedence_rules','parsers.py',502),
  ('expr_term6 -> expr_term6 infix_operator_6 expr_term7','expr_term6',3,'p_expressions_precedence_rules','parsers.py',504),
  ('expr_term6 -> expr_term7','expr_term6',1,'p_expressions_precedence_rules','parsers.py',505),
  ('expr_term2 -> expr_term2 infix_operator_2 expr_term6','expr_term2',3,'p_expressions_precedence_rules','parsers.py',507),
  ('expr_term2 -> expr_term6','expr_term2',1,'p_expressions_precedence_rules','parsers.py',508),
  ('expr_term0 -> expr infix_operator_0 expr_term0','expr_term0',3,'p_expressions_precedence_rules','parsers.py',510),
  ('expr_term0 -> expr_term2','expr_term0',1,'p_expressions_precedence_rules','parsers.py',511),
  ('st_expr -> expr','st_expr',1,'p_standalone_definitions','parsers.py',524),
  ('expr -> expr_term0','expr',1,'p_standalone_definitions','parsers.py',526),
  ('expr_factor -> literal','expr_factor',1,'p_standalone_definitions','parsers.py',528),
  ('expr_factor -> identifier','expr_factor',1,'p_standalone_definitions','parsers.py',529),
  ('expr_factor -> enclosed_expr','expr_factor',1,'p_standalone_definitions','parsers.py',530),
  ('expr_factor -> unit_value','expr_factor',1,'p_standalone_definitions','parsers.py',531),
  ('expr_factor -> letexpr','expr_factor',1,'p_standalone_definitions','parsers.py',532),
  ('expr_factor -> where_expr','expr_factor',1,'p_standalone_definitions','parsers.py',533),
  ('expr_factor -> lambda_expr','expr_factor',1,'p_standalone_definitions','parsers.py',534),
  ('st_type_expr -> type_expr','st_type_expr',1,'p_standalone_definitions','parsers.py',536),
  ('literal -> number','literal',1,'p_literals','parsers.py',544),
  ('literal -> concrete_number','literal',1,'p_literals','parsers.py',545),
  ('literal -> string','literal',1,'p_literals','parsers.py',546),
  ('literal -> char','literal',1,'p_literals','parsers.py',547),
  ('literal -> date','literal',1,'p_literals','parsers.py',548),
  ('literal -> datetime','literal',1,'p_literals','parsers.py',549),
  ('literal -> date_interval','literal',1,'p_literals','parsers.py',550),
  ('literal -> datetime_interval','literal',1,'p_literals','parsers.py',551),
  ('date -> DATE','date',1,'p_date','parsers.py',557),
  ('datetime -> DATETIME','datetime',1,'p_datetime','parsers.py',563),
  ('date_interval -> DATE_INTERVAL','date_interval',1,'p_date_interval','parsers.py',569),
  ('datetime_interval -> DATETIME_INTERVAL','datetime_interval',1,'p_datetime_interval','parsers.py',575),
  ('unit_value -> LPAREN RPAREN','unit_value',2,'p_unit_value','parsers.py',581),
  ('char -> CHAR','char',1,'p_char','parsers.py',587),
  ('string -> STRING','string',1,'p_string','parsers.py',592),
  ('identifier -> _identifier','identifier',1,'p_variable','parsers.py',597),
  ('_identifier -> UNDER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',604),
  ('_identifier -> UPPER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',605),
  ('_identifier -> LOWER_IDENTIFIER','_identifier',1,'p_bare_identifier','parsers.py',606),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','parsers.py',613),
  ('expr_factor -> enclosed_expr expr_factor','expr_factor',2,'p_application_after_paren','parsers.py',618),
  ('expr_factor -> expr_factor enclosed_expr','expr_factor',2,'p_application_after_paren','parsers.py',619),
  ('enclosed_expr -> LPAREN DOT_OPERATOR RPAREN','enclosed_expr',3,'p_operators_as_expressios','parsers.py',625),
  ('enclosed_expr -> LPAREN operator RPAREN','enclosed_expr',3,'p_operators_as_expressios','parsers.py',626),
  ('infix_operator_9 -> DOT_OPERATOR','infix_operator_9',1,'p_operator','parsers.py',636),
  ('infix_operator_7 -> STAR','infix_operator_7',1,'p_operator','parsers.py',638),
  ('infix_operator_7 -> SLASH','infix_operator_7',1,'p_operator','parsers.py',639),
  ('infix_operator_7 -> DOUBLESLASH','infix_operator_7',1,'p_operator','parsers.py',640),
  ('infix_operator_7 -> PERCENT','infix_operator_7',1,'p_operator','parsers.py',641),
  ('infix_operator_6 -> PLUS','infix_operator_6',1,'p_operator','parsers.py',643),
  ('infix_operator_6 -> MINUS','infix_operator_6',1,'p_operator','parsers.py',644),
  ('infix_operator_2 -> OPERATOR','infix_operator_2',1,'p_operator','parsers.py',646),
  ('infix_operator_2 -> ARROW','infix_operator_2',1,'p_operator','parsers.py',647),
  ('infix_operator_0 -> TICK_OPERATOR','infix_operator_0',1,'p_operator','parsers.py',649),
  ('operator -> infix_operator_0','operator',1,'p_operator','parsers.py',651),
  ('operator -> infix_operator_2','operator',1,'p_operator','parsers.py',652),
  ('operator -> infix_operator_6','operator',1,'p_operator','parsers.py',653),
  ('operator -> infix_operator_7','operator',1,'p_operator','parsers.py',654),
  ('number -> BASE10_INTEGER','number',1,'p_integer','parsers.py',661),
  ('number -> BASE16_INTEGER','number',1,'p_integer','parsers.py',662),
  ('number -> BASE8_INTEGER','number',1,'p_integer','parsers.py',663),
  ('number -> BASE2_INTEGER','number',1,'p_integer','parsers.py',664),
  ('number -> FLOAT','number',1,'p_float','parsers.py',693),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','parsers.py',698),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','parsers.py',699),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','parsers.py',700),
  ('empty -> <empty>','empty',0,'p_empty','parsers.py',709),
  ('lambda_expr -> BACKSLASH parameters ARROW expr','lambda_expr',4,'p_lambda_definition','parsers.py',714),
  ('parameters -> _identifier _parameters','parameters',2,'p_parameters','parsers.py',722),
  ('_parameters -> SPACE _identifier _parameters','_parameters',3,'p_parameters','parsers.py',723),
  ('_parameters -> empty','_parameters',1,'p_empty__parameters','parsers.py',732),
  ('pattern -> parameters','pattern',1,'p_pattern','parsers.py',738),
  ('equation -> pattern EQ expr','equation',3,'p_equation','parsers.py',744),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','parsers.py',754),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','parsers.py',763),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','parsers.py',772),
  ('letexpr -> KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','parsers.py',782),
  ('where_expr -> expr KEYWORD_WHERE SPACE equations','where_expr',4,'p_where_expr','parsers.py',790),
  ('where_expr -> expr KEYWORD_WHERE PADDING equations','where_expr',4,'p_where_expr','parsers.py',791),
  ('type_expr -> type_function_expr','type_expr',1,'p_type_expr','parsers.py',801),
  ('type_expr -> type_term','type_expr',1,'p_type_expr','parsers.py',802),
  ('type_function_expr -> type_term ARROW _maybe_padding type_function_expr','type_function_expr',4,'p_type_function_expr','parsers.py',807),
  ('type_function_expr -> type_term','type_function_expr',1,'p_type_function_expr','parsers.py',808),
  ('type_term -> type_app_expression','type_term',1,'p_type_term','parsers.py',818),
  ('type_term -> type_factor','type_term',1,'p_type_term','parsers.py',819),
  ('type_app_expression -> type_factor _app_args_non_empty','type_app_expression',2,'p_type_application_expr','parsers.py',824),
  ('_app_args -> SPACE type_factor _app_args','_app_args',3,'p_type_application_args','parsers.py',836),
  ('_app_args_non_empty -> SPACE type_factor _app_args','_app_args_non_empty',3,'p_type_application_args','parsers.py',837),
  ('_app_args -> empty','_app_args',1,'p_type_application_args_empty','parsers.py',845),
  ('type_variable -> LOWER_IDENTIFIER','type_variable',1,'p_type_variable','parsers.py',850),
  ('type_cons -> UPPER_IDENTIFIER','type_cons',1,'p_type_cons','parsers.py',855),
  ('type_factor -> type_variable','type_factor',1,'p_type_factor_identifier','parsers.py',860),
  ('type_factor -> type_cons','type_factor',1,'p_type_factor_identifier','parsers.py',861),
  ('type_factor -> LPAREN _maybe_padding type_expr _maybe_padding RPAREN','type_factor',5,'p_type_factor_paren','parsers.py',868),
  ('type_factor -> LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET','type_factor',5,'p_type_factor_bracket','parsers.py',873),
  ('_maybe_padding -> PADDING','_maybe_padding',1,'p_maybe_padding','parsers.py',878),
  ('_maybe_padding -> empty','_maybe_padding',1,'p_maybe_padding','parsers.py',879),
  ('program -> definitions','program',1,'p_program','parsers.py',885),
  ('definitions -> definition _definition_set','definitions',2,'p_definitions','parsers.py',901),
  ('_definition_set -> NEWLINE definition _definition_set','_definition_set',3,'p_definition_set','parsers.py',909),
  ('_definition_set -> empty','_definition_set',1,'p_definition_set2','parsers.py',917),
  ('definition -> nametype_decl','definition',1,'p_definition','parsers.py',923),
  ('definition -> valuedef','definition',1,'p_definition','parsers.py',924),
  ('definition -> datatype_definition','definition',1,'p_definition','parsers.py',925),
  ('valuedef -> equation','valuedef',1,'p_valuedef','parsers.py',931),
  ('nametype_decl -> _identifier COLON COLON st_type_expr','nametype_decl',4,'p_nametype_decl','parsers.py',937),
  ('datatype_definition -> _datatype_lhs EQ _data_rhs','datatype_definition',3,'p_datatype_definition','parsers.py',946),
  ('_datatype_lhs -> KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params','_datatype_lhs',4,'p_datatype_lhs','parsers.py',954),
  ('_cons_params -> SPACE LOWER_IDENTIFIER _cons_params','_cons_params',3,'p_datatype_cons_params','parsers.py',963),
  ('_cons_params -> empty','_cons_params',1,'p_datatype_cons_params_empty','parsers.py',972),
  ('_data_rhs -> data_cons _data_conses','_data_rhs',2,'p_datatype_body','parsers.py',978),
  ('_data_conses -> _maybe_padding PIPE data_cons _data_conses','_data_conses',4,'p_datatype_body','parsers.py',979),
  ('_data_conses -> empty','_data_conses',1,'p_datatype_conses_empty','parsers.py',988),
  ('data_cons -> _data_cons','data_cons',1,'p_data_cons','parsers.py',993),
  ('_data_cons -> UPPER_IDENTIFIER _cons_args','_data_cons',2,'p_bare_data_cons','parsers.py',999),
  ('_cons_args -> SPACE cons_arg _cons_args','_cons_args',3,'p_data_cons_args','parsers.py',1004),
  ('_cons_args -> empty','_cons_args',1,'p_data_cons_args_empty','parsers.py',1013),
  ('cons_arg -> type_variable','cons_arg',1,'p_cons_arg','parsers.py',1019),
  ('cons_arg -> type_cons','cons_arg',1,'p_cons_arg','parsers.py',1020),
  ('cons_arg -> _cons_arg_factor','cons_arg',1,'p_cons_arg','parsers.py',1021),
  ('_cons_arg_factor -> LPAREN type_expr RPAREN','_cons_arg_factor',3,'p_cons_arg_factor','parsers.py',1027),
  ('_cons_arg_factor -> LBRACKET type_expr RBRACKET','_cons_arg_factor',3,'p_cons_arg_factor_list','parsers.py',1033),
]
