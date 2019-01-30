=====================================
 The AST of the expressions language
=====================================

.. automodule:: xotl.fl.ast.expressions
   :members: find_free_names, replace_free_occurrences, build_lambda

.. testsetup::

   from xotl.fl.ast.expressions import *
   from xotl.fl.parsers.expressions import parse


.. _ast-objects:

Core objects of the abstract syntax
===================================

.. autoclass:: Identifier

.. autoclass:: Literal

.. autoclass:: Lambda

.. autoclass:: Application

.. autoclass:: Let

.. autoclass:: Letrec


Pattern matching and value definitions
--------------------------------------

.. module:: xotl.fl.ast.pattern

The parser does not parse directly to `~xotl.fl.ast.expressions.Let`:class: or
`~xotl.fl.ast.expressions.Letrec`:class:, because those AST nodes does not
support constructions for pattern matching.

.. autoclass:: ConcreteLet

.. autoclass:: Equation

.. autoclass:: ConsPattern



Data types
==========

.. module:: xotl.fl.ast.adt

The following objects are used in the parser while recognizing the program.

.. autoclass:: DataType
   :members: implied_env, pattern_matching_env, full_typeenv

.. autoclass:: DataCons


Type classes and instances
==========================

.. module:: xotl.fl.ast.typeclasses

.. autoclass:: TypeClass

.. autoclass:: Instance
