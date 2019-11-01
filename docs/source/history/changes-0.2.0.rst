Not released.  The following only accounts for a summary of work done, but
probably obsolete.

- The parser is now complete.  New features:

  - Comments.  Comments always introduce a NEWLINE, so they are not allowed in
    places where a newline is not expected (e.g 'inside' a data type
    declaration.)

  - Special syntax for tuples and lists; and tuple types.

  - Pattern matching definitions.

  - Type classes, instances and type constraints.  Data types can declare
    derivations of type classes.

- Changes in the builtins:

  - New type classes:

    - ``Eq a``.  So the type of ``(==)`` is now ``Eq a => a -> a -> Bool``.

    - ``Eq a => Ord a``.  The type of comparison operators is restricted to
      the instances of ``Ord``.

  - The data types Bool, Either and Maybe are instances of Eq and Ord.

    .. note:: Number is still a single type instead of type class.

  - The type of ``is_member`` changed to ``Eq a => a -> [a] -> Bool``.

  - The data types Date, Time and DateTime are now instances of Eq and Ord.
    The meaning of ordering is the order in time (is earlier, later, etc).
