#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Iterable, Tuple
from xotl.fl.ast.types import Type, TypeCons, TypeVariable, find_tvars

from .subst import delta, sidentity, scompose, subtype, Substitution
from .exceptions import UnificationError


def unify(e1: Type, e2: Type, *, phi: Substitution = sidentity) -> Substitution:
    """Extend `phi` so that it unifies `e1` and `e2`.

    If `phi` is None, uses the identity substitution `Identity`:class:.

    If there's no substitution that unifies the given terms, raise a
    `UnificationError`:class:.

    """

    def extend(phi: Substitution, name: str, t: Type) -> Substitution:
        if isinstance(t, TypeVariable) and name == t.name:
            return phi
        elif name in {tv.name for tv in find_tvars(t)}:
            raise UnificationError(f"Cannot unify {name!s} with {t!s}")
        else:
            # TODO: Make the result *descriptible*
            return scompose(delta(name, t), phi)

    def unify_with_tvar(tvar, t):
        phitvn = phi(tvar.name)
        if phitvn == tvar:
            return extend(phi, tvar.name, subtype(phi, t))
        else:
            return unify(phitvn, subtype(phi, t), phi=phi)

    if isinstance(e1, TypeVariable):
        return unify_with_tvar(e1, e2)
    elif isinstance(e2, TypeVariable):
        return unify_with_tvar(e2, e1)
    else:
        assert isinstance(e1, TypeCons) and isinstance(e2, TypeCons)
        if e1.cons == e2.cons:
            return unify_exprs(zip(e1.subtypes, e2.subtypes), p=phi)
        else:
            raise UnificationError(f"Cannot unify {e1!s} with {e2!s}")


TypePairs = Iterable[Tuple[Type, Type]]


# This is the unifyl in the Book.
def unify_exprs(exprs: TypePairs, *, p: Substitution = sidentity) -> Substitution:
    """Extend `p` to unify all pairs of type expressions in `exprs`."""
    for se1, se2 in exprs:
        p = unify(se1, se2, phi=p)
    return p
