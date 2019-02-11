#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''The HM(X) type checker.

Instead of using substitutions like the one in :mod:`xotl.fl.typecheck`, this
algorithm uses constraints solving.

The algorithm is described in Pottier and Rémy’s chapter "The Essence of ML
Type Inference" in *Advanced Topics in Types and Programming Languages*
Pierce, Benjamin C. ed.

'''
# We don't currently have the notion of Constructor and Destructor; as defined
# in Rémy and Pottier's chapter: Constructors create values, while destructors
# *operate* on values (to produce another, but that's only after execution).
#
# So, '(,)' is constructor while '(+)' is a destructor; '(x,y)' is a value iff
# 'x' and 'y' are values; '(+) 1' is a value, but '1 + 2' is not.
#
# Every data constructor is a constructor.  Functions are usually destructors.
#
# Notice that the identifier '[]' is a nullary data constructor, thus, a
# value.  The ':' is a constructor; 'x:xs' is a value iff 'x' and 'xs' are
# both values; e.g: '1:2:[]' is a value; but '(1 + 2):3:[]' is not.


# Constraint generation rules from [PottierATPL2005]_, p. 431:
#
# [[x: T]]                 -> x ≼ T
# [[\z.t : T]]             -> ∃XY.(let z:X in [[t: Y]] ∧ X -> Y <= T)
# [[ f n : T]]             -> ∃Y.([[f : Y -> T]] ∧ [[n : Y]])
# [[ let z = a in e : T]]  -> let z: ∀X[ [[a: X]] ].X in [[e : T]]
#
# σ ≼ T'; is defined as ∃X.(D ∧ T ≤ T') where σ is ∀X[D].T and X#ftv(T')
#
