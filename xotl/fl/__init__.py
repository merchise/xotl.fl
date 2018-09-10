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

VERSION = '0.1.0'


def parse(program_source: str, *, debug: bool = False):
    '''Parse the program source and return its AST.

    This function doesn't type-check the program.

    '''
    from .parsers import program_parser, lexer
    return program_parser.parse(program_source, lexer=lexer, debug=debug)


def type_parse(code: str, debug=False, tracking=False):
    '''Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.types.base>`:mod:.

    Example:

       >>> parse('a -> b')
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
