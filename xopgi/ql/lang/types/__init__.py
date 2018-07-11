#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A very simple type-expression language.

This (at the moment) just to implement the type-checker of chapter 9 of 'The
Implementation of Functional Programming Languages'.

.. note:: We should see if the types in stdlib's typing module are
          appropriate.

'''
from .base import (   # noqa: reexport
    TypeVariable, TVar, T,

    ConsType,

    FunctionType, F,

    ListType, TupleType,
    IntType,

    scompose, delta, subtype, sidentity,
)
