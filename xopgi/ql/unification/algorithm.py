#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Unification algorithm.

'''
from typing import List, Tuple
from .ast import Var, Term, Function


def consistent(t1, t2):
    'Return True if t1 and t2 are consistent'
    if isinstance(t1, Var) or isinstance(t2, Var):
        return True
    else:
        if t1 == t2:
            if isinstance(t1, Function):
                return all(consistent(a, b) for a, b in zip(t1.args, t2.args))
            else:
                return True


def unify(equations: List[Tuple[Term, Term]]) -> List[Tuple[Var, Term]]:
    '''Find a unification of all the equations.

    '''
