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
from typing import List, Callable, Tuple
from itertools import zip_longest


class Type:
    pass


class TypeVariable(Type):
    '''A type variable, which may stand for any type.

    '''
    def __init__(self, name: str, *, check=True):
        # `check` is only here to avoid the check when generating internal
        # names (which start with a dot)
        self.name = name
        assert not check or name.isidentifier()

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

    def __len__(self):
        return 0   # So that 'Int' has a bigger size than 'a'.


T = TVar = TypeVariable


class ConsType(Type):
    def __init__(self, constructor: str, subtypes: List[Type] = None, *, binary=False):
        assert not subtypes or all(isinstance(t, Type) for t in subtypes)
        self.cons = constructor
        self.subtypes = subtypes or []
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

    def __len__(self):
        return 1 + sum(len(st) for st in self.subtypes)


F = FunctionType = lambda a, b: ConsType('->', [a, b], binary=True)
TupleType = lambda *ts: ConsType('tuple', list(ts))
ListType = lambda t: ConsType('list', [t])
IntType = ConsType('int', [])

Substitution = Callable[[str], Type]


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TypeVariable):
        return [t.name]
    else:
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]


def subtype(phi: Substitution, t: Type) -> Type:
    if isinstance(t, TypeVariable):
        return phi(t.name)
    else:
        return ConsType(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )


def scompose(f: Substitution, g: Substitution) -> Substitution:
    '''Compose two substitutions.

    The crucial property of scompose is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    '''
    def result(s: str) -> Type:
        return subtype(f, g(s))
    return result


def sidentity(s: str) -> Type:
    'The identity substitution.'
    return T(s)


class delta:  # type: Substitution
    '''A `delta substitution` from a variable name `vname`.

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
    def __init__(self, vname: str, const, *args):
        self.vname = vname
        self.const = const
        self.args = args

    def __call__(self, s: str) -> Type:
        return self.result if s == self.vname else TVar(s)

    @property
    def result(self):
        return self.const(*self.args)


class UnificationError(SyntaxError):
    pass


def unify(phi: Substitution, exps: Tuple[Type, Type]) -> Substitution:

    def extend(phi: Substitution, name: str, t: Type) -> Substitution:
        if isinstance(t, TVar) and name == t.name:
            return phi
        elif name in find_tvars(t):
            raise UnificationError(f'Cannot unify {name} with {t}')
        else:
            # TODO: Make the result *descriptible*
            return scompose(delta(name, lambda: t), phi)

    def unify_with_tvar(tvar, t):
        phitvn = phi(tvar.name)
        if phitvn == tvar:
            return extend(phi, tvar.name, subtype(phi, t))
        else:
            return unify(phi, (phitvn, subtype(phi, t)))

    def unify_subtypes(p: Substitution, types: List[Tuple[Type, Type]]) -> Substitution:
        for eqn in types:
            p = unify(p, eqn)
        return p

    t1, t2 = exps
    if isinstance(t1, TVar):
        return unify_with_tvar(t1, t2)
    elif isinstance(t2, TVar):
        return unify_with_tvar(t2, t1)
    else:
        assert isinstance(t1, ConsType) and isinstance(t2, ConsType)
        if t1.cons == t2.cons:
            return unify_subtypes(phi, zip(t1.subtypes, t2.subtypes))
        else:
            raise UnificationError(f'Cannot unify {t1} with {t2}')
