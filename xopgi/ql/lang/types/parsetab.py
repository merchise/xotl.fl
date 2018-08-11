
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
# type: ignore
# flake8: noqa
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'type_exprrightARROWleftSPACEARROW CONS LPAREN RPAREN SPACE TYPEVARtype_expr : TYPEVARtype_expr : CONStype_expr : type_expr SPACE type_exprtype_expr : LPAREN type_expr RPARENtype_expr : type_expr ARROW type_expr'

_lr_action_items = {'TYPEVAR':([0,4,5,6,],[2,2,2,2,]),'CONS':([0,4,5,6,],[3,3,3,3,]),'LPAREN':([0,4,5,6,],[4,4,4,4,]),'$end':([1,2,3,8,9,10,],[0,-1,-2,-3,-5,-4,]),'SPACE':([1,2,3,7,8,9,10,],[5,-1,-2,5,-3,5,-4,]),'ARROW':([1,2,3,7,8,9,10,],[6,-1,-2,6,-3,6,-4,]),'RPAREN':([2,3,7,8,9,10,],[-1,-2,10,-3,-5,-4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'type_expr':([0,4,5,6,],[1,7,8,9,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> type_expr","S'",1,None,None,None),
  ('type_expr -> TYPEVAR','type_expr',1,'p_tvar','parser.py',50),
  ('type_expr -> CONS','type_expr',1,'p_cons','parser.py',55),
  ('type_expr -> type_expr SPACE type_expr','type_expr',3,'p_application','parser.py',60),
  ('type_expr -> LPAREN type_expr RPAREN','type_expr',3,'p_paren','parser.py',74),
  ('type_expr -> type_expr ARROW type_expr','type_expr',3,'p_expression_fntype','parser.py',79),
]
