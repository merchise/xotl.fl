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
    'IDENTIFIER',
    'SPACE',
    'LBRACKET',
    'RBRACKET',
)

t_ARROW = r'->[\t\s]*'
t_IDENTIFIER = r'[A-Za-z_]\w*'


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


def p_type_expr(prod):
    '''type_expr : type_function_expr
                 | type_term'''
    prod[0] = prod[1]


def p_type_function_expr(prod):
    'type_function_expr : type_term ARROW type_term'
    prod[0] = TypeCons('->', [prod[1], prod[3]], binary=True)


def p_type_term(prod):
    '''type_term : type_app_expression
                 | type_factor'''
    prod[0] = prod[1]


def p_type_application_expr(prod):
    'type_app_expression : type_factor _app_args'
    cons = prod[1]
    args = prod[2]
    if isinstance(cons, TypeVar):
        f = TypeCons(cons.name)
    else:
        assert isinstance(cons, TypeCons)
        f = cons
    prod[0] = TypeCons(f.cons, f.subtypes + args, binary=f.binary)


def p_type_application_args(prod):
    '_app_args : SPACE type_factor _app_args'
    args = prod[3]
    args.insert(0, prod[2])
    prod[0] = args


def p_type_application_args_empty(prod):
    '_app_args : empty'
    prod[0] = []


def p_empty(prod):
    '''empty : '''
    pass


def p_type_identifier(prod):
    'type_factor : IDENTIFIER'
    name = prod[1]
    if name[0] == '_' or name[0].islower():
        prod[0] = TypeVar(name)
    else:
        prod[0] = TypeCons(name)


def p_type_factor_paren(p):
    'type_factor : LPAREN type_expr RPAREN'
    p[0] = p[2]


def p_type_factor_bracket(prod):
    'type_factor : LBRACKET type_expr RBRACKET'
    prod[0] = ListTypeCons(prod[2])


def p_error(p):
    raise ParserError(f'Invalid input {p!r}')


parser = yacc.yacc(debug=True, start='type_expr')
