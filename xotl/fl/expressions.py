#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass
from typing import (
    Any,
    Deque,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Reversible,
    Sequence,
    Tuple,
    Type as Class,
    Union,
)
from collections import deque, ChainMap

from xoutil.objects import validate_attrs
from xoutil.fp.tools import fst

from xotl.fl.types import (
    AST,
    Type,
    TypeCons,
    TypeEnvironment,
    TypeScheme,
    Symbol,
)
from xotl.fl.builtins import UnitType
from xotl.fl.utils import namesupply


class Identifier(AST):
    '''A name (variable if you like).'''
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name!r})'

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash((Identifier, self.name))

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.name == other.name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Identifier):
            return not (self == other)
        else:
            return NotImplemented


# An extension to the algorithm.  Literals are allowed, but have a the
# most specific type possible.
class Literal(AST):
    '''A literal value with its type.

    The `parser <xotl.fl.expressions.parse>`:func: only recognizes strings,
    chars, and numbers (integers and floats are represented by a single type).

    '''
    def __init__(self, value: Any, type_: Type, annotation: Any = None) -> None:
        self.value = value
        self.type_ = type_
        self.annotation = annotation

    def __repr__(self):
        if self.annotation is not None:
            return f'Literal({self.value!r}, {self.type_!r}, {self.annotation!r})'
        else:
            return f'Literal({self.value!r}, {self.type_!r})'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return validate_attrs(self, other, ('type', 'value', 'annotation'))
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Literal):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Literal, self.value, self.type_, self.annotation))


class Lambda(AST):
    '''A lambda abstraction over a single parameter. '''
    def __init__(self, varname: str, body: AST) -> None:
        self.varname = varname
        self.body = body

    def __repr__(self):
        return f'Lambda({self.varname!r}, {self.body!r})'

    def __str__(self):
        return f'\{self.varname!s} -> {self.body!s}'

    def __eq__(self, other):
        if isinstance(other, Lambda):
            return self.varname == other.varname and self.body == other.body
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Lambda):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Lambda, self.varname, self.body))


class Application(AST):
    '''The application of `e1` to its *argument* e2.'''
    def __init__(self, e1: AST, e2: AST) -> None:
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return f'Application({self.e1!r}, {self.e2!r})'

    def __str__(self):
        return f'{self.e1!s} {self.e2!s}'

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.e1 == other.e1 and self.e2 == other.e2
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Application):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Application, self.e1, self.e2))


# We assume (as the Book does) that there are no "translation" errors; i.e
# that you haven't put a Let where you needed a Letrec.
class _LetExpr(AST):
    def __init__(self, bindings: Mapping[str, AST], body: AST,
                 localenv: TypeEnvironment = None) -> None:
        # Sort by names (in a _LetExpr names can't be repeated, repetition for
        # pattern-matching should be translated to a lambda using the MATCH
        # operator).
        self.bindings = tuple(sorted(bindings.items(), key=fst))
        self.localenv = localenv or {}  # type: TypeEnvironment
        self.body = body

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.bindings == other.bindings and
                    self.localenv == other.localenv and
                    self.body == self.body)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((type(self), self.keys(), self.values(),
                     self.localenv, self.body))

    def keys(self) -> Iterator[str]:
        return (k for k, _ in self.bindings)

    def values(self) -> Iterator[AST]:
        return (v for _, v in self.bindings)


class Let(_LetExpr):
    '''A non-recursive Let expression.

    The `parser <xotl.fl.expressions.parse>`:func: automatically selects
    between `Let`:class: and `Letrec`:class.  If you're creating the program
    by hand you should choose appropriately.

    '''
    def __repr__(self):
        return f'Let({self.bindings!r}, {self.body!r})'


class Letrec(_LetExpr):
    '''A recursive Let expression.

    .. seealso:: `Let`:class:

    '''
    def __repr__(self):
        return f'Letrec({self.bindings!r}, {self.body!r})'


def parse(code: str, debug=False, tracking=False) -> AST:
    '''Parse a single expression `code`.
    '''
    from xotl.fl.parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def build_lambda(params: Reversible[str], body: AST) -> Lambda:
    '''Create a Lambda from several parameters.

    Example:

       >>> build_lambda(['a', 'b'], Identifier('a'))
       Lambda('a', Lambda('b', Identifier('a')))

    '''
    assert params
    result = body
    for param in reversed(params):
        if isinstance(param, Identifier):
            result = Lambda(param.name, result)
        else:
            # TODO: Transform to pattern matching operators
            result = Lambda(param, result)  # type: ignore
    return result  # type: ignore


def find_free_names(expr: AST, *, exclude: Sequence[str] = None) -> List[str]:
    '''Find all names that appear free in `expr`.

    Example:

      >>> set(find_free_names(parse('let id x = x in map id xs')))  # doctest: +LITERAL_EVAL
      {'map', 'xs'}

    Names can be repeated:

      >>> find_free_names(parse('twice x x')).count('x')
      2

    If `exclude` is None, we exclude any special identifiers used internally.  If you want
    to expose them, pass the empty tuple:

       >>> program = """
       ...     let length [] = 0
       ...         length x:xs = 1 + length xs
       ...     in length
       ... """
       >>> set(find_free_names(parse(program), exclude=()))  # doctest: +LITERAL_EVAL
       {'+', ':NO_MATCH_ERROR:', ':OR:'}

    '''
    from xotl.fl.pattern import MATCH_OPERATOR, NO_MATCH_ERROR
    from xotl.fl.pattern import Match, Extract, MatchLiteral
    from xotl.fl.let import ConcreteLet

    POPFRAME = None  # remove a binding from the 'stack'
    result: List[str] = []
    if exclude is None:
        bindings: Deque[str] = deque([MATCH_OPERATOR.name, NO_MATCH_ERROR.name])
    else:
        bindings = deque([])
    nodes: Deque[Optional[AST]] = deque([expr])
    while nodes:
        node = nodes.pop()
        if node is POPFRAME:
            bindings.pop()
        elif isinstance(node, Identifier):
            if node.name not in bindings:
                if isinstance(node.name, str):
                    result.append(node.name)
                else:
                    assert isinstance(node.name, (Match, Extract, MatchLiteral))
        elif isinstance(node, Literal):
            if isinstance(node.annotation, AST):
                nodes.append(node)
        elif isinstance(node, Application):
            nodes.extend([
                node.e1,
                node.e2,
            ])
        elif isinstance(node, Lambda):
            bindings.append(node.varname)
            nodes.append(POPFRAME)
            nodes.append(node.body)
        elif isinstance(node, (ConcreteLet, Let, Letrec)):
            if isinstance(node, ConcreteLet):
                node = node.ast
            # This is tricky; the bindings can be used recursively in the
            # bodies of a letrec:
            #
            #    letrec f1 = ....f1 ... f2 ....
            #           f2 = ... f1 ... f2 ....
            #           ....
            #    in ... f1 ... f2 ...
            #
            # So we must make all the names in the bindings bound and then
            # look at all the definitions.
            #
            # We push several POPFRAME to account for that.
            bindings.extend(node.keys())
            nodes.extend(POPFRAME for _ in node.keys())
            nodes.extend(node.values())
            nodes.append(node.body)
        else:
            assert False, f'Unknown AST node: {node!r}'
    return result


def replace_free_occurrences(self: AST,
                             substitutions: Mapping[str, str]) -> AST:
    '''Create a new expression replacing free occurrences of variables.

    You are responsible to avoid the name capture problem::

      >>> replace_free_occurrences(expr_parse('\id -> id x'), {'x': 'id'})
      Lambda('id', Application(Identifier('id'), Identifier('id')))

    '''
    from xotl.fl.pattern import NO_MATCH_ERROR, MATCH_OPERATOR

    def replace(expr: AST, bindings: FrozenSet[str]):
        if isinstance(expr, Identifier):
            if expr.name not in bindings:
                replacement = substitutions.get(expr.name, None)
                if replacement is not None:
                    return Identifier(replacement)
            return expr
        elif isinstance(expr, Literal):
            if isinstance(expr.annotation, AST):
                return Literal(
                    expr.value,
                    expr.type_,
                    replace(expr.annotation, bindings)
                )
            else:
                return expr
        elif isinstance(expr, Application):
            return Application(
                replace(expr.e1, bindings),
                replace(expr.e2, bindings),
            )
        elif isinstance(expr, Lambda):
            return Lambda(
                expr.varname,
                replace(expr.body, bindings | {expr.varname})
            )
        elif isinstance(expr, _LetExpr):
            newvars = {name for name, _ in expr.bindings}
            newbindings = bindings | newvars
            return type(expr)(
                {name: replace(dfn, newbindings)
                 for name, dfn in expr.bindings},
                replace(expr.body, newbindings),
                expr.localenv
            )
        else:
            assert False

    return replace(self, frozenset({NO_MATCH_ERROR.name, MATCH_OPERATOR.name}))


def build_tuple(*exprs):
    '''Return the AST expression of a tuple of expressions.

    If `exprs` is empty, return the unit value.  Otherwise it must contains at
    least two expressions; in this case, return the Application the
    appropriate tuple-builder function to the arguments.

    Example:

       >>> build_tuple(Identifier('a'), Identifier('b'), Identifier('c'))
       Application(Identifier(',,'), ...)

    '''
    if not exprs:
        return UnitValue
    else:
        cons = ',' * (len(exprs) - 1)
        if not cons:
            raise TypeError('Cannot build a 1-tuple')
        return build_application(cons, *exprs)


UnitValue = Literal((), UnitType)


def build_application(f, arg, *args) -> Application:
    'Build the Application of `f` to many args.'
    if isinstance(f, str):
        f = Identifier(f)
    result = Application(f, arg)
    for arg in args:
        result = Application(result, arg)
    return result


def build_list_expr(*items) -> AST:
    result: AST = Nil
    for item in reversed(items):
        result = Cons(item, result)
    return result


#: The empty list AST expression
Nil = Identifier('[]')


def Cons(x, xs) -> Application:
    'Return x:xs'
    return Application(Application(Identifier(':'), x), xs)
