==============================================================
 :mod:`xotl.fl.expressions` -- The expressions language
==============================================================

.. automodule:: xotl.fl.expressions
   :members: parse

.. testsetup::

   from xotl.fl.expressions import *


The AST of the type expressions
===============================

.. autoclass:: Identifier

.. autoclass:: Literal

.. autoclass:: Lambda

.. autoclass:: Application

.. autoclass:: Let

.. autoclass:: Letrec


The type expression grammar
===========================

.. seealso:: :mod:`xotl.fl.parsers`


The function `~xotl.fl.expressions.parse`:func: parses a single
standalone expression; not *full programs*.

The simplest expressions are those made up of a single identifier or a literal
value.

Identifiers are made up of letters, digits and '_' but they must not start
with a digit.

Examples:

   >>> parse('a')
   Identifier('a')

   >>> parse('_1e')
   Identifier('_1e')

The expression language allows literal values of `the builtin types`_.  There
are just three builtin types which have a literal representation.

- Unicode characters are surrounded  with apostrophes ``'``.  You can use the
  backslash (``\``) to enter the apostrophe, the backslash itself and other
  Unicode code points.

  Examples:

     >>> parse(r"'\\'")
     Literal('\\', TypeCons('Char', ()))

     >>> parse(r"'\''")
     Literal("'", TypeCons('Char', ()))

     >>> parse(r"'\x20'")
     Literal(' ', TypeCons('Char', ()))

     >>> parse(r"'\u0020'")
     Literal(' ', TypeCons('Char', ()))

  Notice that the value in the `~xotl.fl.expressions.Literal`:class:
  object is a Python string; but it will always one character.

- Strings are surrounded with quotation mark ``"``.  You can use the backslash
  to enter the quotation mark, the backslash itself and other Unicode code
  points.

  Example:

     >>> parse('""')
     Literal('', TypeCons('[]', (TypeCons('Char', ()),)))

     >>> parse(r'"\""')
     Literal('"', TypeCons('[]', (TypeCons('Char', ()),)))

     >>> parse(r'"\\"')
     Literal('\\', TypeCons('[]', (TypeCons('Char', ()),)))

  Notice the String type is just the list of Char.

- Numbers.  We collapse integers and floats into a single type the numbers.
  Integers can be written in base 10, 2, 8 and 16:

     >>> parse('1000') == parse('0x03e8') == parse('0b001111101000')
     True

     >>> parse('1000') == parse('0o1750')
     True

  You can use '_' as a padding to make your numbers more readable:

     >>> parse('1_000') == parse('0x03e8') == parse('0b0011_1110_1000')
     True

  You can use as many as you like and wherever you need it (except at the
  beginning):

     >>> parse('0b0_1_01___0') == parse('0b1010')
     True

  You can use the exponent to represent floating point numbers:

     >>> parse('1e+200')  # doctest: +ELLIPSIS
     Literal(1e+200, ...)

  But beware of a leading '_':

     >>> parse('_1e+200')  # doctest: +ELLIPSIS
     Application(Application(Identifier('+'), Identifier('_1e')), ...)

- The unit value.  This is the only value of the
  `~xotl.fl.builtins.UnitType`:obj:\ :

    >>> parse('()')
    Literal((), TypeCons('Tuple', ()))


Application
-----------

Application (function invocation in other languages) is represented by
white space.

Examples:

  >>> parse('f a')
  Application(Identifier('f'), Identifier('a'))

Application is left associative and it's the operation with the highest
priority:

  >>> parse('f a b') == parse('(f a) b')
  True


Composition
-----------

The dot operator (``.``) represents composition of functions.  In the AST this
is just the application of the identifier '.' to its arguments:

  >>> parse('f . g')
  Application(Application(Identifier('.'), Identifier('f')), Identifier('g'))

  >>> parse('f . g') == parse('(.) f g')
  True

  >>> parse('(.) f')
  Application(Identifier('.'), Identifier('f'))

  >>> parse('(.)')
  Identifier('.')

It gains special treatment because it associates to the right and, after the
application, is next in priority:

  >>> parse('f . g . h') == parse('f . (g . h)')
  True

  >>> parse('f g . h') == parse('(f g) . h')
  True

  >>> # This funny expression is syntactically valid, but it won't type-check.
  >>> parse('f . g + 1') == parse('(f.g) + 1')
  True


Operators
---------

The standard operators ``+``, ``-``, ``*``, ``/``, ``//``, ``%`` stand for
binary operations between numbers.  They all associate to the left.  The
operators ``*``, ``/``, ``//`` and ``%`` have the same precedence between
them, but higher than ``+``, and ``-``:

   >>> parse('a + b * c') == parse('a + (b * c)')
   True

   >>> parse('a * b / c') == parse('(a * b)/c')
   True

Any other combination of those symbols along with any of ``<>$^&!@#=|`` are
`user operators` and they have less precedence that the binary operators.
Notice that standard comparison operators (``<``, ``>``, ``<=``, ``>=``,
``==`` and ``!=``) are in this category:

   >>> parse('a + b <= c - d') == parse('(a + b) <= (c - d)')
   True

   >>> parse('return >=> m')
   Application(Application(Identifier('>=>'), Identifier('return')), Identifier('m'))


Any identifier can become an infix operator by enclosing it in ticks (`````).
Infix has the lowest precedence:

   >>> parse('a `f` b') == parse('f a b')
   True

   >>> parse('a > b `f` c - d') == parse('(a > b) `f` (c - d)')
   True


Lambdas
-------

Lambda abstractions are represented with the concise syntax of Haskell::

  \args -> body

Even though the AST `~xotl.fl.expressions.Lambda`:class: supports a
single argument the parser admits several and does the expected currying:

   >>> parse(r'\a b -> a') == parse(r'\a -> \b -> a')
   True

   >>> parse(r'\a -> \b -> a')
   Lambda('a', Lambda('b', Identifier('a')))


Let and where
-------------

A let expression has the general schema::

    let <pattern 1> = <body 1>
        <pattern 2> = <body 2>
    in <expression>

The patterns must be a sequence of identifiers (or a single identifier).  The
first identifier in the pattern is the name being *defined*.  If the pattern
has more than one identifier, the *excess* of identifiers are pushed to the
body as parameters of a lambda:

   >>> parse('let id x = x in id') == parse(r'let id = \x -> x in id')
   True

When doing several definitions you must split each definition with a newline.

You can't have several definitions for the same name:

   >>> code = '''let if True t f = t
   ...               if False t f = f
   ...           in g . if'''

   >>> parse(code)   # doctest: +ELLIPSIS
   Traceback (most recent call last):
      ...
   ParserError: More than one definition ...

The parser will produce a `~xotl.fl.expressions.Let`:class: node if there are
no recursive definitions, otherwise it will create a
`~xotl.fl.expressions.Letrec`:class:.

The 'where' expressions produce the same AST.  The general schema is::

     <expression> where <pattern 1> = <body 1>
                        <pattern 2> = <body 2>
                        ...

There may be a newline after and before the 'where' keyword.  The same
restrictions of the 'let' expressions apply.


The builtin types
=================

.. automodule:: xotl.fl.builtins
