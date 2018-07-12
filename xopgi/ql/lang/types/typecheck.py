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

from .base import Type, TVar
from .unification import subtype, find_tvars, Substitution


class TypeScheme:
    def __init__(self, names: List[str], t: Type):
        self.names = names
        self.t = names

    @property
    def unknowns(self) -> List[str]:
        return [name for name in find_tvars(self.t) if name not in self.names]


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.'''
    exclude = lambda s: phi(s) if s not in ts.names else TVar(s)
    return TypeScheme(ts.names, subtype(exclude, ts.t))


def genvars(prefix='a', *, limit=None):
    '''An stream of type variables.

    Each variable will be name '.{prefix}{index}'; where the index starts at 0
    and increases by one at each new name.

    If `limit` is None (or 0), return a unending stream; otherwise yield as
    many items as `limit`:

       >>> list(genvars(limit=2))
       [TypeVariable('.a0'), TypeVariable('.a1')]

    '''
    i = 0
    while not limit or i < limit:
        yield TVar(f'.{prefix}{i}', check=False)
        i += 1


class AST:
    pass


class Variable(AST):
    def __init__(self, name: str):
        self.name = name


class Literal(AST):
    # An extension to the algorithm.  Literals are allowed, but have a
    # definite type: the most specific type possible.
    def __init__(self, value: Any, type_: Type):
        self.value = value
        self.type = type_


class LambdaAbs(AST):
    def __init__(self, varname: str, body: AST):
        self.varname = varname
        self.body = body


class Application(AST):
    def __init__(self, e1: AST, e2: AST):
        self.e1 = e1
        self.e2 = e2


class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST):
        self.bindings = bindings
        self.body = body


class LetExpression(_LetExpr):
    pass


class LetrecExpression(_LetExpr):
    pass
