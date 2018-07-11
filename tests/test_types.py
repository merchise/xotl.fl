#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from functools import partial
from xoutil.fp.tools import compose

from xopgi.ql.lang.types import TypeVariable as T, FunctionType as F
from xopgi.ql.lang.types import scompose, subtype, delta
from xopgi.ql.lang.types.typecheck import genvars


# The id function type
I = F(T('a'), T('a'))


# The K combinator: a -> b -> a
K = F(T('a'), F(T('b'), T('a')))


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
