#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass
from typing import Iterable, Tuple

from xotl.fl.meta import Symbol
from xotl.fl.ast.base import AST
from xotl.fl.ast.pattern import ConsPattern, Equation, Pattern
from xotl.fl.ast.expressions import Application, Identifier, Literal, Lambda
from xotl.fl.utils import namesupply


class FunctionDefinition:
    """A single function definition (as a sequence of equations).

    """

    def __init__(self, eqs: Iterable[Equation]) -> None:
        equations: Tuple[Equation, ...] = tuple(eqs)
        names = {eq.name for eq in equations}
        name = names.pop()
        assert not names
        first, *rest = equations
        arity = len(first.patterns)
        if any(len(eq.patterns) != arity for eq in rest):
            raise ArityError(
                "Function definition with different parameters count", equations
            )
        self.name = name
        self.equations = equations
        self.arity = arity

    def append(self, item) -> "FunctionDefinition":
        return FunctionDefinition(self.equations + (item,))

    def extend(self, items: Iterable[Equation]) -> "FunctionDefinition":
        return FunctionDefinition(self.equations + tuple(items))

    def compile(self) -> AST:
        """Return the compiled form of the function definition.

        """
        from xotl.fl.ast.expressions import build_lambda, build_application

        # This is similar to the function `match` in 5.2 of [PeytonJones1987];
        # but I want to avoid *enlarging* simple functions needlessly.
        if self.arity:
            vars = list(namesupply(f".{self.name}_arg", limit=self.arity))
            body: AST = NO_MATCH_ERROR
            for eq in self.equations:
                dfn = eq.body
                patterns: Iterable[Tuple[str, Pattern]] = zip(vars, eq.patterns)
                for var, pattern in patterns:
                    if isinstance(pattern, str):
                        # Our algorithm is trivial but comes with a cost:
                        # ``id x = x`` is must be translated to
                        # ``id = \.id_arg0 -> (\x -> x) .id_arg0``.
                        dfn = Application(Lambda(pattern, dfn), Identifier(var))
                    elif isinstance(pattern, Literal):
                        # ``fib 0 = 1``; is transformed to
                        # ``fib = \.fib_arg0 -> <MatchLiteral 0> .fib_arg0 1``
                        dfn = build_application(
                            Identifier(MatchLiteral(pattern)),  # type: ignore
                            Identifier(var),
                            dfn,
                        )
                    elif isinstance(pattern, ConsPattern):
                        if not pattern.params:
                            # This is just a Match; similar to MatchLiteral
                            dfn = build_application(
                                Identifier(Match(pattern.cons)),  # type: ignore
                                Identifier(var),
                                dfn,
                            )
                        else:
                            for i, param in reversed(
                                list(enumerate(pattern.params, 1))
                            ):
                                if isinstance(param, str):
                                    dfn = build_application(
                                        Identifier(
                                            Extract(pattern.cons, i)
                                        ),  # type: ignore
                                        Identifier(var),
                                        Lambda(param, dfn),
                                    )
                                else:
                                    raise NotImplementedError(
                                        f"Nested patterns {param}"
                                    )
                    else:
                        assert False
                body = build_lambda(vars, build_application(MATCH_OPERATOR, dfn, body))
            return body
        else:
            # This should be a simple value, so we return the body of the
            # first equation.
            return self.equations[0].body  # type: ignore


class ArityError(TypeError):
    pass


MATCH_OPERATOR = Identifier(":OR:")
NO_MATCH_ERROR = Identifier(":NO_MATCH_ERROR:")


@dataclass(frozen=True)
class Match(Symbol):
    'A symbol for the pattern matching "match" function.'
    name: str

    def __str__(self):
        return f":match:{self.name}:"

    def __repr__(self):
        return f"<Match: {self.name}>"


@dataclass(frozen=True)
class Extract(Symbol):
    'A symbol for the pattern matching "extract" function.'
    name: str
    arg: int

    def __str__(self):
        return f":extract:{self.name}:{self.arg}:"

    def __repr__(self):
        return f"<Extract: {self.arg} from {self.name}>"


@dataclass(frozen=True)
class Select(Symbol):
    'A symbol for the pattern matching "select" function.'
    arg: int

    def __str__(self):
        return f":select:{self.arg}:"

    def __repr__(self):
        return f"<Select: {self.arg}>"


@dataclass(frozen=True)
class MatchLiteral(Symbol):
    value: Literal

    def __init__(self, value: Literal) -> None:
        super().__init__()
        str.__setattr__(self, "value", value)

    def __str__(self):
        return f":value:{self.value}:"

    def __repr__(self):
        return f"<Match value: {self.value}>"
