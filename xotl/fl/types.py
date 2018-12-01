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
from typing import (
    Iterable,
    Sequence,
    List,
    Mapping,
    Deque,
    Set,
    Union,
    Tuple,
)
from typing import Optional  # noqa
from itertools import zip_longest
from dataclasses import dataclass


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

    def __rshift__(self, other):
        '''Return the function type 'self -> other'.'''
        if isinstance(other, Type):
            return FunctionTypeCons(self, other)
        else:
            t1 = type(self).__name__
            t2 = type(other).__name__
            raise TypeError(
                f"unsupported operand type(s) for >>: '{t1}' and '{t2}'"
            )


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

    def __bool__(self):
        return True   # needed because __len__ is 0.


@dataclass
class TypeConstraint:
    name: str   # This is the name of the constraint, e.g 'Eq'
    variable: TypeVariable

    def __str__(self):
        return f'{self.name} {self.variable.name}'


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


class TypeScheme(Type):
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
    def from_typeexpr(cls, type_: Type, *,
                      generics: Sequence[str] = None) -> 'TypeScheme':
        '''Create a type scheme from a type expression assuming all type
        variables are generic.'''
        if isinstance(type_, TypeScheme):
            return type_
        if generics is None:
            generics = list(sorted(set(find_tvars(type_))))  # avoid repetitions.
        return cls(generics, type_)

    @classmethod
    def from_str(cls, source: str, *, generics:
                 Sequence[str] = None) -> 'TypeScheme':
        '''Create a type scheme from a type expression assuming all type variables are
        generic.

        Example:

           >>> TypeScheme.from_str('a -> b -> a')
           <TypeScheme: forall a b. a -> (b -> a)>

        '''
        type_ = parse(source)
        return cls.from_typeexpr(type_, generics=generics)


@dataclass
class ConstrainedType(Type):
    constraints: Tuple[TypeConstraint, ...]
    type: Type

    def __init__(self, constraints: Sequence[TypeConstraint], t: Type) -> None:
        constraints = tuple(constraints)
        constrained = {c.variable.name for c in constraints}
        names = set(find_tvars(t))
        if constrained - names:
            raise TypeError(
                f'Constraint not applied: {constrained - names}'
            )
        self.constraints = constraints
        self.type = t

    def __str__(self):
        constraints = ', '.join(map(str, self.constraints))
        return f'{constraints} => {self.type!s}'


#: Shortcut to create function types
FunctionTypeCons = lambda a, b: TypeCons('->', [a, b], binary=True)


#: Shortcut to create a tuple type from types `ts`.  The Unit type can be
#: regarded as the tuple type without arguments.
class TupleTypeCons(TypeCons):
    def __init__(self, *ts: Type) -> None:
        if not ts:
            name = 'Unit'
        else:
            if len(ts) == 1:
                name = 'Singleton'
            else:
                name = ',' * (len(ts) - 1)
        super().__init__(name, ts)

    def __str__(self):
        ts = self.subtypes
        if not ts:
            return '()'
        else:
            if len(ts) == 1:
                return f'({ts[0]!s}, )'
            else:
                types = ', '.join(map(str, ts))
                return f'({types})'


class ListTypeCons(TypeCons):
    def __init__(self, t: Type) -> None:
        super().__init__('[]', [t])

    def __str__(self):
        t = self.subtypes[0]
        return f'[{t!s}]'


class Symbol:
    pass


TypeEnvironment = Mapping[Union[str, Symbol], TypeScheme]
EMPTY_TYPE_ENV: TypeEnvironment = {}


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single type expression `code`.

    Return a `type expression AST <xotl.fl.types>`:mod:.

    Example:

       >>> parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    '''
    from xotl.fl.parsers import type_parser, lexer
    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def find_tvars(t: Type) -> List[str]:
    '''Get all variables names (possibly repeated) in type `t`.

    Example:

       >>> find_tvars(Type.from_str('a -> b -> c -> a'))
       ['a', 'c', 'b', 'a']

    If `t` is (or contains a TypeScheme) its generics variables will be
    excluded (unless they're repeated):

       >>> find_tvars(Type.from_str('a -> [forall b. b] -> a'))
       ['a', 'a']

       >>> find_tvars(Type.from_str('[forall a. a] -> b -> a'))
       ['a', 'b']

    '''
    result: Deque[str] = deque([])
    queue: Deque[Type] = deque([t])
    generics: Deque[Set[str]] = deque([])
    POP_GENERICS: Type = None  # type: ignore
    while queue:
        t = queue.pop()
        if t is POP_GENERICS:
            generics.pop()
        elif isinstance(t, TypeVariable):
            skip = generics[-1] if generics else set()
            if t.name not in skip:
                result.append(t.name)
        elif isinstance(t, TypeScheme):
            if generics:
                current = generics[-1]
            else:
                current = set()
            generics.append(current | set(t.generics))
            queue.append(POP_GENERICS)
        elif isinstance(t, ConstrainedType):
            queue.append(t.type)
        else:
            assert isinstance(t, TypeCons)
            queue.extend(t.subtypes)
    return list(result)
