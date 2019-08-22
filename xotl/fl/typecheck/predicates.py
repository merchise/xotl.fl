#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclass import dataclass
from xotl.fl.ast.types import Type, TypeVariable


@dataclass
class Eq:
    "States t1 unifies to t2 "
    t1: Type
    t2: Type

    def __str__(self):
        return f"{self.t1} ~ {self.t2}"


@dataclass
class Inst:
    "States the `tvar` is an instance of type class `typeclass`"
    tvar: TypeVariable
    typeclass: str

    def __str__(self):
        return f"{self.typeclass} {self.tvar}"
