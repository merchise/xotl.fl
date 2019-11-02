#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from textwrap import dedent

from xotl.fl.ast.adt import DataCons, DataType
from xotl.fl.ast.expressions import Identifier, Let, build_application, build_lambda
from xotl.fl.ast.pattern import ConsPattern, Equation
from xotl.fl.ast.types import Type, TypeScheme
from xotl.fl.parsers.expressions import parse as parse_expression
from xotl.fl.parsers.larkish import program_parser


def parse(source):
    return program_parser.parse(dedent(source).strip())


def test_simple_one_definition():
    assert parse("id x = x")


def test_simple_functions_definition():
    assert parse(
        """
        id x = x

        const :: a -> b -> a
        const a x = a
        """
    )


def test_typedecls():
    assert (
        parse(
            """
            id :: a -> a
            const :: a -> b -> a
            """
        )
        == [
            {"id": TypeScheme.from_str("a -> a")},
            {"const": TypeScheme.from_str("a -> b -> a")},
        ]
    )


def test_datatype_simple():
    assert parse("data Then a = Then a") == [
        DataType(
            "Then", Type.from_str("Then a"), [DataCons("Then", [Type.from_str("a")])]
        )
    ]


def test_datatype_tree():
    assert parse("data Tree a = Leaf a | Branch (Tree a) (Tree a)") == [
        DataType(
            "Tree",
            Type.from_str("Tree a"),
            [
                DataCons("Leaf", [Type.from_str("a")]),
                DataCons("Branch", [Type.from_str("Tree a"), Type.from_str("Tree a")]),
            ],
        )
    ]


def test_datatype_simple2():
    assert (
        parse(
            """
            data Then a = Then a
            data Else a = Else a
            """
        )
        == [
            DataType(
                "Then",
                Type.from_str("Then a"),
                [DataCons("Then", [Type.from_str("a")])],
            ),
            DataType(
                "Else",
                Type.from_str("Else a"),
                [DataCons("Else", [Type.from_str("a")])],
            ),
        ]
    )


def test_simple_if_program():
    parse(
        """
        if :: Bool -> a -> a -> a
        if True x _  = x
        if False _ x = x
        """,
        debug=True,
    ) == [
        {"id": TypeScheme.from_str("Bool -> a -> a -> a")},
        Equation(
            "if",
            [Identifier("True"), Identifier("x"), Identifier("_")],
            Identifier("x"),
        ),
        Equation(
            "if",
            [Identifier("False"), Identifier("_"), Identifier("x")],
            Identifier("x"),
        ),
    ]


def test_if_program():
    parse(
        """
        data Then a = Then a
        data Else a = Else a

        if :: Bool -> Then a -> Else a -> a
        if True (Then x) _  = x
        if False _ (Else x) = x

        """,
        debug=True,
    )


@pytest.mark.xfail(reason="Failing to split equations")
def test_large_definitions():
    assert (
        parse(
            """
            name =
               let id x = x in id
            """,
            debug=True,
        )
        == parse("name = let id x = x in id")
    )


def test_defs_operators():
    assert parse(
        """
        (.) :: (b -> c) -> (a -> b) -> a -> c
        (.) f g x = f (g x)
        """
    )


def test_matching_lists():
    assert parse(
        """
        head x : _ = x

        tail _:xs = xs

        second _ : x : _ = x
        third  _:_:x:_ = x

        insert x [] = x:[]
        insert x y:xs = x:y:xs

        """
    )

    assert parse(
        """
        reverse [] = []

        -- The ((x:xs)) is just the same as x:xs but with
        -- redundant enclosing parenthesis

        reverse (x:xs) = (reverse xs):x:[]
        """
    )

    assert parse("second f:s:xs = s") == [
        Equation(
            "second",
            [ConsPattern(":", ["f", ConsPattern(":", ["s", "xs"])])],
            Identifier("s"),
        )
    ]


@pytest.mark.xfail(reason="Incomplete pattern matching")
def test_local_definitions():
    # Taken from the paper 'Practical type inference for arbitrary-rank types'
    # by Peyton Jones, Simon et al.
    assert (
        parse(
            """
            foo :: ([Bool], [Char])
            foo = let f :: (forall a. [a] -> [a]) -> ([Bool], [Char])
                      f x = (x [True, False], x ['a', 'b'])
            in f reverse
            """
        )
        == [
            {"foo": TypeScheme.from_str("([Bool], [Char])")},
            Equation(
                "foo",
                [],
                Let(
                    {
                        "f": build_lambda(
                            ["x"], parse_expression("(x [True, False], x ['a', 'b'])")
                        )
                    },
                    build_application("f", Identifier("reverse")),
                    {
                        "f": TypeScheme.from_str(
                            "(forall a. [a] -> [a]) -> ([Bool], [Char])"
                        )
                    },
                ),
            ),
        ]
    )


def test_parse_typeclass():
    parse(
        """
        class Eq a where
          (==) :: a -> a -> Bool
          (==) a b = not (a /= b)

          (/=) :: a -> a -> Bool
          (/=) a b = not (a == b)

        class Eq a => Ord a where
          (<) :: a -> a -> Bool
          (<) a b = not (a >= b)

          (>) :: a -> a -> Bool
          (>) a b = not (a <= b)

          (<=) :: a -> a -> Bool
          (<=) a b = a < b `or` a == b

          (>=) :: a -> a -> Bool
          (>=) a b = a > b `or` a == b
        """
    )


def test_valid_instance():
    parse(
        """
        instance Eq a => Eq [a] where
           (==) [] []     = True
           (==) x:xs y:ys = x == y `and` xs == ys

        instance Eq a, Eq b => Eq (Either a b) where
           (==) (Left a) (Left b)   = a == b
           (==) (Right a) (Right b) = a == b
           (==) _         _         = False
        """
    )


def test_instance_basic_type():
    parse(
        """
        instance Eq Number where
           (==) = _eq_number

        """
    )


def test_parse_deriving_single_typeclass():
    parse(
        """
        data Bool = True
                  | False
          deriving Eq
        """
    )


def test_parse_deriving_several_typeclasses():
    parse("data Bool = True | False deriving (Eq, Ord)")


def test_adt_operators():
    parse(
        """
        data Qual t = [Pred] :=> t
             deriving Eq
        """
    )
