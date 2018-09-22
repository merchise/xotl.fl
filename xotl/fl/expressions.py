#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass, field, InitVar

from typing import Any, Mapping, Iterator, Sequence, Tuple
from xoutil.fp.tools import fst

from .types import AST, Type, TypeCons


@dataclass(frozen=True)
class Identifier(AST):
    '''A name (variable if you like).'''
    name: str


# An extension to the algorithm.  Literals are allowed, but have a the
# most specific type possible.
@dataclass(frozen=True)
class Literal(AST):
    '''A literal value with its type.

    The `parser <xotl.fl.expressions.parse>`:func: only recognizes strings,
    chars, and numbers (integers and floats are represented by a single type).

    '''
    value: Any
    type: Type
    annotation: Any = None

    def __repr__(self):
        if self.annotation is not None:
            return f'Literal({self.value!r}, {self.type!r}, {self.annotation!r})'
        else:
            return f'Literal({self.value!r}, {self.type!r})'


@dataclass(frozen=True)
class Lambda(AST):
    '''A lambda abstraction over a single parameter. '''
    varname: str
    body: AST

    def __str__(self):
        return f'\{self.varname!s} -> {self.body!s}'


@dataclass(frozen=True)
class Application(AST):
    '''The application of `e1` to its *argument* e2.'''
    e1: AST
    e2: AST

    def __str__(self):
        return f'{self.e1!s} {self.e2!s}'


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a Let where you needed a Letrec.

@dataclass(frozen=True)
class _LetExpr(AST):
    bindings: Mapping[str, AST] = field(init=False)
    _defs: InitVar[Mapping[str, AST]]
    body: AST

    def __post_init__(self, _defs) -> None:
        # Sort by names (in a _LetExpr names can't be repeated, repetition for
        # pattern-matching should be translated to a lambda using the MATCH
        # operator).
        object.__setattr__(
            self,
            'bindings',
            tuple(sorted(_defs.items(), key=fst))
        )

    def keys(self) -> Iterator[str]:
        return (k for k, _ in self.bindings)

    def values(self) -> Iterator[AST]:
        return (v for _, v in self.bindings)


class Let(_LetExpr):
    '''A non-recursive Let expression.

    The `parser <xotl.fl.expressions.parse>`:func: automatically selects
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


# Patterns and Equations.  In the final AST, an expression like:
#
#     let id x = x in ...
#
# would actually be like
#
#     let id = \x -> x
#
# with some complications if pattern-matching is allowed:
#
#     let length [] = 0
#         lenght (x:xs) = 1 + length xs
#     in  ...
#
# For now, we allow only the SIMPLEST of all definitions (we don't have a
# 'case' keyword to implement pattern matching.)  But, in any case, having the
# names of productions be 'pattern' and 'equations' is fit.
#
#
# The Pattern and Equation definitions are not part of the final AST, but more
# concrete syntactical object in the source code.  In the final AST, the let
# expressions shown above are indistinguishable.
#
# For value (function) definitions the parser still returns *bare* Equation
# object for each line of the definition.
@dataclass(frozen=True)
class Pattern:
    cons: str
    params: Tuple[str] = field(default_factory=tuple)

    def __str__(self):
        if self.params:
            return f'{self.cons} {self.parameters}'
        else:
            return self.cons

    @property
    def parameters(self):
        return ' '.join(self.params)


@dataclass(frozen=True)
class Equation:
    pattern: Pattern
    body: AST


@dataclass(frozen=True)
class DataCons:
    name: str
    args: Sequence[Type] = field(init=False)
    args_: InitVar[Sequence[Type]]

    def __post_init__(self, args_: Sequence[Type]) -> None:
        object.__setattr__(
            self,
            'args',
            tuple(args_)
        )

    def __repr__(self):
        names = ' '.join(map(str, self.args))
        if names:
            return f'<DataCons {self.name} {names}>'
        else:
            return f'<DataCons {self.name}>'


@dataclass(frozen=True)
class DataType:
    name: str
    t: TypeCons
    dataconses: Sequence[DataCons] = field(init=False)
    _defs: InitVar[Sequence[DataCons]]

    def __post_init__(self, _defs) -> None:
        object.__setattr__(
            self,
            'dataconses',
            tuple(_defs or [])
        )

    def __repr__(self):
        defs = ' | '.join(map(str, self.dataconses))
        return f'<Data {self.t} = {defs}>'


def parse(code: str, debug=False, tracking=False) -> AST:
    '''Parse a single expression `code`.
    '''
    from .parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)
