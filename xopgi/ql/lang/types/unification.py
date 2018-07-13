#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Callable, List, Tuple, Iterator

from .base import C, Type, TVar, T


Substitution = Callable[[str], Type]


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TVar):
        return [t.name]
    else:
        assert isinstance(t, C)
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]


def subtype(phi: Substitution, t: Type) -> Type:
    if isinstance(t, TVar):
        return phi(t.name)
    else:
        assert isinstance(t, C)
        return C(
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
        return T(s)

    def __repr__(self):
        return f'Indentity()'


sidentity = Identity()


class delta:
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
    def __init__(self, vname: str, const, *args) -> None:
        self.vname = vname
        self.const = const
        self.args = args

    def __call__(self, s: str) -> Type:
        return self.result if s == self.vname else TVar(s)

    @property
    def result(self) -> Type:
        return self.const(*self.args)

    def __repr__(self):
        return f'delta({self.vname!r}, {self.result!r})'


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

    def unify_subtypes(p: Substitution,
                       types: Iterator[Tuple[Type, Type]]) -> Substitution:
        for eqn in types:
            p = unify(p, eqn)
        return p

    t1, t2 = exps
    if isinstance(t1, TVar):
        return unify_with_tvar(t1, t2)
    elif isinstance(t2, TVar):
        return unify_with_tvar(t2, t1)
    else:
        assert isinstance(t1, C) and isinstance(t2, C)
        if t1.cons == t2.cons:
            return unify_subtypes(phi, zip(t1.subtypes, t2.subtypes))
        else:
            raise UnificationError(f'Cannot unify {t1} with {t2}')
