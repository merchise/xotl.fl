#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xotl.fl.tarjans import SimpleGraph


def test_scc():
    # The Graph shown the Wikipedia page
    # (https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm)
    graph = SimpleGraph()
    graph.add_many(1, {2, 3})
    graph.add_many(2, {3})
    graph.add_many(3, {1})
    graph.add_many(4, {2, 3, 5})
    graph.add_many(5, {4, 6})
    graph.add_many(6, {3, 7})
    graph.add_many(7, {6})
    graph.add_many(8, {5, 7, 8})
    sccs = graph.get_strongly_connected_components()
    assert len(sccs) == 4
    assert {1, 2, 3} in sccs
    assert {4, 5} in sccs
    assert {6, 7} in sccs
    assert {8} in sccs
