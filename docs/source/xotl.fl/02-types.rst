=========================================================
 :mod:`xotl.fl.types` -- The AST of the type expressions
=========================================================

.. automodule:: xotl.fl.types
   :members: parse, find_tvars

.. testsetup::

   from xotl.fl.types import *


.. autoclass:: Type
   :members:

.. autoclass:: TypeVariable
   :show-inheritance:

.. autoclass:: TypeCons
   :show-inheritance:


.. autoclass:: TypeScheme
   :members:

.. autofunction:: FunctionTypeCons

.. autofunction:: ListTypeCons

.. autofunction:: TupleTypeCons
