#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Implements a type checker (Damas-Hindley-Milner) with extensions.

'''
from typing import (
    Iterable,
    List,
    Mapping,
    Tuple,
    Sequence,
)
from collections import ChainMap
from dataclasses import dataclass

from xotl.fl.meta import Symbolic
from xotl.fl.ast.base import AST
from xotl.fl.ast.types import (
    Type,
    TypeVariable,
    FunctionTypeCons as FuncCons,
    TypeScheme,
    find_tvars,
)
from xotl.fl.ast.expressions import (
    Identifier,
    Literal,
    Lambda,
    Application,
    Let,
    Letrec,
)
from xotl.fl.ast.typeclasses import TypeClass, Instance
from xotl.fl.ast.pattern import ConcreteLet
from xotl.fl.utils import TVarSupply

from .subst import (
    sidentity,
    scompose,
    subscheme,
    subtype,
    Substitution,
)
from .unification import unify, unify_exprs
from .exceptions import UnificationError


@dataclass
class Class:
    typeclass: TypeClass
    instances: Sequence[Instance]


ClassEnvironment = Mapping[Symbolic, Class]
TypeEnvironment = Mapping[Symbolic, TypeScheme]
EMPTY_TYPE_ENV: TypeEnvironment = {}


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


def typecheck(exp: AST, env: TypeEnvironment = None, ns: TVarSupply = None) -> TCResult:
    '''Check the type of `exp` in a given type environment `env`.

    The type environment `env` is a mapping from program identifiers to type
    schemes.  If `env` is None, we use the a `basic type environment
    <xotl.fl.builtins.BuiltinEnvDict>`:class:.

    The type-variables supply `ns` is used to create new type variables
    whenever required.  The name supply must ensure not to create the same
    variable twice.  If `ns` is None, we create `one
    <xotl.fl.utils.tvarsupply>`:class: with prefix set to '.t' (it will create
    '.t0', '.t1', ...).

    '''
    if env is None:
        from xotl.fl.builtins import BuiltinEnvDict
        env = BuiltinEnvDict()
    if ns is None:
        from xotl.fl.utils import tvarsupply
        ns = tvarsupply('.t')
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
    elif isinstance(exp, ConcreteLet):
        # TODO: Remove this
        return typecheck(exp.ast, env, ns)
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
        phi, t = typecheck(expr, env, ns)
        psi, ts = tcl(sub_typeenv(phi, env), ns, exprs)
        # We can safely modify the ts and improve performance.
        ts.insert(0, subtype(psi, t))
        return scompose(psi, phi), ts


def newinstance(ns: TVarSupply, ts: TypeScheme) -> Type:
    '''Create an instance of `ts` drawing names from the supply `ns`.

    Each generic variable in `ts` gets a new name from the supply.

    '''
    newvars: List[Tuple[str, TypeVariable]] = list(zip(ts.generics, ns))
    phi: Substitution = build_substitution(newvars)
    return subtype(phi, ts.type_)


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
    return sidentity, exp.type_


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
    except UnificationError:
        raise UnificationError(
            f'Cannot type-check {exp!s} :: {t1!s} ~ {t2!s} -> {t!s}'
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
        exp.body,
        ChainMap({exp.varname: argtype}, env),
        ns,
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
            (newinstance(ns, local[name]), types[i])
            for i, name in enumerate(names)
            if name in local
        ]
        phi = unify_exprs(typepairs, p=phi)
        types = [subtype(phi, t) for t in types]
        decls = _add_decls(
            sub_typeenv(phi, ChainMap(local, env)),
            ns,
            names,
            types,
            _generalize_over=local.keys(),
        )
    else:
        decls = _add_decls(sub_typeenv(phi, env), ns, names, types)
    psi, t = typecheck(
        exp.body,
        decls,
        ns
    )
    return scompose(psi, phi), t


def _add_decls(env: TypeEnvironment,
               ns: TVarSupply,
               names: Iterable[Symbolic],
               types: Iterable[Type],
               _generalize_over=None) -> TypeEnvironment:
    '''Extend the type environment with new schemes for `names`.

    This function is used for generalization in the context of type-checking
    let and letrec.

    The `_generalize_over` parameter is experimental; it controls which names
    must be generalized as explained in [OutsideInX]_.  If no names are given,
    nothing is generalized.  If some names are given, only those are
    generalized in the result.

    '''
    names = list(names)
    types = list(types)
    assert len(names) == len(types)

    def genbar(unknowns, names, type_, name):
        if not _generalize_over or name in _generalize_over:
            schvars = list({
                tv.name
                for tv in find_tvars(type_)
                if tv.name not in unknowns
            })
            alist: List[Tuple[str, TypeVariable]] = list(zip(schvars, ns))
            restype = subtype(build_substitution(alist), type_)
            return TypeScheme([v.name for _, v in alist], restype)
        else:
            # This correspond to the No Qualification rule explained in
            # [OutsideInX], section 4.2.4; which means that let-bound
            # variables are not generalized but left as unknown.
            return TypeScheme([], type_)

    unknowns = get_typeenv_unknowns(env)
    schemes = (genbar(unknowns, names, t, name) for name, t in zip(names, types))
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
    names: Sequence[Symbolic] = tuple(exp.keys())
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
            (newinstance(ns, local[name]), ts[i])
            for i, name in enumerate(names)
            if name in local
        ]
        phi = unify_exprs(typepairs, p=phi)
        ts = [subtype(phi, t) for t in ts]
        gamma = sub_typeenv(phi, ChainMap(local, env))
    else:
        gamma = sub_typeenv(phi, env)
    nbvs1 = sub_typeenv(phi, nbvs)
    ts1 = [sch.type_ for _, sch in nbvs1.items()]
    psi = unify_exprs(zip(ts, ts1), p=phi)

    # Now we have type-checked the definitions, so we can now typecheck the
    # body in the **proper** environment.
    nbvs1 = sub_typeenv(psi, nbvs)
    ts = [sch.type_ for _, sch in nbvs1.items()]
    psi1, t = typecheck(
        exp.body,
        _add_decls(sub_typeenv(psi, gamma), ns, names, ts, _generalize_over=local.keys()),
        ns
    )
    return scompose(psi1, psi), t
