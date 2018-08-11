#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#


def parse(source):
    from .parser import parser, lexer
    return parser.parse(source, lexer=lexer)


def tokenize(source):
    from .parser import lexer
    lexer = lexer.clone()
    lexer.input(source)
    return [tok for tok in lexer]
