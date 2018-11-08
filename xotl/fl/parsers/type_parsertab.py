
# type_parsertab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_type_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftKEYWORD_WHEREleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON COMMA DATE DATETIME DATETIME_INTERVAL DATE_INTERVAL DOT_OPERATOR DOUBLESLASH EQ FLOAT KEYWORD_CLASS KEYWORD_DATA KEYWORD_IN KEYWORD_INSTANCE KEYWORD_LET KEYWORD_WHERE LBRACKET LOWER_IDENTIFIER LPAREN MINUS NEWLINE OPERATOR PADDING PERCENT PIPE PLUS RBRACKET RPAREN SLASH SPACE STAR STRING TICK_OPERATOR UNDER_IDENTIFIER UPPER_IDENTIFIERexpr_factor : expr_factor SPACE expr_factor\n    expr_term9 : expr_factor infixr_operator_9 expr_term9\n               | expr_factor\n\n    expr_term7 : expr_term7 infixl_operator_7 expr_term9\n               | expr_term9\n\n    expr_term6 : expr_term6 infixl_operator_6 expr_term7\n               | expr_term7\n\n    expr_term2 : expr_term2 infixl_operator_2 expr_term6\n               | expr_term6\n\n    expr_term1 : expr_term2 infixr_operator_2 expr_term1\n               | expr_term2\n\n    expr_term0 : expr infixl_operator_0 expr_term0\n               | expr_term1\n\n    \n    st_expr : expr\n\n    expr : expr_term0\n\n    expr_factor : literal\n                | identifier\n                | enclosed_expr\n                | letexpr\n                | where_expr\n                | lambda_expr\n                | simple_list_expr\n                | simple_tuple_expr\n\n    st_type_expr : type_expr\n\n    literal : number\n             | concrete_number\n             | string\n             | char\n             | date\n             | datetime\n             | date_interval\n             | datetime_interval\n    simple_tuple_expr : LPAREN _list_items RPAREN\n    simple_list_expr : LBRACKET _list_items RBRACKET\n    _list_items : expr _list_items_cont\n       _list_items_cont : COMMA expr _list_items_cont\n    _list_items : empty\n       _list_items_cont : empty\n    date : DATE\n    datetime : DATETIME\n    date_interval : DATE_INTERVAL\n    datetime_interval : DATETIME_INTERVAL\n    char : CHARstring : STRINGidentifier : _identifier\n\n    _identifier : UNDER_IDENTIFIER\n                   | UPPER_IDENTIFIER\n                   | LOWER_IDENTIFIER\n\n    enclosed_expr : LPAREN expr RPARENexpr_factor : enclosed_expr expr_factor\n                   | expr_factor enclosed_expr\n    enclosed_expr : _enclosed_operator\n    _enclosed_operator : LPAREN _st_operator RPAREN\n    infixr_operator_9 : DOT_OPERATOR\n\n    infixl_operator_7 : STAR\n                     | SLASH\n                     | DOUBLESLASH\n                     | PERCENT\n\n    infixl_operator_6 : PLUS\n                     | MINUS\n\n    infixr_operator_2 : COLON\n\n    infixl_operator_2 : OPERATOR\n                      | ARROW\n\n    infixl_operator_0 : TICK_OPERATOR\n\n    _st_operator : infixl_operator_2\n                 | infixr_operator_2\n                 | infixl_operator_6\n                 | infixl_operator_7\n                 | infixr_operator_9\n                 | COMMA\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : lambda_expr : BACKSLASH patterns ARROW expr\n    \n    pattern : identifier\n    pattern : literal\n    pattern : cons_pattern\n    pattern : list_cons_pattern\n    pattern : tuple_cons_pattern\n    pattern : empty_list_pattern\n    pattern : empty_tuple_pattern\n    list_cons_pattern : pattern COLON pattern\n    cons_pattern : LPAREN _identifier SPACE patterns RPARENempty_list_pattern : LBRACKET RBRACKETempty_tuple_pattern : LPAREN RPARENtuple_cons_pattern : error\n    patterns : pattern _patterns\n       _patterns : SPACE pattern _patterns\n    _patterns : empty\n    equation : _identifier _patterns EQ expr\n       equation : _enclosed_operator _patterns EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    \n    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr\n\n    \n    where_expr : expr KEYWORD_WHERE SPACE equations\n    where_expr : expr KEYWORD_WHERE PADDING equations\n    type_expr : type_function_expr\n                 | type_termtype_function_expr : type_term ARROW _maybe_padding type_function_expr\n                          | type_term\n    type_term : type_app_expression\n                 | type_factortype_app_expression : type_factor _app_args_non_empty_app_args : SPACE type_factor _app_args\n       _app_args_non_empty : SPACE type_factor _app_args\n    _app_args : emptytype_variable : LOWER_IDENTIFIERtype_cons : UPPER_IDENTIFIERtype_factor : type_variable\n                   | type_cons\n\n    type_factor : LPAREN _maybe_padding type_expr _maybe_padding RPARENtype_factor : LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET_maybe_padding : PADDING\n                      | empty\n    program : definitions\n    definitions : definition _definition_set\n    _definition_set : NEWLINE definition _definition_set\n    _definition_set : empty\n    definition : nametype_decl\n                  | valuedef\n                  | datatype_definition\n    valuedef : equation\n    nametype_decl : _identifier COLON COLON st_type_expr\n    nametype_decl : LPAREN _st_operator RPAREN COLON COLON st_type_expr\n    datatype_definition : _datatype_lhs EQ _data_rhs\n    _datatype_lhs : KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params\n    _cons_params : SPACE LOWER_IDENTIFIER _cons_params\n    _cons_params : empty\n    _data_rhs : data_cons _data_conses\n       _data_conses : _maybe_padding PIPE data_cons _data_conses\n    _data_conses : emptydata_cons : _data_cons_data_cons : UPPER_IDENTIFIER _cons_args_cons_args : SPACE cons_arg _cons_args\n    _cons_args : empty\n    cons_arg : type_variable\n       cons_arg : type_cons\n       cons_arg : _cons_arg_factor\n    _cons_arg_factor : LPAREN type_expr RPAREN\n    _cons_arg_factor : LBRACKET type_expr RBRACKET\n    '
    
_lr_action_items = {'LPAREN':([0,9,10,13,15,16,17,18,19,20,26,],[9,-79,-79,-79,9,9,-120,-121,9,9,9,]),'LBRACKET':([0,9,10,13,15,16,17,18,19,20,26,],[10,-79,-79,-79,10,10,-120,-121,10,10,10,]),'LOWER_IDENTIFIER':([0,9,10,13,15,16,17,18,19,20,26,],[11,-79,-79,-79,11,11,-120,-121,11,11,11,]),'UPPER_IDENTIFIER':([0,9,10,13,15,16,17,18,19,20,26,],[12,-79,-79,-79,12,12,-120,-121,12,12,12,]),'$end':([1,2,3,4,5,6,7,8,11,12,14,21,24,25,27,28,31,32,33,34,],[0,-24,-104,-105,-108,-109,-116,-117,-114,-115,-110,-79,-107,-106,-112,-113,-79,-118,-119,-111,]),'PADDING':([3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,27,28,31,32,33,34,],[-104,-105,-108,-109,-116,-117,17,17,-114,-115,17,-110,-79,17,17,-107,-106,-112,-113,-79,-118,-119,-111,]),'RPAREN':([3,4,5,6,7,8,11,12,14,17,18,21,22,24,25,27,28,29,31,32,33,34,],[-104,-105,-108,-109,-116,-117,-114,-115,-110,-120,-121,-79,-79,-107,-106,-112,-113,32,-79,-118,-119,-111,]),'RBRACKET':([3,4,5,6,7,8,11,12,14,17,18,21,23,24,25,27,28,30,31,32,33,34,],[-104,-105,-108,-109,-116,-117,-114,-115,-110,-120,-121,-79,-79,-107,-106,-112,-113,33,-79,-118,-119,-111,]),'ARROW':([4,5,6,7,8,11,12,14,21,24,27,28,31,32,33,34,],[13,-108,-109,-116,-117,-114,-115,-110,-79,13,-112,-113,-79,-118,-119,-111,]),'SPACE':([6,7,8,11,12,21,31,32,33,],[15,-116,-117,-114,-115,26,26,-118,-119,]),}

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
  ('expr_factor -> expr_factor SPACE expr_factor','expr_factor',3,'p_application','__init__.py',430),
  ('expr_term9 -> expr_factor infixr_operator_9 expr_term9','expr_term9',3,'p_expressions_precedence_rules','__init__.py',437),
  ('expr_term9 -> expr_factor','expr_term9',1,'p_expressions_precedence_rules','__init__.py',438),
  ('expr_term7 -> expr_term7 infixl_operator_7 expr_term9','expr_term7',3,'p_expressions_precedence_rules','__init__.py',440),
  ('expr_term7 -> expr_term9','expr_term7',1,'p_expressions_precedence_rules','__init__.py',441),
  ('expr_term6 -> expr_term6 infixl_operator_6 expr_term7','expr_term6',3,'p_expressions_precedence_rules','__init__.py',443),
  ('expr_term6 -> expr_term7','expr_term6',1,'p_expressions_precedence_rules','__init__.py',444),
  ('expr_term2 -> expr_term2 infixl_operator_2 expr_term6','expr_term2',3,'p_expressions_precedence_rules','__init__.py',446),
  ('expr_term2 -> expr_term6','expr_term2',1,'p_expressions_precedence_rules','__init__.py',447),
  ('expr_term1 -> expr_term2 infixr_operator_2 expr_term1','expr_term1',3,'p_expressions_precedence_rules','__init__.py',449),
  ('expr_term1 -> expr_term2','expr_term1',1,'p_expressions_precedence_rules','__init__.py',450),
  ('expr_term0 -> expr infixl_operator_0 expr_term0','expr_term0',3,'p_expressions_precedence_rules','__init__.py',452),
  ('expr_term0 -> expr_term1','expr_term0',1,'p_expressions_precedence_rules','__init__.py',453),
  ('st_expr -> expr','st_expr',1,'p_standalone_definitions','__init__.py',466),
  ('expr -> expr_term0','expr',1,'p_standalone_definitions','__init__.py',468),
  ('expr_factor -> literal','expr_factor',1,'p_standalone_definitions','__init__.py',470),
  ('expr_factor -> identifier','expr_factor',1,'p_standalone_definitions','__init__.py',471),
  ('expr_factor -> enclosed_expr','expr_factor',1,'p_standalone_definitions','__init__.py',472),
  ('expr_factor -> letexpr','expr_factor',1,'p_standalone_definitions','__init__.py',473),
  ('expr_factor -> where_expr','expr_factor',1,'p_standalone_definitions','__init__.py',474),
  ('expr_factor -> lambda_expr','expr_factor',1,'p_standalone_definitions','__init__.py',475),
  ('expr_factor -> simple_list_expr','expr_factor',1,'p_standalone_definitions','__init__.py',476),
  ('expr_factor -> simple_tuple_expr','expr_factor',1,'p_standalone_definitions','__init__.py',477),
  ('st_type_expr -> type_expr','st_type_expr',1,'p_standalone_definitions','__init__.py',479),
  ('literal -> number','literal',1,'p_literals','__init__.py',487),
  ('literal -> concrete_number','literal',1,'p_literals','__init__.py',488),
  ('literal -> string','literal',1,'p_literals','__init__.py',489),
  ('literal -> char','literal',1,'p_literals','__init__.py',490),
  ('literal -> date','literal',1,'p_literals','__init__.py',491),
  ('literal -> datetime','literal',1,'p_literals','__init__.py',492),
  ('literal -> date_interval','literal',1,'p_literals','__init__.py',493),
  ('literal -> datetime_interval','literal',1,'p_literals','__init__.py',494),
  ('simple_tuple_expr -> LPAREN _list_items RPAREN','simple_tuple_expr',3,'p_tuple_expr','__init__.py',500),
  ('simple_list_expr -> LBRACKET _list_items RBRACKET','simple_list_expr',3,'p_list_expr','__init__.py',515),
  ('_list_items -> expr _list_items_cont','_list_items',2,'p_list_items','__init__.py',525),
  ('_list_items_cont -> COMMA expr _list_items_cont','_list_items_cont',3,'p_list_items','__init__.py',526),
  ('_list_items -> empty','_list_items',1,'p_list_items_empty','__init__.py',535),
  ('_list_items_cont -> empty','_list_items_cont',1,'p_list_items_empty','__init__.py',536),
  ('date -> DATE','date',1,'p_date','__init__.py',542),
  ('datetime -> DATETIME','datetime',1,'p_datetime','__init__.py',548),
  ('date_interval -> DATE_INTERVAL','date_interval',1,'p_date_interval','__init__.py',554),
  ('datetime_interval -> DATETIME_INTERVAL','datetime_interval',1,'p_datetime_interval','__init__.py',560),
  ('char -> CHAR','char',1,'p_char','__init__.py',566),
  ('string -> STRING','string',1,'p_string','__init__.py',571),
  ('identifier -> _identifier','identifier',1,'p_variable','__init__.py',576),
  ('_identifier -> UNDER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',583),
  ('_identifier -> UPPER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',584),
  ('_identifier -> LOWER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',585),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','__init__.py',592),
  ('expr_factor -> enclosed_expr expr_factor','expr_factor',2,'p_application_after_paren','__init__.py',597),
  ('expr_factor -> expr_factor enclosed_expr','expr_factor',2,'p_application_after_paren','__init__.py',598),
  ('enclosed_expr -> _enclosed_operator','enclosed_expr',1,'p_operators_as_expressios','__init__.py',604),
  ('_enclosed_operator -> LPAREN _st_operator RPAREN','_enclosed_operator',3,'p_enclosed_operator','__init__.py',610),
  ('infixr_operator_9 -> DOT_OPERATOR','infixr_operator_9',1,'p_operator','__init__.py',620),
  ('infixl_operator_7 -> STAR','infixl_operator_7',1,'p_operator','__init__.py',622),
  ('infixl_operator_7 -> SLASH','infixl_operator_7',1,'p_operator','__init__.py',623),
  ('infixl_operator_7 -> DOUBLESLASH','infixl_operator_7',1,'p_operator','__init__.py',624),
  ('infixl_operator_7 -> PERCENT','infixl_operator_7',1,'p_operator','__init__.py',625),
  ('infixl_operator_6 -> PLUS','infixl_operator_6',1,'p_operator','__init__.py',627),
  ('infixl_operator_6 -> MINUS','infixl_operator_6',1,'p_operator','__init__.py',628),
  ('infixr_operator_2 -> COLON','infixr_operator_2',1,'p_operator','__init__.py',630),
  ('infixl_operator_2 -> OPERATOR','infixl_operator_2',1,'p_operator','__init__.py',632),
  ('infixl_operator_2 -> ARROW','infixl_operator_2',1,'p_operator','__init__.py',633),
  ('infixl_operator_0 -> TICK_OPERATOR','infixl_operator_0',1,'p_operator','__init__.py',635),
  ('_st_operator -> infixl_operator_2','_st_operator',1,'p_operator','__init__.py',637),
  ('_st_operator -> infixr_operator_2','_st_operator',1,'p_operator','__init__.py',638),
  ('_st_operator -> infixl_operator_6','_st_operator',1,'p_operator','__init__.py',639),
  ('_st_operator -> infixl_operator_7','_st_operator',1,'p_operator','__init__.py',640),
  ('_st_operator -> infixr_operator_9','_st_operator',1,'p_operator','__init__.py',641),
  ('_st_operator -> COMMA','_st_operator',1,'p_operator','__init__.py',642),
  ('number -> BASE10_INTEGER','number',1,'p_integer','__init__.py',649),
  ('number -> BASE16_INTEGER','number',1,'p_integer','__init__.py',650),
  ('number -> BASE8_INTEGER','number',1,'p_integer','__init__.py',651),
  ('number -> BASE2_INTEGER','number',1,'p_integer','__init__.py',652),
  ('number -> FLOAT','number',1,'p_float','__init__.py',681),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','__init__.py',686),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','__init__.py',687),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','__init__.py',688),
  ('empty -> <empty>','empty',0,'p_empty','__init__.py',697),
  ('lambda_expr -> BACKSLASH patterns ARROW expr','lambda_expr',4,'p_lambda_definition','__init__.py',702),
  ('pattern -> identifier','pattern',1,'p_pattern','__init__.py',711),
  ('pattern -> literal','pattern',1,'p_pattern','__init__.py',712),
  ('pattern -> cons_pattern','pattern',1,'p_pattern','__init__.py',713),
  ('pattern -> list_cons_pattern','pattern',1,'p_pattern','__init__.py',714),
  ('pattern -> tuple_cons_pattern','pattern',1,'p_pattern','__init__.py',715),
  ('pattern -> empty_list_pattern','pattern',1,'p_pattern','__init__.py',716),
  ('pattern -> empty_tuple_pattern','pattern',1,'p_pattern','__init__.py',717),
  ('list_cons_pattern -> pattern COLON pattern','list_cons_pattern',3,'p_list_cons_for_param','__init__.py',723),
  ('cons_pattern -> LPAREN _identifier SPACE patterns RPAREN','cons_pattern',5,'p_param_pattern','__init__.py',729),
  ('empty_list_pattern -> LBRACKET RBRACKET','empty_list_pattern',2,'p_empty_list_as_pattern','__init__.py',734),
  ('empty_tuple_pattern -> LPAREN RPAREN','empty_tuple_pattern',2,'p_unit_value_as_pattern','__init__.py',740),
  ('tuple_cons_pattern -> error','tuple_cons_pattern',1,'p_tuple_cons_pattern','__init__.py',746),
  ('patterns -> pattern _patterns','patterns',2,'p_patterns','__init__.py',751),
  ('_patterns -> SPACE pattern _patterns','_patterns',3,'p_patterns','__init__.py',752),
  ('_patterns -> empty','_patterns',1,'p_patterns_empty','__init__.py',762),
  ('equation -> _identifier _patterns EQ expr','equation',4,'p_equation','__init__.py',768),
  ('equation -> _enclosed_operator _patterns EQ expr','equation',4,'p_equation','__init__.py',769),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','__init__.py',779),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','__init__.py',788),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','__init__.py',797),
  ('letexpr -> KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','__init__.py',807),
  ('where_expr -> expr KEYWORD_WHERE SPACE equations','where_expr',4,'p_where_expr','__init__.py',815),
  ('where_expr -> expr KEYWORD_WHERE PADDING equations','where_expr',4,'p_where_expr','__init__.py',816),
  ('type_expr -> type_function_expr','type_expr',1,'p_type_expr','__init__.py',826),
  ('type_expr -> type_term','type_expr',1,'p_type_expr','__init__.py',827),
  ('type_function_expr -> type_term ARROW _maybe_padding type_function_expr','type_function_expr',4,'p_type_function_expr','__init__.py',832),
  ('type_function_expr -> type_term','type_function_expr',1,'p_type_function_expr','__init__.py',833),
  ('type_term -> type_app_expression','type_term',1,'p_type_term','__init__.py',843),
  ('type_term -> type_factor','type_term',1,'p_type_term','__init__.py',844),
  ('type_app_expression -> type_factor _app_args_non_empty','type_app_expression',2,'p_type_application_expr','__init__.py',849),
  ('_app_args -> SPACE type_factor _app_args','_app_args',3,'p_type_application_args','__init__.py',861),
  ('_app_args_non_empty -> SPACE type_factor _app_args','_app_args_non_empty',3,'p_type_application_args','__init__.py',862),
  ('_app_args -> empty','_app_args',1,'p_type_application_args_empty','__init__.py',870),
  ('type_variable -> LOWER_IDENTIFIER','type_variable',1,'p_type_variable','__init__.py',875),
  ('type_cons -> UPPER_IDENTIFIER','type_cons',1,'p_type_cons','__init__.py',880),
  ('type_factor -> type_variable','type_factor',1,'p_type_factor_identifier','__init__.py',885),
  ('type_factor -> type_cons','type_factor',1,'p_type_factor_identifier','__init__.py',886),
  ('type_factor -> LPAREN _maybe_padding type_expr _maybe_padding RPAREN','type_factor',5,'p_type_factor_paren','__init__.py',893),
  ('type_factor -> LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET','type_factor',5,'p_type_factor_bracket','__init__.py',898),
  ('_maybe_padding -> PADDING','_maybe_padding',1,'p_maybe_padding','__init__.py',903),
  ('_maybe_padding -> empty','_maybe_padding',1,'p_maybe_padding','__init__.py',904),
  ('program -> definitions','program',1,'p_program','__init__.py',910),
  ('definitions -> definition _definition_set','definitions',2,'p_definitions','__init__.py',926),
  ('_definition_set -> NEWLINE definition _definition_set','_definition_set',3,'p_definition_set','__init__.py',934),
  ('_definition_set -> empty','_definition_set',1,'p_definition_set2','__init__.py',942),
  ('definition -> nametype_decl','definition',1,'p_definition','__init__.py',948),
  ('definition -> valuedef','definition',1,'p_definition','__init__.py',949),
  ('definition -> datatype_definition','definition',1,'p_definition','__init__.py',950),
  ('valuedef -> equation','valuedef',1,'p_valuedef','__init__.py',956),
  ('nametype_decl -> _identifier COLON COLON st_type_expr','nametype_decl',4,'p_nametype_decl','__init__.py',962),
  ('nametype_decl -> LPAREN _st_operator RPAREN COLON COLON st_type_expr','nametype_decl',6,'p_nametype_decl_operators','__init__.py',971),
  ('datatype_definition -> _datatype_lhs EQ _data_rhs','datatype_definition',3,'p_datatype_definition','__init__.py',980),
  ('_datatype_lhs -> KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params','_datatype_lhs',4,'p_datatype_lhs','__init__.py',988),
  ('_cons_params -> SPACE LOWER_IDENTIFIER _cons_params','_cons_params',3,'p_datatype_cons_params','__init__.py',997),
  ('_cons_params -> empty','_cons_params',1,'p_datatype_cons_params_empty','__init__.py',1006),
  ('_data_rhs -> data_cons _data_conses','_data_rhs',2,'p_datatype_body','__init__.py',1012),
  ('_data_conses -> _maybe_padding PIPE data_cons _data_conses','_data_conses',4,'p_datatype_body','__init__.py',1013),
  ('_data_conses -> empty','_data_conses',1,'p_datatype_conses_empty','__init__.py',1022),
  ('data_cons -> _data_cons','data_cons',1,'p_data_cons','__init__.py',1027),
  ('_data_cons -> UPPER_IDENTIFIER _cons_args','_data_cons',2,'p_bare_data_cons','__init__.py',1033),
  ('_cons_args -> SPACE cons_arg _cons_args','_cons_args',3,'p_data_cons_args','__init__.py',1038),
  ('_cons_args -> empty','_cons_args',1,'p_data_cons_args_empty','__init__.py',1047),
  ('cons_arg -> type_variable','cons_arg',1,'p_cons_arg','__init__.py',1053),
  ('cons_arg -> type_cons','cons_arg',1,'p_cons_arg','__init__.py',1054),
  ('cons_arg -> _cons_arg_factor','cons_arg',1,'p_cons_arg','__init__.py',1055),
  ('_cons_arg_factor -> LPAREN type_expr RPAREN','_cons_arg_factor',3,'p_cons_arg_factor','__init__.py',1061),
  ('_cons_arg_factor -> LBRACKET type_expr RBRACKET','_cons_arg_factor',3,'p_cons_arg_factor_list','__init__.py',1067),
]
