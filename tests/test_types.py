#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from xotl.fl.types import (
    TypeVariable as T,
    FunctionTypeCons as F,
    TypeCons as C,
    ListTypeCons,
)
from xotl.fl.types import parse
from xotl.fl.typecheck import namesupply


# The id function type
I = parse('a -> a')
assert I == F(T('a'), T('a'))


# The K combinator: a -> b -> a
K = parse('a -> b -> a')
assert K == F(T('a'), F(T('b'), T('a')))
assert K == parse('a -> (b -> a)')


# The S combinator: Lx Ly Lz. x z (y z)
S = parse('(a -> b -> c) -> (a -> b) -> a -> c')
assert S == F(
    F(T('a'), parse('b -> c')),
    F(F(T('a'), T('b')), parse('a -> c'))
)


def test_namesupply():
    assert list(namesupply(limit=2, exclude='.a0')) == [
        T('.a1', check=False),
        T('.a2', check=False)
    ]


def test_parse_with_newlines():
    # I'm not sure if I should allow for newlines at any point.  This test
    # that we should not break before the arrow, but are allowed to break
    # after.  If you want to break before the arrow you must use parenthesis.
    with pytest.raises(Exception):
        parse('a \n -> b')  # You can't just break the arrow like that!

    assert parse('a -> \n b') == parse('a -> b')
    assert parse('(a -> \n b -> c) -> (\n a -> b\n ) -> \n a -> c') == S

    with pytest.raises(Exception):
        parse('a \n b')  # You can't break application.


def test_parse_of_listtypes():
    P = parse
    assert P('[a]') == ListTypeCons(parse('a'))
    assert P('(a -> b) -> [a] -> [b]') == F(
        parse('(a -> b)'),
        F(ListTypeCons(T('a')), ListTypeCons(T('b')))
    )
    assert P('[a -> b]') == ListTypeCons(F(T('a'), T('b')))


def test_parse_application():
    assert parse('a (f b)') == C('a', [C('f', [T('b')])])
    assert parse('A (B b) (C c)') == C('A', [C('B', [T('b')]),
                                             C('C', [T('c')])])

    # Is this ok?
    assert parse('(f b) a') == parse('f b a')
