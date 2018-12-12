#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass
from typing import Type as Class, List, Union, MutableMapping

from xotl.fl.types import (
    AST,
    TypeEnvironment,
)
from xotl.fl.expressions import (
    _LetExpr,
    Let,
    Letrec,
    find_free_names,
)
from xotl.fl.pattern import Equation, FunctionDefinition


@dataclass
class ConcreteLet:
    '''The concrete representation of a let/where expression.

    '''
    definitions: List[Union[Equation, TypeEnvironment]]  # noqa
    body: AST

    @property
    def ast(self) -> _LetExpr:
        return self.compile()

    def compile(self) -> _LetExpr:
        r'''Build a Let/Letrec from a set of equations and a body.

        We need to decide if we issue a Let or a Letrec: if any of declared
        names appear in the any of the bodies we must issue a Letrec, otherwise
        issue a Let.

        Also we need to convert function-patterns into Lambda abstractions::

           let id x = ...

        becomes::

           led id = \x -> ...

        '''
        localenv: TypeEnvironment = {}
        defs: MutableMapping[str, FunctionDefinition] = {}   # noqa
        for dfn in self.definitions:
            if isinstance(dfn, Equation):
                eq = defs.get(dfn.name)
                if not eq:
                    defs[dfn.name] = FunctionDefinition([dfn])
                else:
                    assert isinstance(eq, FunctionDefinition)
                    defs[dfn.name] = eq.append(dfn)
            elif isinstance(dfn, dict):
                localenv.update(dfn)  # type: ignore
            else:
                assert False, f'Unknown definition type {dfn!r}'
        names = set(defs)
        compiled = {name: dfn.compile() for name, dfn in defs.items()}
        if any(set(find_free_names(fn)) & names for fn in compiled.values()):
            klass: Class[_LetExpr] = Letrec
        else:
            klass = Let
        return klass(compiled, self.body, localenv)
