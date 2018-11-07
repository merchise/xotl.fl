===================================================================
 :mod:`xotl.fl.expressions` -- The AST of the expressions language
===================================================================

.. automodule:: xotl.fl.expressions
   :members: parse, find_free_names, build_lambda

.. testsetup::

   from xotl.fl.expressions import *


.. _ast-objects:

Core objects of the abstract syntax
===================================

.. autoclass:: Identifier

.. autoclass:: Literal

.. autoclass:: Lambda

.. autoclass:: Application

.. autoclass:: Let

.. autoclass:: Letrec


Additional objects
==================

The following objects are used in the parser while recognizing the program.

.. autoclass:: DataType

.. autoclass:: DataCons

.. autoclass:: Equation

.. autoclass:: Pattern
