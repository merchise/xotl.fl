=============================
 Description of the language
=============================

.. warning:: This is a work in progress. Not everything described here can be
   taken for granted until we produce a stable release.


Goals and inspiration
=====================

The language is inspired in other functional languages, but if you find it
too Haskell-like, that's not a coincidence.  We're using Haskell as the gold
standard, but our language is much less ambitious.

We only aim to integrate a statically typed language into Python, with type
checking and type inference (Damas-Hindley-Milner) and where pattern matching
is used to do most of the branching.

The idea is to complement programs that expose some sort of programming to its
users, but do not require a general programming language.

We have such a system; users needs to define complex procedures to compute
prices.  However complex, all price schemes seem to be programmable with
simple expressions, function application and composition and a powerful
pattern matching (probably with some extensions for matching dates and date
intervals).

It's not clear if we're going to need type classes.  We suspect we do.

We provide a `parser <xotl.fl.parse>`:func:, but the system using this
language may choose to present its user with a very different way to build
programs.


The language
============

The language allows to *define* algebraic data types (ADTs) and values
(functions, most likely).  A full program is just a *non-empty* sequence of
definitions.

Definitions come in three types:

- Type (scheme) declarations;

- Algebraic data types; and

- Value definitions (functions belong here).

The order of the definitions in a program is unimportant.  But the order of
the equations within a function definition **is** important.

A very simple program:

  >>> from xotl.fl import parse
  >>> parse(r'''
  ...     alias :: [Char]
  ...     alias = name
  ...
  ...     name = "xotl.fl"
  ...
  ...     myId :: a -> a
  ...     myId x = x
  ...
  ...     myId2 = \x -> x
  ...
  ...     myConst :: a -> b -> a
  ...     myConst a _ = a
  ...
  ...     data MyList a = EmptyList
  ...                   | Cons a (MyList a)
  ...
  ...     insert a xs  = Cons a xs
  ...
  ...     isnull :: MyList a -> Bool
  ...     isnull EmptyList = True
  ...     isnull _         = False
  ...
  ...     insert :: a -> MyList a -> MyList a
  ...
  ...     concat :: MyList a -> MyList a -> MyList a
  ... ''')
  [...]


Notice that:

- We use the identifier 'name' in the definition of 'alias', before the very
  definition of 'name'.  This is no problem at all.

- We are not required to provide type declarations for all values.

- We can provide the type declarations after or before the value definition.

- We may even provide type declarations for things we didn't define
  ('concat').

  There are things the `~xotl.fl.parse`:func: allows to do that you shouldn't.
  We might change our mind and prohibit them in the future.

Parsing is not the whole story.  Parsing just creates an Abstract Syntax Tree
out of your source code.  For things to really work, you need to type-check
them and `run them <running-programs>`:ref:.


Expressions
-----------

The right hand side of values (and function) definitions are made up from
expressions.  The AST of expressions is documented in
`xotl.fl.expressions`:mod:.

In the examples below, the return of the `xotl.fl.expression.parse`:func: is
always an instance of some AST class.


Literals and identifiers
~~~~~~~~~~~~~~~~~~~~~~~~

The simplest expressions are those made up of a single identifier or a literal
value.

Identifiers are made up of letters, digits and '_' but they must not start
with a digit.

Examples:

   >>> from xotl.fl.expressions import parse
   >>> parse('a')
   Identifier('a')

   >>> parse('_1e')
   Identifier('_1e')

The expression language allows literal values:

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
  object is a Python string; but it will always be one character long.

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
    Literal((), TypeCons('Unit', ()))


Application
~~~~~~~~~~~

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
~~~~~~~~~~~

The dot operator (``.``) represents composition of functions.  In the AST this
is just the application of the identifier ``.`` to its arguments:

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
  >>> parse('f . g + 1') == parse('(f . g) + 1')
  True

.. warning:: There must be a space before and/or after the dot operator.


Operators
~~~~~~~~~

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


.. _infixed:

Infix form of a function application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any identifier can become an infix operator by enclosing it in ticks (`````).
Infix has the lowest precedence:

   >>> parse('a `f` b') == parse('f a b')
   True

   >>> parse('a > b `f` c - d') == parse('(a > b) `f` (c - d)')
   True


Lambdas
~~~~~~~

Lambda abstractions are represented with the concise syntax of Haskell::

  \args -> body

Even though the AST `~xotl.fl.expressions.Lambda`:class: supports a
single argument the parser admits several and does the expected currying:

   >>> parse(r'\a b -> a') == parse(r'\a -> \b -> a')
   True

   >>> parse(r'\a -> \b -> a')
   Lambda('a', Lambda('b', Identifier('a')))


Let and where
~~~~~~~~~~~~~

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

When doing several definitions you must split each definition with a newline
[#newline]_.

When having several definitions for the same name, the code is transformed to
do pattern matching.  This is represented by transforming your code:

   >>> code = '''let if True t f = t
   ...               if False t f = f
   ...           in g . if'''

   >>> parse(code)   # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
   Let((('if', Application(Application(Identifier(':OR:'), ...Identifier('if')))

The parser will produce a `~xotl.fl.expressions.Let`:class: node if there are
no recursive definitions, otherwise it will create a
`~xotl.fl.expressions.Letrec`:class:.

The 'where' expressions produce the same AST.  The general schema is::

     <expression> where <pattern 1> = <body 1>
                        <pattern 2> = <body 2>
                        ...


The ``:`` operator
------------------

Although the expression language does not support literal lists, we do support
the ``:`` operator, which has the builtin type ``a -> [a] -> [a]``.  ``:`` is
right-associative:

   >>> parse('a:b:xs') == parse('a:(b:xs)')
   True

It has less precedence than any other operator except the `infix form
<infixed_>`__:

   >>> parse('a + b:xs') == parse('(a + b):xs')
   True

   >>> parse('a `f` b:xs') == parse('a `f` (b:xs)')
   True


Type declarations
-----------------

Type declarations state the type of a symbol.  The function
`xotl.fl.types.parse`:func: parses the type expression (the thing after the
two colons) and return an instance of AST for types.

The AST of types as only two constructors:
`~xotl.fl.types.TypeVariable`:class: and `~xotl.fl.types.TypeCons`:class:.

The `~xotl.fl.types.TypeScheme`:class: is not (yet) considered an AST node.
There's no way to express type schemes in the syntax.  Nevertheless, the
`parser <xotl.fl.parse>`:func: do return type schemes:

   >>> from xotl.fl import parse
   >>> from xotl.fl.types import TypeScheme
   >>> parse('id :: a -> a') == [{'id': TypeScheme.from_str('a -> a')}]
   True

In the type expression language we use *identifiers* starting with a
lower-case letter to indicate a `type variable
<xotl.fl.types.base.TypeVariable>`:class:, unless they are applied to other
type expression, in which case they're regarded as type constructors.
Identifiers starting with an upper-case letter always denote a type
constructor.

Examples:

  >>> from xotl.fl.types import parse
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
`~xotl.fl.types.TupleTypeCons`:func: uses the syntax-friendly name 'Tuple':

  >>> parse('Tuple a a')
  TypeCons('Tuple', (TypeVariable('a'), TypeVariable('a')))


New lines
~~~~~~~~~

You can split long type expressions in several lines, but you only do so in a
controlled manner:

- You can't break between constructors and its arguments, nor within the
  arguments themselves; unless you use parenthesis.

- You can't break before the arrow '->', but breaking **after** it is OK, but
  also you need to `indent <indentation>`:ref: the rest of the type
  expression.


Quirks of type expression language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`~xotl.fl.types.TypeCons`:class: does not have an implicit limit to the type
arguments any given constructor admits.  This is the job of the semantic
analyzer.  This also means that the parser has a very liberal rule about type
arguments in a constructor:

  Any type expression to the **left** of a space and another type expression
  is admitted it as an argument.

This makes the parser to recognize funny, unusual types expressions:

  >>> parse('[a] b')
  TypeCons('[]', (TypeVariable('a'), TypeVariable('b')))

  >>> parse('(a -> b) c')
  TypeCons('->', (TypeVariable('a'), TypeVariable('b'), TypeVariable('c')))

Those types have no semantics assigned but the parser recognizes them.  It's
the job of another component (kinds?) to recognize those errors.


Notes
=====

.. [#newline] See the `account of new lines and indentation
              <indentation>`:ref:.
