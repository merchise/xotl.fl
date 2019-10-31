#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import os.path
from lark import Lark, Transformer

type_expr_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="type_expr",
    debug=True,
)
