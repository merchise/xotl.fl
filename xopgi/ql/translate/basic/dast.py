#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Odoo Domain Abstract Syntax Tree.

The Python AST we get from the predicate is, in our view, a more Concrete
Syntax Tree.  The Odoo Domain AST can only represent expression which are
translatable to Odoo Domain.

'''

from collections import namedtuple

_Leaf = namedtuple('Leaf', ('column', 'operator', 'value'))


class Leaf(_Leaf):
    def get_domain(self):
        return [tuple(self)]


class Node:
    pass


class BinaryNode(Node):
    def __init__(self, type, operands):
        assert len(operands) >= 2
        assert all(isinstance(op, (Node, Leaf)) for op in operands)
        self.type = type
        self.operands = operands

    def get_domain(self):
        others = [
            item
            for op in self.operands
            for item in op.get_domain()
        ]
        return [self.type] * (len(self.operands) - 1) + others


class UnaryNode(Node):
    def __init__(self, type, operand):
        assert isinstance(operand, (Node, Leaf))
        self.type = type
        self.operand = operand

    def get_domain(self):
        return [self.type] + self.operand.get_domain()
