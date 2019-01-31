#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest

from xotl.fl.graphs import SimpleGraph


graph = SimpleGraph()
graph.add_many(1, {2, 3})
graph.add_many(2, {3})
graph.add_many(3, {1})
graph.add_many(4, {2, 3, 5})
graph.add_many(5, {4, 6})
graph.add_many(6, {3, 7})
graph.add_many(7, {6})
graph.add_many(8, {5, 7, 8})


def test_scc():
    # The Graph shown the Wikipedia page
    # (https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm)
    sccs = graph.get_sccs()
    assert len(sccs) == 4
    assert {1, 2, 3} in sccs
    assert {4, 5} in sccs
    assert {6, 7} in sccs
    assert {8} in sccs


def test_topo_dag():
    # Take the min node to be the *name* of each SCC
    sccs = {
        min(scc): tuple(scc)
        for scc in graph.get_sccs()
    }
    index = {
        node: name
        for name, scc in sccs.items()
        for node in scc
    }
    # A DAG implied the SCC; we create the DAG of the *names* in sccs.
    newgraph = SimpleGraph()
    for name, scc in sccs.items():
        for node in scc:
            links = {index[l] for l in graph[node] if l not in scc}
            newgraph.add_many(name, links)
    # The DAG should be:
    #
    #    1 <----- 6 <---.
    #    ^        ^     |
    #    | ______/      |
    #    |/             |
    #    4 <----------- 8
    #
    # and it has a single topological order
    order = newgraph.get_topological_order()
    assert order == [1, 6, 4, 8]


def test_top_cycles():
    with pytest.raises(RuntimeError):
        graph.get_topological_order()
