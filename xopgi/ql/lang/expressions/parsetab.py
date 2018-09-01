
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'st_exprrightARROWleftKEYWORD_LETleftKEYWORD_INleftKEYWORD_WHEREleftTICK_OPERATORleftOPERATORleftPLUSMINUSleftSTARSLASHDOUBLESLASHPERCENTrightDOT_OPERATORleftSPACEANNOTATION ARROW BACKSLASH BASE10_INTEGER BASE16_INTEGER BASE2_INTEGER BASE8_INTEGER CHAR COLON DATE DATETIME DATETIME_INTERVAL DATE_INTERVAL DOT_OPERATOR DOUBLESLASH EQ FLOAT IDENTIFIER KEYWORD_CLASS KEYWORD_DATA KEYWORD_IN KEYWORD_INSTANCE KEYWORD_LET KEYWORD_WHERE LPAREN MINUS OPERATOR PADDING PERCENT PLUS RPAREN SLASH SPACE STAR STRING TICK_OPERATORst_expr : expr\n    expr :  literal\n             | identifier\n             | enclosed_expr\n             | letexpr\n             | where_expr\n             | unit_value\n    literal : number\n             | concrete_number\n             | string\n             | char\n             | date\n             | datetime\n             | date_interval\n             | datetime_interval\n    date : DATE\n    datetime : DATETIME\n    date_interval : DATE_INTERVAL\n    datetime_interval : DATETIME_INTERVAL\n    unit_value : LPAREN RPAREN\n    char : CHARstring : STRINGidentifier : IDENTIFIERenclosed_expr : LPAREN expr RPARENexpr : expr TICK_OPERATOR exprexpr : expr SPACE exprexpr : enclosed_expr expr\n            | expr enclosed_expr\n    \n    expr : expr DOT_OPERATOR expr\n    enclosed_expr : LPAREN DOT_OPERATOR RPAREN\n                     | LPAREN operator RPAREN\n    expr : expr operator expr\n\n    \n    operator :  PLUS\n              | MINUS\n              | STAR\n              | SLASH\n              | DOUBLESLASH\n              | PERCENT\n              | ARROW\n              | OPERATOR\n\n    number : BASE10_INTEGER\n              | BASE16_INTEGER\n              | BASE8_INTEGER\n              | BASE2_INTEGER\n    number : PLUS numbernumber : MINUS numbernumber : FLOATconcrete_number :  number ANNOTATION string\n                        | number ANNOTATION char\n                        | number ANNOTATION identifier\n    empty : expr : BACKSLASH parameters ARROW expr\n    parameters : IDENTIFIER _parameters\n    _parameters : SPACE IDENTIFIER _parameters_parameters : empty\n    pattern : parametersequation : pattern EQ expr\n    equations : equation _equation_set\n    \n    _equation_set : PADDING equation _equation_set\n    \n    _equation_set : empty\n    \n    letexpr : KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr\n\n    \n    where_expr : expr KEYWORD_WHERE SPACE equations\n    where_expr : expr KEYWORD_WHERE PADDING equations\n    '
    
_lr_action_items = {'BACKSLASH':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[9,9,9,9,9,9,9,9,-33,-34,-35,-36,-37,-38,-39,-40,9,-24,-30,-31,9,9,]),'IDENTIFIER':([0,5,9,19,34,35,37,38,40,41,42,43,44,45,46,47,48,52,59,66,67,68,70,75,76,77,88,90,92,],[18,18,51,18,18,18,18,18,18,-33,-34,-35,-36,-37,-38,-39,-40,18,51,51,51,18,85,-24,-30,-31,51,18,18,]),'LPAREN':([0,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,34,35,36,37,38,40,41,42,43,44,45,46,47,48,49,53,54,60,61,62,63,64,65,68,72,73,74,75,76,77,79,82,83,84,87,89,90,92,93,94,95,96,],[19,40,-2,-3,19,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,19,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,19,19,-28,19,19,19,-33,-34,-35,-36,-37,-38,-39,-40,40,40,-20,-45,-46,-25,-26,-29,40,19,-48,-49,-50,-24,-30,-31,-51,-62,-63,-52,-58,-60,19,19,-51,40,-61,-59,]),'KEYWORD_LET':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[20,20,20,20,20,20,20,20,-33,-34,-35,-36,-37,-38,-39,-40,20,-24,-30,-31,20,20,]),'BASE10_INTEGER':([0,5,19,25,26,34,35,37,38,40,41,42,43,44,45,46,47,48,57,58,68,75,76,77,90,92,],[21,21,21,21,21,21,21,21,21,21,-33,-34,-35,-36,-37,-38,-39,-40,21,21,21,-24,-30,-31,21,21,]),'BASE16_INTEGER':([0,5,19,25,26,34,35,37,38,40,41,42,43,44,45,46,47,48,57,58,68,75,76,77,90,92,],[22,22,22,22,22,22,22,22,22,22,-33,-34,-35,-36,-37,-38,-39,-40,22,22,22,-24,-30,-31,22,22,]),'BASE8_INTEGER':([0,5,19,25,26,34,35,37,38,40,41,42,43,44,45,46,47,48,57,58,68,75,76,77,90,92,],[23,23,23,23,23,23,23,23,23,23,-33,-34,-35,-36,-37,-38,-39,-40,23,23,23,-24,-30,-31,23,23,]),'BASE2_INTEGER':([0,5,19,25,26,34,35,37,38,40,41,42,43,44,45,46,47,48,57,58,68,75,76,77,90,92,],[24,24,24,24,24,24,24,24,24,24,-33,-34,-35,-36,-37,-38,-39,-40,24,24,24,-24,-30,-31,24,24,]),'PLUS':([0,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,41,42,43,44,45,46,47,48,49,53,54,57,58,60,61,62,63,64,65,68,72,73,74,75,76,77,79,82,83,84,87,89,90,92,93,94,95,96,],[25,41,-2,-3,25,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,57,-41,-42,-43,-44,25,25,-47,-22,-21,-16,-17,-18,-19,25,25,-28,25,25,57,-33,-34,-35,-36,-37,-38,-39,-40,41,41,-20,25,25,-45,-46,41,-26,-29,41,25,-48,-49,-50,-24,-30,-31,-51,-62,-63,41,-58,-60,25,25,-51,41,-61,-59,]),'MINUS':([0,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,41,42,43,44,45,46,47,48,49,53,54,57,58,60,61,62,63,64,65,68,72,73,74,75,76,77,79,82,83,84,87,89,90,92,93,94,95,96,],[26,42,-2,-3,26,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,58,-41,-42,-43,-44,26,26,-47,-22,-21,-16,-17,-18,-19,26,26,-28,26,26,58,-33,-34,-35,-36,-37,-38,-39,-40,42,42,-20,26,26,-45,-46,42,-26,-29,42,26,-48,-49,-50,-24,-30,-31,-51,-62,-63,42,-58,-60,26,26,-51,42,-61,-59,]),'FLOAT':([0,5,19,25,26,34,35,37,38,40,41,42,43,44,45,46,47,48,57,58,68,75,76,77,90,92,],[27,27,27,27,27,27,27,27,27,27,-33,-34,-35,-36,-37,-38,-39,-40,27,27,27,-24,-30,-31,27,27,]),'STRING':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,52,68,75,76,77,90,92,],[28,28,28,28,28,28,28,28,-33,-34,-35,-36,-37,-38,-39,-40,28,28,-24,-30,-31,28,28,]),'CHAR':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,52,68,75,76,77,90,92,],[29,29,29,29,29,29,29,29,-33,-34,-35,-36,-37,-38,-39,-40,29,29,-24,-30,-31,29,29,]),'DATE':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[30,30,30,30,30,30,30,30,-33,-34,-35,-36,-37,-38,-39,-40,30,-24,-30,-31,30,30,]),'DATETIME':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[31,31,31,31,31,31,31,31,-33,-34,-35,-36,-37,-38,-39,-40,31,-24,-30,-31,31,31,]),'DATE_INTERVAL':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[32,32,32,32,32,32,32,32,-33,-34,-35,-36,-37,-38,-39,-40,32,-24,-30,-31,32,32,]),'DATETIME_INTERVAL':([0,5,19,34,35,37,38,40,41,42,43,44,45,46,47,48,68,75,76,77,90,92,],[33,33,33,33,33,33,33,33,-33,-34,-35,-36,-37,-38,-39,-40,33,-24,-30,-31,33,33,]),'$end':([1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23,24,27,28,29,30,31,32,33,36,49,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,-27,-20,-45,-46,-25,-26,-29,-32,-48,-49,-50,-24,-30,-31,-51,-62,-63,-52,-58,-60,-51,-57,-61,-59,]),'TICK_OPERATOR':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23,24,27,28,29,30,31,32,33,36,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[34,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,34,34,-20,-45,-46,-25,-26,-29,34,-48,-49,-50,-24,-30,-31,-51,-62,-63,34,-58,-60,-51,34,-61,-59,]),'SPACE':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,20,21,22,23,24,27,28,29,30,31,32,33,36,39,49,51,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,85,86,87,89,93,94,95,96,],[35,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,59,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,66,35,70,35,-20,-45,-46,35,-26,35,35,-48,-49,-50,-24,-30,-31,-51,-62,-63,35,70,92,-58,-60,-51,35,-61,-59,]),'DOT_OPERATOR':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[37,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,55,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,55,37,37,-20,-45,-46,37,-26,37,37,-48,-49,-50,-24,-30,-31,-51,-62,-63,37,-58,-60,-51,37,-61,-59,]),'KEYWORD_WHERE':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23,24,27,28,29,30,31,32,33,36,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[39,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,39,39,-20,-45,-46,-25,-26,-29,39,-48,-49,-50,-24,-30,-31,-51,-62,-63,39,-58,-60,-51,39,-61,-59,]),'STAR':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[43,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,43,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,43,43,43,-20,-45,-46,43,-26,-29,43,-48,-49,-50,-24,-30,-31,-51,-62,-63,43,-58,-60,-51,43,-61,-59,]),'SLASH':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[44,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,44,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,44,44,44,-20,-45,-46,44,-26,-29,44,-48,-49,-50,-24,-30,-31,-51,-62,-63,44,-58,-60,-51,44,-61,-59,]),'DOUBLESLASH':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[45,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,45,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,45,45,45,-20,-45,-46,45,-26,-29,45,-48,-49,-50,-24,-30,-31,-51,-62,-63,45,-58,-60,-51,45,-61,-59,]),'PERCENT':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[46,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,46,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,46,46,46,-20,-45,-46,46,-26,-29,46,-48,-49,-50,-24,-30,-31,-51,-62,-63,46,-58,-60,-51,46,-61,-59,]),'ARROW':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,50,51,53,54,60,61,62,63,64,65,69,71,72,73,74,75,76,77,79,82,83,84,85,87,89,91,93,94,95,96,],[47,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,47,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,47,47,68,-51,47,-20,-45,-46,-25,-26,-29,47,-53,-55,-48,-49,-50,-24,-30,-31,-51,-62,-63,47,-51,-58,-60,-54,-51,47,-61,-59,]),'OPERATOR':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,40,49,53,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[48,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,48,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,48,48,48,-20,-45,-46,48,-26,-29,48,-48,-49,-50,-24,-30,-31,-51,-62,-63,48,-58,-60,-51,48,-61,-59,]),'RPAREN':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23,24,27,28,29,30,31,32,33,36,43,44,45,46,47,48,49,53,54,55,56,57,58,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,54,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,-35,-36,-37,-38,-39,-40,-27,75,-20,76,77,-33,-34,-45,-46,-25,-26,-29,-32,-48,-49,-50,-24,-30,-31,-51,-62,-63,-52,-58,-60,-51,-57,-61,-59,]),'PADDING':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23,24,27,28,29,30,31,32,33,36,39,49,54,60,61,62,63,64,65,72,73,74,75,76,77,79,82,83,84,87,89,93,94,95,96,],[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,67,-27,-20,-45,-46,-25,-26,-29,-32,-48,-49,-50,-24,-30,-31,88,-62,-63,-52,-58,-60,88,-57,-61,-59,]),'KEYWORD_IN':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23,24,27,28,29,30,31,32,33,36,49,54,60,61,62,63,64,65,72,73,74,75,76,77,78,79,82,83,84,87,89,93,94,95,96,],[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-23,-41,-42,-43,-44,-47,-22,-21,-16,-17,-18,-19,-28,-27,-20,-45,-46,-25,-26,-29,-32,-48,-49,-50,-24,-30,-31,86,-51,-62,-63,-52,-58,-60,-51,-57,-61,-59,]),'ANNOTATION':([10,21,22,23,24,27,60,61,],[52,-41,-42,-43,-44,-47,-45,-46,]),'EQ':([51,69,71,80,81,85,91,],[-51,-53,-55,90,-56,-51,-54,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'st_expr':([0,92,],[1,95,]),'expr':([0,5,19,34,35,37,38,40,68,90,92,],[2,49,53,62,63,64,65,53,84,94,2,]),'literal':([0,5,19,34,35,37,38,40,68,90,92,],[3,3,3,3,3,3,3,3,3,3,3,]),'identifier':([0,5,19,34,35,37,38,40,52,68,90,92,],[4,4,4,4,4,4,4,4,74,4,4,4,]),'enclosed_expr':([0,2,5,19,34,35,37,38,40,49,53,62,63,64,65,68,84,90,92,94,],[5,36,5,5,5,5,5,5,5,36,36,36,36,36,36,5,36,5,5,36,]),'letexpr':([0,5,19,34,35,37,38,40,68,90,92,],[6,6,6,6,6,6,6,6,6,6,6,]),'where_expr':([0,5,19,34,35,37,38,40,68,90,92,],[7,7,7,7,7,7,7,7,7,7,7,]),'unit_value':([0,5,19,34,35,37,38,40,68,90,92,],[8,8,8,8,8,8,8,8,8,8,8,]),'number':([0,5,19,25,26,34,35,37,38,40,57,58,68,90,92,],[10,10,10,60,61,10,10,10,10,10,60,61,10,10,10,]),'concrete_number':([0,5,19,34,35,37,38,40,68,90,92,],[11,11,11,11,11,11,11,11,11,11,11,]),'string':([0,5,19,34,35,37,38,40,52,68,90,92,],[12,12,12,12,12,12,12,12,72,12,12,12,]),'char':([0,5,19,34,35,37,38,40,52,68,90,92,],[13,13,13,13,13,13,13,13,73,13,13,13,]),'date':([0,5,19,34,35,37,38,40,68,90,92,],[14,14,14,14,14,14,14,14,14,14,14,]),'datetime':([0,5,19,34,35,37,38,40,68,90,92,],[15,15,15,15,15,15,15,15,15,15,15,]),'date_interval':([0,5,19,34,35,37,38,40,68,90,92,],[16,16,16,16,16,16,16,16,16,16,16,]),'datetime_interval':([0,5,19,34,35,37,38,40,68,90,92,],[17,17,17,17,17,17,17,17,17,17,17,]),'operator':([2,19,40,49,53,62,63,64,65,84,94,],[38,56,56,38,38,38,38,38,38,38,38,]),'parameters':([9,59,66,67,88,],[50,81,81,81,81,]),'_parameters':([51,85,],[69,91,]),'empty':([51,79,85,93,],[71,89,71,89,]),'equations':([59,66,67,],[78,82,83,]),'equation':([59,66,67,88,],[79,79,79,93,]),'pattern':([59,66,67,88,],[80,80,80,80,]),'_equation_set':([79,93,],[87,96,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> st_expr","S'",1,None,None,None),
  ('st_expr -> expr','st_expr',1,'p_standalone_expr','parser.py',357),
  ('expr -> literal','expr',1,'p_literals_and_basic','parser.py',364),
  ('expr -> identifier','expr',1,'p_literals_and_basic','parser.py',365),
  ('expr -> enclosed_expr','expr',1,'p_literals_and_basic','parser.py',366),
  ('expr -> letexpr','expr',1,'p_literals_and_basic','parser.py',367),
  ('expr -> where_expr','expr',1,'p_literals_and_basic','parser.py',368),
  ('expr -> unit_value','expr',1,'p_literals_and_basic','parser.py',369),
  ('literal -> number','literal',1,'p_literals','parser.py',375),
  ('literal -> concrete_number','literal',1,'p_literals','parser.py',376),
  ('literal -> string','literal',1,'p_literals','parser.py',377),
  ('literal -> char','literal',1,'p_literals','parser.py',378),
  ('literal -> date','literal',1,'p_literals','parser.py',379),
  ('literal -> datetime','literal',1,'p_literals','parser.py',380),
  ('literal -> date_interval','literal',1,'p_literals','parser.py',381),
  ('literal -> datetime_interval','literal',1,'p_literals','parser.py',382),
  ('date -> DATE','date',1,'p_date','parser.py',388),
  ('datetime -> DATETIME','datetime',1,'p_datetime','parser.py',394),
  ('date_interval -> DATE_INTERVAL','date_interval',1,'p_date_interval','parser.py',400),
  ('datetime_interval -> DATETIME_INTERVAL','datetime_interval',1,'p_datetime_interval','parser.py',406),
  ('unit_value -> LPAREN RPAREN','unit_value',2,'p_unit_value','parser.py',412),
  ('char -> CHAR','char',1,'p_char','parser.py',418),
  ('string -> STRING','string',1,'p_string','parser.py',423),
  ('identifier -> IDENTIFIER','identifier',1,'p_variable','parser.py',428),
  ('enclosed_expr -> LPAREN expr RPAREN','enclosed_expr',3,'p_paren_expr','parser.py',433),
  ('expr -> expr TICK_OPERATOR expr','expr',3,'p_infix_application','parser.py',438),
  ('expr -> expr SPACE expr','expr',3,'p_application','parser.py',443),
  ('expr -> enclosed_expr expr','expr',2,'p_application_after_paren','parser.py',448),
  ('expr -> expr enclosed_expr','expr',2,'p_application_after_paren','parser.py',449),
  ('expr -> expr DOT_OPERATOR expr','expr',3,'p_compose','parser.py',456),
  ('enclosed_expr -> LPAREN DOT_OPERATOR RPAREN','enclosed_expr',3,'p_operators_as_expressios','parser.py',463),
  ('enclosed_expr -> LPAREN operator RPAREN','enclosed_expr',3,'p_operators_as_expressios','parser.py',464),
  ('expr -> expr operator expr','expr',3,'p_user_operator_expr','parser.py',471),
  ('operator -> PLUS','operator',1,'p_operator','parser.py',480),
  ('operator -> MINUS','operator',1,'p_operator','parser.py',481),
  ('operator -> STAR','operator',1,'p_operator','parser.py',482),
  ('operator -> SLASH','operator',1,'p_operator','parser.py',483),
  ('operator -> DOUBLESLASH','operator',1,'p_operator','parser.py',484),
  ('operator -> PERCENT','operator',1,'p_operator','parser.py',485),
  ('operator -> ARROW','operator',1,'p_operator','parser.py',486),
  ('operator -> OPERATOR','operator',1,'p_operator','parser.py',487),
  ('number -> BASE10_INTEGER','number',1,'p_integer','parser.py',494),
  ('number -> BASE16_INTEGER','number',1,'p_integer','parser.py',495),
  ('number -> BASE8_INTEGER','number',1,'p_integer','parser.py',496),
  ('number -> BASE2_INTEGER','number',1,'p_integer','parser.py',497),
  ('number -> PLUS number','number',2,'p_pos_number','parser.py',519),
  ('number -> MINUS number','number',2,'p_neg_number','parser.py',524),
  ('number -> FLOAT','number',1,'p_float','parser.py',532),
  ('concrete_number -> number ANNOTATION string','concrete_number',3,'p_concrete_number','parser.py',537),
  ('concrete_number -> number ANNOTATION char','concrete_number',3,'p_concrete_number','parser.py',538),
  ('concrete_number -> number ANNOTATION identifier','concrete_number',3,'p_concrete_number','parser.py',539),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',548),
  ('expr -> BACKSLASH parameters ARROW expr','expr',4,'p_lambda_definition','parser.py',553),
  ('parameters -> IDENTIFIER _parameters','parameters',2,'p_parameters','parser.py',561),
  ('_parameters -> SPACE IDENTIFIER _parameters','_parameters',3,'p__params','parser.py',569),
  ('_parameters -> empty','_parameters',1,'p_empty__parameters','parser.py',576),
  ('pattern -> parameters','pattern',1,'p_pattern','parser.py',625),
  ('equation -> pattern EQ expr','equation',3,'p_equation','parser.py',640),
  ('equations -> equation _equation_set','equations',2,'p_equation_set','parser.py',650),
  ('_equation_set -> PADDING equation _equation_set','_equation_set',3,'p_equation_set2','parser.py',659),
  ('_equation_set -> empty','_equation_set',1,'p_equation_set3','parser.py',668),
  ('letexpr -> KEYWORD_LET SPACE equations KEYWORD_IN SPACE st_expr','letexpr',6,'p_let_expr','parser.py',678),
  ('where_expr -> expr KEYWORD_WHERE SPACE equations','where_expr',4,'p_where_expr','parser.py',686),
  ('where_expr -> expr KEYWORD_WHERE PADDING equations','where_expr',4,'p_where_expr','parser.py',687),
]
