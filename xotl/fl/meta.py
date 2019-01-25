#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
'''Definitions shared by all layers.

'''
from typing import Union


class Symbol:
    '''A complex symbol

    Both typing environments and runtime environments require some non-str
    symbols to be included.

    '''
    # See the symbols Match, Select and Extract in xotl.fl.match
    #


Symbolic = Union[str, Symbol]
