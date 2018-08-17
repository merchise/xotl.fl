#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A grammar for function types.

'''
from ply import lex, yacc
from .base import Type, TypeCons, TypeVariable as TypeVar
from .base import ListTypeCons


class ParserError(SyntaxError):
    pass


tokens = (
    'ARROW',
    'LPAREN',
    'RPAREN',
    'TYPEVAR',
    'CONS',
    'SPACE',
    'LBRACKET',
    'RBRACKET',
)

t_ARROW = r'->[\t\s]*'

t_TYPEVAR = r'[a-z][\.a-zA-Z0-9]*'
t_CONS = r'[A-Z][\.a-zA-Z0-9]*'


# t_NL and tNLE remove runs of empty spaces at the beginning or end of the
# code, this simplifies the treatment of t_SPACE
def t_NL(t):
    r'^\s+'


def t_NLE(t):
    r'\s+$'


# We need to treat space specially in this grammar because it can have a
# semantical value: the application of expressions 'e1 e2'.
#
# We want to emit a SPACE token only when type application is **not
# impossible**.
#
def t_SPACE(t):
    r'[ \t]+'
    # In the expression:
    #
    #    e0   (   e1   e2   )   e3
    #       ^   !    ^    !   ^
    #
    # The run of spaces marked with '^' are important and must be kept,
    # but the spaces above the '!' are just padding and can be ignored
    # (don't create a token for them).
    #
    before = t.lexer.lexdata[t.lexpos - 1]
    after = t.lexer.lexdata[t.lexpos + len(t.value)]
    common = '\n->,'
    if before in common + '([' or after in common + ')]':
        return
    else:
        return t


def t_LPAREN(t):
    r'\(\s*'
    return t


def t_RPAREN(t):
    r'\s*\)'
    return t


def t_LBRACKET(t):
    r'\[[ \t]*'
    return t


def t_RBRACKET(t):
    r'[ \t]*\]'
    return t


lexer = lex.lex(debug=False)

# Note: The order of precedence is from lower to higher.
precedence = (
    ('left', 'LBRACKET', ),

    # function is right-assoc, i.e 'a -> b -> c' means 'a -> (b -> c)'.
    ('right', 'ARROW', ),

    # Application is left-assoc, i.e 'a b c' means '(a b) c'.
    ('left', 'SPACE', ),
)


def p_tvar(p):
    'type_expr : TYPEVAR'
    p[0] = TypeVar(p[1])


def p_cons(p):
    'type_expr : CONS'
    p[0] = TypeCons(p[1])


def p_application(p):
    'type_expr : type_expr SPACE type_expr'
    e1, e2 = p[1], p[3]
    if isinstance(e1, TypeVar):
        # I have to promote to a TypeCons
        f = TypeCons(e1.name)
    else:
        assert isinstance(e1, TypeCons)
        f = e1
    assert isinstance(e2, Type), f'@ {e1!r} {e2!r}'
    p[0] = TypeCons(f.cons, f.subtypes + (e2, ), binary=f.binary)


def p_paren(p):
    'type_expr : LPAREN type_expr RPAREN'
    p[0] = p[2]


def p_bracket(prod):
    'type_expr : LBRACKET type_expr RBRACKET'
    prod[0] = ListTypeCons(prod[2])


def p_expression_fntype(p):
    'type_expr : type_expr ARROW type_expr'
    p[0] = TypeCons('->', [p[1], p[3]], binary=True)


def p_error(p):
    raise ParserError(f'Invalid input {p!r}')


parser = yacc.yacc(debug=True, start='type_expr')
