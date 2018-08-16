#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

import pytest

from xopgi.ql.lang.builtins import (
    NumberType,
    CharType,
    StringType,
    BoolType,
    UnitType,

    builtins_env,
)
from xopgi.ql.lang.expressions import parse
from xopgi.ql.lang.types import parse as type_parse

from xopgi.ql.lang.typecheck import (
    typecheck,
    namesupply,
    sidentity,
    TypeScheme,
    unify,
)


def test_from_literals():
    phi, t = typecheck([], namesupply(), parse(r'let x = 1 in x'))
    assert phi is sidentity
    assert t == NumberType

    phi, t = typecheck([], namesupply(), parse(r'let x = "1" in x'))
    assert phi is sidentity
    assert t == StringType

    phi, t = typecheck([], namesupply(), parse(r"let x = '1' in x"))
    assert phi is sidentity
    assert t == CharType

    # true and false are not recognized as booleans by the parser, so let's
    # provide them as part the env.
    phi, t = typecheck(builtins_env, namesupply(),
                       parse(r"let x = true in x"))
    assert phi is sidentity
    assert t == BoolType

    phi, t = typecheck(builtins_env, namesupply(),
                       parse(r"let x = false in x"))
    assert phi is sidentity
    assert t == BoolType


def test_combinators():
    # Since they're closed expressions they should type-check
    K = parse(r'\a b -> a')
    TK = type_parse('a -> b -> a')
    phi, t = typecheck([], namesupply(), K)
    unify(TK, t)  # we can't ensure TK == t, but they must unify, in fact they
                  # must be same type with alpha-renaming.

    S = parse(r'\x y z -> x z (y z)')
    TS = type_parse('(a -> b -> c) -> (a -> b) -> a -> c')
    phi, t = typecheck([], namesupply(), S)
    unify(TS, t)

    # But the paradoxical combinator doesn't type-check
    Y = parse(r'\f -> (\x -> f (x x))(\x -> f (x x))')
    phi, t = typecheck([], namesupply(), Y)


def test_paradox_omega():
    r'Test `(\x -> x x)` does not type-check'
    with pytest.raises(TypeError):
        typecheck([], namesupply(), parse(r'\x -> x x'))


@pytest.mark.xfail(reason='I have not complete the letrec')
def test_hidden_paradox_omega():
    code = '''
    let id x    = x
        prxI c  = c x id
        p1 x y  = x
        p2 x y  = y
    in prxI p2 (prxI p2)
    '''
    typecheck([('x', TypeScheme.from_str('a', generics=[]))],
              namesupply(), parse(code))
