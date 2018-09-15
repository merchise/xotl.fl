#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from xotl.fl import parse
from xotl.fl.types import Type, TypeScheme
from xotl.fl.expressions import Equation, Pattern, Identifier
from xotl.fl.expressions import DataType, DataCons


def test_simple_one_definition():
    assert parse('id x = x')


def test_simple_functions_definition():
    assert parse('''
       id x = x

       const :: a -> b -> a
       const a x = a
    ''')


def test_typedecls():
    assert parse('''
       id :: a -> a
       const :: a -> b -> a
    ''') == [
        {'id': TypeScheme.from_str('a -> a')},
        {'const': TypeScheme.from_str('a -> b -> a')}
    ]


def test_datatype_simple():
    assert parse('data Then a = Then a') == [
        DataType(
            'Then',
            Type.from_str('Then a'),
            [DataCons('Then', [Type.from_str('a')])]
        )
    ]


def test_datatype_tree():
    assert parse('data Tree a = Leaf a | Branch (Tree a) (Tree a)') == [
        DataType(
            'Tree',
            Type.from_str('Tree a'),
            [
                DataCons('Leaf', [Type.from_str('a')]),
                DataCons('Branch', [
                    Type.from_str('Tree a'),
                    Type.from_str('Tree a'),
                ])
            ]
        )
    ]


def test_datatype_simple2():
    assert parse('''
       data Then a = Then a
       data Else a = Else a
    ''') == [
        DataType(
            'Then',
            Type.from_str('Then a'),
            [DataCons('Then', [Type.from_str('a')])]
        ),
        DataType(
            'Else',
            Type.from_str('Else a'),
            [DataCons('Else', [Type.from_str('a')])]
        )
    ]


def test_simple_if_program():
    parse('''
        if :: Bool -> a -> a -> a
        if True x _  = x
        if False _ x = x
    ''', debug=True) == [
        {'id': TypeScheme.from_str('Bool -> a -> a -> a')},
        Equation(Pattern('if', ('True', 'x', '_')), Identifier('x')),
        Equation(Pattern('if', ('False', '_', 'x')), Identifier('x')),
    ]


@pytest.mark.xfail(reason='Failing to parse pattern-matching parameters')
def test_if_program():
    parse('''
        data Then a = Then a
        data Else a = Else a

        if :: Bool -> Then a -> Else a -> a
        if True (Then x) _  = x
        if False _ (Else x) = x

    ''', debug=True)


@pytest.mark.xfail(reason='Failing to split equations')
def test_large_definitions():
    assert parse('''
       name =
          let id x = x in id
    ''', debug=True) == parse('name = let id x = x in id')


@pytest.mark.xfail(reason='Failing to define operators')
def test_defs_operators():
    assert parse('''
       (.) :: (b -> c) -> (a -> b) -> a -> c
       (.) f g x = f (g x)
    ''')
