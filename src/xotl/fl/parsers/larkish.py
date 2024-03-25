#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import os.path
from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable

from lark import Lark, Token, Transformer, v_args
from xotl.fl.ast.expressions import Identifier, Literal, build_application, build_list_expr
from xotl.fl.ast.types import (
    ConstrainedType,
    ListTypeCons,
    TupleTypeCons,
    Type,
    TypeCons,
    TypeConstraint,
    TypeRecord,
    TypeSchema,
    TypeVariable,
)
from xotl.fl.builtins import NumberType


class LexerHelper:
    """Provides functions the lexer alone cannot do.

    Introduces an _END token at points where the lexer already saw a
    block-beginning token (BLOCK_BEGIN_types) and reaches a token that leaves
    the indentation mark of the block.

    """

    BLOCK_END_type = "_END"
    BLOCK_BEGIN_types = (
        "KEYWORD_WHERE",
        "KEYWORD_DATA",
        "KEYWORD_CLASS",
        "KEYWORD_INSTANCE",
    )

    def _process(self, stream: Iterable[Token]) -> Iterable[Token]:
        stack: Deque[Token] = deque([])

        last_line = 0
        for token in stream:
            if token.type == "_NL":
                # +1 because columns in lark start at 1.
                column = len(token.value.split("\n")[-1]) + 1
                while stack and column <= stack[-1].column:
                    tk = stack.pop()
                    yield Token.new_borrow_pos(self.BLOCK_END_type, tk.value, token)

            if token.type in self.BLOCK_BEGIN_types:
                stack.append(token)
                yield token
            else:
                yield token
            last_line = token.end_line or token.line
        while stack:
            token = stack.pop()
            t = Token.new_borrow_pos(self.BLOCK_END_type, token.value, token)
            t.line = last_line + 1
            yield t

    def process(self, stream: Iterable[Token]) -> Iterable[Token]:
        yield from self._process(stream)


class ASTBuilder(Transformer):
    @v_args(tree=True)
    def type_variable(self, tree):
        token: Token = tree.children[0]
        return TypeVariable(token.value)

    @v_args(tree=True)
    def type_cons(self, tree):
        token: Token = tree.children[0]
        return TypeCons(token.value)

    @v_args(tree=True)
    def type_app_expression(self, tree):
        f, *factors = tree.children
        if isinstance(f, TypeVariable):
            f = TypeCons(f.name)
        assert isinstance(f, TypeCons)
        return TypeCons(f.cons, f.subtypes + tuple(factors), binary=f.binary)

    @v_args(tree=True)
    def type_function_expr(self, tree):
        # The type_function_expr is written as 'type_term (_arrow _NL?
        # _type_function_expr)+'; so we get a list [type, ARROW, type, ARROW, type, ...].
        assert all(
            isinstance(t, Type) or (isinstance(t, Token) and t.type == "ARROW")
            for t in tree.children
        )
        types = list(t for t in tree.children if isinstance(t, Type))
        types.reverse()  # reverse to get right-associativity
        t1, t2, *rest = types
        result = t2 >> t1
        for t in rest:
            result = t >> result
        return result

    @v_args(inline=True)
    def type_factor_enclosed_type_expr(self, _lparen, result, _rparen):
        return result

    @v_args(tree=True)
    def type_constraint(self, tree):
        name, var = tree.children
        assert isinstance(name, Token) and name.type == "UPPER_IDENTIFIER"
        assert isinstance(var, TypeVariable)
        return TypeConstraint(name, var)

    @v_args(tree=True)
    def type_expr_no_constraints(self, tree):
        schema, expr = tree.children
        assert isinstance(schema, TypeSchema) and schema.type_ is None  # type: ignore
        assert isinstance(expr, Type)
        schema.type_ = expr
        return schema

    @v_args(meta=True)
    def type_constraints(self, children, meta):
        *types, _fatarrow = children
        assert isinstance(_fatarrow, Token) and _fatarrow.type == "FATARROW"
        assert all(isinstance(t, TypeConstraint) for t in types)
        return types

    @v_args(tree=True)
    def type_expr_no_schema(self, tree):
        constraints, type_expr = tree.children
        return ConstrainedType((), type_expr, constraints)

    @v_args(meta=True)
    def type_schema(self, children, meta):
        forall, *identifiers = children
        assert isinstance(forall, Token) and forall.type == "KEYWORD_FORALL"
        assert all(isinstance(i, Token) and i.type == "LOWER_IDENTIFIER" for i in identifiers)
        # NB: Return a partially built TypeSchema with a type.
        return TypeSchema((i.value for i in identifiers), None)  # type: ignore

    @v_args(tree=True)
    def type_expr(self, tree):
        partial_schema, type_ = tree.children
        if isinstance(type_, ConstrainedType):
            type_.generics = partial_schema.generics
            return type_
        else:
            partial_schema.type_ = type_
            return partial_schema

    @v_args(inline=True)
    def type_factor_list(self, type_expr):
        return ListTypeCons(type_expr)

    @v_args(inline=True)
    def type_factor_tuple(self, *types):
        assert all(isinstance(t, Type) for t in types)
        return TupleTypeCons(*types)

    @v_args(tree=True)
    def type_factor_record(self, tree):
        fields = tree.children
        assert all(isinstance(f, record_type_item) for f in fields)
        if len({f.name for f in fields}) != len(fields):
            raise ValueError(
                f"Duplicated fields in record type at line {tree.line}, "
                f"column {tree.column} in {tree!r}"
            )
        return TypeRecord({f.name: f.type_ for f in fields})

    @v_args(inline=True)
    def record_type_item(self, name, _colon, type_):
        assert isinstance(name, Token)
        assert isinstance(type_, Type)
        return record_type_item(name.value, type_)

    @v_args(tree=True)
    def simple_list_expr(self, tree):
        return build_list_expr(*tree.children)

    @v_args(tree=True)
    def application(self, tree):
        return build_application(*tree.children)

    # We use the following for all expr_termN rules.
    @v_args(inline=True)
    def _arith_exprs(self, term1, operator, term2):
        return build_application(operator, term1, term2)

    expr_term0 = expr_term1 = expr_term2 = expr_term6 = _arith_exprs
    expr_term7 = expr_term9 = _arith_exprs

    @v_args(inline=True)
    def _operator(self, token):
        return Identifier(token.value)

    infixr_operator_2 = infixl_operator_6 = _operator
    infixl_operator_7 = infixr_operator_9 = _operator
    enclosed_operator = _operator

    @v_args(inline=True)
    def identifier(self, token):
        return Identifier(token.value)

    @v_args(inline=True)
    def number(self, token):
        return Literal(eval(token.value), NumberType)


@dataclass
class record_type_item:
    name: str
    type_: Type


type_expr_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="type_expr",
    debug=True,
    postlex=LexerHelper(),
)
expr_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="expr",
    debug=True,
    postlex=LexerHelper(),
)
program_parser = Lark.open(
    os.path.join(os.path.dirname(__file__), "grammar.lark"),
    lexer="standard",
    propagate_positions=True,
    start="program",
    debug=True,
    postlex=LexerHelper(),
)
