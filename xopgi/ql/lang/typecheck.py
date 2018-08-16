#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Any, List, Tuple, Iterator, Callable
from typing import Optional  # noqa

from xopgi.ql.lang.types.base import Type, TypeVariable, TypeCons
from xopgi.ql.lang.expressions.base import (
    AST,
    Identifier,
    Literal,
    Lambda,
    Application,
    Let,
    Letrec,
)


# `Substitution` is a type; `scompose`:class: is a substitution by
# composition, `delta`:class: creates the simplest non-empty substitution.
#
# TODO: We could modify the algorithm so that we can *inspect* which variables
# are being substituted; but that's not essential to the Substitution Type.
Substitution = Callable[[str], Type]


def find_tvars(t: Type) -> List[str]:
    'Get all variables names (possibly repeated) in type `t`.'
    if isinstance(t, TypeVariable):
        return [t.name]
    else:
        assert isinstance(t, TypeCons)
        return [tv for subt in t.subtypes for tv in find_tvars(subt)]


def subtype(phi: Substitution, t: Type) -> Type:
    if isinstance(t, TypeVariable):
        return phi(t.name)
    else:
        assert isinstance(t, TypeCons)
        return TypeCons(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )


class scompose:
    '''Compose two substitutions.

    The crucial property of scompose is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    '''
    def __new__(cls, f, g):
        # type: (Substitution, Substitution) -> Substitution
        if f is sidentity:
            return g
        elif g is sidentity:
            return f
        else:
            res = super().__new__(cls)
            res.__init__(f, g)
            return res

    def __init__(self, f: Substitution, g: Substitution) -> None:
        self.f = f
        self.g = g

    def __call__(self, s: str) -> Type:
        return subtype(self.f, self.g(s))

    def __repr__(self):
        return f'scompose({self.f!r}, {self.g!r})'


class Identity:
    'The identity substitution.'
    def __call__(self, s: str) -> Type:
        return TypeVariable(s)

    def __repr__(self):
        return f'Indentity()'


sidentity = Identity()


class delta:
    '''A `delta substitution` from a variable name `vname`.

    To avoid reusing instances of the same type expression, this function
    takes the type constructor and its arguments.  If you do want to use the
    same instance pass an instance wrapped in a lambda.  Example:

       >>> f = delta('a', T, 'id')
       >>> f('a') is f('a')
       False

       >>> f('b') is f('b')
       False

       >>> f = delta('a', lambda: T('id'))
       >>> f('a') is f('a')
       True

       >>> f('b') is f('b')
       False

    '''
    def __init__(self, vname: str, cons, *args) -> None:
        self.vname = vname
        self.cons = cons
        self.args = args

    def __call__(self, s: str) -> Type:
        return self.result if s == self.vname else TypeVariable(s)

    @property
    def result(self) -> Type:
        return self.cons(*self.args)

    def __repr__(self):
        return f'delta({self.vname!r}, {self.result!r})'


class UnificationError(Exception):
    pass


def unify(e1: Type, e2: Type, *, phi: Substitution = sidentity) -> Substitution:
    '''Extend `phi` so that it unifies `e1` and `e2`.

    If `phi` is None, uses the `identity substitution <Identity>`:class.

    If there's no substitution that unifies the given terms, raise a
    `UnificationError`:class:.

    '''
    def extend(phi: Substitution, name: str, t: Type) -> Substitution:
        if isinstance(t, TypeVariable) and name == t.name:
            return phi
        elif name in find_tvars(t):
            raise UnificationError(f'Cannot unify {name} with {t}')
        else:
            # TODO: Make the result *descriptible*
            return scompose(delta(name, lambda: t), phi)

    def unify_with_tvar(tvar, t):
        phitvn = phi(tvar.name)
        if phitvn == tvar:
            return extend(phi, tvar.name, subtype(phi, t))
        else:
            return unify(phitvn, subtype(phi, t), phi=phi)

    if isinstance(e1, TypeVariable):
        return unify_with_tvar(e1, e2)
    elif isinstance(e2, TypeVariable):
        return unify_with_tvar(e2, e1)
    else:
        assert isinstance(e1, TypeCons) and isinstance(e2, TypeCons)
        if e1.cons == e2.cons:
            return unify_exprs(zip(e1.subtypes, e2.subtypes), p=phi)
        else:
            raise UnificationError(f'Cannot unify {e1} with {e2}')


TypePairs = Iterator[Tuple[Type, Type]]


# This is the unifyl in the Book.
def unify_exprs(exprs: TypePairs, *, p: Substitution = sidentity) -> Substitution:
    '''Extend `p` to unify all pairs of type expressions in `exprs`.'''
    for se1, se2 in exprs:
        p = unify(se1, se2, phi=p)
    return p


class TypeScheme:
    '''A type scheme with generic (schematics) type variables.

    Example:

      >>> from xopgi.ql.lang.types.parser import parse
      >>> map_type = TypeScheme(['a', 'b'],
      ...                       parse('(a -> b) -> List a -> List b'))

      >>> map_type
      <TypeScheme: forall a b. (a -> b) -> ((List a) -> (List b))>

    '''
    # I choose the word 'generic' instead of schematic (and thus non-generic
    # instead of unknown), because that's probably more widespread.
    def __init__(self, generics: List[str], t: Type) -> None:
        self.generics = generics
        self.t = t

    @property
    def nongenerics(self) -> List[str]:
        return [
            name
            for name in find_tvars(self.t)
            if name not in self.generics
        ]

    @property
    def names(self):
        return ' '.join(self.generics)

    def __str__(self):
        if self.generics:
            return f'forall {self.names!s}. {self.t!s}'
        else:
            return str(self.t)

    def __repr__(self):
        return f'<TypeScheme: {self!s}>'

    @classmethod
    def from_typeexpr(cls, type_, *, generics=None):
        # type: (Type, *, Optional[List[str]]) -> TypeScheme
        '''Create a type scheme from a type expression assuming all type
        variables are generic.'''
        if not generics:
            generics = list(set(find_tvars(type_)))  # avoid repetitions.
        return cls(generics, type_)

    @classmethod
    def from_str(cls, source, *, generics=None):
        # type: (str, *, Optional[List[str]]) -> TypeScheme
        '''Create a type scheme from a type expression (given a string)
        assuming all type variables are generic.'''
        from xopgi.ql.lang.types import parse
        type_ = parse(source)
        return cls.from_typeexpr(type_, generics=generics)


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.'''
    exclude: Substitution = lambda s: phi(s) if s not in ts.generics else TypeVariable(s)
    return TypeScheme(ts.generics, subtype(exclude, ts.t))


AssocList = List[Tuple[Any, Any]]


def dom(al: AssocList) -> List[Any]:
    return [k for k, _ in al]


def val(al: AssocList, key: Any) -> List[Any]:
    return [v for k, v in al if k == key]


def rng(al: AssocList) -> List[Any]:
    # The provided implementation in the Book (``map (val al) (dom al)``) is
    # rather inefficient (O(n^2), because for each key it takes all its
    # values).
    return [v for _, v in al]


def install_al(al: AssocList, key: Any, val: Any) -> AssocList:
    # This is inefficient!!!
    return [(key, val)] + al


def insert_al(al: AssocList, key: Any, val: Any) -> AssocList:
    al.insert(0, (key, val))
    return al


#: A subtype of AssocList from names to TypeSchemes.
TypeEnvironment = List[Tuple[str, TypeScheme]]


def get_typeenv_unknowns(te: TypeEnvironment) -> List[str]:
    return sum((t.nongenerics for _, t in te), [])


def sub_typeenv(phi: Substitution, te: TypeEnvironment) -> TypeEnvironment:
    return [(x, subscheme(phi, st)) for x, st in te]


class namesupply:
    '''A names supply.

    Each variable will be name '.{prefix}{index}'; where the index starts at 0
    and increases by one at each new name.

    If `limit` is None (or 0), return a unending stream; otherwise yield as
    many items as `limit`:

       >>> list(namesupply(limit=2))
       [TypeVariable('.a0'), TypeVariable('.a1')]

    '''
    def __init__(self, prefix='a', exclude: List[str] = None,
                 *, limit: int = None) -> None:
        self.prefix = prefix
        self.exclude = exclude
        self.limit = limit
        self.current_index = 0
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> TypeVariable:
        if not self.limit or self.count < self.limit:
            result = None
            while not result:
                name = f'.{self.prefix}{self.current_index}'
                if not self.exclude or name not in self.exclude:
                    result = name
                self.current_index += 1
            self.count += 1
            return TypeVariable(result, check=False)
        else:
            raise StopIteration


NameSupply = Iterator[TypeVariable]
TCResult = Tuple[Substitution, Type]


def typecheck(env: TypeEnvironment, ns: NameSupply, exp: AST) -> TCResult:
    '''Check the type of `exp` in a given type environment.

    '''
    def typecheck_var(env, ns, exp: Identifier) -> TCResult:
        pass

    def typecheck_literal(env, ns, exp: Literal) -> TCResult:
        pass

    def typecheck_app(env, ns, exp: Application) -> TCResult:
        pass

    def typecheck_lambda(env, ns, exp: Lambda) -> TCResult:
        pass

    def typecheck_let(env, ns, exp: Let) -> TCResult:
        pass

    def typecheck_letrec(env, ns, exp: Letrec) -> TCResult:
        pass

    if isinstance(exp, Identifier):
        return typecheck_var(env, ns, exp)
    elif isinstance(exp, Literal):
        return typecheck_literal(env, ns, exp)
    elif isinstance(exp, Application):
        return typecheck_app(env, ns, exp)
    elif isinstance(exp, Lambda):
        return typecheck_lambda(env, ns, exp)
    elif isinstance(exp, Let):
        return typecheck_let(env, ns, exp)
    elif isinstance(exp, Letrec):
        return typecheck_letrec(env, ns, exp)
    else:
        assert False, f'Unknown AST node {exp!r}'


TCLResult = Tuple[Substitution, List[Type]]


def tcl(env: TypeEnvironment, ns: NameSupply, exprs: List[AST]) -> TCLResult:
    def tcl2(phi, t, tcs):
        # type: (Substitution, Type, TCLResult) -> TCLResult
        psi, ts = tcs
        return scompose(psi, phi), [subtype(psi, t)] + ts

    def tcl1(env, ns, exprs, tc):
        # type: (TypeEnvironment, NameSupply, List[AST], TCResult) -> TCLResult
        phi, t = tc
        return tcl2(phi, t, tcl(sub_typeenv(phi, env), ns, exprs))

    if not exprs:
        return sidentity, []
    else:
        expr, *exprs = exprs
        return tcl1(env, ns, exprs, typecheck(env, ns, expr))
