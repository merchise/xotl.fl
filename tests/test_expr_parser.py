#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

from xopgi.ql.lang.expressions import parse


def test_malformed_trivial():
    parse('')


def test_wellformed_basic_expressions():
    assert parse('a') == parse('   a   ')
    assert parse('(a)') == parse('a')
