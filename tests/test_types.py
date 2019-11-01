#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from textwrap import dedent

from xotl.fl.ast.types import (
    TypeVariable as T,
    FunctionTypeCons as F,
    TypeCons as C,
    ListTypeCons,
    ConstrainedType,
    TypeConstraint,
)
from xotl.fl.parsers.larkish import type_expr_parser
from xotl.fl.parsers import ParserError

from xotl.fl.utils import tvarsupply


def parse(source):
    return type_expr_parser.parse(dedent(source).strip())


# The id function type
I = parse("a -> a")


def test_i_combinator():
    assert I == F(T("a"), T("a"))


# The K combinator: a -> b -> a
K = parse("a -> b -> a")


def test_k_combinator():
    assert K == F(T("a"), F(T("b"), T("a")))
    assert K == parse("a -> (b -> a)")


# The S combinator: Lx Ly Lz. x z (y z)
S = parse("(a -> b -> c) -> (a -> b) -> a -> c")


def test_s_combinator():
    assert S == F(F(T("a"), parse("b -> c")), F(F(T("a"), T("b")), parse("a -> c")))


def test_tvarsupply():
    assert list(tvarsupply(".a", limit=2, exclude=".a0")) == [
        T(".a1", check=False),
        T(".a2", check=False),
    ]


def test_parse_with_newlines():
    # I'm not sure if I should allow for newlines at any point.  This test
    # that we should not break before the arrow, but are allowed to break
    # after.  If you want to break before the arrow you must use parenthesis.
    with pytest.raises(Exception):
        parse("a \n -> b")  # You can't just break the arrow like that!

    assert parse("a -> \n b") == parse("a -> b")
    assert parse("(a -> \n b -> c) -> (\n a -> b\n ) -> \n a -> c") == S

    with pytest.raises(Exception):
        parse("a \n b")  # You can't break application.


def test_parse_of_listtypes():
    P = parse
    assert P("[a]") == ListTypeCons(parse("a"))
    assert P("(a -> b) -> [a] -> [b]") == F(
        parse("(a -> b)"), F(ListTypeCons(T("a")), ListTypeCons(T("b")))
    )
    assert P("[a -> b]") == ListTypeCons(F(T("a"), T("b")))


def test_parse_application():
    assert parse("a (f b)") == C("a", [C("f", [T("b")])])
    assert parse("A (B b) (C c)") == C("A", [C("B", [T("b")]), C("C", [T("c")])])

    # Is this ok?
    assert parse("(f b) a") == parse("f b a")


def test_valid_constraints():
    assert parse("Eq a => a -> a -> Bool") == ConstrainedType(
        ("a",), parse("a -> a -> Bool"), [TypeConstraint("Eq", T("a"))]
    )
    assert parse("Eq a, Ord a => a -> a -> Bool") == ConstrainedType(
        ("a",),
        parse("a -> a -> Bool"),
        [TypeConstraint("Eq", T("a")), TypeConstraint("Ord", T("a"))],
    )


def test_invalid_constraints():

    with pytest.raises(TypeError):
        parse("Eq c => a")

    with pytest.raises(ParserError):
        parse("Eq a, Ord a -> a => Bool")
