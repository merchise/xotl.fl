==============================================================
 :mod:`xopgi.ql.lang.expressions` -- The expressions language
==============================================================

.. automodule:: xopgi.ql.lang.expressions
   :members: parse, find_free_names

.. testsetup::

   from xopgi.ql.lang.expressions.base import *
   from xopgi.ql.lang.expressions import *


The AST of the type expressions
===============================

.. automodule:: xopgi.ql.lang.expressions.base
   :members: Identifier, Literal, Lambda, Application, Let, Letrec


The type expression grammar
===========================

.. module:: xopgi.ql.lang.expression.parser


The parser recognizes a single expression.
