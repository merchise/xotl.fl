===============================================
 :mod:`xotl.fl.parsers` -- The internal parser
===============================================

.. testsetup::

   from xotl.fl.expressions import parse, find_free_names

.. automodule:: xotl.fl.parsers


The parser is written using Ply_.  It started as two separate parsers: one for
the types language, and other for the expression language; however now it has
been merged into a single parser to allow for more real-world like programs

There are no public API for the parsers.  You get access to them by calling:

- `xotl.fl.parse`:func: for full programs;

- `xotl.fl.type_parse`:func: for a single type expression; and

- `xotl.fl.expr_parse`:func: for a single expression.


.. _ply: http://www.dabeaz.com/ply/ply.html
