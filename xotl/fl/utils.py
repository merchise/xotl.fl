#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Sequence, Iterator
from xotl.fl.types import TypeVariable


NameSupply = Iterator[TypeVariable]


class namesupply:
    '''A names supply.

    Each variable will be name '{prefix}{index}'; where the index starts at 0
    and increases by one at each new name.  You can put some invalid char in
    the prefix to ensure no programmer-provided name be produced.

    If `limit` is None (or 0), return a unending stream; otherwise yield as
    many items as `limit`:

       >>> list(namesupply(limit=2))
       [TypeVariable('a0'), TypeVariable('a1')]

    '''
    def __init__(self, prefix='a', exclude: Sequence[str] = None,
                 *, limit: int = None) -> None:
        self.prefix = prefix
        self.exclude = exclude
        self.limit = limit
        self.current_index = 0
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> TypeVariable:
        assert self.count < 20000, \
            'No expression should be so complex to require 20 000 new type variables'

        if not self.limit or self.count < self.limit:
            result = None
            while not result:
                name = f'{self.prefix}{self.current_index}'
                if not self.exclude or name not in self.exclude:
                    result = name
                self.current_index += 1
            self.count += 1
            return TypeVariable(result, check=False)
        else:
            raise StopIteration
