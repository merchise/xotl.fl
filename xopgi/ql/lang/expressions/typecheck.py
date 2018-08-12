#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Any, List, Tuple, Iterator

from ..types.base import Type, TypeVariable as TypeVar
from ..types.unification import subtype, find_tvars, Substitution

from .base import AST


class TypeScheme:
    '''A type scheme with generic (schematics) type variables.

    Example:

      >>> from xopgi.ql.lang.types.parser import parse
      >>> map_type = TypeScheme(['a', 'b'],
      ...                       parse('(a -> b) -> List a -> List b'))

      >>> map_type
      <TypeScheme: forall a b. (a -> b) -> ((List a) -> (List b))>

    '''
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

    @property
    def names(self):
        return ' '.join(self.generics)

    def __str__(self):
        return f'forall {self.names!s}. {self.t!s}'

    def __repr__(self):
        return f'<TypeScheme: {self!s}>'


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.'''
    exclude: Substitution = lambda s: phi(s) if s not in ts.generics else TypeVar(s)
    return TypeScheme(ts.generics, subtype(exclude, ts.t))


AssocList = List[Tuple[Any, Any]]


def dom(al: AssocList) -> List[Any]:
    return [k for k, _ in al]


def val(al: AssocList, key: Any) -> List[Any]:
    return [v for k, v in al if k == key]


def rng(al: AssocList) -> List[Any]:
    # The provided implementation in the Book (``map (val al) (dom al)``) is
    # rather inefficient (O(n^2), because for each key it takes all its
    # values).
    return [v for _, v in al]


def install_al(al: AssocList, key: Any, val: Any) -> AssocList:
    # This is inefficient!!!
    return [(key, val)] + al


def insert_al(al: AssocList, key: Any, val: Any) -> AssocList:
    al.insert(0, (key, val))
    return al


#: A subtype of AssocList from names to TypeSchemes.
TypeEnvironment = List[Tuple[str, TypeScheme]]


def get_typeenv_unknowns(te: TypeEnvironment) -> List[str]:
    return sum((t.nongenerics for _, t in te), [])


def sub_typeenv(phi: Substitution, te: TypeEnvironment) -> TypeEnvironment:
    return [(x, subscheme(phi, st)) for x, st in te]


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

    def __next__(self) -> TypeVar:
        if not self.limit or self.count < self.limit:
            result = None
            while not result:
                name = f'.{self.prefix}{self.current_index}'
                if not self.exclude or name not in self.exclude:
                    result = name
                self.current_index += 1
            self.count += 1
            return TypeVar(result, check=False)
        else:
            raise StopIteration


class TypeChecker:
    def __init__(self, env: TypeEnvironment, ns: Iterator[TypeVar]) -> None:
        self.env = env
        self.ns = ns

    def __call__(self, exp: AST) -> None:
        typecheck(self.env, self.ns, exp)


def typecheck(env: TypeEnvironment, ns: Iterator[TypeVar], exp: AST):
    '''Check the type of `exp` in a given type environment.

    '''
    pass
