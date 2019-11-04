#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import os.path
from collections import deque
from typing import Iterable, Deque

from lark import Lark, Transformer, Token
from lark.indenter import Indenter


class LexerHelper:
    """Provides functions the lexer alone cannot do.

    Introduces an _END token at points where the lexer already saw a
    block-beginning token (BLOCK_BEGIN_types) and reaches a token that leaves
    the indentation mark of the block.

    """

    BLOCK_END_type = "_END"
    BLOCK_BEGIN_types = (
        "KEYWORD_WHERE",
        "KEYWORD_DATA",
        "KEYWORD_CLASS",
        "KEYWORD_INSTANCE",
    )

    def _process(self, stream: Iterable[Token]) -> Iterable[Token]:
        stack: Deque[Token] = deque([])
        last_line = 0
        for token in stream:
            if token.type == "_NL":
                last_column = len(token.value.split("\n")[-1])
                while stack and last_column <= stack[-1].column:
                    tk = stack.pop()
                    yield Token.new_borrow_pos(self.BLOCK_END_type, tk.value, token)

            if token.type in self.BLOCK_BEGIN_types:
                stack.append(token)
                yield token
            else:
                yield token
            last_line = token.end_line or token.line
        while stack:
            token = stack.pop()
            t = Token.new_borrow_pos(self.BLOCK_END_type, token.value, token)
            t.line = last_line + 1
            yield t

    def process(self, stream: Iterable[Token]) -> Iterable[Token]:
        for token in self._process(stream):
            print(token, token.type)
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
program_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="program",
    debug=True,
    postlex=LexerHelper(),
)
