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

from xopgi.ql.lang.typecheck import (
    typecheck,
    namesupply,
    sidentity,
    TypeScheme,
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
