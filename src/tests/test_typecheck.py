#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest

from hypothesis import given, settings

from xotl.fl.builtins import (
    NumberType,
    CharType,
    StringType,
    BoolType,
    builtins_env,
    BuiltinEnvDict,
)
from xotl.fl.parsers.expressions import parse as parse_expression
from xotl.fl.ast.types import Type, TypeScheme, find_tvars
from xotl.fl.typecheck import typecheck, sidentity, unify, EMPTY_TYPE_ENV

from xotl.fl.testing.strategies.trees import welltyped_expressions
from xotl.fl.testing.strategies.tools import TestTypingEnvironment


@settings(max_examples=20)
@given(welltyped_expressions)
def test_generation_of_welltyped_expressions(expr):
    typecheck(expr, TestTypingEnvironment())


def test_from_literals():
    phi, t = typecheck(parse_expression(r"let x = 1 in x"), EMPTY_TYPE_ENV)
    assert phi is sidentity
    assert t == NumberType

    phi, t = typecheck(parse_expression(r'let x = "1" in x'), EMPTY_TYPE_ENV)
    assert phi is sidentity
    assert t == StringType

    phi, t = typecheck(parse_expression(r"let x = '1' in x"), EMPTY_TYPE_ENV)
    assert phi is sidentity
    assert t == CharType

    # true and false are not recognized as booleans by the parser, so let's
    # provide them as part the env.
    phi, t = typecheck(parse_expression(r"let x = True in x"), builtins_env)
    assert phi is sidentity
    assert t == BoolType

    phi, t = typecheck(parse_expression(r"let x = False in x"), builtins_env)
    assert phi is sidentity
    assert t == BoolType


def test_combinators():
    # Since they're closed expressions they should type-check
    K = parse_expression(r"\a b -> a")
    TK = Type.from_str("a -> b -> a")
    phi, t = typecheck(K, EMPTY_TYPE_ENV)
    # we can't ensure TK == t, but they must unify, in fact they
    # must be same type with alpha-renaming.
    unify(TK, t)

    S = parse_expression(r"\x y z -> x z (y z)")
    TS = Type.from_str("(a -> b -> c) -> (a -> b) -> a -> c")
    phi, t = typecheck(S, EMPTY_TYPE_ENV)
    unify(TS, t)

    # But the paradoxical combinator doesn't type-check
    Y = parse_expression(r"\f -> (\x -> f (x x))(\x -> f (x x))")
    with pytest.raises(TypeError):
        phi, t = typecheck(Y, EMPTY_TYPE_ENV)


def test_paradox_omega():
    r"Test `(\x -> x x)` does not type-check"
    with pytest.raises(TypeError):
        typecheck(parse_expression(r"\x -> x x"), EMPTY_TYPE_ENV)


def test_hidden_paradox_omega_letrec():
    code = r"""
    let id x = x
        prxI :: forall b c. (free -> (b -> b) -> c) -> c
        prxI c  = c free id
        p1 x y  = x
        p2 :: x -> y -> y
        p2 x y  = y
    in prxI p2 (prxI p2)
    """
    env = BuiltinEnvDict({"free": TypeScheme.from_str("free", generics=[])})
    typecheck(parse_expression(code), env)


def test_hidden_paradox_omega_let():
    code = r"""
    let prxI c  = c free id
        p1 x y  = x
        p2 x y  = y
    in prxI p2 (prxI p2)
    """
    env = BuiltinEnvDict(
        {
            "free": TypeScheme.from_str("f", generics=[]),
            "id": TypeScheme.from_str("a -> a"),
        }
    )
    typecheck(parse_expression(code), env)


def test_hidden_paradox_omega_2():
    code = """
    let id x    = x
        prxI c  = c x id
        p1 x y  = x
        p2 x y  = y
    in prxI p1 (prxI p1)
    """
    env = BuiltinEnvDict({"x": TypeScheme.from_str("a", generics=[])})
    with pytest.raises(TypeError):
        typecheck(parse_expression(code), env)


def test_basic_builtin_types():
    with pytest.raises(TypeError):
        # not :: Bool -> Bool, but passed a Number
        typecheck(parse_expression("not 0"), builtins_env)

    phi, t = typecheck(parse_expression("not True"), builtins_env)
    assert t == BoolType
    phi, t = typecheck(parse_expression("not False"), builtins_env)
    assert t == BoolType

    userfuncs = {"toString": TypeScheme.from_str("a -> [Char]")}
    phi, t = typecheck(
        parse_expression("either toString id"), dict(builtins_env, **userfuncs)
    )
    assert len(find_tvars(t)) == 1
    unify(Type.from_str("Either a [Char] -> [Char]"), t)


def test_composition():
    phi, t = typecheck(parse_expression("let id x = x in id . id"), builtins_env)
    unify(Type.from_str("a -> a"), t)
    unify(Type.from_str("(a -> a) -> (a -> a)"), t)

    phi, t = typecheck(parse_expression("Left . Right"), builtins_env)
    unify(Type.from_str("a -> Either (Either b a) c"), t)

    # In our case, (+) is not polymorphic (Number is not a type-class), so it
    # can't be composed with Either.
    with pytest.raises(TypeError):
        typecheck(parse_expression("(+) . Left"), builtins_env)
    # If we had a polymorphic (+), it would be composable
    phi, t = typecheck(
        parse_expression("(+) . Left"),
        dict(builtins_env, **{"+": TypeScheme.from_str("a -> a -> a")}),
    )
    unify(Type.from_str("a -> Either a b -> Either a b"), t)
    phi, t = typecheck(
        parse_expression("(+) . Right"),
        dict(builtins_env, **{"+": TypeScheme.from_str("a -> a -> a")}),
    )
    unify(Type.from_str("b -> Either a b -> Either a b"), t)


def test_typecheck_recursion():
    then = TypeScheme.from_str("a -> Then a")
    else_ = TypeScheme.from_str("a -> Else a")
    if_then_else = TypeScheme.from_str("Bool -> Then a -> Else a -> a")
    Nil = TypeScheme.from_str("[a]")
    tail = TypeScheme.from_str("[a] -> [a]")
    matches = TypeScheme.from_str("a -> b -> Bool")
    add = TypeScheme.from_str("a -> a -> a")
    env = BuiltinEnvDict(
        {
            "if": if_then_else,
            "then": then,
            "else": else_,
            "matches": matches,
            "Nil": Nil,
            "+": add,
            "tail": tail,
        }
    )
    phi, t = typecheck(
        # I need to put parenthesis because of the failure of precedence we
        # have; otherwise we could use $ to connect if then and else (they are
        # still functions): 'if cond $ then result $ else other_result'.
        # `matches` would be a simple pattern matching function.  The real
        # function would have to operate on values and patterns (which are no
        # representable here.)
        parse_expression(
            """
            let count xs = if (xs `matches` Nil) \
                              (then 0) \
                              (else let ts = tail xs in 1 + (count ts))
            in count
            """
        ),
        env,
    )
    # The count functions counts the number of elements.
    unify(Type.from_str("[a] -> Number"), t)


def test_type_checking_tuples():
    typecheck(parse_expression("(1, 2, 3)"), builtins_env)


def test_local_type_annotation_let():
    phi, t = typecheck(
        parse_expression(
            """let g = [1, 2, 3]
               in reverse g"""
        ),
        BuiltinEnvDict(
            {
                "reverse": TypeScheme.from_str("[a] -> [a]"),
                ":": TypeScheme.from_str("a -> [a] -> [a]"),
            }
        ),
    )
    assert t == Type.from_str("[Number]")

    phi, t = typecheck(
        parse_expression(
            """let g :: [Number]
                   g = []
               in reverse g"""
        ),
        BuiltinEnvDict(
            {
                "reverse": TypeScheme.from_str("[a] -> [a]"),
                ":": TypeScheme.from_str("a -> [a] -> [a]"),
            }
        ),
    )
    assert t == Type.from_str("[Number]")

    phi, t = typecheck(
        parse_expression(
            """let g :: [a]
                   g = [1, 2, 3]
                in reverse g"""
        ),
        BuiltinEnvDict(
            {
                "reverse": TypeScheme.from_str("[a] -> [a]"),
                ":": TypeScheme.from_str("a -> [a] -> [a]"),
            }
        ),
    )
    assert t == Type.from_str("[Number]")

    with pytest.raises(TypeError):
        typecheck(
            parse_expression(
                """let g :: [Char]
                       g = [1, 2, 3]
                   in reverse g"""
            ),
            BuiltinEnvDict(
                {
                    "reverse": TypeScheme.from_str("[a] -> [a]"),
                    ":": TypeScheme.from_str("a -> [a] -> [a]"),
                }
            ),
        )


def test_local_type_annotation_letrec():
    phi, t = typecheck(
        parse_expression(
            """let count :: Number -> [Number]
                   count x = x:count (x + 1)
                   g :: [a]
                   g = count 1
                   g2 = reverse g
                in g2"""
        ),
        BuiltinEnvDict(
            {
                "reverse": TypeScheme.from_str("[a] -> [a]"),
                ":": TypeScheme.from_str("a -> [a] -> [a]"),
                "+": TypeScheme.from_str("a -> a -> a"),
            }
        ),
    )
    assert t == Type.from_str("[Number]")

    with pytest.raises(TypeError):
        typecheck(
            parse_expression(
                """let count :: Number -> [Number]
                       count x = x:count (x + 1)
                       g :: [Char]
                       g = count 1
                    in reverse g"""
            ),
            BuiltinEnvDict(
                {
                    "reverse": TypeScheme.from_str("[a] -> [a]"),
                    ":": TypeScheme.from_str("a -> [a] -> [a]"),
                    "+": TypeScheme.from_str("a -> a -> a"),
                }
            ),
        )


def test_ill_typed_match():
    with pytest.raises(TypeError):
        typecheck(
            parse_expression(
                """let g x = "a"
                       g x = 1
                   in g"""
            )
        )


@pytest.mark.xfail(reason="Incomplete pattern matching type-checking")
def test_ill_count1():
    with pytest.raises(TypeError):
        typecheck(
            parse_expression(
                """let count [] = 0
                       count 2  = 1
                   in count"""
            )
        )


def test_regression_missing_dynamic_builtins():
    phi, t = typecheck(parse_expression("let pair x y = (x, y) in pair 1 2"))
    assert unify(t, Type.from_str("(Number, Number)"))


def test_regression_typing_if():
    expr = parse_expression(
        r"""
        let map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
        in map
        """
    )
    typecheck(expr, builtins_env)


#
# The following examples are extracted from [Mycroft1984].
#
# The problem we currently (2019-06-06) face is that `map` is not generalized;
# the HM system assigns a new type variable to 'map' when it's found in the
# letrec (it's a letrec because we use map in the RHS of other definitions),
# but the first usage of it inside 'squarelist' unifies that variable with
# usage in '\x -> x * x'; and that forces it to become too specific.
#
# As shown below we can easily rewrite that let into a form similar to
# test_resolved_uses_of_non_generalized_map, by doing dependency analysis.
#
# See also the section 6.2.8 of [PeytonJones1987].
#


def test_conflicting_uses_of_non_generalized_map():
    expr = parse_expression(
        r"""
        let map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
            squarelist xs = map (\x -> x * x) xs
            conflict   xs = map (\x -> "" ++ x) xs
        in conflict
        """
    )
    typecheck(expr, builtins_env)


def test_annotated_uses_of_non_generalized_map():
    expr = parse_expression(
        r"""
        let map :: (a -> b) -> [a] -> [b]
            map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
            squarelist xs = map (\x -> x * x) xs
            conflict   xs = map (\x -> "" ++ x) xs
        in conflict
        """
    )
    typecheck(expr, builtins_env)


def test_resolved_uses_of_non_generalized_map():
    # This is the same as test_conflicting_uses_of_non_generalized_map
    # But we have extracted map so that it can become generalized.
    expr = parse_expression(
        r"""
        let map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
        in let squarelist xs = map (\x -> x * x) xs
               conflict   xs = map (\x -> "" ++ x) xs
           in conflict
        """
    )
    typecheck(expr, builtins_env)


def test_parse_with_dependency_analysis_generlizes_map():
    explicit = parse_expression(
        r"""
        let map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
        in let squarelist xs = map (\x -> x * x) xs
               conflict   xs = map (\x -> "" ++ x) xs
           in conflict
        """
    )
    explicit_ast = explicit.ast
    implicit = parse_expression(
        r"""
        let map = \f xs -> if (is_null xs) (then xs) (else (f (head xs):map f (tail xs)))
            squarelist xs = map (\x -> x * x) xs
            conflict   xs = map (\x -> "" ++ x) xs
        in conflict
        """
    )
    implicit_ast = implicit.ast
    assert explicit_ast == implicit_ast


# This test shows that our type-inference algorithm is following HM system;
# which make it put a single non-generalized unification var to the argument
# 'get'; that's why it fails to infer a type for 'get'.  But when we type it
# ourselves, it checks the type correctly.
#
# This test will fail when we move beyond HM.
#
# The road to type-systems was (according to
# http://lhc-compiler.blogspot.com/2016/09/haskell-suite-type-inference.html):
# first HM [Damas1982], then bidirectional type inference [Pierce2000],
# followed by boxy types [Vytiniotis2006] and finalizing with OutsideIn(X)
# [OutsideInX]
#
# I don't know yet which system is best to our needs; but I'm beginning to
# believe it should support extensible type classes and/or records.
def test_HM_does_monomorphic_arguments():
    ast = parse_expression(r"let f get = (get [1,2], get ['a','b','c']) in f")
    with pytest.raises(TypeError):
        typecheck(ast, builtins_env)

    ast = parse_expression(
        r"""
        let f :: (forall a. a -> a) -> (Num, Char)
            f get = (get [1,2], get ['a','b','c'])
          in f
        """
    )
    with pytest.raises(TypeError):
        typecheck(ast, builtins_env)
