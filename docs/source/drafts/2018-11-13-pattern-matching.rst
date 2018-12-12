==========================================================
 Implementing basic transformations for pattern matching.
==========================================================

.. note:: These notes were extracted from a commit_; but improved after
   re-reading the book and having ourselves convinced about needing another
   approach.


First attempt
=============

While trying to implement the pattern matching, some things come to my
attention.

I was trying to compile each equation separately, but I then came to an
invalid translations.  Example::

    count []   = 0
    count x:xs = 1 + count xs

I was getting something like::

   count = \.lst -> ((\.nil -> 0) (<Match Nil> .lst))
                    `:OR:`
                    ((\.xs -> 1 + count .xs) (<Extract 2 from :> .lst))
                    `:OR:`
                    :NO_MATCH_ERROR:

This is semantically incorrect because the argument ``.nil`` is never
evaluated in the lambda's body, and, consequently, the application ``<Match
Nil> .lst`` is not evaluated.  Which means that this version of 'count' always
returns 0.


The *right* translation
=======================

I need to take a step back::

   count = \.lst -> ((\[] -> 0) .lst) `:OR:`
                    ((\(x:xs) -> 1 + count xs) .lst) `:OR:`
                    :NO_MATCH_ERROR:

Those inner lambdas are pattern-matching lambdas; and they must evaluate
``.lst`` as much as they need to perform the pattern matching.

Fixing the issues takes some refactoring.  Lazy pattern evaluation and, at the
same time, strict order of evaluation of several equations, require to take
the set of equations as whole.

A *correct* translation would be::

    count = \.lst -> (<Match Nil> .lst 0)
                     `:OR:`
                     (<Extract 1 from :> .lst (\x -> (<Extract 2 from :> .lst (\xs -> 1 + count xs))))
                     `:OR`:
                     :NO_MATCH_ERROR:

The types of the match/extract function change to take the values (lambdas in
Extract; and AST in Match).  The semantics are to evaluate the argument (.lst)
to perform the pattern matching.

The commit_ is the beginning of such a refactor.  But, now simpler functions
like ``id x = x`` get translated to::

   id = \.id_arg0 -> ((\x -> x) .id_arg0) `:OR:` :NO_MATCH_ERROR:


Sum and product types
---------------------

.. admonition:: Incorrect argument

   The translation provided in the previous section might make
   pattern-matching of product-types *strict*.  This can be seen in the
   translation of::

     fst (x, y) = x

   Which becomes::

     fst = \.p -> (<Extract 1 from ,> .p
                     (\x -> <Extract 2 from ,> .p \y -> x)) `:OR:` :NO_MATCH_ERROR:

   The semantics of ``<Extract 2 from,>`` might force the evaluation of the
   second component of ``.p``, even if it is not used.

I thought that the translation of ``fst (x, y)`` would make pattern matching
strict.  But now I realise that is not the case.  Let's make an equivalent
program::

  data Pair a b = Pair a b
  fstPair (Pair x y) = x

This is isomorphic with the tuples constructed by ``(,)``.  I was fooled by
the simplicity of the *data constructor*.  So ``<Extract 2 from ,>`` is the
"same" as ``<Extract 2 from Pair>``; and this evaluates its first argument
up-to the *constructor*, it does not evaluate any of its sub-expressions.

So, it seems that our translation has *lazy semantics* after all.


The translation algorithm
-------------------------

I could try to follow the `match` algorithm described by Wadler's chapter
'Efficient compilation of pattern-matching' in [PeytonJones1987]_.  However,
since at the moment I'm not actually running programs but just type-checking
them, I'm going to try to produce the "final" Expression Tree without `case`
nodes.  I haven't reached the later chapters where they develop the G-Machine;
so I don't know whether the `case` nodes are needed there or not.

The algorithm is, however, similar to the function `match`, but produce
lambdas with calls to, ``<Match...>``, ``<Extract...>``, and ``:OR:``.  I will
avoid generating pattern-matching calls whenever possible.


.. _commit: https://gitlab.merchise.org/merchise/xotl.fl/commit/b125f81b842d3468d6a7e3ad941a48e356dbe8c7
