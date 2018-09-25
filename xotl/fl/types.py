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
from collections import deque
from typing import Iterable, Sequence, List, Mapping, Deque, Tuple
from typing import Optional  # noqa
from dataclasses import dataclass, InitVar, field


class AST:
    pass


class Type(AST):
    @classmethod
    def from_str(cls, source: str) -> 'Type':
        '''Parse a single type expression.

        Example:

            >>> Type.from_str('a -> b -> a')
            TypeCons('->', (TypeVariable('a'), TypeCons('->', (...))))

        '''
        return parse(source)


@dataclass(frozen=True)
class TypeVariable(Type):
    '''A type variable, which may stand for any type.

    '''
    name: str
    check: InitVar[bool] = True

    def __post_init__(self, check=True) -> None:
        # `check` is only here to avoid the check when generating internal
        # names (which start with a dot)
        assert not check or self.name.isidentifier()

    def __str__(self):
        return f'{self.name}'

    def __len__(self):
        return 0   # So that 'Int' has a bigger size than 'a'.


@dataclass(frozen=True)
class TypeCons(Type):
    '''The syntax for a type constructor expression.

    '''
    cons: str
    subtypes: Tuple[Type] = field(init=False)
    subtypes_: InitVar[Iterable[Type]] = []
    binary: bool = False

    def __post_init__(self, subtypes_: Iterable[Type] = None) -> None:
        assert not subtypes_ or all(isinstance(t, Type) for t in subtypes_), \
            f'Invalid subtypes: {subtypes_!r}'
        object.__setattr__(
            self,
            'subtypes',
            tuple(subtypes_ or [])
        )

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

    def __len__(self):
        return 1 + sum(len(st) for st in self.subtypes)


# Q: Should I make TypeScheme a sub-type?
@dataclass(frozen=True)
class TypeScheme:
    '''A type scheme with generic (schematics) type variables.

    Example:

      >>> from xotl.fl import type_parse
      >>> map_type = TypeScheme(['a', 'b'],
      ...                       type_parse('(a -> b) -> List a -> List b'))

      >>> str(map_type)
      'forall a b. (a -> b) -> ((List a) -> (List b))'

    '''
    # I choose the word 'generic' instead of schematic (and thus non-generic
    # instead of unknown), because that's probably more widespread.
    generics: Sequence[str]
    t: Type

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
        if self.generics:
            return f'forall {self.names!s}. {self.t!s}'
        else:
            return str(self.t)

    @classmethod
    def from_typeexpr(cls, type_: Type, *,
                      generics: Sequence[str] = None) -> 'TypeScheme':
        '''Create a type scheme from a type expression assuming all type
        variables are generic.'''
        if generics is None:
            generics = list(sorted(set(find_tvars(type_))))  # avoid repetitions.
        return cls(generics, type_)

    @classmethod
    def from_str(cls, source: str, *,
                 generics: Sequence[str] = None) -> 'TypeScheme':
        '''Create a type scheme from a type expression assuming all type variables are
        generic.

        Example:

           >>> TypeScheme.from_str('a -> b -> a')
           <TypeScheme: forall a b. a -> (b -> a)>

        '''
        type_ = parse(source)
        return cls.from_typeexpr(type_, generics=generics)


#: Shortcut to create function types
FunctionTypeCons = lambda a, b: TypeCons('->', [a, b], binary=True)

#: Shortcut to create a tuple type from types `ts`.  The Unit type can be
#: regarded as the tuple type without arguments.
TupleTypeCons = lambda *ts: TypeCons('Tuple', ts)

#: Shortcut to create a list type from type `t`.
ListTypeCons = lambda t: TypeCons('[]', [t])


TypeEnvironment = Mapping[str, TypeScheme]
EMPTY_TYPE_ENV: TypeEnvironment = {}


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.types>`:mod:.

    Example:

       >>> parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    '''
    from .parsers import type_parser, lexer
    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def find_tvars(t: Type) -> List[str]:
    '''Get all variables names (possibly repeated) in type `t`.

    Example:

       >>> find_tvars(Type.from_str('a -> b -> a'))
       ['a', 'b', 'a']

    '''
    result: Deque[str] = deque([])
    queue: Deque[Type] = deque([t])
    while queue:
        t = queue.pop()
        if isinstance(t, TypeVariable):
            result.append(t.name)
        else:
            assert isinstance(t, TypeCons)
            queue.extend(t.subtypes)
    return list(result)
