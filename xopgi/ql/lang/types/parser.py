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
from .base import Type, TypeCons, TypeVar


class ParserError(SyntaxError):
    pass


tokens = (
    'ARROW',
    'LPAREN',
    'RPAREN',
    'TYPEVAR',
    'CONS',
    'SPACE',
)

t_SPACE = r'[\s\t]+'
t_ARROW = r'[\s\t]*->[\s\t]*'
t_LPAREN = r'[\s\t]*\([\s\t]*'
t_RPAREN = r'[\s\t]*\)[\s\t]*'

t_TYPEVAR = r'[a-z][\.a-zA-Z0-9]*'
t_CONS = r'[A-Z][\.a-zA-Z0-9]*'

lexer = lex.lex(debug=False)

# Note: The order of precedence is from lower to higher.
precedence = (
    # function is right-assoc, i.e 'a -> b -> c' means 'a -> (b -> c)'.
    ('right', 'ARROW', ),

    # Application is left-assoc, i.e 'a b c' means '(a b) c'.
    ('left', 'SPACE', ),
)


def p_expression_tvar(p):
    'expr : TYPEVAR'
    p[0] = TypeVar(p[1])


def p_expression_cons(p):
    'expr : CONS'
    p[0] = TypeCons(p[1])


def p_expression_application(p):
    'expr : expr SPACE expr'
    e1, e2 = p[1], p[3]
    if isinstance(e1, TypeVar):
        # I have to promote to a TypeCons
        f = TypeCons(e1.name)
    else:
        assert isinstance(e1, TypeCons)
        f = e1
    assert isinstance(e2, Type), f'@ {e1!r} {e2!r}'
    f.subtypes.append(e2)
    p[0] = f


def p_expression_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]


def p_expression_fntype(p):
    'expr : expr ARROW expr'
    p[0] = TypeCons('->', [p[1], p[3]], binary=True)


def p_error(p):
    raise ParserError(f'Invalid input {p!r}')


parser = yacc.yacc(debug=False, start='expr')


if __name__ == '__main__':
    # Allow python -m xopgi.ql.lang.types.parser
    terminate = False
    while not terminate:
        try:
            source = input('> ')
            if source.startswith('? '):
                line = source[2:]
                lexer.input(line)
                result = [tok for tok in lexer]
            else:
                result = parser.parse(source)
            print(type(result), result)
        except (AssertionError, SyntaxError, lex.LexError):
            import traceback
            traceback.print_exc()
        except (EOFError, KeyboardInterrupt):
            terminate = True
