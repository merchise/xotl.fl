#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass
from typing import Sequence, Tuple, Union

from xotl.fl.ast.base import AST
from xotl.fl.ast.pattern import Equation
from xotl.fl.ast.types import (
    ConstrainedType,
    SimpleType,
    TypeConstraint,
    TypeEnvironment,
    TypeScheme,
    find_tvars,
)

Definition = Union[Equation, TypeEnvironment]
Definitions = Sequence[Definition]


@dataclass
class TypeClass(AST):
    # class [superclasses =>] newclass where
    #     local_definitions
    superclasses: Tuple[TypeConstraint, ...]
    newclass: TypeConstraint
    definitions: Definitions  # noqa

    def __init__(
        self,
        superclasses: Sequence[TypeConstraint],
        newclass: TypeConstraint,
        definitions: Definitions,
    ) -> None:
        def _constrain_scheme(scheme: TypeScheme) -> TypeScheme:
            # makes 'forall a. ...' be 'forall a. Constrain ...'
            return ConstrainedType(scheme.generics, scheme.type_, (newclass,))

        def _constrain_definition(d: Definition) -> Definition:
            if isinstance(d, Equation):
                return d
            else:
                assert isinstance(d, dict)
                return {name: _constrain_scheme(scheme) for name, scheme in d.items()}

        self._check_qual(superclasses, newclass)
        self.superclasses = tuple(superclasses or [])
        self.newclass = newclass
        # Reject non-matching or non-applied type variables, e.g
        # 'class Eq b => Ord a'.
        self.definitions = [_constrain_definition(d) for d in definitions]

    @property
    def type_environment(self) -> TypeEnvironment:
        return {
            name: scheme
            for definition in self.definitions
            if isinstance(definition, dict)
            for name, scheme in definition.items()
        }

    @classmethod
    def _check_qual(cls, constraints: Sequence[TypeConstraint], newclass: TypeConstraint) -> None:
        """Check that all type variables in constraints match the class_'s."""
        if constraints:
            # TypeConstraint admits only one variable, so all constraints must
            # share the same one.  That's why we can use set's intersection
            # operator.
            tvars = set.intersection({newclass.type_}, *({tc.type_} for tc in constraints))
            if not tvars:
                tcs = ", ".join(map(str, constraints))
                raise TypeError(f"Constraints don't match: {tcs} => {newclass}")


@dataclass
class Instance(AST):
    constraints: Tuple[TypeConstraint, ...]
    typeclass_name: str
    type_: SimpleType
    definitions: Sequence[Definition]  # noqa

    def __init__(
        self,
        constraints: Sequence[TypeConstraint],
        typeclass_name: str,
        type_: SimpleType,
        definitions: Definitions,
    ) -> None:
        self._check_qual(constraints, typeclass_name, type_)
        self.constraints = tuple(constraints or [])
        self.typeclass_name = typeclass_name
        self.type_ = type_
        # Unlike TypeClass we cannot create the type environment now.  We need
        # to match the type-class.
        #
        # For instance, the type of (==) in the instance Eq (Maybe a) is
        # ``(==) :: (Maybe a) -> (Maybe a) -> Bool``.
        #
        # In general if a type class defines something like::
        #
        #    class Tc x where
        #        f :: x -> b -> c
        #
        # withing the context of the instance:
        #
        #      instance Tc (Cons a) where
        #          ...
        #
        # the type `x` becomes `Cons a` (non-generic 'a', i.e NOT `forall
        # a. Cons a`).
        self.definitions = list(definitions)

    @classmethod
    def _check_qual(
        cls, constraints: Sequence[TypeConstraint], class_: str, type_: SimpleType
    ) -> None:
        """Check that instances type variables are not partially applied"""
        tvars = set(find_tvars(type_))
        cvars = {tc.type_ for tc in constraints}
        if tvars != cvars:
            if constraints:
                tcs = ", ".join(map(str, constraints))
                raise TypeError(
                    "Unconstrained instance type variables: " f"{tcs} => {class_} {type_}"
                )
            else:
                raise TypeError("Unconstrained instance type variables: " f"{class_} {type_}")
