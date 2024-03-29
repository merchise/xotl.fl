#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""The *type* objects of builtins types."""

import re

from xotl.fl.ast.types import (  # We need to import here because the AST imports the builtins UnitType
    ListTypeCons,
    TupleTypeCons,
    Type,
    TypeCons,
    TypeEnvironment,
    TypeScheme,
)
from xotl.tools.modules import moduleproperty

# This is the type of all numbers in our language.  The expression language
# will assign this type to every literal that matches a number; we don't
# really distinguish between floats and ints.  Even xotl.tools's concrete
# numbers will have this type.
NumberType = TypeCons("Number", [])


# We're going to assign the StringType to strings.  The internal value will be
# a normal Python string (in unicode).  The parser will take UTF-8 encoded
# strings.  The Char type is a single Unicode character.
CharType = TypeCons("Char", [])
StringType = ListTypeCons(CharType)


# The unit type is the type that its inhabited by a single value ``()``.
UnitType = TupleTypeCons()


BoolType = TypeCons("Bool", [])


DateType = TypeCons("Date", [])
DateTimeType = TypeCons("Datetime", [])
DateIntervalType = TypeCons("DateInterval")
DateTimeIntervalType = TypeCons("DateTimeInterval")


_gamma = None


@moduleproperty
def builtins_env(self) -> TypeEnvironment:
    global _gamma
    if _gamma is None:
        _gamma = _load_builtin_typeenv()
    return BuiltinEnvDict(_gamma)


TUPLE_CONS = re.compile(r",+")
EXTRACT_FROM_PRODUCT = re.compile(r":extract:(?P<type>.*):::")
EXTRACT_FROM_CONS = re.compile(r":extract:(?P<cons>[,\w]+)(:(?P<idx>\d+))?")


class BuiltinEnvDict(dict):
    """Type environment that contains type schemes for parser-available \
    identifiers.

    """

    def __init__(self, d=None, **kw):
        from xotl.fl.ast.types import TypeScheme
        from xotl.fl.match import MATCH_OPERATOR, NO_MATCH_ERROR, Extract, Match

        if not d:
            d = {}
        init = {
            # These can't be parsed (yet) and are really builtin -- their
            # values cannot be directly expressed in the language, even
            # though isomorphic types can be expressed, i.e 'data List a =
            # Nil | Cons a (List a)'.
            "[]": TypeScheme.from_str("[a]"),
            # There are special identifiers provided for translation of
            # pattern matching: The FATBAR (MATCH) operator; notice that
            # type-wise this is operator takes two arguments or equal type and
            # returns the first if it matches or the second.
            MATCH_OPERATOR.name: TypeScheme.from_str("a -> a -> a"),
            NO_MATCH_ERROR.name: TypeScheme.from_str("a"),
            # These are 'match' and 'extract' for lists pattern matching.
            Match("[]"): TypeScheme.from_str("[a] -> b -> b"),
            Extract(":", 1): TypeScheme.from_str("[a] -> ([a] -> b) -> b"),
            Extract(":", 2): TypeScheme.from_str("[a] -> ([a] -> b) -> b"),
            # Pattern matching requires 'extracting' the type from the Pattern
            # Cons.  These are dynamic and require knowledge from the locally
            # (program) defined types; we cannot provide the types here.
        }
        init.update(d)
        super().__init__(init, **kw)

    def __missing__(self, key) -> TypeScheme:
        from xotl.fl.ast.types import TypeVariable
        from xotl.fl.match import Extract, MatchLiteral
        from xotl.fl.utils import tvarsupply

        # Constructors of tuples are not fixed, since now you can have (1, 2,
        # 3..., 10000); that's a long tuple with a single constructor
        # (,,...,,); i.e 9999 commas.
        if isinstance(key, str) and TUPLE_CONS.match(key):
            items = len(key) + 1
            names = list(tvarsupply(limit=items))
            type: Type = TypeCons(key, names)
            for name in reversed(names):
                type = name >> type
            return TypeScheme.from_typeexpr(type)
        elif isinstance(key, Extract) and TUPLE_CONS.match(key.name):
            # The type of 'extract' for tuple varies with the number of
            # components of the tuple.  Example, for a triple, Extract(',,',
            # 2) -- i.e. extracting the second element; has the type scheme
            # 'forall a b c r. (a, b, c) -> (b -> r) -> r'.
            type_ = self[key.name].type_
            assert isinstance(type_, TypeCons)
            res = TypeVariable(".r", check=False)
            return TypeScheme.from_typeexpr(type_ >> ((type_.subtypes[key.arg - 1] >> res) >> res))
        elif isinstance(key, MatchLiteral):
            # The match has type 'a -> (a -> r) -> r'; where a is the type of
            # the literal.  We must ensure to generate a new variable not free
            # in type a.  Everywhere else we generate types '.a0', '.a1'.
            # Let's use '.r' as the result type.
            a = key.value.type_
            res = TypeVariable(".r", check=False)
            return TypeScheme.from_typeexpr(a >> ((a >> res) >> res))
        else:
            raise KeyError(key)  # pragma: no cover


def _load_builtins_program():
    import pkg_resources
    from xotl.fl import parse

    builtins = pkg_resources.resource_filename("xotl.fl", "builtins.fl")
    with open(builtins, "r", encoding="utf-8") as f:
        source = f.read()
    program = parse(source)
    return program


def _load_builtin_typeenv():
    from xotl.fl.ast.adt import DataType
    from xotl.fl.ast.typeclasses import TypeClass

    res = _load_builtins_program()
    gamma = {}
    # The strange dict(**gamma, **x) are there to catch duplicated annotations
    # that may cause trouble.
    for definition in res:
        if isinstance(definition, dict):
            duplicates = set(gamma) & set(definition)
            assert not duplicates, f"Duplicated type(s): {duplicates}"
            gamma.update(definition)
        elif isinstance(definition, DataType):
            duplicates = set(gamma) & set(definition.full_typeenv)
            assert not duplicates, f"Duplicated type(s): {duplicates}"
            gamma.update(definition.full_typeenv)
        elif isinstance(definition, TypeClass):
            duplicates = set(gamma) & set(definition.type_environment)
            assert not duplicates, f"Duplicated type(s): {duplicates}"
            gamma.update(definition.type_environment)
    return gamma


del re
