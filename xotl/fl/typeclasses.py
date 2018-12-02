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

from xotl.fl.types import (
    TypeConstraint,
    TypeEnvironment,
    TypeScheme,
    ConstrainedType,
)
from xotl.fl.expressions import Equation


Definition = Union[Equation, TypeEnvironment]
Definitions = Sequence[Definition]


@dataclass
class TypeClass:
    # class [constrains =>] newclass where
    #     local_definitions
    constraints: Tuple[TypeConstraint, ...]
    newclass: TypeConstraint
    definitions: Definitions  # noqa

    @property
    def type_environment(self) -> TypeEnvironment:
        return {
            name: scheme
            for definition in self.definitions
            if isinstance(definition, dict)
            for name, scheme in definition.items()
        }

    def __init__(self, constraints: Sequence[TypeConstraint],
                 newclass: TypeConstraint,
                 definitions: Definitions) -> None:

        def _constrain_scheme(scheme: TypeScheme) -> TypeScheme:
            # makes 'forall a. ...' be 'forall a. Constrain ...'
            return ConstrainedType(scheme.generics, scheme.t, (newclass, ))

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


@dataclass
class Instance:
    constraints: Tuple[TypeConstraint, ...]
    instance: TypeConstraint
    definitions: Sequence[Union[Equation, TypeEnvironment]]  # noqa
