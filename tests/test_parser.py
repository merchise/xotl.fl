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
    NEW_LINE,
    DOLLAR_SIGN,
    UNDERSCORE,
    get_identifier
)
from xopgi.ql.unification.parser.exceptions import ParserError


def test_tokenizer():
    # Notice tokenizer does not do grammar sense
    assert list(tokenize('f(+x_ - \ny\n ( $z _y:\nis.ok)')) == [
        get_identifier('f'),
        LEFT_PAREN,
        PLUS_SIGN,
        get_identifier('x_'),
        MINUS_SIGN,
        NEW_LINE,
        get_identifier('y'),
        NEW_LINE,
        LEFT_PAREN,
        DOLLAR_SIGN,
        get_identifier('z'),
        UNDERSCORE,
        get_identifier('y:'), NEW_LINE, get_identifier('is.ok'),
        RIGHT_PAREN,
    ]
    assert list(tokenize('f()\n')) == [
        get_identifier('f'),
        LEFT_PAREN,
        RIGHT_PAREN,
        NEW_LINE,
    ]



def test_tokenizer_invalid_token():
    with pytest.raises(ParserError):
        list(tokenize(';'))
