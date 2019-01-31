#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Implements algorithms for Direct Graphs.

'''
from typing import AbstractSet, Deque, List, MutableMapping, Set
from typing import Generic, TypeVar
from collections import deque


T = TypeVar('T')


class Graph(Generic[T]):
    nodes: MutableMapping[T, Set[T]]

    def add_edge(self, from_: T, to_: T) -> None:
        ...

    def add_many(self, from_: T, to_: AbstractSet[T]) -> None:
        ...

    def get_strongly_connected_components(self) -> List[AbstractSet[T]]:
        ...


class SimpleGraph(Graph[T]):
    def __init__(self) -> None:
        self.nodes = {}

    def __getitem__(self, node: T) -> AbstractSet[T]:
        return self.nodes.get(node, set())

    def add_edge(self, from_: T, to_: T) -> None:
        links = self.nodes.setdefault(from_, set())
        links.add(to_)

    def add_many(self, from_: T, to_: AbstractSet[T]):
        links = self.nodes.setdefault(from_, set())
        links |= to_

    def get_topological_order(self) -> List[T]:
        '''Find a topological sort of the nodes.

        If the graph contains cycles, raise a RuntimeError.

        '''
        def raise_on_cycle(func):
            '''Make `func` to raise on the first recursive call with the same
            argument.

            '''
            stack = deque([])

            def inner(node):
                if node in stack:
                    raise NonDAGError(
                        'Cycle detected: %r' % (list(stack) + [node])
                    )
                else:
                    stack.append(node)
                    try:
                        return func(node)
                    finally:
                        stack.pop()
            return inner

        @raise_on_cycle
        def score(node):
            links = self.nodes.get(node, [])
            if links:
                return max(score(dep) for dep in links) + 1
            else:
                return 0

        return list(sorted(self.nodes.keys(), key=score))

    def get_sccs(self) -> List[AbstractSet[T]]:
        '''Find the Strongly Connected Components.

        This is an implementation of Tarjan's Algorithm [Tarjan1972]_.

        '''
        def _find_scc(node):
            nonlocal index
            indexed[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            for link in self[node]:
                if link not in indexed:
                    _find_scc(link)
                    lowlinks[node] = min(lowlinks[node], lowlinks[link])
                elif link in stack:
                    # Successor link is in stack and hence in the current SCC
                    # If link is not on stack, then (node, link) is a
                    # cross-edge in the DFS tree and must be ignored.
                    #
                    # The next line may look odd - but is correct.  It says
                    # indexed[link] and not lowlinks[link]; that is deliberate
                    # and from the original paper
                    lowlinks[node] = min(lowlinks[node], indexed[link])
            if indexed[node] == lowlinks[node]:
                w = stack.pop()
                scc = {w}
                while w != node:
                    w = stack.pop()
                    scc.add(w)
                result.append(scc)

        index = 0
        indexed: MutableMapping[T, int] = {}
        lowlinks: MutableMapping[T, int] = {}
        result: List[Set[T]] = []
        stack: Deque[T] = deque([])
        for node in self.nodes:
            if node not in indexed:
                _find_scc(node)
        return result  # type: ignore


class NonDAGError(RuntimeError):
    pass
