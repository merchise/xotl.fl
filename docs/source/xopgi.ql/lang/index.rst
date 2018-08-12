===================================================================
 `xopgi.ql.lang`:mod: - Simple functional language on expressions.
===================================================================

.. warning:: This is a work in progress.

   Not everything described here can be taken for granted.  See the
   :mod:`xopgi.ql.lang.types` and :mod:`xopgi.ql.lang.expressions`.

.. module:: xopgi.ql.lang


Overview of the language syntax and semantics
=============================================

The only constructs we can define in this language are functions::

  id :: a -> a
  id x = x

A function definition starts with its type signature (required), and follows
several equations


Implementation notes
====================

Reminder
--------

- The notation E[x:=e] means replace the free occurrences of 'x' in E with e
  (taking care about the name-capture problem).

  The name-capture problem can be illustrated with E being the expression
  ``λy.xy``, and trying to do E[x:=y], with ``y`` being a variable.

- beta-reduction allows to "replace" or "evaluate" a redex::

    (λx. E) y -> E[x:=y]

- beta-abstraction goes the other way: provided 'x' is not free in E, and it
  contains some "value" y, we can abstract the value in a lambda abstraction.

  Example::

    f 1 2 <- (λx. f 1 x) 2

  You may see that is just beta-reduction flipped::

    (λx. f 1 x) 2  -> f 1 2

  Furthermore::

    f 1 2 <- (λx. f 1 x) 2
          <- (λy. (λx. f y x) 2) 1
          <- (λf. (λy. (λx. f y x) 2) 1) f


- beta-conversion is the equivalence relation given by beta-reduction and
  beta-abstraction together.


- alpha-conversion allows to rename formal parameters in lambda abstractions::

    λx. E ==  λy. E[x:=y];  where 'y' does not occurs free in E.


- eta-conversion allows to capture the idea that *functions* behave like
  lambda abstractions::

    λx. F x === F; if 'x' does not occurs free in F and F is a *function*

  Using Haskell syntax we can demonstrate eta-conversion in ``let f x = id x
  in f 12``; you can avoid the entire definition of ``f`` and replace by
  ``id``: ``id 12``.
