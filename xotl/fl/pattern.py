#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Pattern Matching.

'''
from typing import Union, Sequence, Tuple, Iterable
from dataclasses import dataclass

from xotl.fl.types import (
    AST,
    Symbol,
)
from xotl.fl.expressions import (
    Identifier,
    Literal,
    Application,
    Lambda,
)
from xotl.fl.utils import namesupply


# Patterns and Equations.  In the final AST, an expression like:
#
#     let id x = x in ...
#
# would actually be like
#
#     let id = \x -> x
#
# with some complications if pattern-matching is allowed:
#
#     let length [] = 0
#         lenght (x:xs) = 1 + length xs
#     in  ...
#
# The Pattern and Equation definitions are not part of the final AST, but more
# concrete syntactical object in the source code.  In the final AST, the let
# expressions shown above are indistinguishable.
#
# For value (function) definitions the parser still returns *bare* Equation
# object for each line of the definition.


@dataclass(frozen=True)
class Match(Symbol):
    'A symbol for the pattern matching "match" function.'
    name: str

    def __str__(self):
        return f':match:{self.name}:'

    def __repr__(self):
        return f'<Match: {self.name}>'


@dataclass(frozen=True)
class Extract(Symbol):
    'A symbol for the pattern matching "extract" function.'
    name: str
    arg: int

    def __str__(self):
        return f':extract:{self.name}:{self.arg}:'

    def __repr__(self):
        return f'<Extract: {self.arg} from {self.name}>'


@dataclass(frozen=True)
class Select(Symbol):
    'A symbol for the pattern matching "select" function.'
    arg: int

    def __str__(self):
        return f':select:{self.arg}:'

    def __repr__(self):
        return f'<Select: {self.arg}>'


@dataclass(frozen=True)
class MatchLiteral(Symbol):
    value: Literal

    def __str__(self):
        return f':value:{self.value}:'

    def __repr__(self):
        return f'<Match value: {self.value}>'


class ConsPattern:
    '''The syntactical notion of a pattern.

    '''
    def __init__(self, cons: str, params=None) -> None:
        self.cons: str = cons
        self.params = tuple(params or [])

    def __repr__(self):
        return f'<pattern {self.cons!r} {self.params!r}>'

    def __str__(self):
        if self.params:
            return f'{self.cons} {self._parameters}'
        else:
            return self.cons

    @property
    def _parameters(self):
        def _str(x):
            if isinstance(x, str):
                return x
            elif isinstance(x, ConsPattern):
                return f'({x})'
            else:
                return repr(x)

        return ' '.join(map(_str, self.params))

    def __eq__(self, other):
        if isinstance(other, ConsPattern):
            return self.cons == other.cons and self.params == other.params
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ConsPattern):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((ConsPattern, self.cons, self.params))


Pattern = Union[str, Literal, ConsPattern]


class Equation:
    '''The syntactical notion of an equation.

    '''
    def __init__(self, name: str, patterns: Sequence[Pattern], body: AST) -> None:
        self.name = name
        self.patterns: Tuple[Pattern, ...] = tuple(patterns or [])
        self.body = body

    def __repr__(self):
        def _str(x):
            result = str(x)
            if ' ' in result:
                return f'({result})'
            else:
                return result

        if self.patterns:
            args = ' '.join(map(_str, self.patterns))
            return f'<equation {self.name!s} {args} = {self.body!r}>'
        else:
            return f'<equation {self.name!s} = {self.body!r}>'

    def __eq__(self, other):
        if isinstance(other, Equation):
            return (self.name == other.name and
                    self.patterns == other.patterns and
                    self.body == other.body)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Equation):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Equation, self.name, self.patterns, self.body))


class FunctionDefinition:
    '''A single function definition (as a sequence of equations).

    '''
    def __init__(self, eqs: Iterable[Equation]) -> None:
        equations: Tuple[Equation, ...] = tuple(eqs)
        names = {eq.name for eq in equations}
        name = names.pop()
        assert not names
        first, *rest = equations
        arity = len(first.patterns)
        if any(len(eq.patterns) != arity for eq in rest):
            raise ArityError(
                "Function definition with different parameters count",
                equations
            )
        self.name = name
        self.equations = equations
        self.arity = arity

    def append(self, item) -> 'FunctionDefinition':
        return FunctionDefinition(self.equations + (item, ))

    def extend(self, items: Iterable[Equation]) -> 'FunctionDefinition':
        return FunctionDefinition(self.equations + tuple(items))

    def compile(self) -> AST:
        '''Return the compiled form of the function definition.

        '''
        from xotl.fl.expressions import build_lambda, build_application
        # This is similar to the function `match` in 5.2 of [PeytonJones1987];
        # but I want to avoid *enlarging* simple functions needlessly.
        if self.arity:
            vars = list(namesupply(f'.{self.name}_arg', limit=self.arity))
            body: AST = NO_MATCH_ERROR
            for eq in self.equations:
                dfn = eq.body
                patterns: Iterable[Tuple[str, Pattern]] = zip(vars, eq.patterns)
                for var, pattern in patterns:
                    if isinstance(pattern, str):
                        # Our algorithm is trivial but comes with a cost:
                        # ``id x = x`` is must be translated to
                        # ``id = \.id_arg0 -> (\x -> x) .id_arg0``.
                        dfn = Application(
                            Lambda(pattern, dfn),
                            Identifier(var)
                        )
                    elif isinstance(pattern, Literal):
                        # ``fib 0 = 1``; is transformed to
                        # ``fib = \.fib_arg0 -> <MatchLiteral 0> .fib_arg0 1``
                        dfn = build_application(
                            Identifier(MatchLiteral(pattern)),  # type: ignore
                            Identifier(var),
                            dfn
                        )
                    elif isinstance(pattern, ConsPattern):
                        if not pattern.params:
                            # This is just a Match; similar to MatchLiteral
                            dfn = build_application(
                                Identifier(Match(pattern.cons)),  # type: ignore
                                Identifier(var),
                                dfn
                            )
                        else:
                            for i, param in reversed(list(enumerate(pattern.params, 1))):
                                if isinstance(param, str):
                                    dfn = build_application(
                                        Identifier(Extract(pattern.cons, i)),  # type: ignore
                                        Identifier(var),
                                        Lambda(param, dfn)
                                    )
                                else:
                                    raise NotImplementedError(
                                        f"Nested patterns {param}"
                                    )
                    else:
                        assert False
                body = build_lambda(
                    vars,
                    build_application(
                        MATCH_OPERATOR,
                        dfn,
                        body
                    )
                )
            return body
        else:
            # This should be a simple value, so we return the body of the
            # first equation.
            return self.equations[0].body


MATCH_OPERATOR = Identifier(':OR:')
NO_MATCH_ERROR = Identifier(':NO_MATCH_ERROR:')


class ArityError(TypeError):
    pass
