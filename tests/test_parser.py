#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from xopgi.ql.unification.parser.tokenizer import (
    tokenize,
    LEFT_PAREN,
    RIGHT_PAREN,
    PLUS_SIGN,
    MINUS_SIGN,
    DOLLAR_SIGN,
    UNDERSCORE,
    get_identifier
)
from xopgi.ql.unification.parser.exceptions import ParserError


def test_tokenizer():
    # Notice tokenizer does not do grammar sense
    assert list(tokenize('f(+x_ - y ( $z _y.is_ok)')) == [
        get_identifier('f'),
        LEFT_PAREN,
        PLUS_SIGN,
        get_identifier('x_'),
        MINUS_SIGN,
        get_identifier('y'),
        LEFT_PAREN,
        DOLLAR_SIGN,
        get_identifier('z'),
        UNDERSCORE,
        get_identifier('y.is_ok'),
        RIGHT_PAREN,
    ]


def test_tokenizer_invalid_token():
    with pytest.raises(ParserError):
        list(tokenize(':'))
