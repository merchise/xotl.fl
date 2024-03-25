#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Callable
from typing import Any  # noqa

from xotl.fl.ast.types import Type, TypeCons, TypeVariable, TypeScheme, find_tvars


_STR_PADDING = " " * 4


# `Substitution` is a type; `scompose`:class: is a substitution by
# composition, `delta`:class: creates the simplest non-empty substitution.
#
# TODO: We could modify the algorithm so that we can *inspect* which variables
# are being substituted; but that's not essential to the Substitution Type.
Substitution = Callable[[str], Type]


class Composition:
    def __init__(self, f: Substitution, g: Substitution) -> None:
        assert self is not f
        self.f = f
        self.g = g

    def __call__(self, s: str) -> Type:
        return subtype(self.f, self.g(s))

    def __repr__(self):
        return f"Composition({self.f!r}, {self.g!r})"

    def __str__(self):
        import textwrap

        if self._composes_deltas:
            deltas = "\n".join(
                textwrap.indent(str(dl), _STR_PADDING) for dl in self._deltas
            )
            return f"Composition of\n{deltas}"
        else:
            f = textwrap.indent(str(self.f), _STR_PADDING)
            g = textwrap.indent(str(self.g), _STR_PADDING)
            return f"Composition of\n{f}and\n{g}"

    @property
    def _composes_deltas(self):  # pragma: no cover
        first = (
            isinstance(self.f, delta)
            or isinstance(self.f, Composition)
            and self.f._composes_deltas
        )
        if first:
            second = (
                isinstance(self.g, delta)
                or isinstance(self.g, Composition)
                and self.g._composes_deltas
            )
        else:
            second = True  # it doesn't really matter
        return first and second

    @property
    def _deltas(self):  # pragma: no cover
        from collections import deque

        stack = deque([self.g, self.f])
        while stack:
            node = stack.pop()
            if isinstance(node, delta):
                yield node
            elif isinstance(node, Composition):
                stack.append(node.g)
                stack.append(node.f)
            else:
                assert False


class Identity:
    "The identity substitution."

    def __call__(self, s: str) -> Type:
        return TypeVariable(s, check=False)

    def __repr__(self):
        return "Identity()"


sidentity = Identity()


class delta:
    """A `delta substitution` from a variable name `vname`.

    """

    def __init__(self, vname: str, t: Type) -> None:
        self.vname = vname
        self.type_ = t

    def __call__(self, s: str) -> Type:
        return self.type_ if s == self.vname else TypeVariable(s, check=False)

    def __repr__(self):
        return f"delta({self.vname!r}, {self.type_!r})"

    def __str__(self):
        return f"delta: {self.vname.ljust(20)}{self.type_!s}"


def subtype(phi: Substitution, t: Type) -> Type:
    """Get the sub-type of `t` by applying the substitution `phi`.

    """
    # 'subtype(sidentity, t) == t'; and since Type, TypeVariables and TypeCons
    # are treated immutably we should be safe to return the same type.
    if phi is sidentity:
        return t
    elif isinstance(t, TypeVariable):
        return phi(t.name)
    elif isinstance(t, TypeCons):
        return TypeCons(
            t.cons, [subtype(phi, subt) for subt in t.subtypes], binary=t.binary
        )
    elif isinstance(t, TypeScheme):
        psi = Exclude(phi, t)
        return TypeScheme(t.generics, subtype(psi, t.type_))
    else:
        assert False, f"Node of unknown type {t!r}"


def scompose(f: Substitution, g: Substitution) -> Substitution:
    """Compose two substitutions.

    The crucial property of `scompose`:func: is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    """
    if f is sidentity:
        return g
    elif g is sidentity:
        return f
    else:
        return Composition(f, g)


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    """Apply a substitution to a type scheme.

    .. warning:: You must ensure that the type scheme's generic variables are
       distinct from the variables occurring in the result of applying the
       substitution `phi` to any of the non-generic variables of `ts`.

       The way in which we ensure this (in the algorithm) is to guarantee that
       the names of the generic variables in the type scheme are always
       distinct from those which can occur in the range of the substitution
       (which are always non-generic).

    """
    # From Damas1982:
    #
    # If S is a substitution of types for type variables, often written
    # [τ1/α1, ..., τn/αn ] or [τi/αi], and σ is a type-scheme, then Sσ is the
    # type-scheme obtained by replacing each free occurrence of αi in σ by τi,
    # renaming the generic variables of σ if necessary.  Then Sσ is called an
    # instance of σ; the notions of substitution and instance extend naturally
    # to larger syntactic constructs containing type-schemes.
    #
    assert all(
        not bool(scvs & set(tv.name for tv in find_tvars(phi(unk))))
        for scvs in (set(ts.generics),)
        for unk in ts.nongenerics
    )
    return TypeScheme(ts.generics, subtype(Exclude(phi, ts), ts.type_))


class Exclude:
    """A substitution over the non-generics in a type scheme.

    Applies `phi` only if the variable name is a non-generic of the type
    scheme `ts`.

    """

    def __new__(cls, phi, ts):
        # type: (Any, Substitution, TypeScheme) -> Substitution
        if not ts.generics:
            return phi
        else:
            res = super().__new__(cls)  # type: ignore
            res.__init__(phi, ts)
            return res

    def __init__(self, phi: Substitution, ts: TypeScheme) -> None:
        self.phi = phi
        self.ts = ts

    def __call__(self, s: str) -> Type:
        if s not in self.ts.generics:
            return self.phi(s)
        else:
            return TypeVariable(s, check=False)

    def __repr__(self):
        return f"Exclude({self.phi!r}, {self.ts!r})"

    def __str__(self):
        import textwrap

        sub = textwrap.indent(str(self.phi), _STR_PADDING)
        return f"exclude all {self.ts.generics} in \n{sub}"
