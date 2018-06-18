#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

from xopgi.ql.translate.basic import filtered


def test_simplest_and_invalid_predicates():
    assert filtered(lambda r: r.name == '1') == [('name', '=', '1')]
    assert filtered(lambda r: not (r.name == '1')) == ['!', ('name', '=', '1')]
    assert filtered(lambda r: not (not (r.name == '1'))) == ['!', '!', ('name', '=', '1')]
    assert filtered(lambda r: r.name == '1' and r.age < 1) == [
        '&', ('name', '=', '1'), ('age', '<', 1)
    ]
    assert filtered(lambda r: r.age < r.parent.age) == [
        ('age', '<', 'parent.age')
    ]
    assert filtered(lambda r: (not(r.name == '1') and r.age < 1) or (r.name != '1' and r.age > 1)) == [
        '|',
        '&', '!', ('name', '=', '1'), ('age', '<', 1),
        '&', ('name', '!=', '1'), ('age', '>', 1)
    ]
    assert filtered(lambda r: (r.name == '1' and r.age < 1) or (r.name != '1' and r.age > 1) or r.name == 'power') == [
        '|',
        '|',
        '&', ('name', '=', '1'), ('age', '<', 1),
        '&', ('name', '!=', '1'), ('age', '>', 1),
        ('name', '=', 'power')
    ]
