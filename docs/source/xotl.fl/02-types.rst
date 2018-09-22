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


.. data:: TypeEnvironment

   A `type object <typing>`:mod: defined as ``Mapping[str ,TypeScheme]``.
   When type-checking you do so in such an environment.


.. data:: EMPTY_TYPE_ENV

   The empty `TypeEnvironment`:any:.
