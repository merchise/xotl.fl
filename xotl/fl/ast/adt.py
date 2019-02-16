#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Algebraic Data Types.'''
from typing import Sequence, Iterator, Tuple
from collections import ChainMap
from xoutil.objects import memoized_property

from xotl.fl.meta import Symbolic

from xotl.fl.ast.types import (
    Type,
    TypeCons,
    TypeEnvironment,
    TypeScheme,
)


class DataCons:
    '''The syntactical notion a data constructor in the type language.

    '''
    def __init__(self, cons: str, args: Sequence[Type]) -> None:
        self.name = cons
        self.args: Sequence[Type] = tuple(args)

    @property
    def free_type_variables(self):
        from xotl.fl.ast.types import find_tvars
        return {name for type_ in self.args for name in find_tvars(type_)}

    def __repr__(self):
        def _str(x):
            res = str(x)
            if ' ' in res:
                return f'({res})'
            else:
                return res

        names = ' '.join(map(_str, self.args))
        if names:
            return f'<DataCons {self.name} {names}>'
        else:
            return f'<DataCons {self.name}>'

    def __eq__(self, other):
        if isinstance(other, DataCons):
            return self.name == other.name and self.args == other.args
        else:
            return NotImplemented

    def __hash__(self):
        return hash((DataCons, self.name, self.args))


class DataType:
    '''A data type definition.

    A data type defines both a type and several values of that type.

    You should note that `DataCons`:class: is NOT a value.  Therefore these
    are not actual objects carrying values in the running program; but imply
    the compiler (or interpreter) must produce those values and match the
    type.

    '''
    def __init__(self, name: str, type_: TypeCons,
                 defs: Sequence[DataCons],
                 derivations: Sequence[str] = None) -> None:
        assert name == type_.cons
        self.name = name
        self.type_ = type_
        self.dataconses = tuple(defs)
        self.derivations = tuple(derivations or [])
        self._check_non_repeated_datacons()
        self._check_non_existential_vars()
        self._check_non_unused_vars()

    def _check_non_repeated_datacons(self):
        names = {dc.name for dc in self.dataconses}
        if len(names) != len(self.dataconses):
            raise TypeError(f"Repeated data constructor in: {self}")

    def _check_non_existential_vars(self):
        existential = self.dataconses_vars - self.free_type_variables
        if existential:
            svars = ", ".join(map(str, existential))
            raise TypeError(f"Non allowed existential variables: {svars}")

    def _check_non_unused_vars(self):
        unused = self.free_type_variables - self.dataconses_vars
        if unused:
            svars = ", ".join(map(str, unused))
            raise TypeError(f"Unused type variables: {svars}")

    @memoized_property
    def free_type_variables(self):
        from xotl.fl.ast.types import find_tvars
        return set(find_tvars(self.type_))

    @memoized_property
    def dataconses_vars(self):
        return set.union(*(dc.free_type_variables for dc in self.dataconses))

    def is_product_type(self):
        return len(self.dataconses) == 1

    def __repr__(self):
        defs = ' | '.join(map(str, self.dataconses))
        if self.derivations:
            derivations = ', '.join(map(str, self.derivations))
            return f'<Data {self.type_} = {defs} deriving ({derivations})>'
        else:
            return f'<Data {self.type_} = {defs}>'

    def __eq__(self, other):
        # Derivations are not part of the logical structure of the data type,
        # they might just as well be provided separately.
        if isinstance(other, DataType):
            return (self.name == other.name and
                    self.type_ == other.type_ and
                    set(self.dataconses) == set(other.dataconses))
        else:
            return NotImplemented

    def __hash__(self):
        return hash((DataType, self.name, self.type_, self.dataconses))

    @property
    def implied_env(self) -> TypeEnvironment:
        '''The implied type environment by the data type.

        Each data constructor is a function (or value) of type of the data
        type.

        A simple example is the Bool data type:

            >>> from xotl.fl import parse
            >>> datatype = parse('data Bool = True | False')[0]
            >>> datatype.implied_env
            {'True': <TypeScheme: Bool>, 'False': <TypeScheme: Bool>}

        Both True and False are just values of type Bool.

        The Either data type shows data constructors with parameters:

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data Either a b = Left a | Right b')[0]
            >>> datatype.implied_env
            {'Left': <TypeScheme: forall a b. a -> (Either a b)>,
             'Right': <TypeScheme: forall a b. b -> (Either a b)>}

        Right takes any value of type `a` and returns a value of type `Either
        a b` (for any type `b`).

        '''
        from xotl.fl.ast.types import FunctionTypeCons

        def _implied_type(dc: DataCons) -> Type:
            result = self.type_
            for arg in reversed(dc.args):
                result = FunctionTypeCons(arg, result)
            return result

        return {
            dc.name: TypeScheme.from_typeexpr(_implied_type(dc))
            for dc in self.dataconses
        }

    @property
    def pattern_matching_env(self) -> TypeEnvironment:
        r'''The type environment needed to pattern-match the data constructors.

        A program like::

            data List a = Nil | Cons a (List a)

            count Nil = 0
            count (Cons x xs) = 1 + (count xs)

        Is transformed to the equivalent (I take some liberties to ease
        reading, this program cannot be parsed)::

            data List a = Nil | Cons a (List a)

            count arg1 = let eq1 eqarg1 = (\x1 -> 0) (:match:Nil: eqarg1)
                             eq2 eqarg1 = (\x -> \xs -> 1 + (count xs))
                                          (:extract:Cons:1: eqarg1)
                                          (:extract:Cons:2: eqarg1)
                    in (eq1 arg1) `:OR:` (eq2 arg1) `:OR:` NO_MATCH

        The operator ``:OR`` returns the first argument if it is not a
        pattern-match error; otherwise it returns the second argument.  This
        is a special operator.  The ``:match:Nil:``, ``:extract:Cons:1:``, and
        ``:extract:Cons:2:`` match its argument with the expected data
        constructor and, possibly, extract one of the components.

        The ``pattern_matching_evn`` returns the type environment of those
        functions:

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data List a = Nil | Cons a (List a)')[0]

            >>> datatype.pattern_matching_env
            {<Match: Nil>: <TypeScheme: forall a. List a>,
             <Extract: 1 from Cons>: <TypeScheme: forall a. (List a) -> a>,
             <Extract: 2 from Cons>: <TypeScheme: forall a. (List a) -> (List a)>}

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data Pair a b = Pair a b')[0]

            >>> datatype.pattern_matching_env
            {<Extract: 1 from Pair>: <TypeScheme: forall a b. (Pair a b) -> a>,
             <Extract: 2 from Pair>: <TypeScheme: forall a b. (Pair a b) -> b>}

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data Unit = Unit')[0]

            >>> datatype.pattern_matching_env
            {<Match: Unit>: <TypeScheme: Unit>}

        .. note:: The names of those special functions are not strings.

        '''
        from xotl.fl.match import Match, Extract
        from xotl.fl.ast.types import FunctionTypeCons as F

        def _implied_funs(dc: DataCons) -> Iterator[Tuple[Symbolic, TypeScheme]]:
            scheme = TypeScheme.from_typeexpr
            if not dc.args:
                yield Match(dc.name), scheme(self.type_)
            else:
                for i, type_ in enumerate(dc.args):
                    yield Extract(dc.name, i + 1), scheme(F(self.type_, type_))

        return {
            name: ts
            for dc in self.dataconses
            for name, ts in _implied_funs(dc)
        }

    @property
    def full_typeenv(self) -> TypeEnvironment:
        'Both `pattern_matching_env`:attr: and `implied_env`:attr: together.'
        return ChainMap(self.pattern_matching_env, self.implied_env)
