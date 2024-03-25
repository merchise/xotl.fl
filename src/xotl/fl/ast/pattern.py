#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Pattern Matching."""

from dataclasses import dataclass
from itertools import groupby
from typing import Iterator, List, Mapping, MutableMapping, Sequence, Tuple
from typing import Type as Class
from typing import Union

from xotl.fl.ast.adt import DataCons
from xotl.fl.ast.base import AST, ILC
from xotl.fl.ast.expressions import Let, Letrec, Literal, _LetExpr, find_free_names
from xotl.fl.ast.types import TypeEnvironment
from xotl.tools.fp.tools import fst, snd
from xotl.tools.objects import memoized_property

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


UnnamedPattern = Union[str, Literal, "ConsPattern"]
Pattern = Union[str, Literal, "ConsPattern", "NamedPattern"]


class ConsPattern(AST):
    """The syntactical notion of a pattern."""

    def __init__(self, cons: str, params: Sequence[Pattern] = None) -> None:
        self.cons: str = cons
        self.params: Tuple[Pattern, ...] = tuple(params or [])

    def __repr__(self):
        return f"<pattern {self.cons!r} {self.params!r}>"

    def __str__(self):
        if self.params:
            return f"{self.cons} {self._parameters}"
        else:
            return self.cons

    @property
    def _parameters(self):
        def _str(x):
            if isinstance(x, str):
                return x
            elif isinstance(x, ConsPattern):
                return f"({x})"
            else:
                return repr(x)

        return " ".join(map(_str, self.params))

    def __eq__(self, other):
        if isinstance(other, ConsPattern):
            return self.cons == other.cons and self.params == other.params
        else:
            return NotImplemented

    def __hash__(self):
        return hash((ConsPattern, self.cons, self.params))

    @property
    def bindings(self) -> Iterator[str]:
        for param in self.params:
            if isinstance(param, str) and param != "_":
                yield param
            elif isinstance(param, ConsPattern):
                yield from param.bindings
            elif isinstance(param, NamedPattern):
                yield from param.bindings


class NamedPattern(AST):
    def __init__(self, name: str, pattern: UnnamedPattern) -> None:
        self.name = name
        self.pattern = pattern

    def __str__(self):
        return f"{self.name} @ {self.pattern}"

    @property
    def bindings(self) -> Iterator[str]:
        yield self.name
        pattern = self.pattern
        if isinstance(pattern, str) and pattern != "_":
            yield pattern
        elif isinstance(pattern, ConsPattern):
            yield from pattern.bindings
        elif isinstance(pattern, NamedPattern):
            yield from pattern.bindings


class Equation(AST):
    """The syntactical notion of an equation."""

    def __init__(self, name: str, patterns: Sequence[Pattern], body: AST) -> None:
        self.name = name
        self.patterns: Tuple[Pattern, ...] = tuple(patterns or [])
        self.body = body
        self._check_non_repeated_vars()

    def _check_non_repeated_vars(self):
        names = list(n for n in self.bindings)
        if len(names) != len(set(names)):
            raise ValueError(f"Repeated bindings in patterns: {self!s}")

    def __repr__(self):
        def _str(x):
            result = str(x)
            if " " in result:
                return f"({result})"
            else:
                return result

        if self.patterns:
            args = " ".join(map(_str, self.patterns))
            return f"<equation {self.name!s} {args} = {self.body!r}>"
        else:
            return f"<equation {self.name!s} = {self.body!r}>"

    def __eq__(self, other):
        if isinstance(other, Equation):
            return (
                self.name == other.name
                and self.patterns == other.patterns
                and self.body == other.body
            )
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Equation, self.name, self.patterns, self.body))

    @property
    def bindings(self) -> Iterator[str]:
        """The names bound in the arguments"""
        for pattern in self.patterns:
            if isinstance(pattern, str) and pattern != "_":
                yield pattern
            elif isinstance(pattern, ConsPattern):
                yield from pattern.bindings


LocalDefinition = Union[Equation, TypeEnvironment]
ValueDefinitions = Mapping[str, List[Equation]]


@dataclass(init=False, unsafe_hash=True)
class ConcreteLet(AST):
    """The concrete representation of a let/where expression."""

    definitions: Tuple[LocalDefinition, ...]  # noqa
    body: AST

    def __init__(self, definitions: Sequence[LocalDefinition], body: AST) -> None:
        self.definitions = tuple(definitions)
        self.body = body

    @memoized_property
    def ast(self) -> _LetExpr:
        return self.compile()

    @memoized_property
    def value_definitions(self) -> ValueDefinitions:
        """The function definitions."""
        return fst(self._definitions)

    @memoized_property
    def local_environment(self) -> TypeEnvironment:
        return snd(self._definitions)

    @memoized_property
    def _definitions(self) -> Tuple[ValueDefinitions, TypeEnvironment]:
        localenv: TypeEnvironment = {}
        defs: MutableMapping[str, List[Equation]] = {}  # noqa
        for dfn in self.definitions:
            if isinstance(dfn, Equation):
                equations = defs.setdefault(dfn.name, [])
                equations.append(dfn)
            elif isinstance(dfn, dict):
                localenv.update(dfn)  # type: ignore
            else:
                assert False, f"Unknown definition type {dfn!r}"
        return defs, localenv

    def compile(self) -> _LetExpr:
        r"""Build a Let/Letrec from a set of equations and a body.

        We need to decide if we issue a Let or a Letrec: if any of declared
        names appear in the any of the bodies we must issue a Letrec,
        otherwise issue a Let.

        Also we need to convert function-patterns into Lambda abstractions::

           let id x = ...

        becomes::

           led id = \x -> ...

        """
        from xotl.fl.graphs import Graph
        from xotl.fl.match import FunctionDefinition

        # Type checking letrecs don't generalize definitions, we could end up
        # in a situation like the one described in [Mycroft1984] -- see the
        # test `test_conflicting_uses_of_non_generalized_map`.
        #
        # The solution is to first do a dependency analysis of the symbols in
        # the ContreteLet definition and rewrite the definition into several
        # nested Let/Letrec.
        #
        # We create a graph where nodes are (essentially) the names defined in
        # the ConcreteLet and there's an edge from name A to name B, if B is
        # used free in the RHS of A.
        #
        nodes = {}
        for name, equations in self.value_definitions.items():
            nodes[name] = _LetGraphNode(name, tuple(equations))
        graph: Graph[_LetGraphNode] = Graph()
        for node in nodes.values():
            graph.add_node(node)
            for dependency in node.dependencies:
                if dependency in nodes:
                    graph.add_edge(node, nodes[dependency])
        #
        # After the graph is created; we compute the Strongly Connected
        # Components (SCC).  Each SCC will be a bundle of mutually-recursive
        # nodes.
        #
        components = []
        components_index = {}
        for scc in graph.get_sccs():
            component = _ComponentNode(tuple(scc))
            for name in component.names:
                components_index[name] = component
            components.append(component)
        del nodes, graph
        #
        # Each SCC has the names that must be kept together.  But a node may
        # depend on another one in a different SCC, so there's still some
        # order we need to respect: Construct another graph, where the nodes
        # are the SCCs and there's an edge from a node C to D if any of names
        # in C depends on any of the names in D (this graph is guaranteed to
        # have no cycles, aka a DAG).
        #
        dag: Graph[_ComponentNode] = Graph()
        for component in components:
            dag.add_node(component)
            for dep in component.other_dependencies:
                if dep in components_index:
                    dag.add_edge(component, components_index[dep])
        #
        # Construct several nested Let/Letrec nodes following the reversed
        # topological sort of the DAG.  But we collapse the components with
        # the same score: those has no mutual dependencies between them and
        # thus introduce no generalization problem.
        #
        body: _LetExpr = self.body  # type: ignore
        for score, collapsable in groupby(
            dag.get_topological_order(reverse=True, with_score=True), key=snd
        ):
            component = _ComponentNode.union(*(comp for comp, _ in collapsable))
            defs = {node.name: FunctionDefinition(node.equations) for node in component.nodes}
            compiled = {name: dfn.compile() for name, dfn in defs.items()}
            if component.recursive:
                klass: Class[_LetExpr] = Letrec
            else:
                klass = Let
            body = klass(
                compiled,
                body,
                {k: v for k, v in self.local_environment.items() if k in component.names},
            )
        return body


@dataclass(unsafe_hash=True)
class _LetGraphNode:
    name: str
    equations: Sequence[Equation]

    @property
    def dependencies(self):
        from functools import reduce
        from operator import or_

        return reduce(or_, (set(find_free_names(eq)) for eq in self.equations), set())


@dataclass(unsafe_hash=True)
class _ComponentNode:
    nodes: Sequence[_LetGraphNode]

    @property
    def names(self):
        return {node.name for node in self.nodes}

    @property
    def dependencies(self):
        from functools import reduce
        from operator import or_

        return reduce(or_, (node.dependencies for node in self.nodes), set())

    @property
    def other_dependencies(self):
        names = self.names
        return {dep for dep in self.dependencies if dep not in names}

    @property
    def recursive(self):
        deps = self.dependencies
        return any(name in deps for name in self.names)

    def __eq__(self, other):
        if isinstance(other, _ComponentNode):
            return self.names == other.names
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, _ComponentNode):
            return _ComponentNode(tuple(self.nodes) + tuple(other.nodes))
        else:
            return NotImplemented

    def union(self, *others) -> "_ComponentNode":
        from functools import reduce
        from operator import or_

        return reduce(or_, others, self)


class Case(ILC):
    """The case expression.

    Part of the intermediate language.  ConcreteLet, if using pattern matching
    may get translated to case expressions.

    """

    def __init__(self, expr: ILC, branches: Sequence[Tuple["CaseBranch", ILC]]) -> None:
        pass


class CaseBranch:
    pass


@dataclass
class LiteralBranch(CaseBranch):
    value: Literal

    def __init__(self, value: Literal) -> None:
        self.value = value


@dataclass
class ConstructorBranch(CaseBranch):
    datacons: DataCons

    @property
    def params(self):
        from xotl.fl.utils import namesupply

        return list(namesupply(limit=len(self.datacons.args)))

    @property
    def cons(self):
        return self.datacons.name

    def __repr__(self):
        if self.params:
            params = " ".join(map(str, self.params))
            return f"{{{self.cons} {params}}}"
        else:
            return f"{{{self.cons}}}"
