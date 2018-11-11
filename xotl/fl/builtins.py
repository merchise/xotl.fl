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
import re
from xoutil.modules import moduleproperty

from xotl.fl.types import (
    Type,
    TypeScheme,
    TypeCons,
    ListTypeCons,
    TupleTypeCons,
    TypeEnvironment,
)


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


_gamma = None


@moduleproperty
def builtins_env(self) -> TypeEnvironment:
    global _gamma
    if _gamma is None:
        _gamma = _load_builtins()
    return BuiltinEnvDict(_gamma)


TUPLE_CONS = re.compile(r',+')
EXTRACT_FROM_PRODUCT = re.compile(r':extract:(?P<type>.*):::')
EXTRACT_FROM_CONS = re.compile(r':extract:(?P<cons>[,\w]+)(:(?P<idx>\d+))?')


class BuiltinEnvDict(dict):
    def __init__(self, d=None, **kw):
        from xotl.fl.types import TypeScheme
        from xotl.fl.expressions import NO_MATCH_ERROR, MATCH_OPERATOR
        from xotl.fl.expressions import Match, Extract
        if not d:
            d = {}
        init = {
            # These can't be parsed (yet) and are really builtin -- their
            # values cannot be directly expressed in the language, even
            # though isomorphic types can be expressed, i.e 'data List a =
            # Nil | Cons a (List a)'.
            '[]': TypeScheme.from_str('[a]'),

            # There are special identifiers provided for translation of pattern
            # matching:  The FATBAR (MATCH) operator; notice that type-wise this
            # is operator takes two arguments or equal type and returns the first
            # if it matches or the second.
            MATCH_OPERATOR.name: TypeScheme.from_str('a -> a -> a'),
            NO_MATCH_ERROR.name: TypeScheme.from_str('a'),

            # These are 'match' and 'extract' for lists pattern matching.
            Match('[]'): TypeScheme.from_str('[a]'),
            Extract(':', 1): TypeScheme.from_str('[a] -> a'),
            Extract(':', 2): TypeScheme.from_str('[a] -> [a]'),

            # Pattern matching requires 'extracting' the type from the Pattern
            # Cons.  These are dynamic are require knowledge from the locally
            # (program) defined types; we cannot provide the types here.
        }
        init.update(d)
        super().__init__(init, **kw)

    def __missing__(self, key):
        from xotl.fl.utils import namesupply
        # Constructors of tuples are not fixed, since now you can have (1, 2,
        # 3..., 10000); that's a long tuple with a single constructor
        # (,,...,,); i.e 9999 commas.
        if TUPLE_CONS.match(key):
            items = len(key) + 1
            names = list(namesupply(limit=items))
            type: Type = TypeCons(key, names)
            for name in reversed(names):
                type = name >> type
            self[key] = result = TypeScheme.from_typeexpr(type)
            return result
        else:
            raise KeyError(key)


def _load_builtins():
    import pkg_resources
    from xotl.fl import parse
    from xotl.fl.expressions import DataType
    builtins = pkg_resources.resource_filename('xotl.fl', 'builtins.fl')
    with open(builtins, 'r') as f:
        code = f.read()
    # I have to remove comments my self because the parser doesn't have
    # comments.  But I do it line by line.
    source = [
        line
        for source_line in code.split('\n')
        for line in (_strip_comment(source_line), )
        if line
    ]
    res = parse('\n'.join(source))
    gamma = {}
    for definition in res:
        if isinstance(definition, dict):
            gamma.update(definition)
        elif isinstance(definition, DataType):
            gamma.update(definition.full_typeenv)
    return gamma


def _strip_comment(line):
    if line.strip().startswith('--'):
        return '\n'  # leave an emtpy line
    else:
        return line


del re
