#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xopgi.ql.lang import parse
from xopgi.ql.lang.types import TypeScheme


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
    assert parse('data Then a = Then a')


def test_datatype_tree():
    assert parse('data Tree a = Leaf a | Branch (Tree a) (Tree a)')


def test_datatype_simple2():
    assert parse('''
       data Then a = Then a
       data Else a = Else a
    ''')


def test_simple_if_program():
    parse('''
        if :: Bool -> a -> a -> a
        if True x _  = x
        if False _ x = x
    ''', debug=True)


def test_if_program():
    parse('''
        data Then a = Then a
        data Else a = Else a

        if :: Bool -> Then a -> Else a -> a
        if True (Then x) _  = x
        if False _ (Else x) = x

    ''', debug=True)
