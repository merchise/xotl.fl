=============================================================
 :mod:`xopgi.ql.lang.types` -- The type expressions language
=============================================================

.. automodule:: xopgi.ql.lang.types
   :members: parse


The AST of the type expressions
===============================

.. automodule:: xopgi.ql.lang.types.base
   :members: TypeVariable, TypeCons, FunctionTypeCons, ListTypeCons,
             TupleTypes


The type expression grammar
===========================

.. module:: xopgi.ql.lang.types.parser

.. note:: I have to do some serious work to present the grammar.  For the time
          being, enjoy the output of the 'ply.yacc.yacc' generator.

.. literalinclude:: types-parser.txt
