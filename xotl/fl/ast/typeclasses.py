#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Tuple, Sequence, Union
from dataclasses import dataclass

from xotl.fl.ast.base import AST
from xotl.fl.ast.types import (
    TypeConstraint,
    TypeEnvironment,
    TypeScheme,
    ConstrainedType,
    SimpleType,
)
from xotl.fl.ast.pattern import Equation


Definition = Union[Equation, TypeEnvironment]
Definitions = Sequence[Definition]


@dataclass
class TypeClass(AST):
    # class [constrains =>] newclass where
    #     local_definitions
    constraints: Tuple[TypeConstraint, ...]
    newclass: TypeConstraint
    definitions: Definitions  # noqa

    def __init__(self, constraints: Sequence[TypeConstraint],
                 newclass: TypeConstraint,
                 definitions: Definitions) -> None:

        def _constrain_scheme(scheme: TypeScheme) -> TypeScheme:
            # makes 'forall a. ...' be 'forall a. Constrain ...'
            return ConstrainedType(scheme.generics, scheme.type_, (newclass, ))

        def _constrain_definition(d: Definition) -> Definition:
            if isinstance(d, Equation):
                return d
            else:
                assert isinstance(d, dict)
                return {
                    name: _constrain_scheme(scheme)
                    for name, scheme in d.items()
                }

        self.constraints = tuple(constraints or [])
        self.newclass = newclass
        self.definitions = [_constrain_definition(d) for d in definitions]

    @property
    def type_environment(self) -> TypeEnvironment:
        return {
            name: scheme
            for definition in self.definitions
            if isinstance(definition, dict)
            for name, scheme in definition.items()
        }


@dataclass
class Instance(AST):
    constraints: Tuple[TypeConstraint, ...]
    typeclass_name: str
    type_: SimpleType
    definitions: Sequence[Union[Equation, TypeEnvironment]]  # noqa

    def __init__(self, constraints: Sequence[TypeConstraint],
                 typeclass_name: str,
                 type_: SimpleType,
                 definitions: Definitions) -> None:

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
