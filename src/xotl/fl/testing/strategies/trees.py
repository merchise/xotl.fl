#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Strategies to generate expressions.

I got the idea from a `comment`__ in a Hypothesis issue about generating
source-code from lark grammar specifications.  However, these strategies
generate the AST nodes directly, but the strategies themselves resemble the
grammar.

We provide two sets of strategies: one for well-typed programs, and the other
for programs which may contain type errors.  By default, each non-explicitly
marked ill-typed strategy is type-safe.  So 'expressions' is the same as
'welltyped_expressions' whereas 'maybe_unsafe_applications' generates
instances of Application which may or may not be well-typed.

__ https://github.com/HypothesisWorks/hypothesis/issues/1804#issuecomment-552047942

"""

from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy
from xotl.fl.ast.base import AST
from xotl.fl.ast.expressions import (
    Application,
    Identifier,
    Literal,
    build_application,
    build_lambda,
)
from xotl.fl.builtins import CharType, DateTimeType, DateType, NumberType, StringType
from xotl.fl.utils import namesupply

from .tools import builds

welltyped_expressions: SearchStrategy[AST] = st.deferred(
    lambda: identifiers | literals | welltyped_applications
)
expressions = welltyped_expressions

LOWER_IDENTIFIERS = st.from_regex(r"[a-z][\w_]*")
UPPER_IDENTIFIERS = st.from_regex(r"[A-Z][\w_]*")
UNDER_IDENTIFIERS = st.from_regex(r"_[\w_]*")
_idenfifiers = LOWER_IDENTIFIERS | UPPER_IDENTIFIERS | UNDER_IDENTIFIERS

lower_identifiers: SearchStrategy[Identifier] = st.builds(Identifier, name=LOWER_IDENTIFIERS)
upper_identifiers: SearchStrategy[Identifier] = st.builds(Identifier, name=UPPER_IDENTIFIERS)
under_identifiers: SearchStrategy[Identifier] = st.builds(Identifier, name=UNDER_IDENTIFIERS)
identifiers: SearchStrategy[Identifier] = lower_identifiers


# TODO: Include intervals, check Date and DateTime representation (am I going
# to use Python's date and datetime or go with a product-type value:
# data Date= Date Int Int Int)
literals: SearchStrategy[Literal] = st.deferred(
    lambda: numbers | concrete_numbers | strings | chars | dates | datetimes
)

_numbers = st.integers() | st.floats(allow_infinity=False, allow_nan=False)
numbers: SearchStrategy[Literal] = st.builds(Literal, value=_numbers, type_=st.just(NumberType))
concrete_numbers: SearchStrategy[Literal] = st.builds(
    Literal, value=_numbers, type_=st.just(NumberType), annotation=_idenfifiers
)

strings: SearchStrategy[Literal] = st.builds(Literal, value=st.text(), type_=st.just(StringType))
chars: SearchStrategy[Literal] = st.builds(Literal, value=st.characters(), type_=st.just(CharType))
dates: SearchStrategy[Literal] = st.builds(Literal, value=st.dates(), type_=st.just(DateType))
datetimes: SearchStrategy[Literal] = st.builds(
    Literal, value=st.datetimes(), type_=st.just(DateTimeType)
)


_apps_args = st.lists(expressions, min_size=2, max_size=100)

maybe_unsafe_applications: SearchStrategy[Application] = _apps_args.map(
    lambda args: build_application(*args)
)


@builds(_apps_args)
def welltyped_applications(args) -> Application:
    # To make this well-typed we simply create:
    #   (\_anonN -> ...  (\_anon2 -> (\_anon1 -> e1) e2) e3...) eN
    #
    anonymous_names = namesupply(prefix="_anon")
    result, *exprs = args
    for expr in exprs:
        result = build_application(build_lambda(next(anonymous_names), result), expr)
    return result
