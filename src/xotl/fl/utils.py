#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Sequence, Iterator
from xotl.fl.ast.types import TypeVariable


NameSupply = Iterator[str]
TVarSupply = Iterator[TypeVariable]


class namesupply:
    """A names supply.

    Each name has the format '{prefix}{index}'; where the index starts at 0
    and increases by one at each new name.  You can put some invalid char in
    the prefix to ensure no programmer-provided name be produced.

    If `limit` is None (or 0), return a unending stream; otherwise yield as
    many items as `limit`:

       >>> list(namesupply(limit=2))
       ['a0', 'a1']

    """

    def __init__(
        self, prefix="a", exclude: Sequence[str] = None, *, limit: int = None
    ) -> None:
        self.prefix = prefix
        self.exclude = exclude
        self.limit = limit
        self.current_index = 0
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        assert (
            self.count < 20000
        ), "No expression should be so complex to require 20 000 new type variables"

        if self.limit is None or self.count < self.limit:
            result = None
            while not result:
                name = f"{self.prefix}{self.current_index}"
                if not self.exclude or name not in self.exclude:
                    result = name
                self.current_index += 1
            self.count += 1
            return result
        else:
            raise StopIteration


class tvarsupply:
    """A supply of TypeVariables.

    Works the same as `namesupply`:class: but instead of producing strings,
    produces TypeVariables.

    """

    def __init__(
        self, prefix="a", exclude: Sequence[str] = None, *, limit: int = None
    ) -> None:
        self.ns = iter(namesupply(prefix, exclude, limit=limit))

    def __iter__(self):
        return self

    def __next__(self) -> TypeVariable:
        name = next(self.ns)
        return TypeVariable(name, check=False)
