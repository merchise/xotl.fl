#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A very simple type-expression language.

This (at the moment) just to implement the type-checker of chapter 9 of 'The
Implementation of Functional Programming Languages'.

.. note:: We should see if the types in stdlib's typing module are
          appropriate.

'''
from typing import List, Callable
from itertools import zip_longest


class Type:
    pass


class TypeVariable(Type):
    '''A type variable, which may stand for any type.

    '''
    def __init__(self, name: str, *, check=True):
        # `check` is only here to avoid the check when generating internal
        # names (which start with a dot)
        assert not check or name.isidentifier()
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'TypeVariable({self.name!r})'

    def __eq__(self, other):
        if isinstance(other, TypeVariable):
            return self.name == other.name
        elif isinstance(other, Type):
            return False
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


T = TVar = TypeVariable


class ConsType(Type):
    def __init__(self, constructor: str, subtypes: List[Type], *, binary=False):
        assert all(isinstance(t, Type) for t in subtypes)
        self.cons = constructor
        self.subtypes = subtypes
        self.binary = binary

    def __str__(self):
        def wrap(s):
            s = str(s)
            return f'({s})' if ' ' in s else s

        if self.binary:
            return f'{wrap(self.subtypes[0])} {self.cons} {wrap(self.subtypes[1])}'
        elif self.subtypes:
            return f'{self.cons} {" ".join(wrap(s) for s in self.subtypes)}'
        else:
            return self.cons

    def __repr__(self):
        return f'ConsType({self.cons!r}, {self.subtypes!r})'

    def __eq__(self, other):
        if isinstance(other, ConsType):
            return self.cons == other.cons and all(
                t1 == t2
                for t1, t2 in zip_longest(self.subtypes, other.subtypes)
            )
        elif isinstance(other, Type):
            return False
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.cons, self.subtypes))


F = FunctionType = lambda a, b: ConsType('->', [a, b], binary=True)
TupleType = lambda *ts: ConsType('tuple', list(ts))
ListType = lambda t: ConsType('list', [t])
IntType = ConsType('int', [])

SubstitutionType = Callable[[str], Type]


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TypeVariable):
        return [t.name]
    else:
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]


def subtype(phi: SubstitutionType, t: Type) -> Type:
    if isinstance(t, TypeVariable):
        return phi(t.name)
    else:
        return ConsType(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )


def scompose(f: SubstitutionType, g: SubstitutionType) -> SubstitutionType:
    '''Compose two substitutions.

    The crucial property of scompose is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    '''
    def result(s: str) -> Type:
        return subtype(f, g(s))
    return result


def delta(vname: str, const, *args) -> SubstitutionType:
    '''Create a `delta substitution` from a variable name `vname`.

    To avoid reusing instances of the same type expression, this function
    takes the constructor and it's arguments.  If you do want to use the same
    instance pass an instance wrapped in a lambda.  Example:

       >>> f = delta('a', T, 'id')
       >>> f('a') is f('a')
       False

       >>> f('b') is f('b')
       False

       >>> id = T('id')
       >>> f = delta('a', lambda: id)
       >>> f('a') is f('a')
       True

       >>> f('b') is f('b')
       False


    '''
    return lambda s: const(*args) if s == vname else TVar(s)


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
        yield TypeVariable(f'.{prefix}{i}', check=False)
        i += 1
