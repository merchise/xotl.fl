#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#


class NormalizationError(TypeError):
    "Indicates the failure to normalize a constraint"


class UnificationError(NormalizationError):
    'Failure to unify two types; i.e. normalize the constraint "t1 ~ t2"'
