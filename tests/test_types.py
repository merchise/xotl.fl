#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest

from functools import partial
from ply import lex
from xoutil.fp.tools import compose

from xopgi.ql.lang.types import (
    TypeVariable as T,
    FunctionTypeCons as F,
    TypeCons as C,
)
from xopgi.ql.lang.types import parse
from xopgi.ql.lang.types.unification import scompose, subtype, delta, sidentity
from xopgi.ql.lang.types.unification import unify, UnificationError
from xopgi.ql.lang.expressions.typecheck import namesupply


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


def test_scompose_property():
    # subtype (scompose f g) = (subtype f) . (subtype g)
    f = delta('a', T, 'id')
    g = delta('b', T, 'bb')
    fog1 = partial(subtype, scompose(f, g))
    fog2 = compose(partial(subtype, f), partial(subtype, g))
    assert fog1(I) == fog2(I), f'{fog1(I)} != {fog2(I)}'
    assert fog1(K) == fog2(K), f'{fog1(K)} != {fog2(K)}'
    assert fog1(S) == fog2(S), f'{fog1(S)} != {fog2(S)}'


def test_namesupply():
    assert list(namesupply(limit=2, exclude='.a0')) == [T('.a1', check=False), T('.a2', check=False)]


def test_unify_basic_vars():
    t1 = T('a')
    t2 = T('b')
    unification = unify(sidentity, (t1, t2))
    assert subtype(unification, t1) == subtype(unification, t2)

    assert unification(t1.name) == t2
    assert unification(t2.name) != t1

    unification = unify(sidentity, (t2, t1))
    assert unification(t1.name) == unification(t2.name)


def test_unify_vars_with_cons():
    t1 = T('a')
    t2 = parse('x -> y')
    unification = unify(sidentity, (t1, t2))
    assert subtype(unification, t1) == subtype(unification, t2)
    unification = unify(sidentity, (t2, t1))
    assert subtype(unification, t1) == subtype(unification, t2)


def test_unify_cons():
    t1 = parse('a -> b -> c')
    t2 = parse('x -> y')
    unification = unify(sidentity, (t1, t2))
    assert subtype(unification, t1) == subtype(unification, t2)
    # TODO: dig in the result, 'unification' must make a = x, and (b -> c) = y
    with pytest.raises(UnificationError):
        unify(sidentity, (C('Int'), C('Num')))

    aa = I
    ab = parse('a -> b')
    ba = parse('b -> a')
    # 'b -> a' and 'a -> b' unify because we can do a = b.  Also 'a -> a' and
    # 'b -> a' for the same reason; notice that 'b -> a' does not imply
    # they must be different.
    unification = unify(sidentity, (ab, ba))
    assert subtype(unification, ab) == subtype(unification, ba)

    unification = unify(sidentity, (aa, ba))
    assert subtype(unification, aa) == subtype(unification, ba)

    # We can't unify 'Int -> b' with 'b -> Num', because b can't be both Int
    # and Num...
    with pytest.raises(UnificationError):
        unify(sidentity, (parse('Int -> b'), parse('b -> Num')))
    # But we can unify 'Int -> b' with 'b -> a'...
    unify(sidentity, (parse('Int -> b'), ba))


def test_parse_with_newlines():
    # I'm not sure if I should allow for newlines at any point.  This test
    # that we should not break before the arrow, but are allowed to break
    # after.  If you want to break before the arrow you must use parenthesis.
    with pytest.raises(lex.LexError):
        parse('a \n -> b')  # You can't just break the arrow like that!

    assert parse('a -> \n b') == parse('(a) \n -> b')
    assert parse('(a -> \n b -> c) \n -> (\n a -> b\n) -> \n a -> c') == S

    with pytest.raises(lex.LexError):
        parse('a \n b')  # You can't break application.
