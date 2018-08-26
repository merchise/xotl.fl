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

    # I'm putting Left, Right and (,) not because they are necessarily
    # built-in; but to show that data constructors have the same type as
    # functions.
    #
    # However, there's no way you can't actually write those functions in the
    # expression language, because you would not be able to *build* the
    # values.  This reveals the need for a data type language would allow the
    # classical:
    #
    #    data Either a b = Left a | Right b
    #
    # and it would create the Left and Right functions.
    #
    # The case of tuples do require some parsing extensions if we're two allow
    # triplets, 4-tuples, etc..
    #
    # Notice however, we don't have any execution model in the language and no
    # real values beyond what literals allow.  I presume that we will use
    # Python values while executing; but that would have to revised in order
    # to make non-strict Python referentially transparent.
    #
    ',': TypeScheme.from_str('a -> b -> Tuple a b'),
    ',,': TypeScheme.from_str('a -> b -> c Tuple a b c'),
    ',,,': TypeScheme.from_str('a -> b -> c -> d -> Tuple a b c d'),
    ',,,,': TypeScheme.from_str('a -> b -> c -> d -> e -> Tuple a b c d e'),
    ',,,,,': TypeScheme.from_str('a -> b -> c -> d -> e -> f -> Tuple a b c d e f'),

    'Left': TypeScheme.from_str('a -> Either a b'),
    'Right': TypeScheme.from_str('b -> Either a b'),
    'either': TypeScheme.from_str('(a -> c) -> (b -> c) -> Either a b -> c'),


    'Nothing': TypeScheme.from_str('Maybe a'),
    'Just': TypeScheme.from_str('a -> Maybe a'),
    'maybe': TypeScheme.from_str('a -> (a -> b) -> Maybe a -> b'),
    'isJust': TypeScheme.from_str('Maybe a -> Bool'),
    'isNothing': TypeScheme.from_str('Maybe a -> Bool'),
    'fromMaybe': TypeScheme.from_str('a -> Maybe a -> a'),

    # Common operations on lists.

    'head': TypeScheme.from_str('[a] -> a'),
    'tail': TypeScheme.from_str('[a] -> [a]'),
    'single': TypeScheme.from_str('a -> [a]'),

    'safe_head': TypeScheme.from_str('[a] -> Maybe a'),
    'safe_tail': TypeScheme.from_str('[a] -> Maybe [a]'),

    'nil': TypeScheme.from_str('[a]'),
    'append': TypeScheme.from_str('a -> [a] -> [a]'),
    'insert': TypeScheme.from_str('a -> [a] -> [a]'),

    'is_member': TypeScheme.from_str('a -> [a] -> Bool'),
    'is_null': TypeScheme.from_str('[a] -> Bool'),

    '++': TypeScheme.from_str('[a] -> [a] -> [a]'),

    'pair': TypeScheme.from_str('a -> b -> Tuple a b'),
    'fst': TypeScheme.from_str('Tuple a b -> a'),
    'snd': TypeScheme.from_str('Tuple a b -> b'),

    # Date operations.  It's quite evident that I will need type-classes and
    # instances; otherwise, writing the simplest formulae may get really
    # involved.
    'date_to_datetime': TypeScheme.from_str('Date -> DateTime'),
    'is_earlier': TypeScheme.from_str('DateTime -> DateTime -> Bool'),
    'is_later': TypeScheme.from_str('DateTime -> DateTime -> Bool'),

    'interval_overlap': TypeScheme.from_str(
        'DateInterval -> DateInterval -> DateInterval'
    ),
    'is_fully_contained': TypeScheme.from_str('DateInterval -> DateInterval -> Bool'),
    'is_interval_empty': TypeScheme.from_str('DateInterval -> Bool'),
    'interval': TypeScheme.from_str('Maybe Date -> Maybe Date -> DateInterval'),
}

for op in '+-*/%^':
    gamma[op] = TypeScheme.from_str('Number -> Number -> Number')


for op in ('==', '!='):
    gamma[op] = TypeScheme.from_str('a -> a -> Bool')


for op in ('<', '>', '<=', '>='):
    gamma[op] = TypeScheme.from_str('a -> a -> Bool')


builtins_env = list(gamma.items())
