=============================================================
 :mod:`xopgi.ql.lang.types` -- The type expressions language
=============================================================

.. automodule:: xopgi.ql.lang.types
   :members: parse

.. testsetup::

   from xopgi.ql.lang.types import *



The AST of the type expressions
===============================

.. autoclass:: TypeVariable

.. autoclass:: TypeCons

.. autoclass:: FunctionTypeCons

.. autoclass:: ListTypeCons

.. autoclass:: TupleTypeCons


The type expression language (and grammar)
==========================================

.. seealso:: :mod:`xopgi.ql.lang.parsers`

In the type expression language we use *identifiers* starting with a
lower-case letter to indicate a `type variable
<xopgi.ql.lang.types.base.TypeVariable>`:class:, unless they are applied to
other type expression, in which case they're regarded as type constructors.
Identifiers starting with an upper-case letter always denote a type
constructor.

Examples:

  >>> parse('a')
  TypeVariable('a')

  >>> parse('a b')
  TypeCons('a', (TypeVariable('b'),))

  >>> parse('a B c')
  TypeCons('a', (TypeCons('B', ()), TypeVariable('c')))


Notice that the type variable 'c' is an argument for the type constructor 'a',
and not for 'B'.  You can use parenthesis to make it so:

  >>> parse('a (B c)')
  TypeCons('a', (TypeCons('B', (TypeVariable('c'),)),))


The function type constructor is the arrow '->':

  >>> parse('a -> B')
  TypeCons('->', (TypeVariable('a'), TypeCons('B', ())))


The list type constructor is the pair of brackets '[]':

  >>> parse('[a]')
  TypeCons('[]', (TypeVariable('a'),))


Even though the type expression language recognizes those type constructions
specially there's nothing really special about them in terms of the type
language AST; they are simply TypeCons with some funny names; for which we
expect that components that assign meaning to these constructions (i.e
semantics) assign them with the usual ones.

There's no syntactical support to express tuples yet.  The
`~xopgi.ql.lang.types.base.TupleTypeCons`:func: uses the syntax-friendly name
'Tuple':

  >>> parse('Tuple a a')
  TypeCons('Tuple', (TypeVariable('a'), TypeVariable('a')))


New lines
---------

You can split long type expressions in several lines, but you only do so in a
controlled manner:

- You can't break between constructors and its arguments, nor within the
  arguments themselves; unless you use parenthesis.

- You can't break before the arrow '->', but breaking **after** it is OK, but
  also you need to *indent* the rest of the type expression.

Invalid examples::


  >>> parse('a \n -> b')   # breaks before the arrow
  >>> parse('a b \n c')    # breaks the arguments of the cons.
  >>> parse('a (b \n c)')  # idem.
  >>> parse('a \n[b]')     # breaks
  >>> parse('[\na]')       # same logic, '[]' is a type constructor.


Valid examples:

  >>> parse('a -> \n   b') == parse('a -> b')
  True

  >>> parse('a (\n  b c\n  )') == parse('a (b c)')
  True


Quirks
------

`~xopgi.ql.lang.types.base.TypeCons`:class: does not have an implicit limit to
the type arguments any given constructor admits.  This is the job of the
semantic analyzer.  This also means that the parser has a very liberal rule
about type arguments in a constructor:

  Any type expression to the **left** of a space and another type expression
  admits it as an argument.

This makes the parser to recognize funny, unusual types expressions:


  >>> parse('[a] b')
  TypeCons('[]', (TypeVariable('a'), TypeVariable('b')))

  >>> parse('(a -> b) c')
  TypeCons('->', (TypeVariable('a'), TypeVariable('b'), TypeVariable('c')))

Those types have no semantics assigned but the parser recognizes them.  It's
the job of another component (kinds?) to recognize those errors.
