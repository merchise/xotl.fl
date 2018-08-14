#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A type-expression language.

Implements the type checker/inference of chapters 8 and 9 of Book 'The
Implementation of Functional Programming Languages' -- Peyton Jones, S et al.;
Prentice Hall.

Other notable sources:

- Principal type-schemes for functional programs.  Luis Damas and Robin
  Milner.  POPL ’82: Proceedings of the 9th ACM SIGPLAN-SIGACT symposium on
  Principles of programming languages, ACM, pp. 207–212

- Type Assignment in Programming Languages.  PhD. Thesis of Luis Manuel
  Martins Damas.

.. note:: We should see if the types in stdlib's typing module are
          appropriate.

'''
from .base import (   # noqa: reexport
    Type,
    TypeVariable,
    TypeCons,
    FunctionTypeCons,
    ListTypeCons,
    TupleTypeCons,
)


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single type expression `code`.

    Return a `type expression AST <xopgi.ql.lang.types.base>`:mod:.

    Example:

       >>> from xopgi.ql.lang.types import parse
       >>> parse('a -> b')
       TypeCons('->', [TypeVariable('a'), TypeVariable('b')])

    '''
    from .parser import parser, lexer
    return parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def tokenize(source):
    from .parser import lexer
    lexer = lexer.clone()
    lexer.input(source)
    return [tok for tok in lexer]
