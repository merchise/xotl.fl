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


class Identifier(AST):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name!r})'

    def __hash__(self):
        return hash((Identifier, self.name))

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.name == other.name
        else:
            return NotImplemented


# An extension to the algorithm.  Literals are allowed, but have a the
# most specific type possible.
class Literal(AST):
    def __init__(self, value: Any, type_: Type, annotation: Any = None) -> None:
        self.value = value
        self.type = type_
        self.annotation = annotation

    def __repr__(self):
        if self.annotation is not None:
            return f'Literal({self.value!r}, {self.type!r}, {self.annotation!r})'
        else:
            return f'Literal({self.value!r}, {self.type!r})'


class Lambda(AST):
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body

    def __repr__(self):
        return f'Lambda({self.varname!r}, {self.body!r})'


class Application(AST):
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return f'Application({self.e1!r}, {self.e2!r})'


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a Let where you needed a Letrec.
class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST) -> None:
        self.bindings = bindings
        self.body = body


class Let(_LetExpr):
    def __repr__(self):
        return f'Let({self.bindings!r}, {self.body!r})'


class Letrec(_LetExpr):
    def __repr__(self):
        return f'Letrec({self.bindings!r}, {self.body!r})'
