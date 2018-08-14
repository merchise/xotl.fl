=============================================================
 :mod:`xopgi.ql.lang.types` -- The type expressions language
=============================================================

.. automodule:: xopgi.ql.lang.types
   :members: parse


The AST of the type expressions
===============================

.. automodule:: xopgi.ql.lang.types.base
   :members: TypeVariable, TypeCons, FunctionTypeCons, ListTypeCons,
             TupleTypeCons


The type expression language (and grammar)
==========================================

.. module:: xopgi.ql.lang.types.parser


In the type expression language we use *identifiers* starting with a
lower-case letter to indicate a `type variable
<xopgi.ql.lang.types.base.TypeVariable>`:class:, unless they are applied to
other type expression, in which case they're regarded as type constructors.
Identifiers starting with an upper-case letter always denote a type
constructor.

Examples:

  >>> from xopgi.ql.lang.types import parse
  >>> parse('a')
  TypeVariable('a')

  >>> parse('a b')
  TypeCons('a', [TypeVariable('b')])

  >>> parse('a B c')
  TypeCons('a', [TypeCons('B', []), TypeVariable('c')])


Notice that the type variable 'c' is an argument for the type constructor 'a',
and not for 'B'.  You can use parenthesis to make it so:

  >>> parse('a (B c)')
  TypeCons('a', [TypeCons('B', [TypeVariable('c')])])


The function type constructor is the arrow '->':

  >>> parse('a -> B')
  TypeCons('->', [TypeVariable('a'), TypeCons('B', [])])


The list type constructor is the pair of brackets '[]':

  >>> parse('[a]')
  TypeCons('[]', [TypeVariable('a')])


Even though the type expression language recognizes those type constructions
specially there's nothing really special about them in terms of the type
language AST; they are simply TypeCons with some funny names; for which we
expect that components that assign meaning to these constructions (i.e
semantics) assign them with the usual ones.

There's no syntactical support to express tuples yet.  The
`~xopgi.ql.lang.types.base.TupleTypeCons`:func: uses the syntax-friendly name
'Tuple':

  >>> from xopgi.ql.lang.types.base import TupleTypeCons, TypeVariable
  >>> TupleTypeCons(TypeVariable('a'), TypeVariable('a'))
  TypeCons('Tuple', [TypeVariable('a'), TypeVariable('a')])

You can use the general type constructors syntax:

  >>> parse('Tuple a a')
  TypeCons('Tuple', [TypeVariable('a'), TypeVariable('a')])


New lines
---------

You can split long type expressions in several lines, but you only do so in a
controlled manner:

- You can't break between constructors and its arguments, nor within the
  arguments themselves; unless you use parenthesis.

- You can't break before the arrow '->', but breaking **after** it is ok.

Invalid examples::


  >>> parse('a \n -> b')   # breaks before the arrow
  >>> parse('a b \n c')    # breaks the arguments of the cons.
  >>> parse('a (b \n c)')  # idem.
  >>> parse('a \n[b]')     # breaks
  >>> parse('[\na]')       # same logic, '[]' is a type constructor.


Valid examples:

  >>> parse('a -> \nb') == parse('a -> b')  # breaks after the arrow
  True

  >>> # Breaks just after an opening '(', or just before a closing ')'.
  >>> parse('a (\nb c\n)') == parse('a (b c)')
  True
