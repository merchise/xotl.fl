#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Any, Mapping
from xoutil.objects import validate_attrs

from ..types.base import Type


class AST:
    pass


class Identifier(AST):
    '''A name (variable if you like).'''
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
    '''A literal value with is type.

    The `~xopgi.ql.lang.expressions.parser`:mod: only recognizes strings,
    chars, and numbers (integers and floats are represented by a single type).

    .. note:: This is an extension to the algorithm, but you can easily that
       we may replace literals by identifiers with a predefined type.

    '''
    def __init__(self, value: Any, type_: Type, annotation: Any = None) -> None:
        self.value = value
        self.type = type_
        self.annotation = annotation

    def __repr__(self):
        if self.annotation is not None:
            return f'Literal({self.value!r}, {self.type!r}, {self.annotation!r})'
        else:
            return f'Literal({self.value!r}, {self.type!r})'

    def __eq__(self, other):
        if isinstance(other, Literal):
            return validate_attrs(self, other, ('type', 'value', 'annotation'))
        else:
            return NotImplemented


class Lambda(AST):
    '''A lambda abstraction over a single parameter. '''
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body

    def __repr__(self):
        return f'Lambda({self.varname!r}, {self.body!r})'

    def __eq__(self, other):
        if isinstance(other, Lambda):
            return self.varname == other.varname and self.body == other.body
        else:
            return NotImplemented


class Application(AST):
    '''The application of `e1` to its *argument* e2.'''
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return f'Application({self.e1!r}, {self.e2!r})'

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.e1 == other.e1 and self.e2 == other.e2
        else:
            return NotImplemented


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a Let where you needed a Letrec.
class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST) -> None:
        self.bindings = bindings
        self.body = body

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.bindings == other.bindings and self.body == self.body
        else:
            return NotImplemented


class Let(_LetExpr):
    '''A non-recursive Let expression.

    The `~xopgi.ql.lang.expressions.parser`:mod: automatically selects between
    `Let`:class: and `Letrec`:class.  If you're creating the program by hand
    you should choose appropriately.  (But the type-checker doesn't really
    care.)

    '''
    def __repr__(self):
        return f'Let({self.bindings!r}, {self.body!r})'


class Letrec(_LetExpr):
    '''A recursive Let expression.

    .. sealso:: `Let`:class:

    '''
    def __repr__(self):
        return f'Letrec({self.bindings!r}, {self.body!r})'
