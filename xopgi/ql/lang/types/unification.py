#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Callable, List, Tuple, Iterator

from .base import (
    Type,
    TypeCons,
    TypeVariable,
)


# `Substitution` is a type; `scompose`:class: is a substitution by
# composition, `delta`:class: creates the simplest non-empty substitution.
#
# TODO: We could modify the algorithm so that we can *inspect* which variables
# are being substituted; but that's not essential to the Substitution Type.
Substitution = Callable[[str], Type]


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TypeVariable):
        return [t.name]
    else:
        assert isinstance(t, TypeCons)
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]


def subtype(phi: Substitution, t: Type) -> Type:
    if isinstance(t, TypeVariable):
        return phi(t.name)
    else:
        assert isinstance(t, TypeCons)
        return TypeCons(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )


class scompose:
    '''Compose two substitutions.

    The crucial property of scompose is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    '''
    def __init__(self, f: Substitution, g: Substitution) -> None:
        self.f = f
        self.g = g

    def __call__(self, s: str) -> Type:
        return subtype(self.f, self.g(s))

    def __repr__(self):
        return f'scompose({self.f!r}, {self.g!r})'


class Identity:
    'The identity substitution.'
    def __call__(self, s: str) -> Type:
        return TypeVariable(s)

    def __repr__(self):
        return f'Indentity()'


sidentity = Identity()


class delta:
    '''A `delta substitution` from a variable name `vname`.

    To avoid reusing instances of the same type expression, this function
    takes the type constructor and its arguments.  If you do want to use the
    same instance pass an instance wrapped in a lambda.  Example:

       >>> f = delta('a', T, 'id')
       >>> f('a') is f('a')
       False

       >>> f('b') is f('b')
       False

       >>> f = delta('a', lambda: T('id'))
       >>> f('a') is f('a')
       True

       >>> f('b') is f('b')
       False

    '''
    def __init__(self, vname: str, cons, *args) -> None:
        self.vname = vname
        self.cons = cons
        self.args = args

    def __call__(self, s: str) -> Type:
        return self.result if s == self.vname else TypeVariable(s)

    @property
    def result(self) -> Type:
        return self.cons(*self.args)

    def __repr__(self):
        return f'delta({self.vname!r}, {self.result!r})'


class UnificationError(Exception):
    pass


def unify(e1: Type, e2: Type, *, phi: Substitution = sidentity) -> Substitution:
    '''Extend `phi` so that it unifies `e1` and `e2`.

    If `phi` is None, uses the `identity substitution <Identity>`:class.

    If there's no substitution that unifies the given terms, raise a
    `UnificationError`:class:.

    '''
    # This a combination of the function unifyl and unify in the Book.  I
    # don't see any value in following the Book exactly.
    def extend(phi: Substitution, name: str, t: Type) -> Substitution:
        if isinstance(t, TypeVariable) and name == t.name:
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
            return unify(phitvn, subtype(phi, t), phi=phi)

    def unify_subtypes(p: Substitution,
                       types: Iterator[Tuple[Type, Type]]) -> Substitution:
        for se1, se2 in types:
            p = unify(se1, se2, phi=p)
        return p

    if isinstance(e1, TypeVariable):
        return unify_with_tvar(e1, e2)
    elif isinstance(e2, TypeVariable):
        return unify_with_tvar(e2, e1)
    else:
        assert isinstance(e1, TypeCons) and isinstance(e2, TypeCons)
        if e1.cons == e2.cons:
            return unify_subtypes(phi, zip(e1.subtypes, e2.subtypes))
        else:
            raise UnificationError(f'Cannot unify {e1} with {e2}')
