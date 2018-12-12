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


@dataclass
class ConcreteLet:
    '''The concrete representation of a let/where expression.

    '''
    definitions: List[Union['Equation', TypeEnvironment]]  # noqa
    body: AST

    @property
    def ast(self) -> _LetExpr:
        return self.compile()

    def compile(self) -> _LetExpr:
        r'''Build a Let/Letrec from a set of equations and a body.

        We need to decide if we issue a Let or a Letrec: if any of declared
        names appear in the any of the bodies we must issue a Letrec, otherwise
        issue a Let.

        Also we need to convert function-patterns into Lambda abstractions::

           let id x = ...

        becomes::

           led id = \x -> ...

        '''
        localenv: TypeEnvironment = {}
        defs: MutableMapping[str, FunctionDefinition] = {}   # noqa
        for dfn in self.definitions:
            if isinstance(dfn, Equation):
                eq = defs.get(dfn.name)
                if not eq:
                    defs[dfn.name] = FunctionDefinition([dfn])
                else:
                    assert isinstance(eq, FunctionDefinition)
                    defs[dfn.name] = eq.append(dfn)
            elif isinstance(dfn, dict):
                localenv.update(dfn)  # type: ignore
            else:
                assert False, f'Unknown definition type {dfn!r}'
        names = set(defs)
        compiled = {name: dfn.compile() for name, dfn in defs.items()}
        if any(set(find_free_names(fn)) & names for fn in compiled.values()):
            klass: Class[_LetExpr] = Letrec
        else:
            klass = Let
        return klass(compiled, self.body, localenv)


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

@dataclass(frozen=True)
class Match(Symbol):
    'A symbol for the pattern matching "match" function.'
    name: str

    def __str__(self):
        return f':match:{self.name}:'

    def __repr__(self):
        return f'<Match: {self.name}>'


@dataclass(frozen=True)
class Extract(Symbol):
    'A symbol for the pattern matching "extract" function.'
    name: str
    arg: int

    def __str__(self):
        return f':extract:{self.name}:{self.arg}:'

    def __repr__(self):
        return f'<Extract: {self.arg} from {self.name}>'


@dataclass(frozen=True)
class Select(Symbol):
    'A symbol for the pattern matching "select" function.'
    arg: int

    def __str__(self):
        return f':select:{self.arg}:'

    def __repr__(self):
        return f'<Select: {self.arg}>'


@dataclass(frozen=True)
class MatchLiteral(Symbol):
    value: Literal

    def __str__(self):
        return f':value:{self.value}:'

    def __repr__(self):
        return f'<Match value: {self.value}>'


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
            return f'{self.cons} {self._parameters}'
        else:
            return self.cons

    @property
    def _parameters(self):
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


Pattern = Union[str, Literal, ConsPattern]


class Equation:
    '''The syntactical notion of an equation.

    '''
    def __init__(self, name: str, patterns: Sequence[Pattern], body: AST) -> None:
        self.name = name
        self.patterns: Tuple[Pattern, ...] = tuple(patterns or [])
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


class DataCons:
    '''The syntactical notion a data constructor in the type language.

    '''
    def __init__(self, cons: str, args: Sequence[Type]) -> None:
        self.name = cons
        self.args: Sequence[Type] = tuple(args)

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

    You should note that `DataCons`:class: is NOT a value.  Therefore these
    are not actual objects carrying values in the running program; but imply
    the compiler (or interpreter) must produce those values and match the
    type.

    '''
    def __init__(self, name: str, type_: TypeCons,
                 defs: Sequence[DataCons],
                 derivations: Sequence[str] = None) -> None:
        self.name = name
        self.type_ = type_
        self.dataconses = tuple(defs)
        self.derivations = tuple(derivations or [])

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

    def __ne__(self, other):
        if isinstance(other, DataType):
            return not (self == other)
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
        from xotl.fl.types import FunctionTypeCons

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

        For product types, Extract becomes select and there's no Match::

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data Pair a b = Pair a b')[0]

            >>> datatype.pattern_matching_env
            {<Select: 1>: <TypeScheme: forall a b. (Pair a b) -> a>,
             <Select: 2>: <TypeScheme: forall a b. (Pair a b) -> b>}

        The unit type (any type with a single value) has none::

        .. doctest::
           :options: +NORMALIZE_WHITESPACE

            >>> datatype = parse('data Unit = Unit')[0]

            >>> datatype.pattern_matching_env
            {}


        .. note:: The names of those special functions are not strings.

        '''
        from xotl.fl.types import FunctionTypeCons as F

        def _implied_funs(dc: DataCons) -> Iterator[Tuple[Symbol, TypeScheme]]:
            scheme = TypeScheme.from_typeexpr
            if not self.is_product_type():
                if not dc.args:
                    yield Match(dc.name), scheme(self.type_)
                else:
                    for i, type_ in enumerate(dc.args):
                        yield Extract(dc.name, i + 1), scheme(F(self.type_, type_))
            else:
                for i, type_ in enumerate(dc.args):
                    yield Select(i + 1), scheme(F(self.type_, type_))

        return {
            name: ts
            for dc in self.dataconses
            for name, ts in _implied_funs(dc)
        }

    @property
    def full_typeenv(self) -> TypeEnvironment:
        'Both `pattern_matching_env`:attr: and `implied_env`:attr: together.'
        return ChainMap(self.pattern_matching_env, self.implied_env)


class FunctionDefinition:
    '''A single function definition (as a sequence of equations).

    '''
    def __init__(self, eqs: Iterable[Equation]) -> None:
        equations: Tuple[Equation, ...] = tuple(eqs)
        names = {eq.name for eq in equations}
        name = names.pop()
        assert not names
        first, *rest = equations
        arity = len(first.patterns)
        if any(len(eq.patterns) != arity for eq in rest):
            raise ArityError(
                "Function definition with different parameters count",
                equations
            )
        self.name = name
        self.equations = equations
        self.arity = arity

    def append(self, item) -> 'FunctionDefinition':
        return FunctionDefinition(self.equations + (item, ))

    def extend(self, items: Iterable[Equation]) -> 'FunctionDefinition':
        return FunctionDefinition(self.equations + tuple(items))

    def compile(self) -> AST:
        '''Return the compiled form of the function definition.

        '''
        # This is similar to the function `match` in 5.2 of [PeytonJones1987];
        # but I want to avoid *enlarging* simple functions needlessly.
        if self.arity:
            vars = list(namesupply(f'.{self.name}_arg', limit=self.arity))
            body: AST = NO_MATCH_ERROR
            for eq in self.equations:
                dfn = eq.body
                patterns: Iterable[Tuple[str, Pattern]] = zip(vars, eq.patterns)
                for var, pattern in patterns:
                    if isinstance(pattern, str):
                        # Our algorithm is trivial but comes with a cost:
                        # ``id x = x`` is must be translated to
                        # ``id = \.id_arg0 -> (\x -> x) .id_arg0``.
                        dfn = Application(
                            Lambda(pattern, dfn),
                            Identifier(var)
                        )
                    elif isinstance(pattern, Literal):
                        # ``fib 0 = 1``; is transformed to
                        # ``fib = \.fib_arg0 -> <MatchLiteral 0> .fib_arg0 1``
                        dfn = build_application(
                            Identifier(MatchLiteral(pattern)),  # type: ignore
                            Identifier(var),
                            dfn
                        )
                    elif isinstance(pattern, ConsPattern):
                        if not pattern.params:
                            # This is just a Match; similar to MatchLiteral
                            dfn = build_application(
                                Identifier(Match(pattern.cons)),  # type: ignore
                                Identifier(var),
                                dfn
                            )
                        else:
                            for i, param in reversed(list(enumerate(pattern.params, 1))):
                                if isinstance(param, str):
                                    dfn = build_application(
                                        Identifier(Extract(pattern.cons, i)),  # type: ignore
                                        Identifier(var),
                                        Lambda(param, dfn)
                                    )
                                else:
                                    raise NotImplementedError(
                                        f"Nested patterns {param}"
                                    )
                    else:
                        assert False
                body = build_lambda(
                    vars,
                    build_application(
                        MATCH_OPERATOR,
                        dfn,
                        body
                    )
                )
            return body
        else:
            # This should be a simple value, so we return the body of the
            # first equation.
            return self.equations[0].body


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


MATCH_OPERATOR = Identifier(':OR:')
NO_MATCH_ERROR = Identifier(':NO_MATCH_ERROR:')


class ArityError(TypeError):
    pass
