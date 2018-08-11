#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Any, Mapping
from ..types.base import Type


class AST:
    pass


class Variable(AST):
    def __init__(self, name: str) -> None:
        self.name = name


class Literal(AST):
    # An extension to the algorithm.  Literals are allowed, but have a
    # definite type: the most specific type possible.
    def __init__(self, value: Any, type_: Type) -> None:
        self.value = value
        self.type = type_


class Lambda(AST):
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body


class Application(AST):
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a LetExpression where you needed a LetrecExpression.
#
class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST) -> None:
        self.bindings = bindings
        self.body = body


class LetExpression(_LetExpr):
    pass


class LetrecExpression(_LetExpr):
    pass
