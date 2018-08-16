#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''The *type* objects of builtins types.

'''
from .types.base import TypeCons, ListTypeCons, TupleTypeCons
from .typecheck import TypeScheme

# This is the type of all numbers in our language.  The expression language
# will assign this type to every literal that matches a number; we don't
# really distinguish between floats and ints.  Even xoutil's concrete numbers
# will have this type.
NumberType = TypeCons('Number', [])


# We're going to assign the StringType to strings.  The internal value will be
# a normal Python string (in unicode).  The parser will take UTF-8 encoded
# strings.  The Char type is a single Unicode character.
CharType = TypeCons('Char', [])
StringType = ListTypeCons(CharType)


# The unit type is the type that its inhabited by a single value ``()``.
UnitType = TupleTypeCons()


BoolType = TypeCons('Bool', [])


DateType = TypeCons('Date', [])
DateTimeType = TypeCons('Datetime', [])
DateIntervalType = TypeCons('DateInterval')
DateTimeIntervalType = TypeCons('DateTimeInterval')


gamma = {
    '$': TypeScheme.from_str('(a -> b) -> a -> b'),
    '.': TypeScheme.from_str('(b -> c) -> (a -> b) -> a -> c'),

    'id': TypeScheme.from_str('a -> a'),
    'map': TypeScheme.from_str('(a -> b) -> [a] -> [b]'),
    'foldr': TypeScheme.from_str('(a -> b -> b) -> b -> [a] -> b'),

    'and': TypeScheme.from_str('Bool -> Bool -> Bool'),
    'or': TypeScheme.from_str('Bool -> Bool -> Bool'),
    'xor': TypeScheme.from_str('Bool -> Bool -> Bool'),
    'not': TypeScheme.from_str('Bool -> Bool'),

    'true': TypeScheme.from_typeexpr(BoolType),
    'false': TypeScheme.from_typeexpr(BoolType),

    '//': TypeScheme.from_str('Number -> Number -> Number'),
}

for op in '+-*/%^':
    gamma[op] = TypeScheme.from_str('Number -> Number -> Number')


for op in ('==', '!='):
    gamma[op] = TypeScheme.from_str('Eq a -> Eq a -> Bool')


for op in ('<', '>', '<=', '>='):
    gamma[op] = TypeScheme.from_str('Ord a -> Ord a -> Bool')


builtins_env = list(gamma.items())
