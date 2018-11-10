#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

import pytest

from xotl.fl.builtins import (
    NumberType,
    CharType,
    StringType,
    BoolType,
    builtins_env,
    BuiltinEnvDict,
)
from xotl.fl.expressions import parse
from xotl.fl.types import Type, TypeScheme, EMPTY_TYPE_ENV, find_tvars
from xotl.fl.typecheck import typecheck, sidentity, unify
from xotl.fl.utils import namesupply


def test_from_literals():
    phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), parse(r'let x = 1 in x'))
    assert phi is sidentity
    assert t == NumberType

    phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), parse(r'let x = "1" in x'))
    assert phi is sidentity
    assert t == StringType

    phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), parse(r"let x = '1' in x"))
    assert phi is sidentity
    assert t == CharType

    # true and false are not recognized as booleans by the parser, so let's
    # provide them as part the env.
    phi, t = typecheck(builtins_env, namesupply('.a'),
                       parse(r"let x = True in x"))
    assert phi is sidentity
    assert t == BoolType

    phi, t = typecheck(builtins_env, namesupply('.a'),
                       parse(r"let x = False in x"))
    assert phi is sidentity
    assert t == BoolType


def test_combinators():
    # Since they're closed expressions they should type-check
    K = parse(r'\a b -> a')
    TK = Type.from_str('a -> b -> a')
    phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), K)
    unify(TK, t)  # we can't ensure TK == t, but they must unify, in fact they
                  # must be same type with alpha-renaming.

    S = parse(r'\x y z -> x z (y z)')
    TS = Type.from_str('(a -> b -> c) -> (a -> b) -> a -> c')
    phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), S)
    unify(TS, t)

    # But the paradoxical combinator doesn't type-check
    Y = parse(r'\f -> (\x -> f (x x))(\x -> f (x x))')
    with pytest.raises(TypeError):
        phi, t = typecheck(EMPTY_TYPE_ENV, namesupply('.a'), Y)


def test_paradox_omega():
    r'Test `(\x -> x x)` does not type-check'
    with pytest.raises(TypeError):
        typecheck(EMPTY_TYPE_ENV, namesupply('.a'), parse(r'\x -> x x'))


def test_hidden_paradox_omega():
    code = '''
    let id x    = x
        prxI c  = c x id
        p1 x y  = x
        p2 x y  = y
    in prxI p2 (prxI p2)
    '''
    typecheck({'x': TypeScheme.from_str('a', generics=[])},
              namesupply('.a'), parse(code))

    code = '''
    let id x    = x
        prxI c  = c x id
        p1 x y  = x
        p2 x y  = y
    in prxI p1 (prxI p1)
    '''
    with pytest.raises(TypeError):
        typecheck({'x': TypeScheme.from_str('a', generics=[])},
                  namesupply('.a'), parse(code))


def test_basic_builtin_types():
    with pytest.raises(TypeError):
        # not :: Bool -> Bool, but passed a Number
        typecheck(builtins_env, namesupply('.a'), parse('not 0'))

    phi, t = typecheck(builtins_env, namesupply('.a'), parse('not True'))
    assert t == BoolType
    phi, t = typecheck(builtins_env, namesupply('.a'), parse('not False'))
    assert t == BoolType

    userfuncs = {'toString': TypeScheme.from_str('a -> [Char]')}
    phi, t = typecheck(
        dict(builtins_env, **userfuncs),
        namesupply('.a'),
        parse('either toString id')
    )
    assert len(find_tvars(t)) == 1
    unify(Type.from_str('Either a [Char] -> [Char]'), t)


def test_composition():
    phi, t = typecheck(
        builtins_env,
        namesupply('.a'),
        parse('let id x = x in id . id')
    )
    unify(Type.from_str('a -> a'), t)
    unify(Type.from_str('(a -> a) -> (a -> a)'), t)

    phi, t = typecheck(
        builtins_env,
        namesupply('.a'),
        parse('Left . Right')
    )
    unify(Type.from_str('a -> Either (Either b a) c'), t)

    # In our case, (+) is not polymorphic (Number is not a type-class), so it
    # can't be composed with Either.
    with pytest.raises(TypeError):
        typecheck(
            builtins_env,
            namesupply('.a'),
            parse('(+) . Left')
        )
    # If we had a polymorphic (+), it would be composable
    phi, t = typecheck(
        dict(builtins_env, **{'+': TypeScheme.from_str('a -> a -> a')}),
        namesupply('.a'),
        parse('(+) . Left')
    )
    unify(Type.from_str('a -> Either a b -> Either a b'), t)
    phi, t = typecheck(
        dict(builtins_env, **{'+': TypeScheme.from_str('a -> a -> a')}),
        namesupply('.a'),
        parse('(+) . Right')
    )
    unify(Type.from_str('b -> Either a b -> Either a b'), t)


def test_typecheck_recursion():
    then = TypeScheme.from_str('a -> Then a')
    else_ = TypeScheme.from_str('a -> Else a')
    if_then_else = TypeScheme.from_str('Bool -> Then a -> Else a -> a')
    Nil = TypeScheme.from_str('[a]')
    tail = TypeScheme.from_str('[a] -> [a]')
    matches = TypeScheme.from_str('a -> b -> Bool')
    add = TypeScheme.from_str('a -> a -> a')
    env = {'if': if_then_else,
           'then': then,
           'else': else_,
           'matches': matches,
           'Nil': Nil,
           '+': add,
           'tail': tail}
    phi, t = typecheck(
        env,
        namesupply('.a'),
        # I need to put parenthesis because of the failure of precedence we
        # have; otherwise we could use $ to connect if then and else (they are
        # still functions): 'if cond $ then result $ else other_result'.
        # `matches` would be a simple pattern matching function.  The real
        # function would have to operate on values and patterns (which are no
        # representable here.)
        parse('''
            let count xs = if (xs `matches` Nil) \
                              (then 0) \
                              (else let ts = tail xs in 1 + (count ts))
            in count
        ''')
    )
    # The count functions counts the number of elements.
    unify(Type.from_str('[a] -> Number'), t)


def test_type_checking_tuples():
    typecheck(builtins_env, namesupply('.a'), parse('(1, 2, 3)'))


def test_local_type_annotation_let():
    phi, t = typecheck(
        BuiltinEnvDict({
            '[]': TypeScheme.from_str('[a]'),
            'reverse': TypeScheme.from_str('[a] -> [a]'),
            ':': TypeScheme.from_str('a -> [a] -> [a]')
        }),
        namesupply('.a'),
        parse('''let g = [1, 2, 3]
                 in reverse g''')
    )
    assert t == Type.from_str('[Number]')

    phi, t = typecheck(
        BuiltinEnvDict({
            '[]': TypeScheme.from_str('[a]'),
            'reverse': TypeScheme.from_str('[a] -> [a]'),
            ':': TypeScheme.from_str('a -> [a] -> [a]')
        }),
        namesupply('.a'),
        parse('''let g :: [Number]
                     g = []
                 in reverse g''')
    )
    assert t == Type.from_str('[Number]')

    phi, t = typecheck(
        BuiltinEnvDict({
            '[]': TypeScheme.from_str('[a]'),
            'reverse': TypeScheme.from_str('[a] -> [a]'),
            ':': TypeScheme.from_str('a -> [a] -> [a]')
        }),
        namesupply('.a'),
        parse('''let g :: [a]
                     g = [1, 2, 3]
                 in reverse g''')
    )
    assert t == Type.from_str('[Number]')

    with pytest.raises(TypeError):
        typecheck(
            BuiltinEnvDict({
                '[]': TypeScheme.from_str('[a]'),
                'reverse': TypeScheme.from_str('[a] -> [a]'),
                ':': TypeScheme.from_str('a -> [a] -> [a]')
            }),
            namesupply('.a'),
            parse('''let g :: [Char]
                         g = [1, 2, 3]
                     in reverse g''')
        )


def test_local_type_annotation_letrec():
    phi, t = typecheck(
        BuiltinEnvDict({
            '[]': TypeScheme.from_str('[a]'),
            'reverse': TypeScheme.from_str('[a] -> [a]'),
            ':': TypeScheme.from_str('a -> [a] -> [a]'),
            '+': TypeScheme.from_str('a -> a -> a'),
        }),
        namesupply('.a'),
        parse('''let count :: Number -> [Number]
                     count x = x:count (x + 1)
                     g :: [Number]
                     g = count 1
                     g2 = reverse g
                 in reverse g''')
    )
    assert t == Type.from_str('[Number]')

    with pytest.raises(TypeError):
        typecheck(
            BuiltinEnvDict({
                '[]': TypeScheme.from_str('[a]'),
                'reverse': TypeScheme.from_str('[a] -> [a]'),
                ':': TypeScheme.from_str('a -> [a] -> [a]'),
                '+': TypeScheme.from_str('a -> a -> a'),
            }),
            namesupply('.a'),
            parse('''let count :: Number -> [Number]
                         count x = x:count (x + 1)
                         g :: [Char]
                         g = count 1
                     in reverse g''')
        )
