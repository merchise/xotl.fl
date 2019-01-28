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


def test_non_existential_variables():
    with pytest.raises(TypeError):
        parse('data T = A a')


def test_non_unused_variables():
    with pytest.raises(TypeError):
        parse('data T a = A')


def test_non_repeated_datacons():
    with pytest.raises(TypeError):
        parse('data B = T | T')
