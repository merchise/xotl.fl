#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Implements Tarjan's algorithm__ to find a Graph's Strongly Connected
Components.

__ https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm

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

    def add_edge(self, from_: T, to_: T) -> None:
        links = self.nodes.setdefault(from_, set())
        links.add(to_)

    def add_many(self, from_: T, to_: AbstractSet[T]):
        links = self.nodes.setdefault(from_, set())
        links |= to_

    def get_strongly_connected_components(self) -> List[AbstractSet[T]]:

        def _find_scc(node):
            nonlocal index
            indexed[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            for link in self.nodes.get(node, []):
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
