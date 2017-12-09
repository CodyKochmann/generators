# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-10-12 11:39:06
# @Last Modified 2017-10-12
# @Last Modified time: 2017-12-09 10:23:27

import sys
import os.path

sys.path.append(os.path.dirname(__file__))

del sys
del os

from iterable import iterable
from itertools import islice
from collections import deque
from strict_functions import strict_globals


@strict_globals(iterable=iterable, islice=islice, deque=deque)
def all_subslices(itr):
    """ generates every possible slice that can be generated from an iterable """
    assert iterable(itr), 'generators.all_subslices only accepts iterable arguments, not {}'.format(itr)
    if not hasattr(itr, '__len__'): # if itr isnt materialized, make it a deque
        itr = deque(itr)
    len_itr = len(itr)
    for start,_ in enumerate(itr):
        d = deque()
        for i in islice(itr, start, len_itr): # how many slices for this round
            d.append(i)
            yield tuple(d)


del iterable
del islice
del deque
del strict_globals
