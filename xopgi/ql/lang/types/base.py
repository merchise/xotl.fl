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
from typing import List
from itertools import zip_longest
from collections import deque


class Type:
    pass


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
    def __init__(self, constructor: str, subtypes: List[Type] = None,
                 *, binary=False) -> None:
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
C = ConsType
TupleType = lambda *ts: ConsType('tuple', list(ts))
ListType = lambda t: ConsType('list', [t])
IntType = ConsType('int', [])


def parse(code):
    '''Parse the simplest type expressions.

    '''
    def take():
        tk = tokens.pop()
        if tk.isidentifier():
            if tk[0].isupper():
                stack[:] = [C(tk, stack[:])]
            else:
                stack.append(T(tk))
        return tk

    tokens = deque(code.split())
    stack = []
    while tokens:
        tk = take()
        if tk == '->':
            g = stack.pop()
            take()  # take the previous before '->' to create the Function
            f = stack.pop()
            stack.append(F(f, g))
    assert len(stack) == 1
    return stack[0]
