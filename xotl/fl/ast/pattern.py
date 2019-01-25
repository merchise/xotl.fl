#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Pattern Matching.

'''
from typing import (
    List,
    MutableMapping,
    Union,
    Sequence,
    Tuple,
    Type as Class,
)
from dataclasses import dataclass

from .base import AST
from .types import TypeEnvironment
from .expressions import (
    Literal,
    _LetExpr,
    Let,
    Letrec,
    find_free_names,
)


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
# The Pattern and Equation definitions are not part of the final AST, but more
# concrete syntactical object in the source code.  In the final AST, the let
# expressions shown above are indistinguishable.
#
# For value (function) definitions the parser still returns *bare* Equation
# object for each line of the definition.


class ConsPattern(AST):
    '''The syntactical notion of a pattern.

    '''
    def __init__(self, cons: str, params=None) -> None:
        self.cons: str = cons
        self.params = tuple(params or [])

    def __repr__(self):
        return f'<pattern {self.cons!r} {self.params!r}>'

    def __str__(self):
        if self.params:
            return f'{self.cons} {self._parameters}'
        else:
            return self.cons

    @property
    def _parameters(self):
        def _str(x):
            if isinstance(x, str):
                return x
            elif isinstance(x, ConsPattern):
                return f'({x})'
            else:
                return repr(x)

        return ' '.join(map(_str, self.params))

    def __eq__(self, other):
        if isinstance(other, ConsPattern):
            return self.cons == other.cons and self.params == other.params
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ConsPattern):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((ConsPattern, self.cons, self.params))


Pattern = Union[str, Literal, ConsPattern]


class Equation(AST):
    '''The syntactical notion of an equation.

    '''
    def __init__(self, name: str, patterns: Sequence[Pattern], body: AST) -> None:
        self.name = name
        self.patterns: Tuple[Pattern, ...] = tuple(patterns or [])
        self.body = body

    def __repr__(self):
        def _str(x):
            result = str(x)
            if ' ' in result:
                return f'({result})'
            else:
                return result

        if self.patterns:
            args = ' '.join(map(_str, self.patterns))
            return f'<equation {self.name!s} {args} = {self.body!r}>'
        else:
            return f'<equation {self.name!s} = {self.body!r}>'

    def __eq__(self, other):
        if isinstance(other, Equation):
            return (self.name == other.name and
                    self.patterns == other.patterns and
                    self.body == other.body)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Equation):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Equation, self.name, self.patterns, self.body))


LocalDefinition = Union[Equation, TypeEnvironment]


@dataclass
class ConcreteLet(AST):
    '''The concrete representation of a let/where expression.

    '''
    definitions: List[LocalDefinition]  # noqa
    body: AST

    @property
    def ast(self) -> _LetExpr:
        return self.compile()

    def compile(self) -> _LetExpr:
        r'''Build a Let/Letrec from a set of equations and a body.

        We need to decide if we issue a Let or a Letrec: if any of declared
        names appear in the any of the bodies we must issue a Letrec, otherwise
        issue a Let.

        Also we need to convert function-patterns into Lambda abstractions::

           let id x = ...

        becomes::

           led id = \x -> ...

        '''
        from xotl.fl.match import FunctionDefinition
        localenv: TypeEnvironment = {}
        defs: MutableMapping[str, FunctionDefinition] = {}   # noqa
        for dfn in self.definitions:
            if isinstance(dfn, Equation):
                eq = defs.get(dfn.name)
                if not eq:
                    defs[dfn.name] = FunctionDefinition([dfn])
                else:
                    assert isinstance(eq, FunctionDefinition)
                    defs[dfn.name] = eq.append(dfn)
            elif isinstance(dfn, dict):
                localenv.update(dfn)  # type: ignore
            else:
                assert False, f'Unknown definition type {dfn!r}'
        names = set(defs)
        compiled = {name: dfn.compile() for name, dfn in defs.items()}
        if any(set(find_free_names(fn)) & names for fn in compiled.values()):
            klass: Class[_LetExpr] = Letrec
        else:
            klass = Let
        return klass(compiled, self.body, localenv)
