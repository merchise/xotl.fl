#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""The language AST."""


class ILC:
    """The intermediate language nodes.

    They are subject to type-checking and compilation.

    """


class AST:
    """A AST node in the language.

    """

    def translate(self) -> ILC:  # pragma: no cover
        ...


class Dual(AST, ILC):
    def translate(self) -> ILC:  # pragma: no cover
        return self
