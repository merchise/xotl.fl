#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import MutableMapping, Optional, TypeVar

from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

from xotl.fl.ast.base import AST
from xotl.fl.ast.types import Type as FLType, TypeCons, TypeVariable, TypeSchema
from xotl.fl.ast.expressions import Lambda, Identifier
from xotl.fl.utils import namesupply
from xotl.fl.builtins import BuiltinEnvDict


def builds(*args, **kwargs):
    """A decorator version of strategies.builds
    """

    def decorator(fn):
        return st.builds(fn, *args, **kwargs)

    return decorator


anonymous_names = namesupply(prefix="_anon")


def from_fltype(fltype: FLType) -> SearchStrategy[AST]:
    if isinstance(fltype, TypeVariable):
        # To keep consistent types and names, for a type variable 'a', I
        # create an identifier 'a'.
        return st.just(Identifier(fltype.name))
    elif isinstance(fltype, TypeCons) and fltype.cons == "->":
        # This is a -> b; but since Lambda is not typed on the argument
        # don't need an expression of type 'a', but just one of type 'b';
        # the expression returned in equivalent to a call of 'const'
        #
        #   const a b = b
        #
        _, b = fltype.subtypes
        return from_fltype(b).flatmap(
            lambda b: st.just(Lambda(next(anonymous_names), b))
        )
    else:
        raise AssertionError(f"Don't know how to generate {fltype}")


class TestTypingEnvironment(BuiltinEnvDict):
    def __missing__(self, key) -> TypeSchema:
        try:
            return super().__missing__(key)
        except KeyError:
            var = TypeVariable(key, check=False)
            return TypeSchema.from_typeexpr(var)
