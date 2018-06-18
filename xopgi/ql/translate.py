#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import ast
import inspect
from types import LambdaType
from collections import namedtuple


def filtered(predicate, model=None):
    '''Takes a predicate over a single record and produces an Odoo domain.

    Support only comparison of attributes with values.  Not even attributes
    compared to other attributes since this not translatable to Odoo domains.

    Use other functions for more complex predicates.

    If model is not None, it should either the name of the model, a model
    class definition, or a recordset.  In such case you must call within the
    context of a valid Odoo DB environment.  We only use to type-check the
    predicate.

    '''
    from xotl.ql.revenge import Uncompyled
    translator = FilterTranslator(predicate, model=model)
    uncompiler = Uncompyled(predicate, islambda=False)
    qst = uncompiler.qst
    translator.visit(qst)
    return translator.domain


class FilterTranslator(ast.NodeVisitor):
    def __init__(self, predicate, model=None):
        # The predicate MUST have at least a positional argument (which is the
        # subject of the predicate).  We allow for other positional arguments
        # **with defaults**, or kwonly arguments with defaults.
        self.model = model
        self.stack = []
        self.predicate = SimplePredicate(predicate)

    @property
    def domain(self):
        assert len(self.stack) == 1, \
            f'More than one item the in stack: {self.stack!r}'
        top = self.stack.pop()
        get_domain = getattr(top, 'get_domain', lambda: top)
        return get_domain()

    def visit_Compare(self, node):
        if len(node.comparators) != 1:
            raise PredicateSyntaxError('Unsupported multiple comparasion')
        self.visit(node.left)
        left = self.stack.pop()
        self.visit(node.comparators[0])
        right = self.stack.pop()
        self.stack.append(Leaf(left, get_comparator_str(node.ops[0]), right))

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            self.visit(node.operand)
            operand = self.stack.pop()
            self.stack.append(UnaryNode('!', operand))
        else:
            raise PredicateSyntaxError(
                f'Unsupported unary operator {node.op!r}'
            )

    def visit_BoolOp(self, node):
        for expr in node.values:
            self.visit(expr)
        operators = self.stack[-len(node.values):]
        del self.stack[-len(node.values):]
        if isinstance(node.op, ast.And):
            self.stack.append(BinaryNode('&', operators))
        elif isinstance(node.op, ast.Or):
            self.stack.append(BinaryNode('|', operators))
        else:
            assert False

    def visit_Name(self, node):
        self.stack.append(node.id)

    def visit_Attribute(self, node):
        # We only support attributes from names or other attributes.  We also
        # avoid a recursive call (``x.y.z``), because we need to make sure to
        # strip the 'this' of the predicate, but only at the top-level.
        val = node.value
        attrs = [node.attr]
        while isinstance(val, ast.Attribute):
            attrs.append(val.attr)
            val = val.value
        if isinstance(val, ast.Name):
            if val.id != self.predicate.this:
                attrs.append(val.id)
        else:
            raise PredicateSyntaxError(
                f'Unsupported syntax. Predicate: {self.predicate.source!r}'
            )
        self.stack.append('.'.join(reversed(attrs)))

    def visit_Num(self, node):
        self.stack.append(node.n)

    def visit_Str(self, node):
        self.stack.append(node.s)

    def visit_NameConstant(self, node):
        self.stack.append(node.value)


class SimplePredicate:
    '''A simple predicate over a subject.

    `predicate` must be a lamdba function.  It must accept a positional
    argument.  It may have other arguments so long as we can call it passing a
    single positional argument: ``predicate(obj)`` MUST not raise a TypeError.

    '''
    def __init__(self, predicate):
        assert isinstance(predicate, LambdaType)
        spec = inspect.getfullargspec(predicate)
        self.spec = self.validate_spec(spec)
        self.predicate = predicate

    @classmethod
    def validate_spec(cls, spec):
        args_count = len(spec.args or [])
        defaults_count = len(spec.defaults or [])
        if args_count - 1 != defaults_count:
            raise PredicateSyntaxError('Invalid predicate')
        kwonly_count = len(spec.kwonlyargs or [])
        kwonlydefauls_count = len(spec.kwonlydefaults or [])
        if kwonly_count != kwonlydefauls_count:
            raise PredicateSyntaxError('Invalid predicate')
        return spec

    @property
    def this(self):
        return self.spec.args[0]

    @property
    def source(self):
        try:
            return inspect.getsource(self.predicate)
        except OSError:
            return '<error ocurred looking for predicate source>'


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


def get_comparator_str(op):
    if isinstance(op, ast.Eq):
        return '='
    elif isinstance(op, ast.NotEq):
        return '!='
    elif isinstance(op, ast.Lt):
        return '<'
    elif isinstance(op, ast.LtE):
        return '<='
    elif isinstance(op, ast.Gt):
        return '>'
    elif isinstance(op, ast.GtE):
        return '>='
    elif isinstance(op, ast.In):
        return 'in'
    elif isinstance(op, ast.NotIn):
        return 'not in'
    else:
        raise PredicateSyntaxError(f'Unsupported comparison operation {op}')


class PredicateSyntaxError(SyntaxError):
    pass
