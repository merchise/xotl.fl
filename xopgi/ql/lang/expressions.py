#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Any, Mapping, Iterator
from xoutil.objects import validate_attrs
from xoutil.fp.tools import fst

from .types import AST, Type


class Identifier(AST):
    '''A name (variable if you like).'''
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name!r})'

    def __str__(self):
        return self.name

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
    '''A literal value with its type.

    The `parser <xopgi.ql.lang.expressions.parse>`:func: only recognizes
    strings, chars, and numbers (integers and floats are represented by a
    single type).

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

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return validate_attrs(self, other, ('type', 'value', 'annotation'))
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Literal, self.value, self.type_, self.annotation))


class Lambda(AST):
    '''A lambda abstraction over a single parameter. '''
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body

    def __repr__(self):
        return f'Lambda({self.varname!r}, {self.body!r})'

    def __str__(self):
        return f'\{self.varname!s} -> {self.body!s}'

    def __eq__(self, other):
        if isinstance(other, Lambda):
            return self.varname == other.varname and self.body == other.body
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Lambda, self.varname, self.body))


class Application(AST):
    '''The application of `e1` to its *argument* e2.'''
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return f'Application({self.e1!r}, {self.e2!r})'

    def __str__(self):
        return f'{self.e1!s} {self.e2!s}'

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.e1 == other.e1 and self.e2 == other.e2
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Application, self.e1, self.e2))


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a Let where you needed a Letrec.
class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST) -> None:
        # Sort by names (in a _LetExpr names can't be repeated, repetition for
        # pattern-matching should be translated to a lambda using the MATCH
        # operator).
        self.bindings = tuple(sorted(bindings.items(), key=fst))
        self.body = body

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.bindings == other.bindings and self.body == self.body
        else:
            return NotImplemented

    def __hash__(self):
        return hash((type(self), self.keys(), self.values(), self.body))

    def keys(self) -> Iterator[str]:
        return (k for k, _ in self.bindings)

    def values(self) -> Iterator[AST]:
        return (v for _, v in self.bindings)


class Let(_LetExpr):
    '''A non-recursive Let expression.

    The `parser <xopgi.ql.lang.expressions.parse>`:func: automatically selects
    between `Let`:class: and `Letrec`:class.  If you're creating the program
    by hand you should choose appropriately.

    '''
    def __repr__(self):
        return f'Let({self.bindings!r}, {self.body!r})'


class Letrec(_LetExpr):
    '''A recursive Let expression.

    .. seealso:: `Let`:class:

    '''
    def __repr__(self):
        return f'Letrec({self.bindings!r}, {self.body!r})'


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single expression `code`.
    '''
    from .parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def tokenize(source):
    from .parsers import lexer
    lexer = lexer.clone()
    lexer.input(source)
    return [tok for tok in lexer]
