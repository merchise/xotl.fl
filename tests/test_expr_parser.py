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

from ply import lex

from xopgi.ql.lang.expressions import parse, tokenize
from xopgi.ql.lang.expressions.base import (
    Identifier,
    Literal,
    Application,
    Lambda,
)
from xopgi.ql.lang.expressions.parser import string_repr

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


@given(s.text())
def test_wfe_string_literals(s):
    code = string_repr(s)
    assert parse(code) == Literal(s, StringType)


@given(s.integers())
def test_wfe_integer_literals(i):
    code = str(i)
    assert parse(code) == Literal(i, NumberType)

    code = hex(i)
    assert parse(code) == Literal(i, NumberType)

    code = bin(i)
    assert parse(code) == Literal(i, NumberType)

    code = oct(i)
    assert parse(code) == Literal(i, NumberType)


@given(s.integers(), s.integers(min_value=0))
def test_wfe_integer_literals_with_under(i, g):
    code = str(i) + '__' + str(g) + '_'
    value = eval(str(i) + str(g) if i else str(g))
    assert parse(code) == Literal(value, NumberType)

    code = hex(i) + '__' + hex(g)[2:] + '_'
    value = eval(hex(i) + hex(g)[2:] if i else hex(g))
    assert parse(code) == Literal(value, NumberType)

    code = oct(i) + '__' + oct(g)[2:] + '_'
    value = eval(oct(i) + oct(g)[2:] if i else oct(g))
    assert parse(code) == Literal(value, NumberType)

    code = bin(i) + '__' + bin(g)[2:] + '_'
    value = eval(bin(i) + bin(g)[2:] if i else bin(g))
    assert parse(code) == Literal(value, NumberType)


@given(s.floats(allow_nan=False, allow_infinity=False))
def test_wfe_float_literals(n):
    code = f'{n!r:.60}'
    assert parse(code) == Literal(n, NumberType)

    assert parse('1_000_.500') == Literal(1000.5, NumberType)
    with pytest.raises(lex.LexError):
        tokenize('_1e+10')
    with pytest.raises(lex.LexError):
        tokenize('_0.1')


def test_wfe_application():
    assert parse('a b') == Application(Identifier('a'), Identifier('b'))
    assert parse('a b c') == parse('(a b) c')
    assert parse('(a)(b)') == parse('(a)b') == parse('a(b)') == parse('a b')
    assert parse('a b') == parse('(a b)')


def test_wfe_composition():
    assert parse('a . b') == parse('(.) a b') == Application(
        Application(Identifier('.'), Identifier('a')),
        Identifier('b')
    )
    assert parse('a . b . c') == parse('a . (b . c)')

    # yay! partial application
    assert parse('((.) a) b') == parse('a . b')
    assert parse('(.)a') == Application(Identifier('.'), Identifier('a'))

    # Application is stronger than composition
    assert parse('a . b c') == parse('a . (b c)')


def test_wfe_infix_func():
    assert parse('a `f` b') == parse('f a b')
    assert parse('a `add` b `mul` c') == parse('mul (add a b) c')

    assert parse('a . b `f` c') == parse('(a . b) `f` c')


@pytest.mark.xfail(reason='programming error')
def test_wfe_infix_func_precedence():
    # The actual result is '(++) a (f b c)' which is kind of weird since
    # 'a ++' is not a well formed expression.  Investigate.
    assert parse('a ++ b `f` c') == parse('(a ++ b) `f` c')

    assert parse('a + b `f` c') == parse('(a + b) `f` c')


@given(s.text(alphabet='@!<>$+-^/', min_size=1))
def test_user_operators(op):
    assert parse(f'a {op} b') == parse(f'({op}) a b') == Application(
        Application(Identifier(op), Identifier('a')),
        Identifier('b')
    )


def test_annotated_numbers():
    assert parse('1e+10@km') == Literal(1e+10, NumberType, Identifier('km'))
    assert parse('1e+10@"km"') == Literal(1e+10, NumberType, Literal('km', StringType))
    assert parse("1e+10@'m'") == Literal(1e+10, NumberType, Literal('m', CharType))

    assert parse('1e+10 @ km') == Application(
        Application(Identifier('@'), Literal(1e+10, NumberType)),
        Identifier('km')
    )

    assert parse('a @ b') == Application(
        Application(Identifier('@'), Identifier('a')),
        Identifier('b')
    )


def test_lambda_definition():
    P = parse
    assert P(r'\a -> a') == Lambda('a', Identifier('a'))
    assert P(r'\a b -> a') == P(r'\a -> \b -> a') == P(r'\a -> (\b -> a)')
    assert P(r'\a b -> a') == Lambda('a', Lambda('b', Identifier('a')))


@pytest.mark.xfail(reason='programming error')
def test_incorrect_lepexpr_assoc():
    P = parse
    with pytest.raises(AssertionError):
        assert P('let id x = x in map id xs') == P('(let id x = x in map) id xs')


@pytest.mark.xfail(reason='programming error')
def test_letbasic_letexpr():
    P = parse
    assert P('let id x = x in map id xs') == P('let id x = x in (map id xs)')
