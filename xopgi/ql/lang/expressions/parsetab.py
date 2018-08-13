
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON DOT_OPERATOR DOUBLESLASH EQ FLOAT IDENTIFIER KEYWORD_IN KEYWORD_LET LPAREN MINUS OPERATOR PADDING PERCENT PLUS RPAREN SLASH SPACE STAR STRING TICK_OPERATORst_expr : expr\n               | PADDING expr\n    expr :  number\n             | concrete_number\n             | string\n             | char\n             | identifier\n             | enclosed_expr\n             | letexpr\n    char : CHARstring : STRINGidentifier : IDENTIFIERenclosed_expr : LPAREN expr RPARENexpr : expr TICK_OPERATOR exprexpr : expr SPACE exprexpr : enclosed_expr expr\n            | expr enclosed_expr\n    \n    expr : expr DOT_OPERATOR expr\n    enclosed_expr : LPAREN DOT_OPERATOR RPAREN\n                     | LPAREN operator RPAREN\n    expr : expr operator expr\n\n    \n    operator :  PLUS\n              | MINUS\n              | STAR\n              | SLASH\n              | DOUBLESLASH\n              | PERCENT\n              | ARROW\n              | OPERATOR\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : PLUS numbernumber : MINUS numbernumber : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : expr : BACKSLASH parameters ARROW expr\n    parameters : IDENTIFIER _parameters\n    _parameters : SPACE IDENTIFIER _parameters_parameters : empty\n    pattern : parametersequation : pattern EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr\n\n    '

_lr_action_items = {'PADDING':([0,2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,26,37,39,42,43,50,51,52,53,54,55,56,61,62,63,65,68,76,77,78,79,],[3,-1,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,-17,-2,-16,-34,-35,-14,-15,-18,-21,-37,-38,-39,-13,-19,-20,72,-41,3,72,-46,-50,]),'BACKSLASH':([0,3,9,22,24,25,27,28,29,30,31,32,33,34,35,36,57,61,62,63,74,76,],[11,11,11,11,11,11,11,11,-22,-23,-24,-25,-26,-27,-28,-29,11,-13,-19,-20,11,11,]),'BASE10_INTEGER':([0,3,9,16,17,22,24,25,27,28,29,30,31,32,33,34,35,36,47,48,57,61,62,63,74,76,],[12,12,12,12,12,12,12,12,12,12,-22,-23,-24,-25,-26,-27,-28,-29,12,12,12,-13,-19,-20,12,12,]),'BASE16_INTEGER':([0,3,9,16,17,22,24,25,27,28,29,30,31,32,33,34,35,36,47,48,57,61,62,63,74,76,],[13,13,13,13,13,13,13,13,13,13,-22,-23,-24,-25,-26,-27,-28,-29,13,13,13,-13,-19,-20,13,13,]),'BASE8_INTEGER':([0,3,9,16,17,22,24,25,27,28,29,30,31,32,33,34,35,36,47,48,57,61,62,63,74,76,],[14,14,14,14,14,14,14,14,14,14,-22,-23,-24,-25,-26,-27,-28,-29,14,14,14,-13,-19,-20,14,14,]),'BASE2_INTEGER':([0,3,9,16,17,22,24,25,27,28,29,30,31,32,33,34,35,36,47,48,57,61,62,63,74,76,],[15,15,15,15,15,15,15,15,15,15,-22,-23,-24,-25,-26,-27,-28,-29,15,15,15,-13,-19,-20,15,15,]),'PLUS':([0,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,39,42,43,44,47,48,50,51,52,53,54,55,56,57,61,62,63,68,74,76,78,79,],[16,29,16,-3,-4,-5,-6,-7,16,-9,-30,-31,-32,-33,16,16,-36,-11,-10,-12,47,16,16,-17,16,16,-22,-23,-24,-25,-26,-27,-28,-29,29,29,-34,-35,29,16,16,29,-15,-18,29,-37,-38,-39,16,-13,-19,-20,29,16,16,29,-50,]),'MINUS':([0,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,39,42,43,44,47,48,50,51,52,53,54,55,56,57,61,62,63,68,74,76,78,79,],[17,30,17,-3,-4,-5,-6,-7,17,-9,-30,-31,-32,-33,17,17,-36,-11,-10,-12,48,17,17,-17,17,17,-22,-23,-24,-25,-26,-27,-28,-29,30,30,-34,-35,30,17,17,30,-15,-18,30,-37,-38,-39,17,-13,-19,-20,30,17,17,30,-50,]),'FLOAT':([0,3,9,16,17,22,24,25,27,28,29,30,31,32,33,34,35,36,47,48,57,61,62,63,74,76,],[18,18,18,18,18,18,18,18,18,18,-22,-23,-24,-25,-26,-27,-28,-29,18,18,18,-13,-19,-20,18,18,]),'STRING':([0,3,9,22,24,25,27,28,29,30,31,32,33,34,35,36,38,57,61,62,63,74,76,],[19,19,19,19,19,19,19,19,-22,-23,-24,-25,-26,-27,-28,-29,19,19,-13,-19,-20,19,19,]),'CHAR':([0,3,9,22,24,25,27,28,29,30,31,32,33,34,35,36,38,57,61,62,63,74,76,],[20,20,20,20,20,20,20,20,-22,-23,-24,-25,-26,-27,-28,-29,20,20,-13,-19,-20,20,20,]),'IDENTIFIER':([0,3,9,11,22,24,25,27,28,29,30,31,32,33,34,35,36,38,49,57,59,61,62,63,72,74,76,],[21,21,21,41,21,21,21,21,21,-22,-23,-24,-25,-26,-27,-28,-29,21,41,21,69,-13,-19,-20,41,21,21,]),'LPAREN':([0,2,3,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,39,42,43,44,50,51,52,53,54,55,56,57,61,62,63,68,74,76,78,79,],[22,22,22,-3,-4,-5,-6,-7,22,-9,-30,-31,-32,-33,-36,-11,-10,-12,22,22,22,-17,22,22,-22,-23,-24,-25,-26,-27,-28,-29,22,22,-34,-35,22,-14,-15,-18,22,-37,-38,-39,22,-13,-19,-20,-41,22,22,22,-50,]),'KEYWORD_LET':([0,3,9,22,24,25,27,28,29,30,31,32,33,34,35,36,57,61,62,63,74,76,],[23,23,23,23,23,23,23,23,-22,-23,-24,-25,-26,-27,-28,-29,23,-13,-19,-20,23,23,]),'$end':([1,2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,26,37,39,42,43,50,51,52,53,54,55,56,61,62,63,68,79,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,-17,-2,-16,-34,-35,-14,-15,-18,-21,-37,-38,-39,-13,-19,-20,-41,-50,]),'TICK_OPERATOR':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[24,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,-17,24,24,-34,-35,24,-14,-15,-18,24,-37,-38,-39,-13,-19,-20,24,24,-50,]),'SPACE':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,23,26,37,39,41,42,43,44,50,51,52,53,54,55,56,61,62,63,68,69,70,78,79,],[25,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,49,-17,25,25,59,-34,-35,25,25,-15,25,25,-37,-38,-39,-13,-19,-20,25,59,76,25,-50,]),'DOT_OPERATOR':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[27,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,45,-17,27,27,-34,-35,27,27,-15,27,27,-37,-38,-39,-13,-19,-20,27,27,-50,]),'STAR':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[31,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,31,-17,31,31,-34,-35,31,31,-15,-18,31,-37,-38,-39,-13,-19,-20,31,31,-50,]),'SLASH':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[32,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,32,-17,32,32,-34,-35,32,32,-15,-18,32,-37,-38,-39,-13,-19,-20,32,32,-50,]),'DOUBLESLASH':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[33,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,33,-17,33,33,-34,-35,33,33,-15,-18,33,-37,-38,-39,-13,-19,-20,33,33,-50,]),'PERCENT':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[34,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,34,-17,34,34,-34,-35,34,34,-15,-18,34,-37,-38,-39,-13,-19,-20,34,34,-50,]),'ARROW':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,40,41,42,43,44,50,51,52,53,54,55,56,58,60,61,62,63,68,69,75,78,79,],[35,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,35,-17,35,35,57,-40,-34,-35,35,-14,-15,-18,35,-37,-38,-39,-42,-44,-13,-19,-20,35,-40,-43,35,-50,]),'OPERATOR':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,22,26,37,39,42,43,44,50,51,52,53,54,55,56,61,62,63,68,78,79,],[36,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,36,-17,36,36,-34,-35,36,36,-15,-18,36,-37,-38,-39,-13,-19,-20,36,36,-50,]),'RPAREN':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,26,31,32,33,34,35,36,37,39,42,43,44,45,46,47,48,50,51,52,53,54,55,56,61,62,63,68,79,],[-1,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,-17,-24,-25,-26,-27,-28,-29,-2,-16,-34,-35,61,62,63,-22,-23,-14,-15,-18,-21,-37,-38,-39,-13,-19,-20,-41,-50,]),'KEYWORD_IN':([2,4,5,6,7,8,9,10,12,13,14,15,18,19,20,21,26,37,39,42,43,50,51,52,53,54,55,56,61,62,63,64,65,68,71,73,77,78,79,80,],[-1,-3,-4,-5,-6,-7,-8,-9,-30,-31,-32,-33,-36,-11,-10,-12,-17,-2,-16,-34,-35,-14,-15,-18,-21,-37,-38,-39,-13,-19,-20,70,-40,-41,-47,-49,-40,-46,-50,-48,]),'ANNOTATION':([4,12,13,14,15,18,42,43,],[38,-30,-31,-32,-33,-36,-34,-35,]),'EQ':([41,58,60,66,67,69,75,],[-40,-42,-44,74,-45,-40,-43,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'st_expr':([0,76,],[1,79,]),'expr':([0,3,9,22,24,25,27,28,57,74,76,],[2,37,39,44,50,51,52,53,68,78,2,]),'number':([0,3,9,16,17,22,24,25,27,28,47,48,57,74,76,],[4,4,4,42,43,4,4,4,4,4,42,43,4,4,4,]),'concrete_number':([0,3,9,22,24,25,27,28,57,74,76,],[5,5,5,5,5,5,5,5,5,5,5,]),'string':([0,3,9,22,24,25,27,28,38,57,74,76,],[6,6,6,6,6,6,6,6,54,6,6,6,]),'char':([0,3,9,22,24,25,27,28,38,57,74,76,],[7,7,7,7,7,7,7,7,55,7,7,7,]),'identifier':([0,3,9,22,24,25,27,28,38,57,74,76,],[8,8,8,8,8,8,8,8,56,8,8,8,]),'enclosed_expr':([0,2,3,9,22,24,25,27,28,37,39,44,50,51,52,53,57,68,74,76,78,],[9,26,9,9,9,9,9,9,9,26,26,26,26,26,26,26,9,26,9,9,26,]),'letexpr':([0,3,9,22,24,25,27,28,57,74,76,],[10,10,10,10,10,10,10,10,10,10,10,]),'operator':([2,22,37,39,44,50,51,52,53,68,78,],[28,46,28,28,28,28,28,28,28,28,28,]),'parameters':([11,49,72,],[40,67,67,]),'_parameters':([41,69,],[58,75,]),'empty':([41,65,69,77,],[60,73,60,73,]),'equations':([49,],[64,]),'equation':([49,72,],[65,77,]),'pattern':([49,72,],[66,66,]),'_equation_set':([65,77,],[71,80,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> st_expr","S'",1,None,None,None),
  ('st_expr -> expr','st_expr',1,'p_standalone_expr','parser.py',293),
  ('st_expr -> PADDING expr','st_expr',2,'p_standalone_expr','parser.py',294),
  ('expr -> number','expr',1,'p_literals_and_basic','parser.py',307),
  ('expr -> concrete_number','expr',1,'p_literals_and_basic','parser.py',308),
  ('expr -> string','expr',1,'p_literals_and_basic','parser.py',309),
  ('expr -> char','expr',1,'p_literals_and_basic','parser.py',310),
  ('expr -> identifier','expr',1,'p_literals_and_basic','parser.py',311),
  ('expr -> enclosed_expr','expr',1,'p_literals_and_basic','parser.py',312),
  ('expr -> letexpr','expr',1,'p_literals_and_basic','parser.py',313),
  ('char -> CHAR','char',1,'p_char','parser.py',319),
  ('string -> STRING','string',1,'p_string','parser.py',324),
  ('identifier -> IDENTIFIER','identifier',1,'p_variable','parser.py',329),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','parser.py',334),
  ('expr -> expr TICK_OPERATOR expr','expr',3,'p_infix_application','parser.py',339),
  ('expr -> expr SPACE expr','expr',3,'p_application','parser.py',344),
  ('expr -> enclosed_expr expr','expr',2,'p_application_after_paren','parser.py',349),
  ('expr -> expr enclosed_expr','expr',2,'p_application_after_paren','parser.py',350),
  ('expr -> expr DOT_OPERATOR expr','expr',3,'p_compose','parser.py',357),
  ('enclosed_expr -> LPAREN DOT_OPERATOR RPAREN','enclosed_expr',3,'p_operators_as_expressios','parser.py',364),
  ('enclosed_expr -> LPAREN operator RPAREN','enclosed_expr',3,'p_operators_as_expressios','parser.py',365),
  ('expr -> expr operator expr','expr',3,'p_user_operator_expr','parser.py',372),
  ('operator -> PLUS','operator',1,'p_operator','parser.py',381),
  ('operator -> MINUS','operator',1,'p_operator','parser.py',382),
  ('operator -> STAR','operator',1,'p_operator','parser.py',383),
  ('operator -> SLASH','operator',1,'p_operator','parser.py',384),
  ('operator -> DOUBLESLASH','operator',1,'p_operator','parser.py',385),
  ('operator -> PERCENT','operator',1,'p_operator','parser.py',386),
  ('operator -> ARROW','operator',1,'p_operator','parser.py',387),
  ('operator -> OPERATOR','operator',1,'p_operator','parser.py',388),
  ('number -> BASE10_INTEGER','number',1,'p_integer','parser.py',395),
  ('number -> BASE16_INTEGER','number',1,'p_integer','parser.py',396),
  ('number -> BASE8_INTEGER','number',1,'p_integer','parser.py',397),
  ('number -> BASE2_INTEGER','number',1,'p_integer','parser.py',398),
  ('number -> PLUS number','number',2,'p_pos_number','parser.py',420),
  ('number -> MINUS number','number',2,'p_neg_number','parser.py',425),
  ('number -> FLOAT','number',1,'p_float','parser.py',433),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','parser.py',438),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','parser.py',439),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','parser.py',440),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',449),
  ('expr -> BACKSLASH parameters ARROW expr','expr',4,'p_lambda_definition','parser.py',454),
  ('parameters -> IDENTIFIER _parameters','parameters',2,'p_parameters','parser.py',462),
  ('_parameters -> SPACE IDENTIFIER _parameters','_parameters',3,'p__params','parser.py',470),
  ('_parameters -> empty','_parameters',1,'p_empty__parameters','parser.py',477),
  ('pattern -> parameters','pattern',1,'p_pattern','parser.py',526),
  ('equation -> pattern EQ expr','equation',3,'p_equation','parser.py',541),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','parser.py',551),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','parser.py',560),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','parser.py',569),
  ('letexpr -> KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','parser.py',575),
]
