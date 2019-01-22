#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from hypothesis import strategies as s, given, example, assume

from ply import lex

from xotl.fl import tokenize
from xotl.fl.expressions import parse
from xotl.fl.expressions import (
    Identifier,
    Literal,
    Application,
    Lambda,
    Let,
    Letrec,
    find_free_names,
)
from xotl.fl.parsers import string_repr, ParserError
from xotl.fl.builtins import (
    NumberType,
    CharType,
    StringType,
    UnitType,
    DateType,
    DateTimeType,
    DateIntervalType,
)


def test_trivially_malformed():
    with pytest.raises(ParserError):
        parse('')


# wfe = well-formed expression
def test_wfe_identifier():
    assert parse('a') == parse('   a   ')
    assert parse('(a)') == parse('a')
    assert parse('a') == Identifier('a')


@given(s.characters())
@example(r"'")
def test_wfe_char_literals(ch):
    if ch == "'":
        code = r"'\''"
    else:
        code = f"{ch!r}"
    assert parse(code) == Literal(ch, CharType)


@given(s.text())
@example(r'"\\"')
def test_wfe_string_literals(s):
    code = string_repr(s)
    assert parse(code) == Literal(s, StringType)


@given(s.integers())
def test_wfe_integer_literals_base10(i):
    code = str(i)
    assert parse(code) == Literal(i, NumberType)


@given(s.integers())
def test_wfe_integer_literals_base16(i):
    code = hex(i)
    assert parse(code) == Literal(i, NumberType)


@given(s.integers())
def test_wfe_integer_literals_base2(i):
    code = bin(i)
    assert parse(code) == Literal(i, NumberType)


@given(s.integers())
def test_wfe_integer_literals_base8(i):
    code = oct(i)
    assert parse(code) == Literal(i, NumberType)


@given(s.integers(), s.integers(min_value=0))
def test_wfe_integer_literals_with_under_base10(i, g):
    code = str(i) + '__' + str(g) + '_'
    value = eval(str(i) + str(g) if i else str(g))
    assert parse(code) == Literal(value, NumberType)


@given(s.integers(), s.integers(min_value=0))
def test_wfe_integer_literals_with_under_base16(i, g):
    code = hex(i) + '__' + hex(g)[2:] + '_'
    value = eval(hex(i) + hex(g)[2:] if i else hex(g))
    assert parse(code) == Literal(value, NumberType)


@given(s.integers(), s.integers(min_value=0))
def test_wfe_integer_literals_with_under_base8(i, g):
    code = oct(i) + '__' + oct(g)[2:] + '_'
    value = eval(oct(i) + oct(g)[2:] if i else oct(g))
    assert parse(code) == Literal(value, NumberType)


@given(s.integers(), s.integers(min_value=0))
def test_wfe_integer_literals_with_under_base2(i, g):
    code = bin(i) + '__' + bin(g)[2:] + '_'
    value = eval(bin(i) + bin(g)[2:] if i else bin(g))
    assert parse(code) == Literal(value, NumberType)


@given(s.floats(allow_nan=False, allow_infinity=False))
def test_wfe_float_literals(n):
    code = f'{n!r:.60}'
    assert parse(code) == Literal(n, NumberType)

    assert parse('1_000_.500') == Literal(1000.5, NumberType)
    assert parse('_1e+10') == Application(
        Application(Identifier('+'), Identifier('_1e')),
        Literal(10, NumberType)
    )
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


def test_wfe_infix_func_precedence():
    assert parse('a ++ b `f` c') == parse('(a ++ b) `f` c')


def test_wfe_infix_func_precedence2():
    assert parse('a + b `f` c') == parse('(a + b) `f` c')


@given(s.text(alphabet='@!<>$+-^/', min_size=1))
def test_user_operators(op):
    assume(not op.startswith('--'))
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


@pytest.mark.xfail(reason='Incomplete pattern matching')
def test_basic_letexpr():
    P = parse
    assert P('let id x = x in map id xs') == P('let id x = x in (map id xs)')
    assert isinstance(P('let id x = x in id'), Let)

    code = '''
    let id x    = x
        prxI c  = c x id
        p1 x y  = x
        p2 x y  = y
    in prxI p2 (prxI p2)
    '''
    Id = Identifier
    App = Application
    L = Lambda
    assert isinstance(parse(code), Letrec)
    assert parse(code) == Letrec(
        {'id': L('x', Id('x')),
         'prxI': L('c', App(App(Id('c'), Id('x')), Id('id'))),
         'p1': L('x', L('y', Id('x'))),
         'p2': L('x', L('y', Id('y')))},
        App(
            App(Id('prxI'), Id('p2')),
            App(Id('prxI'), Id('p2'))
        )
    )


def test_nested_let():
    Id = Identifier
    App = Application
    L = Lambda
    code = '''
    let f1 = x1 x2 x3
        f2 = let g1 = y1 in f1 g1
        f3 = let g2 = y2
                 g3 = g2 y3
             in f2 g3
    in f3
    '''

    assert parse(code) == parse('''
    let f1 = x1 x2 x3
        f2 = (let g1 = y1 in f1 g1)
        f3 = (let g2 = y2
                  g3 = g2 y3
              in f2 g3)
    in f3
    ''') == Letrec(
        {'f1': App(App(Id('x1'), Id('x2')), Id('x3')),
         'f2': Let({'g1': Id('y1')}, App(Id('f1'), Id('g1'))),
         'f3': Letrec({'g2': Id('y2'), 'g3': App(Id('g2'), Id('y3'))},
                      App(Id('f2'), Id('g3')))},
        Id('f3')
    )


def test_find_free_names():
    P = parse
    res = find_free_names(P('let id x = x in map id xs'))
    assert all(n in res for n in ('map', 'xs'))
    assert all(n not in res for n in ('id', 'x'))


def test_where_expr():
    assert parse('''
    let unify phi tvn t = unify phi phitvn phit
                          where
                             phitvn = phi tvn
                             phit   = sub_type phi t
    in unify
    ''') == parse('''
    let unify phi tvn t = (unify phi phitvn phit
                           where
                             phitvn = phi tvn
                             phit   = sub_type phi t)
    in unify
    ''') == parse('''
    let unify phi tvn t = let phitvn = phi tvn
                              phit   = sub_type phi t
                          in unify phi phitvn phit
    in unify
    ''') == parse('''
    unify where unify phi tvn t = let phitvn = phi tvn
                                      phit   = sub_type phi t
                                  in unify phi phitvn phit
    ''') == parse('''
    unify where unify phi tvn t = unify phi phitvn phit
                                  where
                                     phitvn = phi tvn
                                     phit   = sub_type phi t
    ''') == parse('''
    unify where unify phi tvn t = (unify phi phitvn phit
                                   where
                                     phitvn = phi tvn
                                     phit   = sub_type phi t)
    ''')


def test_unit_value():
    assert parse('(   )') == parse('()') == Literal((), UnitType)


@given(s.dates())
def test_date_literals(d):
    code = f'<{d!s}>'
    try:
        res = parse(code)
    except (lex.LexError, ParserError):
        raise AssertionError(f'Unexpected parsing error: {code}')
    assert res == Literal(d, DateType)


@given(s.dates())
def test_date_literals_application(d):
    code = f'f <{d!s}>'
    res = parse(code)
    assert res == Application(Identifier('f'), Literal(d, DateType))

    code = f'f <{d!s}> x'
    res = parse(code)
    assert res == Application(
        Application(Identifier('f'), Literal(d, DateType)),
        Identifier('x')
    )

    # Semantically incorrect but parser must accept it
    code = f'<{d!s}> x'
    res = parse(code)
    assert res == Application(
        Literal(d, DateType),
        Identifier('x')
    )


@given(s.datetimes())
def test_datetime_literals(d):
    code = f'<{d!s}>'
    try:
        res = parse(code)
    except (lex.LexError, ParserError):
        raise AssertionError(f'Unexpected parsing error: {code}')
    assert res == Literal(d, DateTimeType)


@given(s.datetimes())
def test_datetime_literals_application(d):
    code = f'f <{d!s}>'
    res = parse(code)
    assert res == Application(Identifier('f'), Literal(d, DateTimeType))

    code = f'f <{d!s}> x'
    res = parse(code)
    assert res == Application(
        Application(Identifier('f'), Literal(d, DateTimeType)),
        Identifier('x')
    )

    # Semantically incorrect but parser must accept it
    code = f'<{d!s}> x'
    res = parse(code)
    assert res == Application(
        Literal(d, DateTimeType),
        Identifier('x')
    )


def test_regression_confusing_unary_plus():
    assert parse('f a + c') == parse('(f a) + c')


def test_regression_greedy_where():
    assert parse(
        'let a1 = id a in a1 + 1'
    ) == parse(
        'a1 + 1 where a1 = id a'
    ) == parse(
        '(a1 + 1) where a1 = id a'
    )


def test_parens_aroun_dot_regression():
    assert parse('f . g + 1') == parse('(f . g) + 1')


def test_application_and_composition():
    assert parse('f g . h') == parse('(f g) . h')


def test_normal_precedence_of_mul_div():
    assert parse('a * b / c') == parse('(a * b)/c')


def test_bool_op_has_less_precedence():
    assert parse('a + b <= c - d') == parse('(a + b) <= (c - d)')


def test_infix_func_has_less_precedence():
    assert parse('a > b `f` c - d') == parse('(a > b) `f` (c - d)')


def test_no_attr_access():
    assert parse('p.children.len') == parse('p . children . len')


@pytest.mark.xfail(reason='Incomplete pattern matching')
def test_pattern_matching_let():
    code = '''let if True t f = t
                  if False t f = f
              in g . if'''
    assert parse(code) == Let(
        {
            'if': None  # TODO: Pattern-matching lambda abstraction
        },
        Application(Application(Identifier('.'), Identifier('g')),
                    Identifier('if'))
    )


def test_list_cons_operator():
    assert parse('a:b:xs') == parse('a:(b:xs)') == Application(
        Application(Identifier(':'), Identifier('a')),
        Application(
            Application(Identifier(':'), Identifier('b')),
            Identifier('xs')
        )
    )


def test_list_cons_precedence():
    assert parse('a + b : xs') == parse('(a + b):xs')
    assert parse('a `f` b : xs') == parse('a `f` (b:xs)')

    # A custom operator <++>
    assert parse('a <++> b : xs', debug=True) == parse('(a <++> b):xs')


def test_comma_as_an_operator():
    assert parse('(a, b)') == parse('(,) a b') == Application(
        Application(Identifier(','), Identifier('a')),
        Identifier('b')
    )


def test_consed_lists():
    assert parse('[]') == Identifier('[]')
    assert parse('1:2:[]') == parse('1:(2:[])')


def test_list_syntax():
    assert parse('[1, 2]') == parse('1:2:[]')


@pytest.mark.xfail(reason='Incomplete pattern matching')
def test_pattern_matching_nested():
    parse('let second _:x:xs = x in second')


@pytest.mark.xfail(reaseon='Look-ahead by 1 token, I need to work it out')
def test_regression_ambigous_tuple_pattern():
    assert parse('''let count [] = 0
                 count (x:xs) = 1 + (count xs)
             in count
    ''') == parse('''let count [] = 0
                 count x:xs = 1 + (count xs)
             in count
    ''')
