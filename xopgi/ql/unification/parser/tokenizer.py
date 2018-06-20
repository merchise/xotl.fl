#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import re
from typing import Iterator

from .exceptions import ParserError


IDENTIFIER = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9_\.:]*$', re.ASCII)
WHITESPACES = re.compile(r'\s+', re.M)
# NOTE: The UNDERSCORE is in the IDENTIFIER and we divide it when matching
# over it.
SIGNS = re.compile(r'(<=|<|>=|>|==|!=|\+|-|\*|/|\(|\)|\$)')


class Token:
    def __init__(self, type, payload=None):
        self.type = type
        self.payload = payload

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.payload == self.payload
        elif isinstance(other, str):
            return self.type == other and not self.payload
        else:
            return NotImplemented

    def __hash__(self):
        return hash((type(self), self.string))

    def __repr__(self):
        if self.payload is not None:
            return f'<Token({self.type!r}, {self.payload!r})>'
        else:
            return f'<Token({self.type!r})>'


UNDERSCORE = Token('UNDERSCORE')
LT_SIGN = Token('LT_SIGN')
LE_SIGN = Token('LE_SIGN')
GT_SIGN = Token('GT_SIGN')
GE_SIGN = Token('GE_SIGN')
EQ_SIGN = Token('EQ_SIGN')
NE_SIGN = Token('NE_SIGN')
LEFT_PAREN = Token('LEFT_PAREN')
RIGHT_PAREN = Token('RIGHT_PAREN')
PLUS_SIGN = Token('PLUS_SIGN')
MINUS_SIGN = Token('MINUS_SIGN')
MUL_SIGN = Token('MUL_SIGN')
DIV_SIGN = Token('DIV_SIGN')
DOLLAR_SIGN = Token('DOLLAR_SIGN')
TOKENS_MAP = {
    '<': LT_SIGN,
    '<=': LE_SIGN,
    '>': GT_SIGN,
    '>=': GE_SIGN,
    '==': EQ_SIGN,
    '!=': NE_SIGN,
    '(': LEFT_PAREN,
    ')': RIGHT_PAREN,
    '+': PLUS_SIGN,
    '-': MINUS_SIGN,
    '*': MUL_SIGN,
    '/': DIV_SIGN,
    '$': DOLLAR_SIGN,
    '_': UNDERSCORE,
}


def get_identifier(name):
    return Token('identifier', name)


def tokenize(source: str) -> Iterator[Token]:
    '''Tokenize the `source` code.'''
    # TODO: This is quite inefficient because we use a regular expressions for
    # almost everything.
    pos = 0
    source += ' '  # ensure a white-space to allow very simple expressions
    for stop in WHITESPACES.finditer(source):
        chunk = source[pos:stop.start()]
        # If (by chance) the token is known sign emit it right away...
        tk = TOKENS_MAP.get(chunk, None)
        if tk is not None:
            yield tk
        elif IDENTIFIER.match(chunk):
            if chunk.startswith('_'):
                yield UNDERSCORE
                chunk = chunk[1:]
            if chunk:
                yield get_identifier(chunk)
        else:
            # We can a non-spaced program like 'f()' or 'x+y'.  Splitting by
            # SIGNS must yield identifiers and signs...  The simplest case (an
            # identifier) 'f' is done after attempting to find signs.
            pos1 = 0
            for sign in SIGNS.finditer(chunk):
                word = chunk[pos1:sign.start()]
                if word and IDENTIFIER.match(word):
                    if word.startswith('_'):
                        yield UNDERSCORE
                        word = word[1:]
                    if word:
                        yield get_identifier(word)
                elif word:
                    raise ParserError(
                        f'Expected identifier, found {word!r} at {pos + pos1}'
                    )
                yield TOKENS_MAP[sign.group()]
                pos1 = sign.end()
            word = chunk[pos1:]
            if word and IDENTIFIER.match(word):
                yield get_identifier(word)
            elif word:
                raise ParserError(
                    f'Expected identifier, found {word!r} at {pos + pos1}'
                )
        pos = stop.end()
