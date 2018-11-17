#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Implements a basic type checker.

The main algorithm is described in Chapter 9 of [PeytonJones1987]_.  However,
some insights are described in [Damas1982]_ and [Damas1984]_.

'''
from typing import (
    Sequence,
    List,
    Tuple,
    Iterable,
    Callable,
    Union,
)
from typing import Any  # noqa
from collections import ChainMap

from xotl.fl.types import (
    AST,
    Type,
    TypeVariable,
    TypeCons,
    FunctionTypeCons as FuncCons,
    TypeScheme,
    find_tvars,
    TypeEnvironment,
    Symbol,
)
from xotl.fl.expressions import (
    Identifier,
    Literal,
    Lambda,
    Application,
    Let,
    Letrec,
)
from xotl.fl.utils import TVarSupply


_STR_PADDING = ' ' * 4


# `Substitution` is a type; `scompose`:class: is a substitution by
# composition, `delta`:class: creates the simplest non-empty substitution.
#
# TODO: We could modify the algorithm so that we can *inspect* which variables
# are being substituted; but that's not essential to the Substitution Type.
Substitution = Callable[[str], Type]


def subtype(phi: Substitution, t: Type) -> Type:
    '''Get the sub-type of `t` by applying the substitution `phi`.

    '''
    # 'subtype(sidentity, t) == t'; and since Type, TypeVariables and TypeCons
    # are treated immutably we should be safe to return the same type.
    if phi is sidentity:
        return t
    elif isinstance(t, TypeVariable):
        return phi(t.name)
    elif isinstance(t, TypeCons):
        return TypeCons(
            t.cons,
            [subtype(phi, subt) for subt in t.subtypes],
            binary=t.binary
        )
    elif isinstance(t, TypeScheme):
        psi = Exclude(phi, t)
        return TypeScheme(t.generics, subtype(psi, t.t))
    else:
        assert False, f'Node of unknown type {t!r}'


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

    def __str__(self):
        import textwrap
        if self._composes_deltas:
            deltas = '\n'.join(
                textwrap.indent(str(dl), _STR_PADDING)
                for dl in self._deltas
            )
            return f'Composition of\n{deltas}'
        else:
            f = textwrap.indent(str(self.f), _STR_PADDING)
            g = textwrap.indent(str(self.g), _STR_PADDING)
            return f'Composition of\n{f}and\n{g}'

    @property
    def _composes_deltas(self):
        first = (isinstance(self.f, delta) or
                 isinstance(self.f, Composition) and self.f._composes_deltas)
        if first:
            second = (isinstance(self.g, delta) or
                      isinstance(self.g, Composition) and self.g._composes_deltas)
        else:
            second = True   # it doesn't really matter
        return first and second

    @property
    def _deltas(self):
        from collections import deque
        stack = deque([self.g, self.f])
        while stack:
            node = stack.pop()
            if isinstance(node, delta):
                yield node
            elif isinstance(node, Composition):
                stack.append(node.g)
                stack.append(node.f)
            else:
                assert False


class Identity:
    'The identity substitution.'
    def __call__(self, s: str) -> Type:
        return TypeVariable(s, check=False)

    def __repr__(self):
        return 'Identity()'


sidentity = Identity()


class delta:
    '''A `delta substitution` from a variable name `vname`.

    '''
    def __init__(self, vname: str, t: Type) -> None:
        self.vname = vname
        self.t = t

    def __call__(self, s: str) -> Type:
        return self.t if s == self.vname else TypeVariable(s, check=False)

    def __repr__(self):
        return f'delta({self.vname!r}, {self.t!r})'

    def __str__(self):
        return f'delta: {self.vname.ljust(20)}{self.t!s}'


class UnificationError(TypeError):
    pass


def unify(e1: Type, e2: Type, *, phi: Substitution = sidentity) -> Substitution:
    '''Extend `phi` so that it unifies `e1` and `e2`.

    If `phi` is None, uses the identity substitution `Identity`:class:.

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
            return scompose(delta(name, t), phi)

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


def subscheme(phi: Substitution, ts: TypeScheme) -> TypeScheme:
    '''Apply a substitution to a type scheme.

    .. warning:: You must ensure that the type scheme's generic variables are
       distinct from the variables occurring in the result of applying the
       substitution `phi` to any of the non-generic variables of `ts`.

       The way in which we ensure this (in the algorithm) is to guarantee that
       the names of the generic variables in the type scheme are always
       distinct from those which can occur in the range of the substitution
       (which are always non-generic).

    '''
    # From Damas1982:
    #
    # If S is a substitution of types for type variables, often written
    # [τ1/α1, ..., τn/αn ] or [τi/αi], and σ is a type-scheme, then Sσ is the
    # type-scheme obtained by replacing each free occurrence of αi in σ by τi,
    # renaming the generic variables of σ if necessary.  Then Sσ is called an
    # instance of σ; the notions of substitution and instance extend naturally
    # to larger syntactic constructs containing type-schemes.
    #
    assert all(not bool(scvs & set(find_tvars(phi(unk))))
               for scvs in (set(ts.generics), )
               for unk in ts.nongenerics)
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

    def __str__(self):
        import textwrap
        sub = textwrap.indent(str(self.phi), _STR_PADDING)
        return f'exclude all {self.ts.generics} in \n{sub}'


def get_typeenv_unknowns(te: TypeEnvironment) -> List[str]:
    '''Return all the non-generic variables in the environment.'''
    return sum((t.nongenerics for _, t in te.items()), [])


class sub_typeenv(TypeEnvironment):
    '''Create a sub-type environment.

    Read the warning in `subscheme`:func:.

    '''
    def __init__(self, phi: Substitution, env: TypeEnvironment) -> None:
        self.phi = phi
        self.env = env

    def __getitem__(self, key):
        return subscheme(self.phi, self.env[key])

    def __iter__(self):
        return iter(self.env)

    def __len__(self):
        return len(self.env)


TCResult = Tuple[Substitution, Type]


def typecheck(env: TypeEnvironment, ns: TVarSupply, exp: AST) -> TCResult:
    '''Check the type of `exp` in a given type environment `env`.

    The name supply `ns` is used to create new type variables whenever
    required.  The name supply must ensure not to create the same variable
    twice.

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


def tcl(env: TypeEnvironment, ns: TVarSupply, exprs: Iterable[AST]) -> TCLResult:
    '''Type check several expressions in the context of `env`.

    The name supply `ns` is shared across all other functions to ensure no
    names are repeated.

    '''
    if not exprs:
        return sidentity, []
    else:
        expr, *exprs = exprs
        phi, t = typecheck(env, ns, expr)
        psi, ts = tcl(sub_typeenv(phi, env), ns, exprs)
        return scompose(psi, phi), [subtype(psi, t)] + ts


def newinstance(ns: TVarSupply, ts: TypeScheme) -> Type:
    '''Create an instance of `ts` drawing names from the supply `ns`.

    Each generic variable in `ts` gets a new name from the supply.

    '''
    newvars: List[Tuple[str, TypeVariable]] = list(zip(ts.generics, ns))
    phi: Substitution = build_substitution(newvars)
    return subtype(phi, ts.t)


def build_substitution(alist: Sequence[Tuple[str, Type]]) -> Substitution:
    '''Build a substitution from an association list.

    This is the standard *interpretation* of a mapping from names to types.
    The substitution, when called upon, will look the list from beginning to
    end for an item with the same key and return the associated type.

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


def typecheck_literal(env: TypeEnvironment, ns, exp: Literal) -> TCResult:
    # Extension to the original algorithm but easy: a literal always type
    # check with its type.
    return sidentity, exp.type


def typecheck_var(env: TypeEnvironment, ns, exp: Identifier) -> TCResult:
    '''Type check a single identifier.

    The identifier's name must be in the type environment `env`.  If the
    identifier is a generic of the associated type scheme, a new name is
    created.

    This is a combination of the TAUT and INST rules in [Damas1982]_.

    '''
    name = exp.name
    return sidentity, newinstance(ns, env[name])


def typecheck_app(env: TypeEnvironment, ns, exp: Application) -> TCResult:
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


def typecheck_lambda(env: TypeEnvironment, ns, exp: Lambda) -> TCResult:
    # \x -> ...; the type of 'x' can be anything.  Thus, create a type
    # scheme with a new non-generic type variable Tx.  We extend the
    # environment to say 'x :: Tx' and typecheck the body of the lambda in
    # this new environment.
    newvar = next(ns)
    argtype = TypeScheme.from_typeexpr(newvar, generics=[])
    phi, type_ = typecheck(
        ChainMap({exp.varname: argtype}, env),
        ns,
        exp.body
    )
    return phi, FuncCons(phi(newvar.name), type_)


def typecheck_let(env: TypeEnvironment, ns, exp: Let) -> TCResult:
    exprs: Sequence[AST] = tuple(exp.values())
    phi, types = tcl(env, ns, exprs)
    names: Sequence[str] = tuple(exp.keys())
    # At this point all we have inferred (from their bodies) the types of the
    # let definitions; but we must ensure they match their local-annotations
    # (if provided).
    local = exp.localenv or {}
    if local:
        typepairs = [
            (local[name].t, types[i])
            for i, name in enumerate(names)
            if name in local
        ]
        phi = unify_exprs(typepairs, p=phi)
        types = [subtype(phi, t) for t in types]
        decls = add_decls(
            sub_typeenv(phi, ChainMap(local, env)),
            ns,
            names,
            types
        )
    else:
        decls = add_decls(sub_typeenv(phi, env), ns, names, types)
    psi, t = typecheck(
        decls,
        ns,
        exp.body,
    )
    return scompose(psi, phi), t


def add_decls(env: TypeEnvironment,
              ns: TVarSupply,
              names: Iterable[Union[str, Symbol]],
              types: Iterable[Type]) -> TypeEnvironment:
    '''Create an extended type environment with ...'''
    def genbar(unknowns, names, type_):
        schvars = list({
            var
            for var in find_tvars(type_)
            if var not in unknowns
        })
        alist: List[Tuple[str, TypeVariable]] = list(zip(schvars, ns))
        restype = subtype(build_substitution(alist), type_)
        return TypeScheme([v.name for _, v in alist], restype)

    unknowns = get_typeenv_unknowns(env)
    schemes = [genbar(unknowns, names, t) for t in types]
    return ChainMap(dict(zip(names, schemes)), env)


def typecheck_letrec(env: TypeEnvironment,
                     ns, exp: Letrec) -> TCResult:
    # This algorithm is quite elaborate.
    #
    # We expected that at least one of exprs is defined in terms of a name.
    # So, we must type-check all of exprs in a type environment where there's
    # non-generic type associated to each of the names defined in the 'let'.
    #
    #     let x1 = e1
    #         x2 = e2
    #        ...
    #     in body
    #
    # We make a new type scheme for each 'x' ; x1 :: Tx1, x2 :: Tx2, etc...
    # and type-check of the 'exprs' in this extended environment.
    #
    exprs: Sequence[AST] = tuple(exp.values())
    names: Sequence[Union[str, Symbol]] = tuple(exp.keys())
    nbvs = {
        name: TypeScheme.from_typeexpr(var, generics=[])
        for name, var in zip(names, ns)
    }
    phi, ts = tcl(ChainMap(nbvs, env), ns, exprs)

    # At this point `phi` is the substitution that makes all the bindings in
    # the letrec type-check; and `ts` is the list of the types inferred for
    # each expr.
    #
    # We must now see if the inferred types match the annotations
    # (if any).
    #
    # Then, we must unify the types inferred with the types of the names in
    # the non-extended environment, but taking the `phi` into account.
    #
    local = exp.localenv or {}
    if local:
        typepairs = [
            (local[name].t, ts[i])
            for i, name in enumerate(names)
            if name in local
        ]
        phi = unify_exprs(typepairs, p=phi)
        ts = [subtype(phi, t) for t in ts]
        gamma = sub_typeenv(phi, ChainMap(local, env))
    else:
        gamma = sub_typeenv(phi, env)
    nbvs1 = sub_typeenv(phi, nbvs)
    ts1 = [sch.t for _, sch in nbvs1.items()]
    psi = unify_exprs(zip(ts, ts1), p=phi)

    # Now we have type-checked the definitions, so we can now typecheck the
    # body in the **proper** environment.
    nbvs1 = sub_typeenv(psi, nbvs)
    ts = [sch.t for _, sch in nbvs1.items()]
    psi1, t = typecheck(
        add_decls(sub_typeenv(psi, gamma), ns, names, ts),
        ns,
        exp.body
    )
    return scompose(psi1, psi), t
