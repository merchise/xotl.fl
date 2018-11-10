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
    Mapping,
    Iterator,
    Sequence,
    Union,
    List,
    Type as Class,
    Reversible,
    Deque,
    Optional,
)
from collections import deque

from xoutil.objects import validate_attrs
from xoutil.fp.tools import fst

from xotl.fl.types import AST, Type, TypeCons, TypeEnvironment
from xotl.fl.builtins import UnitType


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
        self.type = type_
        self.annotation = annotation

    def __repr__(self):
        if self.annotation is not None:
            return f'Literal({self.value!r}, {self.type!r}, {self.annotation!r})'
        else:
            return f'Literal({self.value!r}, {self.type!r})'

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
        return hash((Literal, self.value, self.type, self.annotation))


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


@dataclass
class ConcreteLet:
    '''The concrete representation of a let/where expression.

    '''
    definitions: List[Union['Equation', TypeEnvironment]]  # noqa
    body: AST

    @property
    def ast(self) -> _LetExpr:
        r'''Build a Let/Letrec from a set of equations and a body.

        We need to decide if we issue a Let or a Letrec: if any of declared
        names appear in the any of the bodies we must issue a Letrec, otherwise
        issue a Let.

        Also we need to convert function-patterns into Lambda abstractions::

           let id x = ...

        becomes::

           led id = \x -> ...

        For the time being (we don't have pattern matching yet), each symbol can
        be defined just once.

        '''
        from xotl.fl.parsers import ParserError
        equations = [
            eq.compiled
            for eq in self.definitions
            if isinstance(eq, Equation)
        ]
        conses = [eq.name for eq in equations]
        names = set(conses)
        if len(names) != len(conses):
            raise ParserError('Several definitions for the same name')
        if any(set(find_free_names(eq.body)) & names for eq in equations):
            klass: Class[_LetExpr] = Letrec
        else:
            klass = Let
        localenv: TypeEnvironment = {
            name: value
            for env in self.definitions
            if isinstance(env, dict)
            for name, value in env.items()
        }
        return klass(
            {eq.name: eq.body for eq in equations},
            self.body,
            localenv
        )


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


# Patterns and Equations.  In the final AST, an expression like:
#
#     let id x = x in ...
#
# would actually be like
#
#     let id = \x -> x
#
# with some complications if pattern-matching is allowed:
#
#     let length [] = 0
#         lenght (x:xs) = 1 + length xs
#     in  ...
#
# For now, we allow only the SIMPLEST of all definitions (we don't have a
# 'case' keyword to implement pattern matching.)  But, in any case, having the
# names of productions be 'pattern' and 'equations' is fit.
#
#
# The Pattern and Equation definitions are not part of the final AST, but more
# concrete syntactical object in the source code.  In the final AST, the let
# expressions shown above are indistinguishable.
#
# For value (function) definitions the parser still returns *bare* Equation
# object for each line of the definition.

class ConsPattern:
    '''The syntactical notion of a pattern.

    '''
    def __init__(self, cons: str, params=None) -> None:
        self.cons: str = cons
        self.params = tuple(params or [])

    def __repr__(self):
        return f'<pattern {self.cons!r} {self.params!r}>'

    def __str__(self):
        if self.params:
            return f'{self.cons} {self.parameters}'
        else:
            return self.cons

    @property
    def parameters(self):
        def _str(x):
            if isinstance(x, str):
                return x
            elif isinstance(x, ConsPattern):
                return f'({x})'
            else:
                return repr(x)

        return ' '.join(map(_str, self.params))

    def __eq__(self, other):
        if isinstance(other, ConsPattern):
            return self.cons == other.cons and self.params == other.params
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ConsPattern):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((ConsPattern, self.cons, self.params))


Pattern = Union[str, Identifier, Literal, ConsPattern]


class Equation:
    '''The syntactical notion of an equation.

    This is just the syntax of a left-hand side being equated to a right-hand
    side.  The LHS is a `Pattern`:class:, while the RHS is any of the objects
    of the `AST <ast-objects>`:ref:.

    '''
    def __init__(self, name: str, patterns: Sequence[Pattern], body: AST) -> None:
        self.name = name
        self.patterns = tuple(patterns or [])
        self.body = body

    def __repr__(self):
        def _str(x):
            result = str(x)
            if ' ' in result:
                return f'({result})'
            else:
                return result

        if self.patterns:
            args = ' '.join(map(_str, self.patterns))
            return f'<equation {self.name!s} {args} = {self.body!r}>'
        else:
            return f'<equation {self.name!s} = {self.body!r}>'

    def __eq__(self, other):
        if isinstance(other, Equation):
            return (self.name == other.name and
                    self.patterns == other.patterns and
                    self.body == other.body)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Equation):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Equation, self.name, self.patterns, self.body))

    def compile_patterns(self) -> AST:
        '''Compile the patterns of the equation in to the lambda calculus.

        '''
        if self.patterns:
            return build_lambda(self.patterns, self.body)
        else:
            return self.body

    @property
    def compiled(self) -> 'Equation':
        'An equivalent equation with all patterns compiled.'
        if self.patterns:
            return Equation(self.name, [], self.compile_patterns())
        else:
            return self


class DataCons:
    '''A data constructor.

    '''
    def __init__(self, cons: str, args: Sequence[Type]) -> None:
        self.name = cons
        self.args = tuple(args)

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

    def __ne__(self, other):
        if isinstance(other, DataCons):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((DataCons, self.name, self.args))


class DataType:
    '''A data type definition.

    A data type defines both a type and several values of that type.

    You should note that `DataCons`:class: is NOT the value.  Therefore these
    are not actual objects carrying values in the running program; but they
    imply the compiler (or interpreter) must produce those values and match
    the type.

    '''
    def __init__(self, name: str, type_: TypeCons, defs: Sequence[DataCons]) -> None:
        self.name = name
        self.t = type_
        self.dataconses = tuple(defs)

    def __repr__(self):
        defs = ' | '.join(map(str, self.dataconses))
        return f'<Data {self.t} = {defs}>'

    def __eq__(self, other):
        if isinstance(other, DataType):
            return (self.name == other.name and
                    self.t == other.t and
                    set(self.dataconses) == set(other.dataconses))
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DataType):
            return not (self == other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((DataType, self.name, self.t, self.dataconses))

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

            >>> datatype = parse('data Either a b = Left a | Right b')[0]
            >>> datatype.implied_env
            {'Left': <TypeScheme: forall a b. a -> (Either a b)>,
             'Right': <TypeScheme: forall a b. b -> (Either a b)>}

        Right takes any value of type `a` and returns a value of type `Either
        a b` (for any type `b`).

        '''
        from xotl.fl.types import TypeScheme, FunctionTypeCons

        def _implied_type(dc: DataCons) -> Type:
            result = self.t
            for arg in reversed(dc.args):
                result = FunctionTypeCons(arg, result)
            return result

        return {
            dc.name: TypeScheme.from_typeexpr(_implied_type(dc))
            for dc in self.dataconses
        }


def parse(code: str, debug=False, tracking=False) -> AST:
    '''Parse a single expression `code`.
    '''
    from xotl.fl.parsers import expr_parser, lexer
    return expr_parser.parse(code, lexer=lexer, debug=debug, tracking=tracking)


def build_lambda(params: Reversible[Pattern], body: AST) -> Lambda:
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


def find_free_names(expr: AST) -> List[str]:
    '''Find all names that appear free in `expr`.

    Example:

      >>> set(find_free_names(parse('let id x = x in map id xs')))  # doctest: +LITERAL_EVAL
      {'map', 'xs'}

    Names can be repeated:

      >>> find_free_names(parse('twice x x')).count('x')
      2

    '''
    POPFRAME = None  # remove a binding from the 'stack'
    result: List[str] = []
    bindings: Deque[str] = deque([])
    nodes: Deque[Optional[AST]] = deque([expr])
    while nodes:
        node = nodes.pop()
        if node is POPFRAME:
            bindings.pop()
        elif isinstance(node, Identifier):
            if node.name not in bindings:
                result.append(node.name)
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
            # We push several POPFRAME at the to account for that.
            bindings.extend(node.keys())
            nodes.extend(POPFRAME for _ in node.keys())
            nodes.extend(node.values())
            nodes.append(node.body)
        else:
            assert False, f'Unknown AST node: {node!r}'
    return result


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


def build_application(f, arg, *args):
    'Build the Application of `f` to many args.'
    if isinstance(f, str):
        f = Identifier(f)
    result = Application(f, arg)
    for arg in args:
        result = Application(result, arg)
    return result


def build_list_expr(*items):
    result = Nil
    for item in reversed(items):
        result = Cons(item, result)
    return result


#: The empty list AST expression
Nil = Identifier('[]')


def Cons(x, xs):
    'Return x:xs'
    return Application(Application(Identifier(':'), x), xs)
