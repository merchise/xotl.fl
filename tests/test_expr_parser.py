#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from hypothesis import strategies as s, given

from xopgi.ql.lang.expressions import parse
from xopgi.ql.lang.expressions.base import Identifier, Literal

from xopgi.ql.lang.builtins import NumberType, CharType, StringType


def test_trivially_malformed():
    with pytest.raises(SyntaxError):
        parse('')


# wfe = well-formed expression
def test_wfe_identifier():
    assert parse('a') == parse('   a   ')
    assert parse('(a)') == parse('a')
    assert parse('a') == Identifier('a')


@given(s.characters())
def test_wfe_char_literals(ch):
    if ch == "'":
        code = r"'''"
    else:
        code = f"{ch!r}"
    assert parse(code) == Literal(ch, CharType)
