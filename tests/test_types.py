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
from xoutil.fp.tools import compose


from xopgi.ql.lang.types import (
    TypeVariable as T,
    FunctionType as F,
    ConsType as C,
)
from xopgi.ql.lang.types.unification import scompose, subtype, delta, sidentity
from xopgi.ql.lang.types.unification import unify, UnificationError, parse
from xopgi.ql.lang.types.typecheck import genvars


# The id function type
I = parse('a -> a')
assert I == F(T('a'), T('a'))


# The K combinator: a -> b -> a
K = parse('a -> b -> a')
assert K == F(T('a'), F(T('b'), T('a')))


# parse doesn't support this type
# The S combinator: Lx Ly Lz. x z (y z)
# (a -> b -> c) -> (a -> b) -> b -> c
bc = F(T('b'), T('c'))
S = F(
    F(T('a'), bc),
    F(F(T('a'), T('b')), bc)
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


def test_genvars():
    assert list(genvars(limit=2)) == [T('.a0', check=False), T('.a1', check=False)]


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
