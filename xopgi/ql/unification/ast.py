#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Optional as Option, List


class Term:
    'Base class of the nodes in the AST.'  # Nothing really interesting here
    def __eq__(self, other):
        return NotImplemented


class Variable(Term):
    '''A variable in the AST.

    The two kinds of variables: named and anonymous.  Anonymous variables
    ignore the name::

       >>> Variable('x', anon=True).name is None
       True

    An anonymous variable is only equal to itself:

       >>> _x = Variable('x', anon=True)
       >>> _x1 = Variable('x', anon=True)
       >>> _x == _x1
       False

       >>> _x == _x
       True

    Named variables are equal by name (case-sensitive):

      >>> Variable('x') == Variable('x')
      True

      >>> Variable('x') == Variable('X')
      False

    '''
    def __init__(self, name: Option[str], anon: bool = False) -> None:
        self.name = name if not anon else id(self)
        self.anon = anon

    def __eq__(self, other):
        if isinstance(other, Variable):
            if self.anon or other.anon:
                return self is other
            else:
                return self.name == other.name
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        if self.anon:
            return f'_{id(self)}'
        else:
            return f'{self.name}'

    def __repr__(self):
        return f'<Var({str(self)!r})>'


Var = Variable


class Literal(Term):
    '''A literal term.

    Literals are opaque terms which only unify with themselves
    (lexicographic).  The `payload` CAN be anything that's hashable and
    supports equality.  Two literals are equal iff their payloads are.

    '''
    def __init__(self, payload):
        self.payload = payload

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.payload == other.payload
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.payload)

    def __repr__(self):
        return f'<Literal({self.payload!r})>'


class Function(Term):
    '''A function call pattern.

    The `args` are just the terms each instance calls.

    Two functions are the same if they have the same name and arity regardless
    of the contents of the arguments:

      >>> goh = Function('compose', [Literal('g'), Literal('h')])
      >>> fog = Function('compose', [Literal('f'), Literal('g')])
      >>> foh == fog
      True

    Notice equality is NOT unification.  It just states both call patterns use
    the same function.

    Unification depends on the arguments.

    '''
    def __init__(self, name: str, args: List[Term]) -> None:
        assert all(isinstance(arg, Term) for arg in args)
        self.name = name
        self.args = args

    @property
    def arity(self):
        return len(self.args)

    def __eq__(self, other):
        # functions with the same name and arity are the same, the arguments
        # must be unified.
        if isinstance(other, Function):
            return self.name == other.name and self.arity == other.arity
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.name, self.arity))

    def __repr__(self):
        if self.arity > 0:
            return f'<Function({self.name!r}, {self.args!r})>'
        else:
            return f'<Function({self.name!r})>'
