#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xopgi.ql.lang import parse


def test_simple_one_definition():
    assert parse('def id x = x')


def test_simple_functions_definition():
    assert parse('''
       def id x = x

       const :: a -> b -> a
       def const a x = a

    ''')


def test_datatype_simple():
    assert parse('data Then a = Then a')


def test_datatype_simple2():
    assert parse('''
       data Then a = Then a
       data Else a = Else a
    ''')


def test_if_program():
    parse('''
        data Then a = Then a
        data Else a = Else a

        if :: Bool -> Then a -> Else a -> a
        def if True (Then x) _  = x
            if False _ (Else x) = x

    ''', debug=True)
