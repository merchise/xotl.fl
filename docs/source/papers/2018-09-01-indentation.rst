.. _indentation:

=============================================
 Dealing with ambiguities due to indentation
=============================================

Our syntax does not have *ends* (like the keyword 'end' in Pascal); and we
find ourselves struggling trying to parse things like::

     data Tree a = Leaf a | Branch (Tree a) (Tree a)

     data List a = Nil
                 | Cons a (List a)

At the end of the first line, the parser is actually trying to look for
another data constructor (possibly in a new line, like in the ``List``).  It
sees the PADDING and (being look-ahead by 1 token) does not notices the
KEYWORD_DATA that comes next; so it shifts the PADDING and enters a state
where the KEYWORD_DATA is no longer valid.

This state of affairs makes our parser work for a single definition.  But also
allows visually unappealing constructions like::

    data List a = Nil
    | Cons a (List a)


Trying to parse indentation
===========================

The solution seems to be to issue a PADDING at the same level of indentation
of the line before, an INDENT if the level of indentation increases, a DEDENT
if the indentation level decreases, and a NEWLINE if more than one '\\n' are
found.

Look at this program::

   fn = let a1 = aa1
            a2 = aa2
            a3 = expr where b1 = bb1
                            b2 = expr2 where c1 = cc1
                                             c2 = cc2
            a4 = aa4
        in a4

   fn2 = fnn2

The current state of the parser (2018-09-10) breaks our intuitions and
"captures" the ``a4 = ...`` as part of the ``where`` expression in ``b2 =
expr2 where ...``.

We expect the equation ``a4 = aa4`` to be part of the outer-most ``let``
expression.

In the program::

   fn = let a1 = aa1
            a2 = aa2
            a3 = expr where b1 = bb1
                            b2 = expr2 where c1 = cc1
                                             c2 = cc2
                            a4 = aa4
        in a4

   fn2 = fnn2

we expect, however, the ``a4 = aa4`` to be part of the outer-most ``where``
expression.

These two examples demonstrate that the rule of issuing a DEDENT when the
indentation level decreases is not sufficient to disambiguate both programs
(they will have the same run of tokens).

If we remove ``where`` expressions from our syntax and rewrite the programs
with ``let`` alone, the ``in`` keyword is enough to disambiguate.


==========
 Decision
==========

1) Keep the ``where`` as it is.   To disambiguate you'll need parenthesis::

     fn = let a1 = aa1
              a2 = aa2
              a3 = (expr where b1 = bb1
                               b2 = expr2 where c1 = cc1
                                                c2 = cc2)
              a4 = aa4
          in a4

     fn2 = fnn2

   Indentation alone won't do it.

   The alternative is to remove ``where`` from the syntax.


2) Introduce 'NEWLINE' to divide definitions:

   a) any chunk of more than one '\\n'

   b) any chunk with single '\\n' but ending with a (possibly empty) run of
      spaces that set the indentation level back to the minimal indentation
      level (set by the first line(s) of the programs).

3) A single definition (expressions, type expressions, and data types) cannot
   contain NEWLINE tokens.  The places where a line break is allowed must be
   indented (but the amount of indentation is not meaningful).

4) Definitions must be separated by NEWLINE tokens.
