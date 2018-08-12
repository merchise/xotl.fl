#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Basic translator for predicates to Odoo domains.

'''
import ast
import inspect
from types import LambdaType
from .dast import Leaf, BinaryNode, UnaryNode


def filtered(predicate):
    '''Translate a predicate over a single record into an Odoo domain.

    The `predicate` must be a lambda function that accepts a positional
    argument.  The name of the positional argument is used to know if we must
    translate an attribute or not:

       >>> filtered(lambda this: this.age < 10)
       [('age', '<', 10)]

    The name 'this' is not included in the domain.

    The allowed semantics of `predicate` match the allowed semantics of the
    Odoo domains.  However, this function allows for certain mismatches in
    semantics:

       >>> filtered(lambda this: this.debit < this.credit)
       [('debit', '<', 'credit')]

    Odoo sees ``'credit'`` as the literal string instead of the name of an
    attribute.  Attributes are only allowed on the left operand of a
    comparison:

       >>> filtered(lambda this: 1 < this.age < 10 == 10)
       ['&', '&', (1, '<', 'age'), ('age', '<', 10), (10, '=', 10)]

    In this case, the ``(1, '<', 'age')`` is incorrect in a Odoo domain.

    Arbitrary expressions can be either fail or be incorrectly translated:

       >>> filtered(lambda this: this.sum/this.count == average)  # doctest: +ELLIPSIS
       Traceback (...)
       ...
       AssertionError: Not just one item the in stack...

    '''
    from xotl.ql.revenge import Uncompyled
    translator = FilterTranslator(predicate)
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
            f'Not just one item the in stack: {self.stack!r}'
        top = self.stack.pop()
        get_domain = getattr(top, 'get_domain', lambda: top)
        return get_domain()

    def visit_Compare(self, node):
        expr = None
        self.visit(node.left)
        left = self.stack.pop()
        for op, right in zip(node.ops, node.comparators):
            self.visit(right)
            right = self.stack.pop()
            leaf = Leaf(left, get_comparator_str(op), right)
            if expr:
                expr = BinaryNode('&', [expr, leaf])
            else:
                expr = leaf
            left = right
        self.stack.append(expr)

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

    def visit_List(self, node):
        for item in reversed(node.elts):
            self.visit(item)
        self.stack.append([self.stack.pop() for _ in range(len(node.elts))])

    def visit_Tuple(self, node):
        for item in reversed(node.elts):
            self.visit(item)
        self.stack.append(tuple(self.stack.pop() for _ in range(len(node.elts))))


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
