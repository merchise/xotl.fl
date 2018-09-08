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
from typing import Iterable, Sequence
from itertools import zip_longest


class AST:
    pass


class Type(AST):
    @classmethod
    def from_str(cls, source):
        '''Parse a single type expression `code`.

        Return a `type expression AST <xopgi.ql.lang.types.base>`:mod:.

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


#: Shortcut to create function types
FunctionTypeCons = lambda a, b: TypeCons('->', [a, b], binary=True)

#: Shortcut to create a tuple type from types `ts`.  The Unit type can be
#: regarded as the tuple type without arguments.
TupleTypeCons = lambda *ts: TypeCons('Tuple', list(ts))

#: Shortcut to create a list type from type `t`.
ListTypeCons = lambda t: TypeCons('[]', [t])


def parse(code: str, debug=False, tracking=False) -> Type:
    '''Parse a single type expression `code`.

    Return a `type expression AST <xopgi.ql.lang.types.base>`:mod:.

    Example:

       >>> parse('a -> b')
       TypeCons('->', (TypeVariable('a'), TypeVariable('b')))

    '''
    from .parsers import type_parser, lexer
    return type_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)
