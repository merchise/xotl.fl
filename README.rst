===================================
 A xotl.ql translator for Odoo ORM
===================================

Implements a `xotl.ql` translator for Odoo ORM.

Current features:

- Translate simple filters.  The `filtered` and `mapped` methods are rewritten
  to be executed in the underlying PostgreSQL if possible and run Python code
  only when actually needed.
