#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from collections import deque
from itertools import islice
from strict_functions import strict_globals

@strict_globals(deque=deque, islice=islice)
def window(iterable, size=2):
    ''' yields wondows of a given size '''
    iterable = iter(iterable)
    d = deque(islice(iterable, size-1), maxlen=size)
    for _ in map(d.append, iterable):
        yield tuple(d)

del deque, islice, strict_globals

if __name__ == '__main__':
    g = window(range(20), 3)
    for i in g:
        print(i)
