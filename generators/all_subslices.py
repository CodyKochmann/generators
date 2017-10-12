# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-10-12 11:39:06
# @Last Modified 2017-10-12
# @Last Modified time: 2017-10-12 12:10:32

import sys
import os.path

sys.path.append(os.path.dirname(__file__))

del sys
del os

from iterable import iterable
from itertools import islice
from collections import deque

def all_subslices(itr):
    """ generates every possible slice that can be generated from an iterable """
    assert iterable(itr), 'generators.all_subslices only accepts iterable arguments, not {}'.format(itr)
    if not hasattr(itr, '__len__'): # if this isnt materialized, make it a list
        itr = list(itr)
    len_itr = len(itr)
    for start,_ in enumerate(itr):
        d = deque()
        for i in islice(itr, start, len_itr): # how many slices for this round
            d.append(i)
            yield tuple(d)
