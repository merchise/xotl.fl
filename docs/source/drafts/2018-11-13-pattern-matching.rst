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

So I need to take a step back::

   count = \.lst -> ((\[] -> 0) .lst) `:OR:`
                    ((\(x:xs) -> 1 + count xs) .lst) `:OR:`
                    :NO_MATCH_ERROR:

But those inner lambdas are pattern-matching lambdas; and they must evaluate
``.lst`` as much as they need to perform the pattern matching.

Fixing the issues takes some refactoring.  Lazy pattern evaluation, but at the
same time strict order of evaluation of several equations, require to take the
set of equations as whole.

The *correct* translation would be::

    count = \.lst -> (<Match Nil> .lst 0)
                     `:OR:`
                     (<Extract 1 from :> .lst (\x -> (<Extract 2 from :> .lst (\xs -> 1 + count xs))))
                     `:OR`:
                     :NO_MATCH_ERROR:

The types of the match/extract function change to take the values (lambdas in
Extract; and AST in Match).  The semantics are to evaluate the argument (.lst)
to perform the pattern matching.

The commit_ is the beginning of such a refactor.  But, now simpler functions
like ``id x = x`` get translated to:

   id = \.id_arg0 -> ((\x -> x) .id_arg0) `:OR:` :NO_MATCH_ERROR:


Sum and product types
=====================

The translation provided in the previous section might make pattern-matching
of product-types *strict*.  This can be seen in the translation of::

  fst (x, y) = x

Which becomes::

  fst = \.p -> (<Extract 1 from ,> .p
                 (\x -> <Extract 2 from ,> .p \y -> x)) `:OR:` :NO_MATCH_ERROR:

The semantics of ``<Extract 2 from,>`` might force the evaluation of the
second component of ``.p``, even it isn't used.


Possible solutions
------------------

Change the semantics of ``Extract`` for product types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On runtime ``Extract`` would see if the type is a product-type and, then,
since type-checking has guaranteed the match, call it's argument with a
``Select``::

  <Extract nth of type> arg f =
       f (<Select nth> arg)


.. _better-translation-product-type:

Know the type of the constructor before translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, we might simply translate differently::

  fst = \.p -> (\x y -> x) (<Select 1st> .p) (<Select 2nd> .p)

To this we have to know whether the type is a product or sum type.


The Haskell approach
--------------------

Testing in ``ghci``::

  Prelude> bottom = bottom
  Prelude> fst (1, bottom)
  1

Which means that Haskell does not evaluates the second component (``bottom``);
otherwise it would fail to terminate.

Another try::

  Prelude> let x = snd (1, bottom) in 1
  1

Since ``x`` is not used ``bottom`` is not evaluated.


Decision
--------

I will attempt the `second <better-translation-product-type_>`__ choice.
Since I don't have yet the evaluation machinery I cannot really project how
the first choice would impact the future.

At the time of writing, the parser performs the translation of 'let' and
'where' expressions inline.  This has to be deferred.  But, we must perform
the translation before (or while) type-checking.

Translating requires the knowledge of whether a data constructor returns a
value of a sum or product type.

Product types don't require keeping the data constructor tag while running.
So they can be represented with a tuple (they are isomorphic); type-checking
have ensured already they are of the right type.


.. _commit: https://gitlab.merchise.org/merchise/xotl.fl/commit/b125f81b842d3468d6a7e3ad941a48e356dbe8c7
