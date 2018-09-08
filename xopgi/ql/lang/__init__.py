#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#


def parse(program_source: str, *, debug: bool = False):
    '''Parse the program source and return its AST.

    This function doesn't type-check the program.

    '''
    from .parsers import program_parser, lexer
    return program_parser.parse(program_source, lexer=lexer, debug=debug)
