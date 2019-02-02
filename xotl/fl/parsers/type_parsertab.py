
# type_parsertab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_type_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftKEYWORD_WHEREleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW ATSYM BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON COMMA DATE DATETIME DATETIME_INTERVAL DATE_INTERVAL DOT_OPERATOR DOUBLESLASH EQ FATARROW FLOAT KEYWORD_CLASS KEYWORD_DATA KEYWORD_DERIVING KEYWORD_FORALL KEYWORD_IN KEYWORD_INSTANCE KEYWORD_LET KEYWORD_WHERE LBRACKET LOWER_IDENTIFIER LPAREN MINUS NEWLINE OPERATOR PADDING PERCENT PIPE PLUS RBRACKET RPAREN SLASH SPACE STAR STRING TICK_OPERATOR UNDER_IDENTIFIER UPPER_IDENTIFIERexpr_factor : expr_factor SPACE expr_factor\n    expr_term9 : expr_factor infixr_operator_9 expr_term9\n               | expr_factor\n\n    expr_term7 : expr_term7 infixl_operator_7 expr_term9\n               | expr_term9\n\n    expr_term6 : expr_term6 infixl_operator_6 expr_term7\n               | expr_term7\n\n    expr_term2 : expr_term2 infixl_operator_2 expr_term6\n               | expr_term6\n\n    expr_term1 : expr_term2 infixr_operator_2 expr_term1\n               | expr_term2\n\n    expr_term0 : expr infixl_operator_0 expr_term0\n               | expr_term1\n\n    \n    st_expr : expr\n\n    expr : expr_term0\n\n    expr_factor : literal\n                | identifier\n                | enclosed_expr\n                | letexpr\n                | where_expr\n                | lambda_expr\n                | simple_list_expr\n                | simple_tuple_expr\n\n    st_type_expr : type_expr\n                 | constrained_type_expr\n\n    literal : number\n             | concrete_number\n             | string\n             | char\n             | date\n             | datetime\n             | date_interval\n             | datetime_interval\n    simple_tuple_expr : LPAREN _list_items RPAREN\n    simple_list_expr : LBRACKET _list_items RBRACKET\n    _list_items : expr _list_items_cont\n       _list_items_cont : COMMA expr _list_items_cont\n    _list_items : empty\n       _list_items_cont : empty\n    date : DATE\n    datetime : DATETIME\n    date_interval : DATE_INTERVAL\n    datetime_interval : DATETIME_INTERVAL\n    char : CHARstring : STRINGidentifier : _identifier\n\n    _identifier : UNDER_IDENTIFIER\n                   | UPPER_IDENTIFIER\n                   | LOWER_IDENTIFIER\n\n    enclosed_expr : LPAREN expr RPARENexpr_factor : enclosed_expr expr_factor\n                   | expr_factor enclosed_expr\n    enclosed_expr : _enclosed_operator\n    _enclosed_operator : LPAREN _st_operator RPAREN\n    infixr_operator_9 : DOT_OPERATOR\n\n    infixl_operator_7 : STAR\n                     | SLASH\n                     | DOUBLESLASH\n                     | PERCENT\n\n    infixl_operator_6 : PLUS\n                     | MINUS\n\n\n    infixr_operator_2 : COLON\n\n    infixl_operator_2 : OPERATOR\n                      | ARROW\n                      | ATSYM\n\n    infixl_operator_0 : TICK_OPERATOR\n\n    _st_operator : infixl_operator_2\n                 | infixr_operator_2\n                 | infixl_operator_6\n                 | infixl_operator_7\n                 | infixr_operator_9\n                 | COMMA\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : lambda_expr : BACKSLASH patterns ARROW expr\n    \n    pattern : possibly_named_pattern\n\n    simple_pattern : literal\n    simple_pattern : cons_pattern\n    simple_pattern : list_cons_pattern\n    simple_pattern : tuple_cons_pattern\n    simple_pattern : empty_list_pattern\n    simple_pattern : empty_tuple_pattern\n    simple_pattern : LOWER_IDENTIFIER\n       simple_pattern : UNDER_IDENTIFIER\n    possibly_named_pattern : _pattern_name simple_pattern\n    _pattern_name : LOWER_IDENTIFIER ATSYM\n    _pattern_name : empty\n    simple_pattern : UPPER_IDENTIFIER\n    list_cons_pattern : pattern COLON pattern\n       list_cons_pattern : simple_pattern COLON simple_pattern\n    cons_pattern : LPAREN _identifier SPACE patterns RPAREN\n    simple_pattern : LPAREN pattern RPAREN\n    simple_pattern : LPAREN simple_pattern RPAREN\n    empty_list_pattern : LBRACKET RBRACKETempty_tuple_pattern : LPAREN RPARENtuple_cons_pattern : LPAREN patterns_comma_sep RPAREN\n    patterns : pattern _patterns\n       patterns : simple_pattern _patterns\n       patterns_comma_sep : pattern _patterns_comma\n       patterns_comma_sep : simple_pattern _patterns_comma\n       _patterns : SPACE pattern _patterns\n       _patterns : SPACE simple_pattern _patterns\n       _patterns_comma : COMMA pattern _patterns_comma_trail\n       _patterns_comma : COMMA simple_pattern _patterns_comma_trail\n       _patterns_comma_trail : COMMA pattern _patterns_comma_trail\n       _patterns_comma_trail : COMMA simple_pattern _patterns_comma_trail\n    _patterns : empty\n       _patterns_comma_trail : empty\n    equation : _identifier _patterns EQ expr\n       equation : _enclosed_operator _patterns EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    \n    letexpr : KEYWORD_LET SPACE local_definitions KEYWORD_IN SPACE st_expr\n\n    \n    where_expr : expr KEYWORD_WHERE SPACE equations\n    where_expr : expr KEYWORD_WHERE PADDING equations\n    type_expr : type_scheme type_function_expr\n                 | type_scheme type_termtype_scheme : emptytype_scheme : KEYWORD_FORALL SPACE _type_scheme_generics_type_scheme_generics : _identifier SPACE _type_scheme_generics_type_scheme_generics : _identifier DOT_OPERATORtype_function_expr : type_term ARROW _maybe_padding type_function_expr\n                          | type_term\n    type_term : type_app_expression\n                 | type_factortype_app_expression : type_factor _app_args_non_empty_app_args : SPACE type_factor _app_args\n       _app_args_non_empty : SPACE type_factor _app_args\n    _app_args : emptytype_variable : LOWER_IDENTIFIERtype_cons : UPPER_IDENTIFIERtype_factor : type_variable\n                   | type_cons\n\n    type_factor : LPAREN _maybe_padding _type_expr_list _maybe_padding RPARENtype_factor : LPAREN RPAREN_type_expr_list : type_expr COMMA _type_expr_list_trail\n       _type_expr_list_trail : type_expr COMMA _type_expr_list_trail\n    _type_expr_list_trail : type_expr\n    type_factor : LPAREN _maybe_padding type_expr _maybe_padding RPARENtype_factor : LBRACKET _maybe_padding type_expr _maybe_padding RBRACKETconstrained_type_expr : _constrained_type_expr_bare\n\n    _constrained_type_expr_bare : type_constraints FATARROW type_expr\n    _maybe_constrained_type_expr : type_expr\n    _maybe_constrained_type_expr : _constrained_type_expr_bare\n    instance : KEYWORD_INSTANCE _maybe_constrained_type_expr                   KEYWORD_WHERE PADDING local_definitionstype_constraints : _type_expr_list_trail\n    _maybe_padding : PADDING\n                      | empty\n    program : definitions _trailing_new_lines\n    _trailing_new_lines : empty\n       _trailing_new_lines : NEWLINE _trailing_new_lines\n    definitions : definition _definition_set\n    _definition_set : newlines definition _definition_set\n    newlines : NEWLINE _trailing_new_lines_definition_set : empty\n       _definition_set : newlines\n    definition : local_definition\n                  | datatype_definition\n                  | typeclass\n                  | instance\n    \n    local_definition : nametype_decl\n                     | valuedef\n    local_definitions : local_definition _local_definition_set\n    _local_definition_set : PADDING definition _local_definition_set\n    _local_definition_set : empty\n    typeclass : KEYWORD_CLASS _typeclass_def                    KEYWORD_WHERE PADDING local_definitions\n    _typeclass_def : simple_type_constraint\n    _typeclass_def : simple_type_constraints FATARROW simple_type_constraint\n    simple_type_constraint : UPPER_IDENTIFIER SPACE type_variable\n    simple_type_constraints : simple_type_constraint _simple_type_constraints\n       _simple_type_constraints : COMMA simple_type_constraint _simple_type_constraints\n    _simple_type_constraints : empty\n    valuedef : equation\n    nametype_decl : _identifier COLON COLON st_type_expr\n    nametype_decl : LPAREN _st_operator RPAREN COLON COLON st_type_expr\n    datatype_definition : _datatype_lhs EQ _data_rhs\n    _datatype_lhs : KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params\n    _cons_params : SPACE LOWER_IDENTIFIER _cons_params\n    _cons_params : empty\n    _data_rhs : data_cons _data_conses\n       _data_conses : _maybe_padding PIPE data_cons _data_conses\n    _data_conses : empty_data_conses : _maybe_padding KEYWORD_DERIVING                        LPAREN _derivations_list RPARENdata_cons : _data_cons_data_cons : UPPER_IDENTIFIER _cons_args_cons_args : SPACE cons_arg _cons_args\n    _cons_args : empty\n    cons_arg : type_variable\n       cons_arg : type_cons\n       cons_arg : _cons_arg_factor\n    _cons_arg_factor : LPAREN type_expr RPAREN\n    _cons_arg_factor : LBRACKET type_expr RBRACKET\n    _derivations_list : UPPER_IDENTIFIER _derivations_list_trail\n       _derivations_list_trail : COMMA UPPER_IDENTIFIER _derivations_list_trail\n    _derivations_list_trail : empty\n    '
    
_lr_action_items = {'KEYWORD_FORALL':([0,10,17,18,22,28,30,31,32,53,],[7,7,-81,-81,7,7,-155,-156,7,7,]),'LPAREN':([0,4,6,10,17,18,22,25,27,28,30,31,32,33,39,45,48,53,55,],[-81,17,-126,-81,-81,-81,-81,-81,17,-81,-155,-156,-81,-127,17,-129,17,-81,-128,]),'LBRACKET':([0,4,6,10,17,18,22,25,27,28,30,31,32,33,39,45,48,53,55,],[-81,18,-126,-81,-81,-81,-81,-81,18,-81,-155,-156,-81,-127,18,-129,18,-81,-128,]),'LOWER_IDENTIFIER':([0,4,6,10,17,18,21,22,25,27,28,30,31,32,33,39,44,45,48,53,55,],[-81,19,-126,-81,-81,-81,37,-81,-81,19,-81,-155,-156,-81,-127,19,37,-129,19,-81,-128,]),'UPPER_IDENTIFIER':([0,4,6,10,17,18,21,22,25,27,28,30,31,32,33,39,44,45,48,53,55,],[-81,20,-126,-81,-81,-81,36,-81,-81,20,-81,-155,-156,-81,-127,20,36,-129,20,-81,-128,]),'$end':([1,2,3,5,11,12,13,14,15,16,19,20,26,29,38,40,46,47,49,50,56,57,58,60,61,],[0,-24,-25,-149,-124,-125,-132,-133,-140,-141,-138,-139,-134,-143,-150,-81,-131,-130,-136,-137,-81,-142,-147,-148,-135,]),'COMMA':([2,11,12,13,14,15,16,19,20,23,26,29,40,42,46,47,49,50,56,57,58,60,61,],[10,-124,-125,-132,-133,-140,-141,-138,-139,10,-134,-143,-81,53,-131,-130,-136,-137,-81,-142,-147,-148,-135,]),'FATARROW':([2,8,9,11,12,13,14,15,16,19,20,23,24,26,29,40,46,47,49,50,56,57,58,60,61,],[-146,22,-154,-124,-125,-132,-133,-140,-141,-138,-139,-146,-145,-134,-143,-81,-131,-130,-136,-137,-81,-142,-147,-148,-135,]),'SPACE':([7,14,15,16,19,20,29,34,35,36,37,40,56,57,58,60,],[21,27,-140,-141,-138,-139,-143,44,-47,-48,-49,48,48,-142,-147,-148,]),'PADDING':([11,12,13,14,15,16,17,18,19,20,23,24,25,26,29,40,41,42,43,46,47,49,50,56,57,58,59,60,61,],[-124,-125,-132,-133,-140,-141,30,30,-138,-139,-146,-145,30,-134,-143,-81,30,30,30,-131,-130,-136,-137,-81,-142,-147,-144,-148,-135,]),'RPAREN':([11,12,13,14,15,16,17,19,20,23,24,26,29,30,31,40,41,42,46,47,49,50,51,52,56,57,58,59,60,61,],[-124,-125,-132,-133,-140,-141,29,-138,-139,-146,-145,-134,-143,-155,-156,-81,-81,-81,-131,-130,-136,-137,57,58,-81,-142,-147,-144,-148,-135,]),'RBRACKET':([11,12,13,14,15,16,19,20,26,29,30,31,40,43,46,47,49,50,54,56,57,58,60,61,],[-124,-125,-132,-133,-140,-141,-138,-139,-134,-143,-155,-156,-81,-81,-131,-130,-136,-137,60,-81,-142,-147,-148,-135,]),'ARROW':([12,13,14,15,16,19,20,26,29,40,46,49,50,56,57,58,60,61,],[25,-132,-133,-140,-141,-138,-139,-134,-143,-81,25,-136,-137,-81,-142,-147,-148,-135,]),'UNDER_IDENTIFIER':([21,44,],[35,35,]),'DOT_OPERATOR':([34,35,36,37,],[45,-47,-48,-49,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'st_type_expr':([0,],[1,]),'type_expr':([0,10,22,28,32,53,],[2,23,38,42,43,23,]),'constrained_type_expr':([0,],[3,]),'type_scheme':([0,10,22,28,32,53,],[4,4,4,4,4,4,]),'_constrained_type_expr_bare':([0,],[5,]),'empty':([0,10,17,18,22,25,28,32,40,41,42,43,53,56,],[6,6,31,31,6,31,6,6,50,31,31,31,6,50,]),'type_constraints':([0,],[8,]),'_type_expr_list_trail':([0,10,53,],[9,24,59,]),'type_function_expr':([4,39,],[11,47,]),'type_term':([4,39,],[12,46,]),'type_app_expression':([4,39,],[13,13,]),'type_factor':([4,27,39,48,],[14,40,14,56,]),'type_variable':([4,27,39,48,],[15,15,15,15,]),'type_cons':([4,27,39,48,],[16,16,16,16,]),'_app_args_non_empty':([14,],[26,]),'_maybe_padding':([17,18,25,41,42,43,],[28,32,39,51,52,54,]),'_type_scheme_generics':([21,44,],[33,55,]),'_identifier':([21,44,],[34,34,]),'_type_expr_list':([28,],[41,]),'_app_args':([40,56,],[49,61,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> st_type_expr","S'",1,None,None,None),
  ('expr_factor -> expr_factor SPACE expr_factor','expr_factor',3,'p_application','__init__.py',531),
  ('expr_term9 -> expr_factor infixr_operator_9 expr_term9','expr_term9',3,'p_expressions_precedence_rules','__init__.py',538),
  ('expr_term9 -> expr_factor','expr_term9',1,'p_expressions_precedence_rules','__init__.py',539),
  ('expr_term7 -> expr_term7 infixl_operator_7 expr_term9','expr_term7',3,'p_expressions_precedence_rules','__init__.py',541),
  ('expr_term7 -> expr_term9','expr_term7',1,'p_expressions_precedence_rules','__init__.py',542),
  ('expr_term6 -> expr_term6 infixl_operator_6 expr_term7','expr_term6',3,'p_expressions_precedence_rules','__init__.py',544),
  ('expr_term6 -> expr_term7','expr_term6',1,'p_expressions_precedence_rules','__init__.py',545),
  ('expr_term2 -> expr_term2 infixl_operator_2 expr_term6','expr_term2',3,'p_expressions_precedence_rules','__init__.py',547),
  ('expr_term2 -> expr_term6','expr_term2',1,'p_expressions_precedence_rules','__init__.py',548),
  ('expr_term1 -> expr_term2 infixr_operator_2 expr_term1','expr_term1',3,'p_expressions_precedence_rules','__init__.py',550),
  ('expr_term1 -> expr_term2','expr_term1',1,'p_expressions_precedence_rules','__init__.py',551),
  ('expr_term0 -> expr infixl_operator_0 expr_term0','expr_term0',3,'p_expressions_precedence_rules','__init__.py',553),
  ('expr_term0 -> expr_term1','expr_term0',1,'p_expressions_precedence_rules','__init__.py',554),
  ('st_expr -> expr','st_expr',1,'p_standalone_definitions','__init__.py',567),
  ('expr -> expr_term0','expr',1,'p_standalone_definitions','__init__.py',569),
  ('expr_factor -> literal','expr_factor',1,'p_standalone_definitions','__init__.py',571),
  ('expr_factor -> identifier','expr_factor',1,'p_standalone_definitions','__init__.py',572),
  ('expr_factor -> enclosed_expr','expr_factor',1,'p_standalone_definitions','__init__.py',573),
  ('expr_factor -> letexpr','expr_factor',1,'p_standalone_definitions','__init__.py',574),
  ('expr_factor -> where_expr','expr_factor',1,'p_standalone_definitions','__init__.py',575),
  ('expr_factor -> lambda_expr','expr_factor',1,'p_standalone_definitions','__init__.py',576),
  ('expr_factor -> simple_list_expr','expr_factor',1,'p_standalone_definitions','__init__.py',577),
  ('expr_factor -> simple_tuple_expr','expr_factor',1,'p_standalone_definitions','__init__.py',578),
  ('st_type_expr -> type_expr','st_type_expr',1,'p_standalone_definitions','__init__.py',580),
  ('st_type_expr -> constrained_type_expr','st_type_expr',1,'p_standalone_definitions','__init__.py',581),
  ('literal -> number','literal',1,'p_literals','__init__.py',589),
  ('literal -> concrete_number','literal',1,'p_literals','__init__.py',590),
  ('literal -> string','literal',1,'p_literals','__init__.py',591),
  ('literal -> char','literal',1,'p_literals','__init__.py',592),
  ('literal -> date','literal',1,'p_literals','__init__.py',593),
  ('literal -> datetime','literal',1,'p_literals','__init__.py',594),
  ('literal -> date_interval','literal',1,'p_literals','__init__.py',595),
  ('literal -> datetime_interval','literal',1,'p_literals','__init__.py',596),
  ('simple_tuple_expr -> LPAREN _list_items RPAREN','simple_tuple_expr',3,'p_tuple_expr','__init__.py',602),
  ('simple_list_expr -> LBRACKET _list_items RBRACKET','simple_list_expr',3,'p_list_expr','__init__.py',609),
  ('_list_items -> expr _list_items_cont','_list_items',2,'p_list_items','__init__.py',616),
  ('_list_items_cont -> COMMA expr _list_items_cont','_list_items_cont',3,'p_list_items','__init__.py',617),
  ('_list_items -> empty','_list_items',1,'p_list_items_empty','__init__.py',623),
  ('_list_items_cont -> empty','_list_items_cont',1,'p_list_items_empty','__init__.py',624),
  ('date -> DATE','date',1,'p_date','__init__.py',630),
  ('datetime -> DATETIME','datetime',1,'p_datetime','__init__.py',636),
  ('date_interval -> DATE_INTERVAL','date_interval',1,'p_date_interval','__init__.py',642),
  ('datetime_interval -> DATETIME_INTERVAL','datetime_interval',1,'p_datetime_interval','__init__.py',648),
  ('char -> CHAR','char',1,'p_char','__init__.py',654),
  ('string -> STRING','string',1,'p_string','__init__.py',659),
  ('identifier -> _identifier','identifier',1,'p_variable','__init__.py',664),
  ('_identifier -> UNDER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',671),
  ('_identifier -> UPPER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',672),
  ('_identifier -> LOWER_IDENTIFIER','_identifier',1,'p_bare_identifier','__init__.py',673),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','__init__.py',680),
  ('expr_factor -> enclosed_expr expr_factor','expr_factor',2,'p_application_after_paren','__init__.py',685),
  ('expr_factor -> expr_factor enclosed_expr','expr_factor',2,'p_application_after_paren','__init__.py',686),
  ('enclosed_expr -> _enclosed_operator','enclosed_expr',1,'p_operators_as_expressios','__init__.py',692),
  ('_enclosed_operator -> LPAREN _st_operator RPAREN','_enclosed_operator',3,'p_enclosed_operator','__init__.py',698),
  ('infixr_operator_9 -> DOT_OPERATOR','infixr_operator_9',1,'p_operator','__init__.py',708),
  ('infixl_operator_7 -> STAR','infixl_operator_7',1,'p_operator','__init__.py',710),
  ('infixl_operator_7 -> SLASH','infixl_operator_7',1,'p_operator','__init__.py',711),
  ('infixl_operator_7 -> DOUBLESLASH','infixl_operator_7',1,'p_operator','__init__.py',712),
  ('infixl_operator_7 -> PERCENT','infixl_operator_7',1,'p_operator','__init__.py',713),
  ('infixl_operator_6 -> PLUS','infixl_operator_6',1,'p_operator','__init__.py',715),
  ('infixl_operator_6 -> MINUS','infixl_operator_6',1,'p_operator','__init__.py',716),
  ('infixr_operator_2 -> COLON','infixr_operator_2',1,'p_operator','__init__.py',719),
  ('infixl_operator_2 -> OPERATOR','infixl_operator_2',1,'p_operator','__init__.py',721),
  ('infixl_operator_2 -> ARROW','infixl_operator_2',1,'p_operator','__init__.py',722),
  ('infixl_operator_2 -> ATSYM','infixl_operator_2',1,'p_operator','__init__.py',723),
  ('infixl_operator_0 -> TICK_OPERATOR','infixl_operator_0',1,'p_operator','__init__.py',725),
  ('_st_operator -> infixl_operator_2','_st_operator',1,'p_operator','__init__.py',727),
  ('_st_operator -> infixr_operator_2','_st_operator',1,'p_operator','__init__.py',728),
  ('_st_operator -> infixl_operator_6','_st_operator',1,'p_operator','__init__.py',729),
  ('_st_operator -> infixl_operator_7','_st_operator',1,'p_operator','__init__.py',730),
  ('_st_operator -> infixr_operator_9','_st_operator',1,'p_operator','__init__.py',731),
  ('_st_operator -> COMMA','_st_operator',1,'p_operator','__init__.py',732),
  ('number -> BASE10_INTEGER','number',1,'p_integer','__init__.py',739),
  ('number -> BASE16_INTEGER','number',1,'p_integer','__init__.py',740),
  ('number -> BASE8_INTEGER','number',1,'p_integer','__init__.py',741),
  ('number -> BASE2_INTEGER','number',1,'p_integer','__init__.py',742),
  ('number -> FLOAT','number',1,'p_float','__init__.py',771),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','__init__.py',776),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','__init__.py',777),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','__init__.py',778),
  ('empty -> <empty>','empty',0,'p_empty','__init__.py',787),
  ('lambda_expr -> BACKSLASH patterns ARROW expr','lambda_expr',4,'p_lambda_definition','__init__.py',792),
  ('pattern -> possibly_named_pattern','pattern',1,'p_pattern','__init__.py',801),
  ('simple_pattern -> literal','simple_pattern',1,'p_pattern','__init__.py',803),
  ('simple_pattern -> cons_pattern','simple_pattern',1,'p_pattern','__init__.py',804),
  ('simple_pattern -> list_cons_pattern','simple_pattern',1,'p_pattern','__init__.py',805),
  ('simple_pattern -> tuple_cons_pattern','simple_pattern',1,'p_pattern','__init__.py',806),
  ('simple_pattern -> empty_list_pattern','simple_pattern',1,'p_pattern','__init__.py',807),
  ('simple_pattern -> empty_tuple_pattern','simple_pattern',1,'p_pattern','__init__.py',808),
  ('simple_pattern -> LOWER_IDENTIFIER','simple_pattern',1,'p_var_pattern','__init__.py',814),
  ('simple_pattern -> UNDER_IDENTIFIER','simple_pattern',1,'p_var_pattern','__init__.py',815),
  ('possibly_named_pattern -> _pattern_name simple_pattern','possibly_named_pattern',2,'p_possibly_named_pattern','__init__.py',821),
  ('_pattern_name -> LOWER_IDENTIFIER ATSYM','_pattern_name',2,'p_pattern_name','__init__.py',832),
  ('_pattern_name -> empty','_pattern_name',1,'p_no_pattern_name','__init__.py',838),
  ('simple_pattern -> UPPER_IDENTIFIER','simple_pattern',1,'p_simplecons_pattern','__init__.py',845),
  ('list_cons_pattern -> pattern COLON pattern','list_cons_pattern',3,'p_list_cons_for_param','__init__.py',851),
  ('list_cons_pattern -> simple_pattern COLON simple_pattern','list_cons_pattern',3,'p_list_cons_for_param','__init__.py',852),
  ('cons_pattern -> LPAREN _identifier SPACE patterns RPAREN','cons_pattern',5,'p_param_pattern','__init__.py',858),
  ('simple_pattern -> LPAREN pattern RPAREN','simple_pattern',3,'p_pattern_trivially_enclosed','__init__.py',866),
  ('simple_pattern -> LPAREN simple_pattern RPAREN','simple_pattern',3,'p_pattern_trivially_enclosed','__init__.py',867),
  ('empty_list_pattern -> LBRACKET RBRACKET','empty_list_pattern',2,'p_empty_list_as_pattern','__init__.py',873),
  ('empty_tuple_pattern -> LPAREN RPAREN','empty_tuple_pattern',2,'p_unit_value_as_pattern','__init__.py',880),
  ('tuple_cons_pattern -> LPAREN patterns_comma_sep RPAREN','tuple_cons_pattern',3,'p_tuple_cons_pattern','__init__.py',886),
  ('patterns -> pattern _patterns','patterns',2,'p_patterns','__init__.py',894),
  ('patterns -> simple_pattern _patterns','patterns',2,'p_patterns','__init__.py',895),
  ('patterns_comma_sep -> pattern _patterns_comma','patterns_comma_sep',2,'p_patterns','__init__.py',896),
  ('patterns_comma_sep -> simple_pattern _patterns_comma','patterns_comma_sep',2,'p_patterns','__init__.py',897),
  ('_patterns -> SPACE pattern _patterns','_patterns',3,'p_patterns','__init__.py',898),
  ('_patterns -> SPACE simple_pattern _patterns','_patterns',3,'p_patterns','__init__.py',899),
  ('_patterns_comma -> COMMA pattern _patterns_comma_trail','_patterns_comma',3,'p_patterns','__init__.py',900),
  ('_patterns_comma -> COMMA simple_pattern _patterns_comma_trail','_patterns_comma',3,'p_patterns','__init__.py',901),
  ('_patterns_comma_trail -> COMMA pattern _patterns_comma_trail','_patterns_comma_trail',3,'p_patterns','__init__.py',902),
  ('_patterns_comma_trail -> COMMA simple_pattern _patterns_comma_trail','_patterns_comma_trail',3,'p_patterns','__init__.py',903),
  ('_patterns -> empty','_patterns',1,'p_patterns_empty','__init__.py',909),
  ('_patterns_comma_trail -> empty','_patterns_comma_trail',1,'p_patterns_empty','__init__.py',910),
  ('equation -> _identifier _patterns EQ expr','equation',4,'p_equation','__init__.py',916),
  ('equation -> _enclosed_operator _patterns EQ expr','equation',4,'p_equation','__init__.py',917),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','__init__.py',927),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','__init__.py',935),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','__init__.py',942),
  ('letexpr -> KEYWORD_LET SPACE local_definitions KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','__init__.py',952),
  ('where_expr -> expr KEYWORD_WHERE SPACE equations','where_expr',4,'p_where_expr','__init__.py',960),
  ('where_expr -> expr KEYWORD_WHERE PADDING equations','where_expr',4,'p_where_expr','__init__.py',961),
  ('type_expr -> type_scheme type_function_expr','type_expr',2,'p_type_expr','__init__.py',971),
  ('type_expr -> type_scheme type_term','type_expr',2,'p_type_expr','__init__.py',972),
  ('type_scheme -> empty','type_scheme',1,'p_type_scheme_empty','__init__.py',981),
  ('type_scheme -> KEYWORD_FORALL SPACE _type_scheme_generics','type_scheme',3,'p_type_scheme','__init__.py',985),
  ('_type_scheme_generics -> _identifier SPACE _type_scheme_generics','_type_scheme_generics',3,'p_type_scheme_generics','__init__.py',992),
  ('_type_scheme_generics -> _identifier DOT_OPERATOR','_type_scheme_generics',2,'p_last_type_scheme_generic','__init__.py',997),
  ('type_function_expr -> type_term ARROW _maybe_padding type_function_expr','type_function_expr',4,'p_type_function_expr','__init__.py',1002),
  ('type_function_expr -> type_term','type_function_expr',1,'p_type_function_expr','__init__.py',1003),
  ('type_term -> type_app_expression','type_term',1,'p_type_term','__init__.py',1013),
  ('type_term -> type_factor','type_term',1,'p_type_term','__init__.py',1014),
  ('type_app_expression -> type_factor _app_args_non_empty','type_app_expression',2,'p_type_application_expr','__init__.py',1019),
  ('_app_args -> SPACE type_factor _app_args','_app_args',3,'p_type_application_args','__init__.py',1031),
  ('_app_args_non_empty -> SPACE type_factor _app_args','_app_args_non_empty',3,'p_type_application_args','__init__.py',1032),
  ('_app_args -> empty','_app_args',1,'p_type_application_args_empty','__init__.py',1038),
  ('type_variable -> LOWER_IDENTIFIER','type_variable',1,'p_type_variable','__init__.py',1043),
  ('type_cons -> UPPER_IDENTIFIER','type_cons',1,'p_type_cons','__init__.py',1048),
  ('type_factor -> type_variable','type_factor',1,'p_type_factor_identifier','__init__.py',1053),
  ('type_factor -> type_cons','type_factor',1,'p_type_factor_identifier','__init__.py',1054),
  ('type_factor -> LPAREN _maybe_padding _type_expr_list _maybe_padding RPAREN','type_factor',5,'p_type_factor_tuple','__init__.py',1061),
  ('type_factor -> LPAREN RPAREN','type_factor',2,'p_type_factor_unit_type','__init__.py',1067),
  ('_type_expr_list -> type_expr COMMA _type_expr_list_trail','_type_expr_list',3,'p_type_expr_list','__init__.py',1072),
  ('_type_expr_list_trail -> type_expr COMMA _type_expr_list_trail','_type_expr_list_trail',3,'p_type_expr_list','__init__.py',1073),
  ('_type_expr_list_trail -> type_expr','_type_expr_list_trail',1,'p_type_expr_list_last_item','__init__.py',1079),
  ('type_factor -> LPAREN _maybe_padding type_expr _maybe_padding RPAREN','type_factor',5,'p_type_factor_paren','__init__.py',1085),
  ('type_factor -> LBRACKET _maybe_padding type_expr _maybe_padding RBRACKET','type_factor',5,'p_type_factor_bracket','__init__.py',1090),
  ('constrained_type_expr -> _constrained_type_expr_bare','constrained_type_expr',1,'p_constrained_type_expr','__init__.py',1122),
  ('_constrained_type_expr_bare -> type_constraints FATARROW type_expr','_constrained_type_expr_bare',3,'p_constrained_type_expr_bare','__init__.py',1130),
  ('_maybe_constrained_type_expr -> type_expr','_maybe_constrained_type_expr',1,'p_maybe_constrained_type_expr_no_constraint','__init__.py',1149),
  ('_maybe_constrained_type_expr -> _constrained_type_expr_bare','_maybe_constrained_type_expr',1,'p_maybe_constrained_type_expr_constrained','__init__.py',1155),
  ('instance -> KEYWORD_INSTANCE _maybe_constrained_type_expr KEYWORD_WHERE PADDING local_definitions','instance',5,'p_instance','__init__.py',1161),
  ('type_constraints -> _type_expr_list_trail','type_constraints',1,'p_type_constraint','__init__.py',1180),
  ('_maybe_padding -> PADDING','_maybe_padding',1,'p_maybe_padding','__init__.py',1186),
  ('_maybe_padding -> empty','_maybe_padding',1,'p_maybe_padding','__init__.py',1187),
  ('program -> definitions _trailing_new_lines','program',2,'p_program','__init__.py',1195),
  ('_trailing_new_lines -> empty','_trailing_new_lines',1,'p_trailing_new_lines','__init__.py',1201),
  ('_trailing_new_lines -> NEWLINE _trailing_new_lines','_trailing_new_lines',2,'p_trailing_new_lines','__init__.py',1202),
  ('definitions -> definition _definition_set','definitions',2,'p_definitions','__init__.py',1207),
  ('_definition_set -> newlines definition _definition_set','_definition_set',3,'p_definition_set','__init__.py',1213),
  ('newlines -> NEWLINE _trailing_new_lines','newlines',2,'p_newlines','__init__.py',1219),
  ('_definition_set -> empty','_definition_set',1,'p_definition_set2','__init__.py',1223),
  ('_definition_set -> newlines','_definition_set',1,'p_definition_set2','__init__.py',1224),
  ('definition -> local_definition','definition',1,'p_definition','__init__.py',1230),
  ('definition -> datatype_definition','definition',1,'p_definition','__init__.py',1231),
  ('definition -> typeclass','definition',1,'p_definition','__init__.py',1232),
  ('definition -> instance','definition',1,'p_definition','__init__.py',1233),
  ('local_definition -> nametype_decl','local_definition',1,'p_local_definition','__init__.py',1240),
  ('local_definition -> valuedef','local_definition',1,'p_local_definition','__init__.py',1241),
  ('local_definitions -> local_definition _local_definition_set','local_definitions',2,'p_local_definitions','__init__.py',1247),
  ('_local_definition_set -> PADDING definition _local_definition_set','_local_definition_set',3,'p_local_definition_set','__init__.py',1253),
  ('_local_definition_set -> empty','_local_definition_set',1,'p_local_definition_set_empty','__init__.py',1259),
  ('typeclass -> KEYWORD_CLASS _typeclass_def KEYWORD_WHERE PADDING local_definitions','typeclass',5,'p_typeclass','__init__.py',1265),
  ('_typeclass_def -> simple_type_constraint','_typeclass_def',1,'p_typeclass_def','__init__.py',1273),
  ('_typeclass_def -> simple_type_constraints FATARROW simple_type_constraint','_typeclass_def',3,'p_typeclass_def_with_constraints','__init__.py',1279),
  ('simple_type_constraint -> UPPER_IDENTIFIER SPACE type_variable','simple_type_constraint',3,'p_type_constraint_def','__init__.py',1285),
  ('simple_type_constraints -> simple_type_constraint _simple_type_constraints','simple_type_constraints',2,'p_type_constraints','__init__.py',1291),
  ('_simple_type_constraints -> COMMA simple_type_constraint _simple_type_constraints','_simple_type_constraints',3,'p_type_constraints','__init__.py',1292),
  ('_simple_type_constraints -> empty','_simple_type_constraints',1,'p_type_constraints_empty','__init__.py',1298),
  ('valuedef -> equation','valuedef',1,'p_valuedef','__init__.py',1304),
  ('nametype_decl -> _identifier COLON COLON st_type_expr','nametype_decl',4,'p_nametype_decl','__init__.py',1310),
  ('nametype_decl -> LPAREN _st_operator RPAREN COLON COLON st_type_expr','nametype_decl',6,'p_nametype_decl_operators','__init__.py',1319),
  ('datatype_definition -> _datatype_lhs EQ _data_rhs','datatype_definition',3,'p_datatype_definition','__init__.py',1328),
  ('_datatype_lhs -> KEYWORD_DATA SPACE UPPER_IDENTIFIER _cons_params','_datatype_lhs',4,'p_datatype_lhs','__init__.py',1341),
  ('_cons_params -> SPACE LOWER_IDENTIFIER _cons_params','_cons_params',3,'p_datatype_cons_params','__init__.py',1350),
  ('_cons_params -> empty','_cons_params',1,'p_datatype_cons_params_empty','__init__.py',1356),
  ('_data_rhs -> data_cons _data_conses','_data_rhs',2,'p_datatype_body','__init__.py',1362),
  ('_data_conses -> _maybe_padding PIPE data_cons _data_conses','_data_conses',4,'p_datatype_body','__init__.py',1363),
  ('_data_conses -> empty','_data_conses',1,'p_datatype_conses_empty','__init__.py',1369),
  ('_data_conses -> _maybe_padding KEYWORD_DERIVING LPAREN _derivations_list RPAREN','_data_conses',5,'p_datatype_derivations','__init__.py',1374),
  ('data_cons -> _data_cons','data_cons',1,'p_data_cons','__init__.py',1380),
  ('_data_cons -> UPPER_IDENTIFIER _cons_args','_data_cons',2,'p_bare_data_cons','__init__.py',1386),
  ('_cons_args -> SPACE cons_arg _cons_args','_cons_args',3,'p_data_cons_args','__init__.py',1391),
  ('_cons_args -> empty','_cons_args',1,'p_data_cons_args_empty','__init__.py',1397),
  ('cons_arg -> type_variable','cons_arg',1,'p_cons_arg','__init__.py',1403),
  ('cons_arg -> type_cons','cons_arg',1,'p_cons_arg','__init__.py',1404),
  ('cons_arg -> _cons_arg_factor','cons_arg',1,'p_cons_arg','__init__.py',1405),
  ('_cons_arg_factor -> LPAREN type_expr RPAREN','_cons_arg_factor',3,'p_cons_arg_factor','__init__.py',1411),
  ('_cons_arg_factor -> LBRACKET type_expr RBRACKET','_cons_arg_factor',3,'p_cons_arg_factor_list','__init__.py',1417),
  ('_derivations_list -> UPPER_IDENTIFIER _derivations_list_trail','_derivations_list',2,'p_derivations_list','__init__.py',1423),
  ('_derivations_list_trail -> COMMA UPPER_IDENTIFIER _derivations_list_trail','_derivations_list_trail',3,'p_derivations_list','__init__.py',1424),
  ('_derivations_list_trail -> empty','_derivations_list_trail',1,'p_derivations_list_trail_empty','__init__.py',1430),
]
