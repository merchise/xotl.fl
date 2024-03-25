.. _empty-list-identifier:

===============================
 The empty list **identifier**
===============================

Our parser recognizes the empty list '[]' as an identifier::

  >>> from xotl.fl.parsers.expressions import parse as expr_parse
  >>> expr_parse('[]')
  Identifier('[]')

Having '[]' as an Identifier could be confusing.  It's a constant.  It should
be a Literal.

However, there's no way we can construct a Literal for it (unless we construct
many types).  The type of '[]' is actually polymorphic (``forall a. [a]``).
The following expressions are both valid:

- ``1:[]``

- ``'a':[]``

Furthermore, if we were to create a program::

   data List a = Nil | Cons a (List a)

   reverse Nil = Nil
   reverse (Cons x xs) = append (reverse xs) (Cons x Nil)

   append:: List a -> a -> List a
   append Nil x = Cons x Nil
   append (Cons h xs) x = Cons h (append xs x)

Our Nil is a data constructor with no argument (i.e an identifier) and it's
type scheme is ``forall a. List a``.

So why ``[]`` should be different than ``Nil``?
