#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Parse type expressions."""

from xotl.fl.ast.types import Type


def parse(code: str, debug=False, tracking=False) -> Type:
    """Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.ast.types>`:mod:.

    Example:

       >>> parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    """
    from xotl.fl.parsers import lexer, type_parser

    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)
