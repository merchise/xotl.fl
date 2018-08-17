#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from collections import deque
from typing import List, Deque, Optional

from .base import AST, Literal, Identifier, Lambda, Application, Let, Letrec


def parse(source: str, debug=False, tracking=False) -> AST:
    '''Parse a single expression.'''
    from .parser import parser, lexer
    return parser.parse(source, lexer=lexer, debug=debug, tracking=tracking)


def tokenize(source):
    from .parser import lexer
    lexer = lexer.clone()
    lexer.input(source)
    return [tok for tok in lexer]


def find_free_names(expr: AST) -> List[str]:
    '''Find all names that appear free in `expr`.

    Example:

      >>> set(find_free_names(parse('let id x = x in map id xs')))  # doctest: +LITERAL_EVAL  # noqa
      {'map', 'xs'}

    Names can be repeated:

      >>> find_free_names(parse('twice x x')).count('x')
      2

    '''
    POPFRAME = None  # remove a binding from the 'stack'
    result: List[str] = []
    bindings: Deque[str] = deque([])
    nodes: Deque[Optional[AST]] = deque([expr])
    while nodes:
        node = nodes.pop()
        if node is POPFRAME:
            bindings.pop()
        elif isinstance(node, Identifier):
            if node.name not in bindings:
                result.append(node.name)
        elif isinstance(node, Literal):
            if isinstance(node.annotation, AST):
                nodes.append(node)
        elif isinstance(node, Application):
            nodes.extend([
                node.e1,
                node.e2,
            ])
        elif isinstance(node, Lambda):
            bindings.append(node.varname)
            nodes.append(POPFRAME)
            nodes.append(node.body)
        elif isinstance(node, (Let, Letrec)):
            # This is tricky; the bindings can be used recursively in the
            # bodies of a letrec:
            #
            #    letrec f1 = ....f1 ... f2 ....
            #           f2 = ... f1 ... f2 ....
            #           ....
            #    in ... f1 ... f2 ...
            #
            # So we must make all the names in the bindings bound and then
            # look at all the definitions.
            #
            # We push several POPFRAME at the to account for that.
            bindings.extend(node.keys())
            nodes.extend(POPFRAME for _ in node.keys())
            nodes.extend(node.values())
            nodes.append(node.body)
        else:
            assert False, f'Unknown AST node: {node!r}'
    return result
