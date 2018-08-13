==============================================================
 :mod:`xopgi.ql.lang.expressions` -- The expressions language
==============================================================

.. automodule:: xopgi.ql.lang.expressions
   :members: parse, find_free_names


The AST of the type expressions
===============================

.. automodule:: xopgi.ql.lang.expressions.base
   :members: Identifier, Literal, Lambda, Application, Let, Letrec


The type expression grammar
===========================

.. module:: xopgi.ql.lang.expression.parser

.. note:: I have to do some serious work to present the grammar.  For the time
          being, enjoy the output of the 'ply.yacc.yacc' generator.

          Beware, it's long!

.. literalinclude:: expr-parser.txt
