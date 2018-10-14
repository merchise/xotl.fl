===================================================================
 :mod:`xotl.fl.expressions` -- The AST of the expressions language
===================================================================

.. automodule:: xotl.fl.expressions
   :members: parse

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
There are two kinds of these objects:

- Those which are purely a concrete syntax construction which are never seen
  by users of the parser.

- Those which entail values in the semantics of the language and are returned
  to the users of the parser.


Semantics-bearing objects
-------------------------

.. autoclass:: DataType

.. autoclass:: DataCons


Purely concrete syntax objects
------------------------------

.. autoclass:: Equation

.. autoclass:: Pattern
