#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import os.path
from typing import Iterable

from lark import Lark, Transformer, Token
from lark.indenter import Indenter


class LexerHelper:
    def __init__(self):
        pass

    def process(self, stream: Iterable[Token]) -> Iterable[Token]:
        for token in stream:
            yield token


type_expr_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="type_expr",
    debug=True,
    postlex=LexerHelper(),
)
expr_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="expr",
    debug=True,
    postlex=LexerHelper(),
)
