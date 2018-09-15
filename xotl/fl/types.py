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
from typing import Iterable, Sequence, List, Mapping
from typing import Optional  # noqa
from itertools import zip_longest


class AST:
    pass


class Type(AST):
    @classmethod
    def from_str(cls, source):
        '''Parse a single type expression `code`.

        Return a `type expression AST <xotl.fl.types.base>`:mod:.

        '''
        return parse(source)


class TypeVariable(Type):
    '''A type variable, which may stand for any type.

    '''
    def __init__(self, name: str, *, check=True) -> None:
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
        else:
            return NotImplemented

    def __hash__(self):
        return hash((TypeVariable, self.name))

    def __len__(self):
        return 0   # So that 'Int' has a bigger size than 'a'.


class TypeCons(Type):
    '''The syntax for a type constructor expression.

    '''
    def __init__(self, constructor: str, subtypes: Iterable[Type] = None,
                 *, binary=False) -> None:
        assert not subtypes or all(isinstance(t, Type) for t in subtypes), \
            f'Invalid subtypes: {subtypes!r}'
        self.cons = constructor
        self.subtypes: Sequence[Type] = tuple(subtypes or [])
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
        return f'TypeCons({self.cons!r}, {self.subtypes!r})'

    def __eq__(self, other):
        if isinstance(other, TypeCons):
            return self.cons == other.cons and all(
                t1 == t2
                for t1, t2 in zip_longest(self.subtypes, other.subtypes)
            )
        else:
            return NotImplemented

    def __hash__(self):
        return hash((TypeCons, self.cons, self.subtypes))

    def __len__(self):
        return 1 + sum(len(st) for st in self.subtypes)


# Q: Should I make TypeScheme a sub-type?
class TypeScheme:
    '''A type scheme with generic (schematics) type variables.

    Example:

      >>> from xotl.fl import type_parse
      >>> map_type = TypeScheme(['a', 'b'],
      ...                       type_parse('(a -> b) -> List a -> List b'))

      >>> map_type
      <TypeScheme: forall a b. (a -> b) -> ((List a) -> (List b))>

    '''
    # I choose the word 'generic' instead of schematic (and thus non-generic
    # instead of unknown), because that's probably more widespread.
    def __init__(self, generics: Sequence[str], t: Type) -> None:
        self.generics = generics
        self.t = t

    @property
    def nongenerics(self) -> List[str]:
        return [
            name
            for name in find_tvars(self.t)
            if name not in self.generics
        ]

    def __eq__(self, other):
        if isinstance(other, TypeScheme):
            return self.generics == other.generics and self.t == other.t
        else:
            return NotImplemented

    def __hash__(self):
        return hash((TypeScheme, self.generics, self.t))

    @property
    def names(self):
        return ' '.join(self.generics)

    def __str__(self):
        if self.generics:
            return f'forall {self.names!s}. {self.t!s}'
        else:
            return str(self.t)

    def __repr__(self):
        return f'<TypeScheme: {self!s}>'

    @classmethod
    def from_typeexpr(cls, type_, *, generics=None):
        # type: (Type, *, Optional[Sequence[str]]) -> TypeScheme
        '''Create a type scheme from a type expression assuming all type
        variables are generic.'''
        if generics is None:
            generics = list(set(find_tvars(type_)))  # avoid repetitions.
        return cls(generics, type_)

    @classmethod
    def from_str(cls, source, *, generics=None):
        # type: (str, *, Optional[Sequence[str]]) -> TypeScheme
        '''Create a type scheme from a type expression (given a string)
        assuming all type variables are generic.'''
        type_ = parse(source)
        return cls.from_typeexpr(type_, generics=generics)


#: Shortcut to create function types
FunctionTypeCons = lambda a, b: TypeCons('->', [a, b], binary=True)

#: Shortcut to create a tuple type from types `ts`.  The Unit type can be
#: regarded as the tuple type without arguments.
TupleTypeCons = lambda *ts: TypeCons('Tuple', list(ts))

#: Shortcut to create a list type from type `t`.
ListTypeCons = lambda t: TypeCons('[]', [t])


TypeEnvironment = Mapping[str, TypeScheme]
EMPTY_TYPE_ENV: TypeEnvironment = {}


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.types.base>`:mod:.

    Example:

       >>> parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    '''
    from .parsers import type_parser, lexer
    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TypeVariable):
        return [t.name]
    else:
        assert isinstance(t, TypeCons)
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]
