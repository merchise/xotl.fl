#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xotl.fl.ast.base import AST


def pretty_str(expr: AST) -> str:
    r'''Return a nicely formatted representation of an expression.

    We try to format the expression in a manner that is readable, and
    uncluttered.  So take into account how application (space), newlines and
    the precedence of operators work in the parser.

    The following must be True for any expression::

        parse(pretty_str(expr)) == expr

    Example:

      >>> from xotl.fl.parsers.expressions import parse
      >>> expr = parse(r"""
      ...    let map f []   = []
      ...        map f x:xs = f x : map f xs
      ...        map2 = \f xs -> if (is_null xs) (then xs) (else let h = head xs
      ...                                                            t = tail xs
      ...                                                        in f h : map2 f t)
      ...    in (map, map2)
      ... """)
      >>> parse(pretty_str(expr)) == expr
      True

    '''
    return ''
