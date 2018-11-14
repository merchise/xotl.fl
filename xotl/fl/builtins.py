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

from .types import (
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
    return BuiltinEnv(_gamma)


TUPLE_CONS = re.compile(r',+')


class BuiltinEnv(dict):
    def __missing__(self, key):
        from xotl.fl.typecheck import namesupply
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


def _load_builtins():
    import pkg_resources
    from xotl.fl import parse
    from xotl.fl.types import TypeScheme
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
    gamma = {
        # These can't be parsed (yet) and are really builtin -- their values
        # cannot be directly expressed in the language, even though isomorphic
        # types can be expressed, i.e 'data List a = Nil | Cons a (List a)'.
        '[]': TypeScheme.from_str('[a]'),
    }
    for definition in res:
        if isinstance(definition, dict):
            gamma.update(definition)
        elif isinstance(definition, DataType):
            gamma.update(definition.implied_env)
    return gamma


def _strip_comment(line):
    if line.strip().startswith('--'):
        return '\n'  # leave an emtpy line
    else:
        return line


del re
