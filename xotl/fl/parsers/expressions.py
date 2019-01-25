#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Parse expressions (not full programs).'''
from xotl.fl.ast.base import AST


def parse(code: str, debug=False, tracking=False) -> AST:
    '''Parse a single expression `code`.
    '''
    from xotl.fl.parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)
