#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A naive type-checking algorithm for the enriched lambda calculus.

An experimental Python implementation of the same type-checker implemented in
chapter 9 of 'The Implementation of Functional Programming Languages'.

'''
from typing import Mapping, Any, List

from .base import Type, TVar, TypeVariable
from .unification import subtype, find_tvars, Substitution


class TypeScheme:
    # I choose the word 'generic' instead of schematic (and thus non-generic
    # instead of unknown), because that's probably more widespread.
    def __init__(self, generics: List[str], t: Type) -> None:
        self.generics = generics
        self.t = t

    @property
    def nongenerics(self) -> List[str]:
        return [
            name
            for name in find_tvars(self.t)
            if name not in self.generics
        ]


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.'''
    exclude: Substitution = lambda s: phi(s) if s not in ts.generics else TVar(s)
    return TypeScheme(ts.generics, subtype(exclude, ts.t))


class namesupply:
    '''A names supply.

    Each variable will be name '.{prefix}{index}'; where the index starts at 0
    and increases by one at each new name.

    If `limit` is None (or 0), return a unending stream; otherwise yield as
    many items as `limit`:

       >>> list(namesupply(limit=2))
       [TypeVariable('.a0'), TypeVariable('.a1')]

    '''
    def __init__(self, prefix='a', exclude: List[str] = None,
                 *, limit: int = None) -> None:
        self.prefix = prefix
        self.exclude = exclude
        self.limit = limit
        self.current_index = 0
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> TypeVariable:
        if not self.limit or self.count < self.limit:
            result = None
            while not result:
                name = f'.{self.prefix}{self.current_index}'
                if not self.exclude or name not in self.exclude:
                    result = name
                self.current_index += 1
            self.count += 1
            return TVar(result, check=False)
        else:
            raise StopIteration


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


class LambdaAbs(AST):
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body


class Application(AST):
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2


class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST) -> None:
        self.bindings = bindings
        self.body = body


class LetExpression(_LetExpr):
    pass


class LetrecExpression(_LetExpr):
    pass
