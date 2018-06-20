#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Parser of patterns.

Implements a tokenizer/parser from a simplified term-language to the Terms AST
in module `ast`.

Named variables start with ``$``.  Anonymous variables start with ``_``.  Only
ASCII letters and digits.  Anonymous variables are NEVER the same.  The
following patterns will have an equivalent (w.r.t unification) AST::

    f(_x, _x)

    f(_x, _y)

Anonymous variables can be unnamed::

    f(_)

Literals are just strings non-space ASCII letters and digits.

Function calls are a name (literal-like) followed by ``(`` and zero or more
terms separated by commas, and a ``)``.

We provide support for logical and arithmetical operations as syntax-suggar.
The following two patterns parse to the same AST::

   f() and $a <= $b + $c and not ($x or $y or $c)

   and(and(f(), le($a, add($b, $c))), not(or(or($x, $y), $c)))


The grammar::

   variable ::= named_variable | anonymous_variable
   named_variable ::= '$' identifier
   anonymous_variable ::= '_' | '_' identifier

   identifier ::= /^[a-zA-Z0-9][a-zA-Z0-9_\.]*$/

   literal ::= identifier

   function_call ::= function_name '()'
   function_call ::= function_name '(' argument_list ')'
   function_name ::= identifier

   argument ::= expr
   argument_list ::= argument | argument ',' argument_list

   expr ::= boolean_expr | comparison_expr | arith_expr
   expr ::= term
   term ::= variable | literal | function_call

   boolean_expr ::= boolean_expr boolean_connector boolean_expr
   boolean_expr ::= 'not' boolean_expr
   boolean_connnector ::= 'and' | 'or'
   boolean_expr ::= term | comparison_expr

   comparison_expr ::= arith_expr comparator arith_expr
   comparator ::= '<' | '<=' | '>' | '>=' | '==' | '!='

   arith_expr ::= expr_term | expr_term arith_op arith_expr
   arith_term_op ::= '+' | '-'
   expr_term ::= factor | factor arith_factor_op expr_term
   arith_factor_op ::= '*' | '/'
   factor ::= term | '(' arith_expr ')'

'''
