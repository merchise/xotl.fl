#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

# AVOID top-level imports since many setup imports this __init__ package when
# importing 'xotl.fl.release'.


def parse(program_source: str, *, debug: bool = False):
    '''Parse the program source and return its AST.

    It returns a list of definitions.  Definitions come in three types:

    - Type annotations, which are dictionaries of type
      `xotl.fl.types.TypeEnvironment`:data:;

    - Value definitions, which may span several `equations
      <xotl.fl.expressions.Equation>`:class:; and

    - Data type definitions, `xotl.fl.expressions.DataType`:class:.

    This function doesn't type-check the program.

    Example:

    .. doctest::
       :options: +NORMALIZE_WHITESPACE

       >>> parse("""
       ...    data List a = Nil | Cons a (List a)
       ...    lhead :: List a -> a
       ...    lhead (Cons a _) = a
       ... """)
       [<Data List a = <DataCons Nil> | <DataCons Cons a (List a)>>,
        {'lhead': <TypeScheme: forall a. (List a) -> a>},
        <equation lhead (Cons Identifier('a') Identifier('_')) = Identifier('a')>]

    '''
    from .parsers import program_parser, lexer
    defs = program_parser.parse(program_source, lexer=lexer, debug=debug)
    # Here we try to perform sanity checks and also *group* otherwise
    # separated stuff (several equations for the same name are given
    # separately, but we group them under a single Equations object).
    return defs


def type_parse(code: str, debug=False, tracking=False):
    '''Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.types>`:mod:.

    Example:

       >>> type_parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    '''
    from .parsers import type_parser, lexer
    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def expr_parse(code: str, debug=False, tracking=False):
    '''Parse a single expression `code`.
    '''
    from .parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def tokenize(source):
    from .parsers import lexer
    lexer = lexer.clone()
    lexer.input(source)
    return [tok for tok in lexer]
