#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
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
    assert filtered(lambda r: r.age in (1, 2, 3)) == [
        ('age', 'in', (1, 2, 3))
    ]
    assert filtered(lambda this: 1 < this.age < 10 == 10) == [
        '&', '&', (1, '<', 'age'), ('age', '<', 10), (10, '=', 10)
    ]


@pytest.mark.xfail(reason='Python 3.6 is folding the literal list into a tuple')
def test_in_list():
    # import dis
    # dis.dis(lambda r: r.age in [1, 2, 3])
    # 1           0 LOAD_FAST                0 (r)
    #             2 LOAD_ATTR                0 (age)
    #             4 LOAD_CONST               4 ((1, 2, 3))
    #             6 COMPARE_OP               6 (in)
    #             8 RETURN_VALUE
    assert filtered(lambda r: r.age in [1, 2, 3]) == [
        ('age', 'in', [1, 2, 3])
    ]
