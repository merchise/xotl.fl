#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import (
    Any,
    Sequence,
    List,
    Tuple,
    Iterator,
    Iterable,
    Callable,
)
from typing import Optional  # noqa

from xopgi.ql.lang.types.base import (
    Type,
    TypeVariable,
    TypeCons,
    FunctionTypeCons as FuncCons,
)
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
    # 'subtype(sidentity, t) == t'; and since Type, TypeVariables and TypeCons
    # are treated immutably we should be safe to return the same type.
    if phi is sidentity:
        return t
    elif isinstance(t, TypeVariable):
        return phi(t.name)
    else:
        assert isinstance(t, TypeCons)
        return TypeCons(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )


def scompose(f: Substitution, g: Substitution) -> Substitution:
    '''Compose two substitutions.

    The crucial property of `scompose`:func: is that::

       subtype (scompose f g) = (subtype f) . (subtype g)

    '''
    if f is sidentity:
        return g
    elif g is sidentity:
        return f
    else:
        return Composition(f, g)


class Composition:
    def __init__(self, f: Substitution, g: Substitution) -> None:
        assert self is not f
        self.f = f
        self.g = g

    def __call__(self, s: str) -> Type:
        return subtype(self.f, self.g(s))

    def __repr__(self):
        return f'Composition({self.f!r}, {self.g!r})'


class Identity:
    'The identity substitution.'
    def __call__(self, s: str) -> Type:
        return TypeVariable(s, check=False)

    def __repr__(self):
        return 'Identity()'


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
        return self.result if s == self.vname else TypeVariable(s, check=False)

    @property
    def result(self) -> Type:
        return self.cons(*self.args)

    def __repr__(self):
        return f'delta({self.vname!r}, {self.result!r})'


class UnificationError(TypeError):
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
            raise UnificationError(f'Cannot unify {name!s} with {t!s}')
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
            raise UnificationError(f'Cannot unify {e1!s} with {e2!s}')


TypePairs = Iterable[Tuple[Type, Type]]


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
    def __init__(self, generics: Sequence[str], t: Type) -> None:
        self.generics = generics
        self.t = t

    @property
    def nongenerics(self) -> List[str]:
        return [
            name
            for name in find_tvars(self.t)
            if name not in self.generics
        ]

    def __hash__(self):
        return hash((TypeScheme, self.generics, self.t))

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
        # type: (Type, *, Optional[Sequence[str]]) -> TypeScheme
        '''Create a type scheme from a type expression assuming all type
        variables are generic.'''
        if generics is None:
            generics = list(set(find_tvars(type_)))  # avoid repetitions.
        return cls(generics, type_)

    @classmethod
    def from_str(cls, source, *, generics=None):
        # type: (str, *, Optional[Sequence[str]]) -> TypeScheme
        '''Create a type scheme from a type expression (given a string)
        assuming all type variables are generic.'''
        from xopgi.ql.lang.types import parse
        type_ = parse(source)
        return cls.from_typeexpr(type_, generics=generics)


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.'''
    return TypeScheme(ts.generics, subtype(Exclude(phi, ts), ts.t))


class Exclude:
    '''A substitution over the non-generics in a type scheme.

    Applies `phi` only if the variable name is a non-generic of the type
    scheme `ts`.

    '''
    def __new__(cls, phi, ts):
        # type: (Any, Substitution, TypeScheme) -> Substitution
        if not ts.generics:
            return phi
        else:
            res = super().__new__(cls)  # type: ignore
            res.__init__(phi, ts)
            return res

    def __init__(self, phi: Substitution, ts: TypeScheme) -> None:
        self.phi = phi
        self.ts = ts

    def __call__(self, s: str) -> Type:
        if s not in self.ts.generics:
            return self.phi(s)
        else:
            return TypeVariable(s, check=False)

    def __repr__(self):
        return f'Exclude({self.phi!r}, {self.ts!r})'


AssocList = List[Tuple[Any, Any]]


def dom(al: AssocList) -> List[Any]:
    return [k for k, _ in al]


def val(al: AssocList, key: Any) -> Any:
    return [v for k, v in al if k == key][0]


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
    def __init__(self, prefix='a', exclude: Sequence[str] = None,
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


def tcl(env: TypeEnvironment, ns: NameSupply, exprs: Iterable[AST]) -> TCLResult:
    if not exprs:
        return sidentity, []
    else:
        expr, *exprs = exprs
        phi, t = typecheck(env, ns, expr)
        psi, ts = tcl(sub_typeenv(phi, env), ns, exprs)
        return scompose(psi, phi), [subtype(psi, t)] + ts


def newinstance(ns: NameSupply, ts: TypeScheme) -> Type:
    'Create an instance of `ts` drawing names from the supply `ns`.'
    newvars: List[Tuple[str, TypeVariable]] = list(zip(ts.generics, ns))
    phi: Substitution = build_substitution(newvars)
    return subtype(phi, ts.t)


def build_substitution(alist: Sequence[Tuple[str, Type]]) -> Substitution:
    '''Build a substitution from an association list.

    This is the standard *interpretation* of a mapping from names to types.
    The substitution, when called upon, will look the from beginning to end
    for an item with the same key and return the associated type.

    If the same name is assigned more than once, return the first one.

    We keep an internal copy of the `alist`.  So, it's safe to change the
    argument afterwards.

    '''
    lst = list(alist)

    def result(name: str) -> Type:
        missing = object()
        restype: Type = missing  # type: ignore
        pos = 0
        while restype is missing and pos < len(lst):
            generic, newvar = lst[pos]
            pos += 1
            if generic == name:
                restype = newvar
        if restype is missing:
            return TypeVariable(name, check=False)
        else:
            return restype
    return result


def typecheck_literal(env, ns, exp: Literal) -> TCResult:
    # Extension to the original algorithm but easy: a literal always type
    # check with its type.
    return sidentity, exp.type


def typecheck_var(env, ns, exp: Identifier) -> TCResult:
    name = exp.name
    return sidentity, newinstance(ns, val(env, name))


def typecheck_app(env, ns, exp: Application) -> TCResult:
    phi, types = tcl(env, ns, [exp.e1, exp.e2])
    t1, t2 = types
    t: TypeVariable = next(ns)
    try:
        result = unify(t1, FuncCons(t2, t), phi=phi)
    except UnificationError as error:
        raise UnificationError(
            f'Cannot type-check ({exp!s}) :: {t1!s} ~ {t2!s} -> {t!s}'
        )
    return result, result(t.name)


def typecheck_lambda(env, ns, exp: Lambda) -> TCResult:
    # \x -> ...; the type of 'x' can be anything.  Thus, create a type
    # scheme with a new non-generic type variable Tx.  We extend the
    # environment to say 'x :: Tx' and typecheck the body of the lambda in
    # this new environment.
    newvar = next(ns)
    argtype = TypeScheme.from_typeexpr(newvar, generics=[])
    phi, type_ = typecheck([(exp.varname, argtype)] + env, ns, exp.body)
    return phi, FuncCons(phi(newvar.name), type_)


def typecheck_let(env, ns, exp: Let) -> TCResult:
    exprs: List[AST] = list(exp.values())
    phi, types = tcl(env, ns, exprs)
    names: List[str] = list(exp.keys())
    psi, t = typecheck(
        add_decls(sub_typeenv(phi, env), ns, names, types),
        ns,
        exp.body,
    )
    return scompose(psi, phi), t


def add_decls(env, ns, names: Sequence[str], types: Iterable[Type]) -> TypeEnvironment:

    def genbar(unknowns, names, type_):
        schvars = list({
            var for var in find_tvars(type_) if var not in unknowns
        })
        alist: List[Tuple[str, TypeVariable]] = list(zip(schvars, ns))
        restype = subtype(build_substitution(alist), type_)
        return TypeScheme([v.name for _, v in alist], restype)

    unknowns = get_typeenv_unknowns(env)
    schemes = [genbar(unknowns, names, t) for t in types]
    return list(zip(names, schemes)) + env

