#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''A type-expression language.

Implements the type checker/inference of Chapter 9 of Book 'The Implementation
of Functional Programming Languages' -- Peyton Jones, S et al.; Prentice Hall.

Other notable sources:

- Principal type-schemes for functional programs.  Luis Damas and Robin
  Milner.  POPL ’82: Proceedings of the 9th ACM SIGPLAN-SIGACT symposium on
  Principles of programming languages, ACM, pp. 207–212

- Type Assignment in Programming Languages.  PhD. Thesis of Luis Manuel
  Martins Damas.

.. note:: We should see if the types in stdlib's typing module are
          appropriate.

'''
from .base import (   # noqa: reexport
    TypeVariable, TVar, T,

    TypeCons, TCons, C,

    FunctionType, F,

    ListType, TupleType,
    IntType,
)

from .base import parse  # noqa
from .typecheck import TypeScheme  # noqa
